from dataclasses import dataclass

from sonusai.mixture.datatypes import AudioT


class TruthFunctionConfig:
    def __init__(self, feature: str, num_classes: int, class_indices: list[int], target_gain: float, config: dict):
        from pyaaware import ForwardTransform
        from pyaaware import InverseTransform
        from pyaaware import feature_forward_transform_config
        from pyaaware import feature_inverse_transform_config
        from pyaaware import feature_parameters

        self.feature = feature
        self.num_classes = num_classes
        self.class_indices = class_indices
        self.target_gain = target_gain
        self.config = config

        self.feature_parameters = feature_parameters(feature)
        ft_config = feature_forward_transform_config(feature)
        it_config = feature_inverse_transform_config(feature)

        self.ttype = it_config["ttype"]
        self.frame_size = it_config["overlap"]

        self.target_fft = ForwardTransform(**ft_config)
        self.noise_fft = ForwardTransform(**ft_config)
        self.mixture_fft = ForwardTransform(**ft_config)
        self.swin = InverseTransform(**it_config).window


@dataclass
class TruthFunctionData:
    target_audio: AudioT
    noise_audio: AudioT
    mixture_audio: AudioT
