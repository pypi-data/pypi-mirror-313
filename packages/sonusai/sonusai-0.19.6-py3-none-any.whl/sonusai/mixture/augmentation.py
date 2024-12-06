from sonusai.mixture.datatypes import AudioT
from sonusai.mixture.datatypes import Augmentation
from sonusai.mixture.datatypes import AugmentationRule
from sonusai.mixture.datatypes import AugmentationRules
from sonusai.mixture.datatypes import ImpulseResponseData
from sonusai.mixture.datatypes import OptionalNumberStr


def get_augmentation_rules(rules: list[dict] | dict, num_ir: int = 0) -> AugmentationRules:
    """Generate augmentation rules from list of input rules

    :param rules: Dictionary of augmentation config rule[s]
    :param num_ir: Number of impulse responses in config
    :return: List of augmentation rules
    """
    from sonusai.utils import dataclass_from_dict

    from .datatypes import AugmentationRule

    processed_rules: list[dict] = []
    if not isinstance(rules, list):
        rules = [rules]

    for rule in rules:
        rule = _parse_ir(rule, num_ir)
        processed_rules = _expand_rules(expanded_rules=processed_rules, rule=rule)

    return [dataclass_from_dict(AugmentationRule, processed_rule) for processed_rule in processed_rules]


def _expand_rules(expanded_rules: list[dict], rule: dict) -> list[dict]:
    """Expand rules

    :param expanded_rules: Working list of expanded rules
    :param rule: Rule to process
    :return: List of expanded rules
    """
    from copy import deepcopy

    from sonusai.utils import convert_string_to_number

    from .constants import VALID_AUGMENTATIONS
    from .eq_rule_is_valid import eq_rule_is_valid

    for key, value in list(rule.items()):
        if value is None:
            del rule[key]

    # replace old 'eq' rule with new 'eq1' rule to allow both for backward compatibility
    rule = {"eq1" if key == "eq" else key: value for key, value in rule.items()}

    for key in rule:
        if key not in VALID_AUGMENTATIONS:
            nice_list = "\n".join([f"  {item}" for item in VALID_AUGMENTATIONS])
            raise ValueError(f"Invalid augmentation: {key}.\nValid augmentations are:\n{nice_list}")

        if key in ["eq1", "eq2", "eq3"]:
            if not eq_rule_is_valid(rule[key]):
                raise ValueError(f"Invalid augmentation value for {key}: {rule[key]}")

            if all(isinstance(el, list) or (isinstance(el, str) and el == "none") for el in rule[key]):
                # Expand multiple rules
                for value in rule[key]:
                    expanded_rule = deepcopy(rule)
                    if isinstance(value, str) and value == "none":
                        expanded_rule[key] = None
                    else:
                        expanded_rule[key] = deepcopy(value)
                    _expand_rules(expanded_rules, expanded_rule)
                return expanded_rules

        elif key in ["mixup"]:
            pass

        else:
            if isinstance(rule[key], list):
                for value in rule[key]:
                    if isinstance(value, list):
                        raise TypeError(f"Invalid augmentation value for {key}: {rule[key]}")
                    expanded_rule = deepcopy(rule)
                    expanded_rule[key] = deepcopy(value)
                    _expand_rules(expanded_rules, expanded_rule)
                return expanded_rules
            else:
                rule[key] = convert_string_to_number(rule[key])
                if not (isinstance(rule[key], float | int) or rule[key].startswith("rand") or rule[key] == "none"):
                    raise ValueError(f"Invalid augmentation value for {key}: {rule[key]}")

    expanded_rules.append(rule)
    return expanded_rules


def _generate_none_rule(rule: dict) -> dict:
    """Generate a new rule from a rule that contains 'none' directives

    :param rule: Rule
    :return: New rule
    """
    from copy import deepcopy

    out_rule = deepcopy(rule)
    for key in out_rule:
        if out_rule[key] == "none":
            out_rule[key] = None

    return out_rule


def _generate_random_rule(rule: dict, num_ir: int = 0) -> dict:
    """Generate a new rule from a rule that contains 'rand' directives

    :param rule: Rule
    :param num_ir: Number of impulse responses in config
    :return: Randomized rule
    """
    from copy import deepcopy
    from random import randint

    out_rule = deepcopy(rule)
    for key in out_rule:
        if key == "ir" and out_rule[key] == "rand":
            # IR is special case
            if num_ir == 0:
                out_rule[key] = None
            else:
                out_rule[key] = randint(0, num_ir - 1)  # noqa: S311
        else:
            out_rule[key] = evaluate_random_rule(str(out_rule[key]))

        # convert EQ values from strings to numbers
        if key in ["eq1", "eq2", "eq3"]:
            for n in range(3):
                if isinstance(out_rule[key][n], str):
                    out_rule[key][n] = eval(out_rule[key][n])  # noqa: S307

    return out_rule


def _rule_has_rand(rule: dict) -> bool:
    """Determine if any keys in the given rule contain 'rand'

    :param rule: Rule
    :return: True if rule contains 'rand'
    """
    return any("rand" in str(rule[key]) for key in rule)


