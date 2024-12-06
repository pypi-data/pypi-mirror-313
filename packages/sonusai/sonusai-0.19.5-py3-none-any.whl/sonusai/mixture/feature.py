from sonusai.mixture.datatypes import AudioT
from sonusai.mixture.datatypes import Feature


def get_feature_from_audio(
    audio: AudioT,
    feature_mode: str,
) -> Feature:
    """Apply forward transform and generate feature data from audio data

    :param audio: Time domain audio data [samples]
    :param feature_mode: Feature mode
    :return: Feature data [frames, strides, feature_parameters]
    """
    import numpy as np
    from pyaaware import FeatureGenerator

    from .datatypes import TransformConfig
    from .helpers import forward_transform

    fg = FeatureGenerator(feature_mode=feature_mode)

    audio_f = forward_transform(
        audio=audio,
        config=TransformConfig(
            length=fg.ftransform_length,
            overlap=fg.ftransform_overlap,
            bin_start=fg.bin_start,
            bin_end=fg.bin_end,
            ttype=fg.ftransform_ttype,
        ),
    )

    transform_frames = audio_f.shape[0]
    feature_frames = transform_frames // (fg.decimation * fg.step)
    feature = np.empty((feature_frames, fg.stride, fg.feature_parameters), dtype=np.float32)

    feature_frame = 0
    for transform_frame in range(transform_frames):
        fg.execute(audio_f[transform_frame])

        if fg.eof():
            feature[feature_frame] = fg.feature()
            feature_frame += 1

    return feature


def get_audio_from_feature(
    feature: Feature,
    feature_mode: str,
    num_classes: int | None = 1,
    truth_mutex: bool | None = False,
) -> AudioT:
    """Apply inverse transform to feature data to generate audio data

    :param feature: Feature data [frames, stride=1, feature_parameters]
    :param feature_mode: Feature mode
    :param num_classes: Number of classes
    :param truth_mutex: Whether to calculate 'other' label
    :return: Audio data [samples]
    """
    import numpy as np
    from pyaaware import FeatureGenerator

    from sonusai.utils.compress import power_uncompress
    from sonusai.utils.stacked_complex import unstack_complex

    from .datatypes import TransformConfig
    from .helpers import inverse_transform

    if feature.ndim != 3:
        raise ValueError("feature must have 3 dimensions: [frames, stride=1, feature_parameters]")

    if feature.shape[1] != 1:
        raise ValueError("Strided feature data is not supported for audio extraction; stride must be 1.")

    fg = FeatureGenerator(feature_mode=feature_mode, num_classes=num_classes, truth_mutex=truth_mutex)

    feature_complex = unstack_complex(feature.squeeze())
    if feature_mode[0:1] == "h":
        feature_complex = power_uncompress(feature_complex)
    return np.squeeze(
        inverse_transform(
            transform=feature_complex,
            config=TransformConfig(
                length=fg.itransform_length,
                overlap=fg.itransform_overlap,
                bin_start=fg.bin_start,
                bin_end=fg.bin_end,
                ttype=fg.itransform_ttype,
            ),
        )
    )
