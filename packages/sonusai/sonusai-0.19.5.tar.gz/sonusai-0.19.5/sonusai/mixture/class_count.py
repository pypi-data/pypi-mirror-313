from sonusai.mixture.datatypes import ClassCount
from sonusai.mixture.datatypes import GeneralizedIDs
from sonusai.mixture.mixdb import MixtureDatabase


def get_class_count_from_mixids(mixdb: MixtureDatabase, mixids: GeneralizedIDs | None = None) -> ClassCount:
    """Sums the class counts for given mixids"""
    total_class_count = [0] * mixdb.num_classes
    m_ids = mixdb.mixids_to_list(mixids)
    for m_id in m_ids:
        class_count = mixdb.mixture_class_count(m_id)
        for cl in range(mixdb.num_classes):
            total_class_count[cl] += class_count[cl]

    return total_class_count
