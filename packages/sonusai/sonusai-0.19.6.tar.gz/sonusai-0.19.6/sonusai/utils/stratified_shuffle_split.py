import numpy as np

from sonusai.mixture import MixtureDatabase


def stratified_shuffle_split_mixid(
    mixdb: MixtureDatabase,
    vsplit: float = 0.2,
    nsplit: int = 0,
    rnd_seed: int | None = 0,
) -> tuple[list[int], list[int], np.ndarray, np.ndarray]:
    """
    Create a training and test/validation list of mixture IDs from all mixtures in a mixture database.
    The test/validation split is specified by vsplit (0.0 to 1.0), default 0.2.
    The mixtures are randomly shuffled by rnd_seed; set to int for repeatability, or None for no shuffle.
    The mixtures are then stratified across all populated classes.

    Inputs:
        mixdb:      Mixture database created by Aaware SonusAI genmixdb.
        vsplit:     Fractional split of mixtures for validation, 1-vsplit for training.
        nsplit:     Number of splits (TBD).
        rnd_seed:   Seed integer for reproducible random shuffling (or None for no shuffling).

    Outputs:
        t_mixid:        list of mixture IDs for training
        v_mixid:        list of mixture IDs for validation
        t_num_mixid:    list of class counts in t_mixid
        v_num_mixid:    list of class counts in v_mixid

    Examples:
        t_mixid, v_mixid, t_num_mixid, v_num_mixid = stratified_shuffle_split_mixid(mixdb, vsplit=vsplit)

    @author: Chris Eddington
    """
    import random
    from copy import deepcopy

    from sonusai import logger
    from sonusai.mixture import get_class_count_from_mixids

    if vsplit < 0 or vsplit > 1:
        raise ValueError("vsplit must be between 0 and 1")

    a_class_mixid: dict[int, list[int]] = {i + 1: [] for i in range(mixdb.num_classes)}
    for mixid, mixture in enumerate(mixdb.mixtures):
        class_count = get_class_count_from_mixids(mixdb, mixid)
        if any(class_count):
            for class_index in mixdb.target_files[mixture.targets[0].file_id].class_indices:
                a_class_mixid[class_index].append(mixid)
        else:
            # no counts and mutex mode means this is all 'other' class
            a_class_mixid[mixdb.num_classes].append(mixid)

    t_class_mixid: list[list[int]] = [[] for _ in range(mixdb.num_classes)]
    v_class_mixid: list[list[int]] = [[] for _ in range(mixdb.num_classes)]

    a_num_mixid = np.zeros(mixdb.num_classes, dtype=np.int32)
    t_num_mixid = np.zeros(mixdb.num_classes, dtype=np.int32)
    v_num_mixid = np.zeros(mixdb.num_classes, dtype=np.int32)

    if rnd_seed is not None:
        random.seed(rnd_seed)

    # For each class pick percentage of shuffled mixids for training, validation
    for ci in range(mixdb.num_classes):
        # total number of mixids for class
        a_num_mixid[ci] = len(a_class_mixid[ci + 1])

        # number of training mixids for class
        t_num_mixid[ci] = int(np.floor(a_num_mixid[ci] * (1 - vsplit)))

        # number of validation mixids for class
        v_num_mixid[ci] = a_num_mixid[ci] - t_num_mixid[ci]

        # indices for all mixids in class
        indices = [*range(a_num_mixid[ci])]
        if rnd_seed is not None:
            # randomize order
            random.shuffle(indices)

        t_class_mixid[ci] = [a_class_mixid[ci + 1][ii] for ii in indices[0 : t_num_mixid[ci]]]
        v_class_mixid[ci] = [a_class_mixid[ci + 1][ii] for ii in indices[t_num_mixid[ci] :]]

    if np.any(~(t_num_mixid > 0)):
        logger.warning(f"Some classes have zero coverage: {np.where(~(t_num_mixid > 0))[0]}")

    # Stratify over non-zero classes
    nz_indices = np.where(t_num_mixid > 0)[0]
    # First stratify pass is min count / 3 times through all classes, one each least populated class count (of non-zero)
    min_class = min(t_num_mixid[nz_indices])
    # number of mixids in each class for stratify by 1
    n0 = int(np.ceil(min_class / 3))
    # 3rd stage for stratify by 1
    n3 = int(n0)
    # 2nd stage stratify by class_count/min(class_count-n3) n2 times
    n2 = int(max(min_class - n0 - n3, 0))

    logger.info(
        f"Stratifying training, x1 cnt {n0}: x(class_count/{n2}): x1 cnt {n3} x1, "
        f"for {len(nz_indices)} populated classes"
    )

    # initialize source list
    tt = deepcopy(t_class_mixid)
    t_num_mixid2 = deepcopy(t_num_mixid)
    t_mixid = []
    for _ in range(n0):
        for ci in range(mixdb.num_classes):
            if t_num_mixid2[ci] > 0:
                # append first
                t_mixid.append(tt[ci][0])
                del tt[ci][0]
                t_num_mixid2[ci] = len(tt[ci])

    # Now extract weighted by how many are left in class minus n3
    # which will leave approx n3 remaining
    if n2 > 0:
        # should always be non-zero
        min_class = int(np.min(t_num_mixid2 - n3))
        class_count = np.floor((t_num_mixid2 - n3) / min_class)
        # class_count = np.maximum(np.floor((t_num_mixid2 - n3) / n2),0) # Counts per class
        for _ in range(min_class):
            for ci in range(mixdb.num_classes):
                if class_count[ci] > 0:
                    for _ in range(int(class_count[ci])):
                        # append first
                        t_mixid.append(tt[ci][0])
                        del tt[ci][0]
                        t_num_mixid2[ci] = len(tt[ci])

    # Now extract remaining mixids, one each class until empty
    # There should be ~n3 remaining mixids in each
    t_mixid = _extract_remaining_mixids(mixdb, t_mixid, t_num_mixid2, tt)

    if len(t_mixid) != sum(t_num_mixid):
        logger.warning("Final stratified training list length does not match starting list length.")

    if any(t_num_mixid2) or any(tt):
        logger.warning("Remaining training mixid list not empty.")

    # Now stratify the validation list, which is probably not as important, so use simple method
    # initialize source list
    vv = deepcopy(v_class_mixid)
    v_num_mixid2 = deepcopy(v_num_mixid)
    v_mixid = _extract_remaining_mixids(mixdb, [], v_num_mixid2, vv)

    if len(v_mixid) != sum(v_num_mixid):
        logger.warning("Final stratified validation list length does not match starting lists length.")

    if any(v_num_mixid2) or any(vv):
        logger.warning("Remaining validation mixid list not empty.")

    return t_mixid, v_mixid, t_num_mixid, v_num_mixid


def _extract_remaining_mixids(
    mixdb: MixtureDatabase,
    mixid: list[int],
    num_mixid: np.ndarray,
    class_mixid: list[list[int]],
) -> list[int]:
    for _ in range(max(num_mixid)):
        for ci in range(mixdb.num_classes):
            if num_mixid[ci] > 0:
                # append first
                mixid.append(class_mixid[ci][0])
                del class_mixid[ci][0]
                num_mixid[ci] = len(class_mixid[ci])

    return mixid
