def max_text_width(number_of_items: int) -> int:
    """Compute maximum text width for the indices of a sequence of items.

    :param number_of_items: Total number of items in sequence
    :return: Text width of largest item index
    """
    import numpy as np

    return int(np.ceil(np.log10(number_of_items)))
