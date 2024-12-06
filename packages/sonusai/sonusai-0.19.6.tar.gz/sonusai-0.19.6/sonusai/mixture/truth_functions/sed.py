from sonusai.mixture.datatypes import Truth
from sonusai.mixture.truth_functions.datatypes import TruthFunctionConfig
from sonusai.mixture.truth_functions.datatypes import TruthFunctionData


def _strictly_decreasing(list_to_check: list) -> bool:
    from itertools import pairwise

    return all(x > y for x, y in pairwise(list_to_check))


def sed_validate(config: dict) -> None:
    if len(config) == 0:
        raise AttributeError("sed truth function is missing config")

    parameters = ["thresholds"]
    for parameter in parameters:
        if parameter not in config:
            raise AttributeError(f"sed truth function is missing required '{parameter}'")

    thresholds = config["thresholds"]
    if not _strictly_decreasing(thresholds):
        raise ValueError(f"sed truth function 'thresholds' are not strictly decreasing: {thresholds}")


def sed_parameters(config: TruthFunctionConfig) -> int:
    return config.num_classes


def sed(data: TruthFunctionData, config: TruthFunctionConfig) -> Truth:
    """Sound energy detection truth generation function

    Calculates sound energy detection truth using simple 3 threshold
    hysteresis algorithm. SED outputs 3 possible probabilities of
    sound presence: 1.0 present, 0.5 (transition/uncertain), 0 not
    present. The output values will be assigned to the truth output
    at the index specified in the config.

    Output shape: [:, num_classes]

    index       Truth index <int> or list(<int>)

    index indicates which truth fields should be set.
    0 indicates none, 1 is first element in truth output vector, 2 2nd element, etc.

                Examples:
                  index = 5       truth in class 5, truth(4, 1)
                  index = [1, 5]  truth in classes 1 and 5, truth([0, 4], 1)

                In mutually-exclusive mode, a frame is expected to only
                belong to one class and thus all probabilities must sum to
                1. This is effectively truth for a classifier with multichannel
                softmax output.

                For multi-label classification each class is an individual
                probability for that class and any given frame can be
                assigned to multiple classes/labels, i.e., the classes are
                not mutually-exclusive. For example, a NN classifier with
                multichannel sigmoid output. In this case, index could
                also be a vector with multiple class indices.
    """
    import numpy as np
    import torch
    from pyaaware import SED

    if len(data.target_audio) % config.frame_size != 0:
        raise ValueError(f"Number of samples in audio is not a multiple of {config.frame_size}")

    frames = config.target_fft.frames(data.target_audio)
    parameters = sed_parameters(config)
    if config.target_gain == 0:
        return np.zeros((frames, parameters), dtype=np.float32)

    # SED wants 1-based indices
    s = SED(
        thresholds=config.config["thresholds"],
        index=config.class_indices,
        frame_size=config.frame_size,
        num_classes=config.num_classes,
    )

    # Back out target gain
    target_audio = data.target_audio / config.target_gain

    # Compute energy
    target_energy = config.target_fft.execute_all(torch.from_numpy(target_audio))[1].numpy()

    if frames != target_energy.shape[0]:
        raise ValueError("Incorrect frames calculation in sed truth function")

    return s.execute_all(target_energy)
