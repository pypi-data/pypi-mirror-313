from sonusai.mixture.datatypes import Truth
from sonusai.mixture.truth_functions.datatypes import TruthFunctionConfig
from sonusai.mixture.truth_functions.datatypes import TruthFunctionData


def file_validate(config: dict) -> None:
    import h5py

    if len(config) == 0:
        raise AttributeError("file truth function is missing config")

    if "file" not in config:
        raise AttributeError("file truth function is missing required 'file'")

    with h5py.File(config["file"], "r") as f:
        if "truth_f" not in f:
            raise ValueError("Truth file does not contain truth_f dataset")


def file_parameters(config: TruthFunctionConfig) -> int:
    import h5py
    import numpy as np

    with h5py.File(config.config["file"], "r") as f:
        truth = np.array(f["truth_f"])

    return truth.shape[-1]


def file(data: TruthFunctionData, config: TruthFunctionConfig) -> Truth:
    """file truth function documentation"""
    import h5py
    import numpy as np

    with h5py.File(config.config["file"], "r") as f:
        truth = np.array(f["truth_f"])

    if truth.ndim != 2:
        raise ValueError("Truth file data is not 2 dimensions")

    if truth.shape[0] != len(data.target_audio) // config.frame_size:
        raise ValueError("Truth file does not contain the right amount of frames")

    return truth
