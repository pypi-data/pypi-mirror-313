import numpy as np

from sonusai.mixture.datatypes import GeneralizedIDs
from sonusai.mixture.datatypes import Truth
from sonusai.mixture.mixdb import MixtureDatabase


def calc_class_weights_from_truth(truth: Truth, other_weight: float | None = None, other_index: int = -1) -> np.ndarray:
    """Calculate class weights.

    Supports non-existent classes (a problem with sklearn) where non-existent
    classes get a weight of 0 (instead of inf).
    Includes optional weighting of an "other" class if specified.

    Reference:
        weights = class_weight.compute_class_weight(class_weight='balanced', classes=clabels, y=labels)

    Arguments:
        truth: Truth data in one-hot format. Size can be:
          - [frames, timesteps, num_classes]
          - [frames, num_classes]
        other_weight: float or `None`. Weight of the "other" class.
            > 1 = increase weighting/importance relative to the true count
            0 > `other_weight` < 1 = decrease weighting/importance relative
            < 0 or `None` = disable, use true count (default = `None`)
        other_index: int. Index of the "other" class in one-hot mode. Defaults to -1 (the last).

    Returns:
        A numpy array containing class weights.
    """
    frames, num_classes = truth.shape

    if num_classes > 1:
        labels = np.argmax(truth, axis=-1)  # [frames, 1 labels] from one-hot, last dim
        count = np.bincount(labels, minlength=num_classes).astype(float)
    else:
        num_classes = 2
        labels = np.array(truth >= 0.5).astype(np.int8)[:, 0]  # quantize to binary and shape (frames,) for bincount
        count = np.bincount(labels, minlength=num_classes).astype(float)

    if other_weight is not None and other_weight > 0:
        count[other_index] = count[other_index] / np.float32(other_weight)

    weights = np.empty((len(count)), dtype=np.float32)
    for n in range(len(weights)):
        if count[n] == 0:
            # Avoid sklearn problem with absent classes and assign non-existent classes a weight of 0.
            weights[n] = 0
        else:
            weights[n] = frames / (num_classes * count[n])

    return weights


def calc_class_weights_from_mixdb(
    mixdb: MixtureDatabase,
    mixids: GeneralizedIDs | None = None,
    other_weight: float = 1,
    other_index: int = -1,
) -> tuple[np.ndarray, np.ndarray]:
    """Calculate class weights using estimated feature counts from a mixture database.

    Arguments:
        mixdb: Mixture database.
        mixids: Mixture ID's.
        other_weight: float or `None`. Weight of the "other" class.
            > 1 = increase weighting/importance relative to the true count
            0 > `other_weight` < 1 = decrease weighting/importance relative
            < 0 or `None` = disable, use true count
        other_index: int. Index of the "other" class in one-hot mode. Defaults to -1 (the last).

    Returns:
        count: Count of features in each class.
        weights: Class weights. [num_classes, 1]
            Note: for Keras use dict(enumerate(weights))
    """
    from sonusai.mixture import get_class_count_from_mixids

    count = np.ceil(np.array(get_class_count_from_mixids(mixdb=mixdb, mixids=mixids)) / mixdb.feature_step_samples)
    if mixdb.truth_mutex and other_weight is not None and other_weight > 0:
        count[other_index] = count[other_index] / np.float32(other_weight)
    total_features = sum(count)

    weights = np.empty(mixdb.num_classes, dtype=np.float32)
    for n in range(len(weights)):
        if count[n] == 0:
            # Avoid sklearn problem with absent classes and assign non-existent classes a weight of 0.
            weights[n] = 0
        else:
            weights[n] = total_features / (mixdb.num_classes * count[n])

    return count, weights
