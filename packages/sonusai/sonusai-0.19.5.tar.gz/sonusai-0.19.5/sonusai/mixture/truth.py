from sonusai.mixture.datatypes import AudioT
from sonusai.mixture.datatypes import Truth
from sonusai.mixture.datatypes import TruthConfig
from sonusai.mixture.mixdb import MixtureDatabase


def truth_function(
    target_audio: AudioT,
    noise_audio: AudioT,
    mixture_audio: AudioT,
    config: TruthConfig,
    feature: str,
    num_classes: int,
    class_indices: list[int],
    target_gain: float,
) -> Truth:
    from sonusai.mixture import truth_functions

    from .truth_functions.datatypes import TruthFunctionConfig
    from .truth_functions.datatypes import TruthFunctionData

    t_config = TruthFunctionConfig(
        feature=feature,
        num_classes=num_classes,
        class_indices=class_indices,
        target_gain=target_gain,
        config=config.config,
    )
    t_data = TruthFunctionData(target_audio, noise_audio, mixture_audio)

    try:
        return getattr(truth_functions, config.function)(t_data, t_config)
    except AttributeError as e:
        raise AttributeError(f"Unsupported truth function: {config.function}") from e
    except Exception as e:
        raise RuntimeError(f"Error in truth function '{config.function}': {e}") from e


def get_truth_indices_for_mixid(mixdb: MixtureDatabase, mixid: int) -> list[int]:
    """Get a list of truth indices for a given mixid."""
    indices: list[int] = []
    for target_id in [target.file_id for target in mixdb.mixture(mixid).targets]:
        indices.append(*mixdb.target_file(target_id).class_indices)

    return sorted(set(indices))


def truth_stride_reduction(truth: Truth, function: str) -> Truth:
    """Reduce stride dimension of truth.

    :param truth: Truth data [frames, stride, truth_parameters]
    :param function: Truth stride reduction function name
    :return: Stride reduced truth data [frames, stride or 1, truth_parameters]
    """
    import numpy as np

    if truth.ndim != 3:
        raise ValueError("Invalid truth shape")

    if function == "none":
        return truth

    if function == "max":
        return np.max(truth, axis=1, keepdims=True)

    if function == "mean":
        return np.mean(truth, axis=1, keepdims=True)

    if function == "first":
        return truth[:, 0, :].reshape((truth.shape[0], 1, truth.shape[2]))

    raise ValueError(f"Invalid truth stride reduction function: {function}")
