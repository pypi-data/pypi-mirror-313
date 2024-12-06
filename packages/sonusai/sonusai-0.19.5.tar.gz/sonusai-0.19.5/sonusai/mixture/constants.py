import re
from importlib.resources import as_file
from importlib.resources import files

REQUIRED_CONFIGS = [
    "asr_configs",
    "class_balancing",
    "class_balancing_augmentation",
    "class_indices",
    "class_labels",
    "class_weights_threshold",
    "feature",
    "impulse_responses",
    "noise_augmentations",
    "noise_mix_mode",
    "noises",
    "num_classes",
    "random_snrs",
    "seed",
    "snrs",
    "spectral_masks",
    "target_augmentations",
    "target_level_type",
    "targets",
    "truth_configs",
]
OPTIONAL_CONFIGS: list[str] = []
VALID_CONFIGS = REQUIRED_CONFIGS + OPTIONAL_CONFIGS
REQUIRED_TRUTH_CONFIGS = ["function", "stride_reduction"]
REQUIRED_ASR_CONFIGS = ["engine"]
VALID_AUGMENTATIONS = [
    "normalize",
    "gain",
    "pitch",
    "tempo",
    "eq1",
    "eq2",
    "eq3",
    "lpf",
    "ir",
    "mixup",
]
VALID_NOISE_MIX_MODES = ["exhaustive", "non-exhaustive", "non-combinatorial"]
RAND_PATTERN = re.compile(r"rand\(([-+]?(\d+(\.\d*)?|\.\d+)),\s*([-+]?(\d+(\.\d*)?|\.\d+))\)")
SAMPLE_RATE = 16000
BIT_DEPTH = 32
ENCODING = "floating-point"
CHANNEL_COUNT = 1
SAMPLE_BYTES = BIT_DEPTH // 8
FLOAT_BYTES = 4
MIXDB_VERSION = 2

with as_file(files("sonusai.data").joinpath("whitenoise.wav")) as path:
    DEFAULT_NOISE = str(path)

with as_file(files("sonusai.data").joinpath("genmixdb.yml")) as path:
    DEFAULT_CONFIG = str(path)

with as_file(files("sonusai.data").joinpath("speech_ma01_01.wav")) as path:
    DEFAULT_SPEECH = str(path)
