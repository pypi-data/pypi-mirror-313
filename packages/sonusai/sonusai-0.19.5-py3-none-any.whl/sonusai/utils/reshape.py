import numpy as np

from sonusai.mixture.datatypes import Feature
from sonusai.mixture.datatypes import Predict
from sonusai.mixture.datatypes import Truth


def get_input_shape(feature: Feature) -> tuple[int, ...]:
    return feature.shape[1:]


def reshape_inputs(
    feature: Feature,
    batch_size: int,
    truth: Truth | None = None,
    timesteps: int = 0,
    flatten: bool = False,
    add1ch: bool = False,
) -> tuple[Feature, Truth | None]:
    """Check SonusAI feature and truth data and reshape feature of size [frames, strides, feature_parameters] into
    one of several options:

    If timesteps > 0: (i.e., for recurrent NNs):
      no-flatten, no-channel:   [sequences, timesteps, strides, feature_parameters]      (4-dim)
      flatten, no-channel:      [sequences, timesteps, strides*feature_parameters]       (3-dim)
      no-flatten, add-1channel: [sequences, timesteps, strides, feature_parameters, 1]   (5-dim)
      flatten, add-1channel:    [sequences, timesteps, strides*feature_parameters, 1]    (4-dim)

    If batch_size is None, then do not reshape; just calculate new input shape and return.

    If timesteps == 0, then do not add timesteps dimension.

    The number of samples is trimmed to be a multiple of batch_size (Keras requirement) for
    both feature and truth.
    Channel is added to last/outer dimension for channel_last support in Keras/TF.

    Returns:
      feature       reshaped feature
      truth         reshaped truth
    """
    frames, strides, feature_parameters = feature.shape
    if truth is not None:
        truth_frames, num_classes = truth.shape
        # Double-check correctness of inputs
        if frames != truth_frames:
            raise ValueError("Frames in feature and truth do not match")
    else:
        num_classes = 0

    if flatten:
        feature = np.reshape(feature, (frames, strides * feature_parameters))

    # Reshape for Keras/TF recurrent models that require timesteps/sequence length dimension
    if timesteps > 0:
        sequences = frames // timesteps

        # Remove frames if remainder exists (not fitting into a multiple of new number of sequences)
        frames_rem = frames % timesteps
        batch_rem = (frames // timesteps) % batch_size
        bf_rem = batch_rem * timesteps
        sequences = sequences - batch_rem
        fr2drop = frames_rem + bf_rem
        if fr2drop:
            if feature.ndim == 2:
                feature = feature[0:-fr2drop,]  # flattened input
            elif feature.ndim == 3:
                feature = feature[0:-fr2drop,]  # un-flattened input

            if truth is not None:
                truth = truth[0:-fr2drop,]

        # Reshape
        if feature.ndim == 2:  # flattened input
            # was [frames, feature_parameters*timesteps]
            feature = np.reshape(feature, (sequences, timesteps, strides * feature_parameters))
            if truth is not None:
                # was [frames, num_classes]
                truth = np.reshape(truth, (sequences, timesteps, num_classes))
        elif feature.ndim == 3:  # un-flattened input
            # was [frames, feature_parameters, timesteps]
            feature = np.reshape(feature, (sequences, timesteps, strides, feature_parameters))
            if truth is not None:
                # was [frames, num_classes]
                truth = np.reshape(truth, (sequences, timesteps, num_classes))
    else:
        # Drop frames if remainder exists (not fitting into a multiple of new number of sequences)
        fr2drop = feature.shape[0] % batch_size
        if fr2drop > 0:
            feature = feature[0:-fr2drop,]
            if truth is not None:
                truth = truth[0:-fr2drop,]

    # Add channel dimension if required for input to model (i.e. for cnn type input)
    if add1ch:
        feature = np.expand_dims(feature, axis=feature.ndim)  # add as last/outermost dim

    return feature, truth


def get_num_classes_from_predict(predict: Predict, timesteps: int = 0) -> int:
    num_dims = predict.ndim
    dims = predict.shape

    if num_dims == 3 or (num_dims == 2 and timesteps > 0):
        # 2D with timesteps - [frames, timesteps]
        if num_dims == 2:
            return 1

        # 3D - [frames, timesteps, num_classes]
        return dims[2]

    # 1D - [frames]
    if num_dims == 1:
        return 1

    # 2D without timesteps - [frames, num_classes]
    return dims[1]


def reshape_outputs(predict: Predict, truth: Truth | None = None, timesteps: int = 0) -> tuple[Predict, Truth | None]:
    """Reshape model output data.

    truth and predict can be either [frames, num_classes], or [frames, timesteps, num_classes]
    In binary case, num_classes dim may not exist; detect this and set num_classes to 1.
    """
    if truth is not None and predict.shape != truth.shape:
        raise ValueError("predict and truth shapes do not match")

    ndim = predict.ndim
    shape = predict.shape

    if not (0 < ndim <= 3):
        raise ValueError(f"do not know how to reshape data with {ndim} dimensions")

    if ndim == 3 or (ndim == 2 and timesteps > 0):
        if ndim == 2:
            # 2D with timesteps - [frames, timesteps]
            num_classes = 1
        else:
            # 3D - [frames, timesteps, num_classes]
            num_classes = shape[2]

        # reshape to remove timestep dimension
        shape = (shape[0] * shape[1], num_classes)
        predict = np.reshape(predict, shape)
        if truth is not None:
            truth = np.reshape(truth, shape)
    elif ndim == 1:
        # convert to 2D - [frames, 1]
        predict = np.expand_dims(predict, 1)
        if truth is not None:
            truth = np.expand_dims(truth, 1)

    return predict, truth