def estimate_augmented_length_from_length(length: int, tempo: OptionalNumberStr = None, frame_length: int = 1) -> int:
    """Estimate the length of audio after augmentation

    :param length: Number of samples in audio
    :param tempo: Tempo rule
    :param frame_length: Pad resulting audio to be a multiple of this
    :return: Estimated length of augmented audio
    """
    import numpy as np

    if tempo is not None:
        length = int(np.round(length / float(tempo)))

    length = _get_padded_length(length, frame_length)

    return length


def get_mixups(augmentations: AugmentationRules) -> list[int]:
    """Get a list of mixup values used

    :param augmentations: List of augmentations
    :return: List of mixup values used
    """
    return sorted({augmentation.mixup for augmentation in augmentations})


def get_augmentation_indices_for_mixup(augmentations: AugmentationRules, mixup: int) -> list[int]:
    """Get a list of augmentation indices for a given mixup value

    :param augmentations: List of augmentations
    :param mixup: Mixup value of interest
    :return: List of augmentation indices
    """
    indices = []
    for idx, augmentation in enumerate(augmentations):
        if mixup == augmentation.mixup:
            indices.append(idx)

    return indices


def pad_audio_to_frame(audio: AudioT, frame_length: int = 1) -> AudioT:
    """Pad audio to be a multiple of frame length

    :param audio: Audio
    :param frame_length: Pad resulting audio to be a multiple of this
    :return: Padded audio
    """
    return pad_audio_to_length(audio, _get_padded_length(len(audio), frame_length))


def _get_padded_length(length: int, frame_length: int) -> int:
    """Get the number of pad samples needed

    :param length: Length of audio
    :param frame_length: Desired length will be a multiple of this
    :return: Padded length
    """
    mod = int(length % frame_length)
    pad_length = frame_length - mod if mod else 0
    return length + pad_length


def pad_audio_to_length(audio: AudioT, length: int) -> AudioT:
    """Pad audio to given length

    :param audio: Audio
    :param length: Length of output
    :return: Padded audio
    """
    import numpy as np

    return np.pad(array=audio, pad_width=(0, length - len(audio)))


def apply_gain(audio: AudioT, gain: float) -> AudioT:
    """Apply gain to audio

    :param audio: Audio
    :param gain: Amount of gain
    :return: Adjusted audio
    """
    return audio * gain


def evaluate_random_rule(rule: str) -> str | float:
    """Evaluate 'rand' directive

    :param rule: Rule
    :return: Resolved value
    """
    import re
    from random import uniform

    from .constants import RAND_PATTERN

    def rand_repl(m):
        return f"{uniform(float(m.group(1)), float(m.group(4))):.2f}"  # noqa: S311

    return eval(re.sub(RAND_PATTERN, rand_repl, rule))  # noqa: S307


def _parse_ir(rule: dict, num_ir: int) -> dict:
    from .helpers import generic_ids_to_list

    def _resolve_str(rule_in: str) -> str | list[int]:
        if rule_in in ["rand", "none"]:
            return rule_in

        rule_out = generic_ids_to_list(num_ir, rule_in)
        if not all(ro in range(num_ir) for ro in rule_out):
            raise ValueError(f"Invalid ir entry of {rule_in}")
        return rule_out

    if "ir" not in rule:
        return rule

    ir = rule["ir"]

    if ir is None:
        return rule

    if isinstance(ir, str):
        rule["ir"] = _resolve_str(ir)
        return rule

    if isinstance(ir, list):
        rule["ir"] = []
        for item in ir:
            result = _resolve_str(item)
            if isinstance(result, str):
                rule["ir"].append(_resolve_str(item))
            else:
                rule["ir"] += _resolve_str(item)

        return rule

    if isinstance(ir, int):
        if ir not in range(num_ir):
            raise ValueError(f"Invalid ir of {ir}")
        return rule

    raise ValueError(f"Invalid ir of {ir}")


def apply_augmentation(audio: AudioT, augmentation: Augmentation, frame_length: int = 1) -> AudioT:
    """Apply augmentations to audio data

    :param audio: Audio
    :param augmentation: Augmentation
    :param frame_length: Pad resulting audio to be a multiple of this
    :return: Augmented audio
    """
    from .torchaudio_augmentation import apply_augmentation

    return apply_augmentation(audio, augmentation, frame_length)


def apply_impulse_response(audio: AudioT, ir: ImpulseResponseData) -> AudioT:
    """Apply impulse response to audio data

    :param audio: Audio
    :param ir: Impulse response data
    :return: Augmented audio
    """
    from .torchaudio_augmentation import apply_impulse_response

    return apply_impulse_response(audio, ir)


def augmentation_from_rule(rule: AugmentationRule, num_ir: int) -> Augmentation:
    from sonusai.utils import dataclass_from_dict

    from .datatypes import Augmentation

    processed_rule = rule.to_dict()
    del processed_rule["mixup"]
    processed_rule = _generate_none_rule(processed_rule)
    if _rule_has_rand(processed_rule):
        processed_rule = _generate_random_rule(processed_rule, num_ir)

    return dataclass_from_dict(Augmentation, processed_rule)
