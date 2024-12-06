from collections.abc import Callable
from typing import Any

from sonusai.mixture.datatypes import GeneralizedIDs
from sonusai.mixture.mixdb import MixtureDatabase


def get_mixids_from_mixture_field_predicate(
    mixdb: MixtureDatabase,
    field: str,
    mixids: GeneralizedIDs = "*",
    predicate: Callable[[Any], bool] | None = None,
) -> dict[int, list[int]]:
    """
    Generate mixture IDs based on mixture field and predicate
    Return a dictionary where:
        - keys are the matching field values
        - values are lists of the mixids that match the criteria
    """
    mixid_out = mixdb.mixids_to_list(mixids)

    if predicate is None:

        def predicate(_: Any) -> bool:
            return True

    criteria_set = set()
    for m_id in mixid_out:
        value = getattr(mixdb.mixture(m_id), field)
        if isinstance(value, list):
            for v in value:
                if predicate(v):
                    criteria_set.add(v)
        elif predicate(value):
            criteria_set.add(value)
    criteria = sorted(criteria_set)

    result: dict[int, list[int]] = {}
    for criterion in criteria:
        result[criterion] = []
        for m_id in mixid_out:
            value = getattr(mixdb.mixture(m_id), field)
            if isinstance(value, list):
                for v in value:
                    if v == criterion:
                        result[criterion].append(m_id)
            elif value == criterion:
                result[criterion].append(m_id)

    return result


def get_mixids_from_truth_configs_field_predicate(
    mixdb: MixtureDatabase,
    field: str,
    mixids: GeneralizedIDs = "*",
    predicate: Callable[[Any], bool] | None = None,
) -> dict[int, list[int]]:
    """
    Generate mixture IDs based on target truth_configs field and predicate
    Return a dictionary where:
        - keys are the matching field values
        - values are lists of the mixids that match the criteria
    """
    from sonusai.mixture import REQUIRED_TRUTH_CONFIGS

    mixid_out = mixdb.mixids_to_list(mixids)

    # Get all field values
    values = get_all_truth_configs_values_from_field(mixdb, field)

    if predicate is None:

        def predicate(_: Any) -> bool:
            return True

    # Get only values of interest
    values = [value for value in values if predicate(value)]

    result = {}
    for value in values:
        # Get a list of targets for each field value
        indices = []
        for t_id in mixdb.target_file_ids:
            target = mixdb.target_file(t_id)
            for truth_config in target.truth_configs.values():
                if field in REQUIRED_TRUTH_CONFIGS:
                    if value in getattr(truth_config, field):
                        indices.append(t_id)
                else:
                    if value in getattr(truth_config.config, field):
                        indices.append(t_id)
        indices = sorted(set(indices))

        mixids = []
        for index in indices:
            for m_id in mixid_out:
                if index in [target.file_id for target in mixdb.mixture(m_id).targets]:
                    mixids.append(m_id)

        mixids = sorted(set(mixids))
        if mixids:
            result[value] = mixids

    return result


def get_all_truth_configs_values_from_field(mixdb: MixtureDatabase, field: str) -> list:
    """
    Generate a list of all values corresponding to the given field in truth_configs
    """
    from sonusai.mixture import REQUIRED_TRUTH_CONFIGS

    result = []
    for target in mixdb.target_files:
        for truth_config in target.truth_configs.values():
            if field in REQUIRED_TRUTH_CONFIGS:
                value = getattr(truth_config, field)
            else:
                value = getattr(truth_config.config, field, None)
            if isinstance(value, str):
                value = [value]
            result.extend(value)

    return sorted(set(result))


def get_mixids_from_noise(
    mixdb: MixtureDatabase,
    mixids: GeneralizedIDs = "*",
    predicate: Callable[[Any], bool] | None = None,
) -> dict[int, list[int]]:
    """
    Generate mixids based on noise index predicate
    Return a dictionary where:
        - keys are the noise indices
        - values are lists of the mixids that match the noise index
    """
    return get_mixids_from_mixture_field_predicate(mixdb=mixdb, mixids=mixids, field="noise_id", predicate=predicate)


def get_mixids_from_target(
    mixdb: MixtureDatabase,
    mixids: GeneralizedIDs = "*",
    predicate: Callable[[Any], bool] | None = None,
) -> dict[int, list[int]]:
    """
    Generate mixids based on a target index predicate
    Return a dictionary where:
        - keys are the target indices
        - values are lists of the mixids that match the target index
    """
    return get_mixids_from_mixture_field_predicate(mixdb=mixdb, mixids=mixids, field="target_ids", predicate=predicate)


def get_mixids_from_snr(
    mixdb: MixtureDatabase,
    mixids: GeneralizedIDs = "*",
    predicate: Callable[[Any], bool] | None = None,
) -> dict[float, list[int]]:
    """
    Generate mixids based on an SNR predicate
    Return a dictionary where:
        - keys are the SNRs
        - values are lists of the mixids that match the SNR
    """
    from typing import Any

    mixid_out = mixdb.mixids_to_list(mixids)

    # Get all the SNRs
    snrs = [float(snr) for snr in mixdb.all_snrs if not snr.is_random]

    if predicate is None:

        def predicate(_: Any) -> bool:
            return True

    # Get only the SNRs of interest (filter on predicate)
    snrs = [snr for snr in snrs if predicate(snr)]

    result: dict[float, list[int]] = {}
    for snr in snrs:
        # Get a list of mixids for each SNR
        result[snr] = sorted([i for i, mixture in enumerate(mixdb.mixtures) if mixture.snr == snr and i in mixid_out])

    return result


def get_mixids_from_class_indices(
    mixdb: MixtureDatabase,
    mixids: GeneralizedIDs = "*",
    predicate: Callable[[Any], bool] | None = None,
) -> dict[int, list[int]]:
    """
    Generate mixids based on a class index predicate
    Return a dictionary where:
        - keys are the class indices
        - values are lists of the mixids that match the class index
    """
    mixid_out = mixdb.mixids_to_list(mixids)

    if predicate is None:

        def predicate(_: Any) -> bool:
            return True

    criteria_set = set()
    for m_id in mixid_out:
        class_indices = mixdb.mixture_class_indices(m_id)
        for class_index in class_indices:
            if predicate(class_index):
                criteria_set.add(class_index)
    criteria = sorted(criteria_set)

    result: dict[int, list[int]] = {}
    for criterion in criteria:
        result[criterion] = []
        for m_id in mixid_out:
            class_indices = mixdb.mixture_class_indices(m_id)
            for class_index in class_indices:
                if class_index == criterion:
                    result[criterion].append(m_id)

    return result


def get_mixids_from_truth_function(
    mixdb: MixtureDatabase,
    mixids: GeneralizedIDs = "*",
    predicate: Callable[[Any], bool] | None = None,
) -> dict[int, list[int]]:
    """
    Generate mixids based on a truth function predicate
    Return a dictionary where:
        - keys are the truth functions
        - values are lists of the mixids that match the truth function
    """
    return get_mixids_from_truth_configs_field_predicate(
        mixdb=mixdb, mixids=mixids, field="function", predicate=predicate
    )
