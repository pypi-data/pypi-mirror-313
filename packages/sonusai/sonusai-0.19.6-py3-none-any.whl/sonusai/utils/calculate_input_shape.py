def calculate_input_shape(feature: str, flatten: bool = False, timesteps: int = 0, add1ch: bool = False) -> list[int]:
    """
    Calculate input shape given feature and user-specified reshape parameters.

    Inputs:
        feature:     String defining the Aaware feature used in SonusAI, typically  mixdb.feature.
        flatten:     If true, flatten the 2D spectrogram from SxB to S*B.
        timesteps:   Pre-pend timesteps dimension if non-zero, size = timesteps.
        add1ch:      Append channel dimension of size 1, (channel last).
    """
    from pyaaware import FeatureGenerator

    fg = FeatureGenerator(feature_mode=feature)

    if flatten:
        in_shape = [fg.stride * fg.feature_parameters]
    else:
        in_shape = [fg.stride, fg.feature_parameters]

    if timesteps > 0:
        in_shape.insert(0, timesteps)

    if add1ch:
        in_shape.append(1)

    return in_shape
