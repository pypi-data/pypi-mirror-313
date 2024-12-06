from typing import Any


def _get_hdf5_name(location: str, index: str) -> str:
    from os.path import join

    return join(location, index + ".h5")


def _get_pickle_name(location: str, index: str, item: str) -> str:
    from os.path import join

    return join(location, index, item + ".pkl")


def read_hdf5_data(location: str, index: str, items: list[str] | str) -> Any:
    """Read mixture, target, or noise data from an HDF5 file

    :param location: Location of the file
    :param index: Mixture, target, or noise index
    :param items: String(s) of data to retrieve
    :return: Data (or tuple of data)
    """
    from os.path import exists
    from typing import Any

    import h5py
    import numpy as np

    def _get_dataset(file: h5py.File, d_name: str) -> Any:
        if d_name in file:
            data = np.array(file[d_name])
            if data.size == 1:
                item = data.item()
                if isinstance(item, bytes):
                    return item.decode("utf-8")
                return item
            return data
        return None

    if not isinstance(items, list):
        items = [items]

    h5_name = _get_hdf5_name(location, index)
    if exists(h5_name):
        try:
            with h5py.File(h5_name, "r") as f:
                result = [_get_dataset(f, item) for item in items]
        except Exception as e:
            raise OSError(f"Error reading {h5_name}: {e}") from e
    else:
        result = [None for _ in items]

    if len(items) == 1:
        result = result[0]

    return result


def write_hdf5_data(location: str, index: str, items: list[tuple[str, Any]] | tuple[str, Any]) -> None:
    """Write mixture, target, or noise data to an HDF5 file

    :param location: Location of the file
    :param index: Mixture, target, or noise index
    :param items: Tuple(s) of (name, data)
    """
    import h5py

    if not isinstance(items, list):
        items = [items]

    h5_name = _get_hdf5_name(location, index)
    with h5py.File(h5_name, "a") as f:
        for item in items:
            if item[0] in f:
                del f[item[0]]
            f.create_dataset(name=item[0], data=item[1])


def read_pickle_data(location: str, index: str, items: list[str] | str) -> Any:
    """Read mixture, target, or noise data from a pickle file

    :param location: Location of the file
    :param index: Mixture, target, or noise index
    :param items: String(s) of data to retrieve
    :return: Data (or tuple of data)
    """
    import pickle
    from os.path import exists
    from typing import Any

    if not isinstance(items, list):
        items = [items]

    result: list[Any] = []
    for item in items:
        pkl_name = _get_pickle_name(location, index, item)
        if exists(pkl_name):
            with open(pkl_name, "rb") as f:
                result.append(pickle.load(f))  # noqa: S301
        else:
            result.append(None)

    if len(items) == 1:
        result = result[0]

    return result


def write_pickle_data(location: str, index: str, items: list[tuple[str, Any]] | tuple[str, Any]) -> None:
    """Write mixture, target, or noise data to a pickle file

    :param location: Location of the file
    :param index: Mixture, target, or noise index
    :param items: Tuple(s) of (name, data)
    """
    import pickle
    from os import makedirs
    from os.path import join

    if not isinstance(items, list):
        items = [items]

    makedirs(join(location, index), exist_ok=True)
    for item in items:
        pkl_name = _get_pickle_name(location, index, item[0])
        with open(pkl_name, "wb") as f:
            f.write(pickle.dumps(item[1]))


def read_cached_data(location: str, name: str, index: str, items: list[str] | str) -> Any:
    """Read cached data from a file

    :param location: Location of the mixture database
    :param name: Data name ('mixture', 'target', or 'noise')
    :param index: Data index (mixture, target, or noise ID)
    :param items: String(s) of data to retrieve
    :return: Data (or tuple of data)
    """
    from os.path import join

    return read_pickle_data(join(location, name), index, items)


def write_cached_data(location: str, name: str, index: str, items: list[tuple[str, Any]] | tuple[str, Any]) -> None:
    """Write mixture data to a file

    :param location: Location of the mixture database
    :param name: Data name ('mixture', 'target', or 'noise')
    :param index: Data index (mixture, target, or noise ID)
    :param items: Tuple(s) of (name, data)
    """
    from os.path import join

    write_pickle_data(join(location, name), index, items)
