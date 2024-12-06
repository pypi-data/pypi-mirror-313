import numpy as np


def calc_sample_weights(class_weights: np.ndarray, truth: np.ndarray) -> np.ndarray:
    """Calculate sample weights from class weights and a given truth with 2D or 3D shape.

    Supports one-hot encoded multi-class or binary truth/labels
    Note returns sum of weighted truth over classes, thus should also work for multi-label ? TBD

    Inputs:
      class_weights [num_classes, 1]        weights for each class
      truth         [frames, timesteps, num_classes] or [frames, num_classes]

    Returns:
      sample_weights [frames, timesteps, 1] or [frames, 1]
    """
    ts = truth.shape
    cs = class_weights.shape

    if ts[-1] == 1 and cs[0] == 2:
        # Binary truth needs 2nd "none" truth dimension
        truth = np.concatenate((truth, 1 - truth), axis=1)

    # broadcast [num_classes, 1] over [frames, num_classes] or [frames, timesteps, num_classes]
    return np.sum(class_weights * truth, axis=-1)
