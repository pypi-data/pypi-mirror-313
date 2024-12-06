from sonusai.mixture.datatypes import ImpulseResponseFile
from sonusai.mixture.datatypes import ImpulseResponseFiles
from sonusai.mixture.datatypes import NoiseFiles
from sonusai.mixture.datatypes import SpectralMasks
from sonusai.mixture.datatypes import TargetFiles
from sonusai.mixture.datatypes import TruthParameters


def raw_load_config(name: str) -> dict:
    """Load YAML config file

    :param name: File name
    :return: Dictionary of config data
    """
    import yaml

    with open(file=name) as f:
        config = yaml.safe_load(f)

    return config


def get_default_config() -> dict:
    """Load default SonusAI config

    :return: Dictionary of default config data
    """
    from .constants import DEFAULT_CONFIG

    try:
        return raw_load_config(DEFAULT_CONFIG)
    except Exception as e:
        raise OSError(f"Error loading default config: {e}") from e


def load_config(name: str) -> dict:
    """Load SonusAI default config and update with given location (performing SonusAI variable substitution)

    :param name: Directory containing mixture database
    :return: Dictionary of config data
    """
    from os.path import join

    return update_config_from_file(filename=join(name, "config.yml"), given_config=get_default_config())


def update_config_from_file(filename: str, given_config: dict) -> dict:
    """Update the given config with the config in the specified YAML file

    :param filename: File name
    :param given_config: Config dictionary to update
    :return: Updated config dictionary
    """
    from copy import deepcopy

    from .constants import REQUIRED_CONFIGS
    from .constants import VALID_CONFIGS
    from .constants import VALID_NOISE_MIX_MODES

    updated_config = deepcopy(given_config)

    try:
        file_config = raw_load_config(filename)
    except Exception as e:
        raise OSError(f"Error loading config from {filename}: {e}") from e

    # Check for unrecognized keys
    for key in file_config:
        if key not in VALID_CONFIGS:
            nice_list = "\n".join([f"  {item}" for item in VALID_CONFIGS])
            raise AttributeError(
                f"Invalid config parameter in {filename}: {key}.\nValid config parameters are:\n{nice_list}"
            )

    # Use default config as base and overwrite with given config keys as found
    for key in updated_config:
        if key in file_config:
            updated_config[key] = file_config[key]

    # Check for required keys
    for key in REQUIRED_CONFIGS:
        if key not in updated_config:
            raise AttributeError(f"{filename} is missing required '{key}'")

    # Validate special cases
    validate_truth_configs(updated_config)
    validate_asr_configs(updated_config)

    # Check for non-empty spectral masks
    if len(updated_config["spectral_masks"]) == 0:
        updated_config["spectral_masks"] = given_config["spectral_masks"]

    # Check for valid noise_mix_mode
    if updated_config["noise_mix_mode"] not in VALID_NOISE_MIX_MODES:
        nice_list = "\n".join([f"  {item}" for item in VALID_NOISE_MIX_MODES])
        raise ValueError(f"{filename} contains invalid noise_mix_mode.\nValid noise mix modes are:\n{nice_list}")

    return updated_config


def validate_truth_configs(given: dict) -> None:
    """Validate fields in given 'truth_configs'

    :param given: The dictionary of given config
    """
    from copy import deepcopy

    from sonusai.mixture import truth_functions

    from .constants import REQUIRED_TRUTH_CONFIGS

    if "truth_configs" not in given:
        raise AttributeError("config is missing required 'truth_configs'")

    truth_configs = given["truth_configs"]
    if len(truth_configs) == 0:
        raise ValueError("'truth_configs' in config is empty")

    for name, truth_config in truth_configs.items():
        for key in REQUIRED_TRUTH_CONFIGS:
            if key not in truth_config:
                raise AttributeError(f"'{name}' in truth_configs is missing required '{key}'")

        optional_config = deepcopy(truth_config)
        for key in REQUIRED_TRUTH_CONFIGS:
            del optional_config[key]

        getattr(truth_functions, truth_config["function"] + "_validate")(optional_config)


def validate_asr_configs(given: dict) -> None:
    """Validate fields in given 'asr_config'

    :param given: The dictionary of given config
    """
    from sonusai.utils import validate_asr

    from .constants import REQUIRED_ASR_CONFIGS

    if "asr_configs" not in given:
        raise AttributeError("config is missing required 'asr_configs'")

    asr_configs = given["asr_configs"]

    for name, asr_config in asr_configs.items():
        for key in REQUIRED_ASR_CONFIGS:
            if key not in asr_config:
                raise AttributeError(f"'{name}' in asr_configs is missing required '{key}'")

        engine = asr_config["engine"]
        config = {x: asr_config[x] for x in asr_config if x != "engine"}
        validate_asr(engine, **config)


def get_hierarchical_config_files(root: str, leaf: str) -> list[str]:
    """Get a hierarchical list of config files in the given leaf of the given root

    :param root: Root of the hierarchy
    :param leaf: Leaf under the root
    :return: List of config files found in the hierarchy
    """
    import os
    from pathlib import Path

    config_file = "config.yml"

    root_path = Path(os.path.abspath(root))
    if not root_path.is_dir():
        raise OSError(f"Given root, {root_path}, is not a directory.")

    leaf_path = Path(os.path.abspath(leaf))
    if not leaf_path.is_dir():
        raise OSError(f"Given leaf, {leaf_path}, is not a directory.")

    common = os.path.commonpath((root_path, leaf_path))
    if os.path.normpath(common) != os.path.normpath(root_path):
        raise OSError(f"Given leaf, {leaf_path}, is not in the hierarchy of the given root, {root_path}")

    top_config_file = os.path.join(root_path, config_file)
    if not Path(top_config_file).is_file():
        raise OSError(f"Could not find {top_config_file}")

    current = leaf_path
    config_files = []
    while current != root_path:
        local_config_file = Path(os.path.join(current, config_file))
        if local_config_file.is_file():
            config_files.append(str(local_config_file))
        current = current.parent

    config_files.append(top_config_file)
    return list(reversed(config_files))


def update_config_from_hierarchy(root: str, leaf: str, config: dict) -> dict:
    """Update the given config using the hierarchical config files in the given leaf of the given root

    :param root: Root of the hierarchy
    :param leaf: Leaf under the root
    :param config: Config to update
    :return: Updated config
    """
    from copy import deepcopy

    new_config = deepcopy(config)
    config_files = get_hierarchical_config_files(root=root, leaf=leaf)
    for config_file in config_files:
        new_config = update_config_from_file(filename=config_file, given_config=new_config)

    return new_config


def get_target_files(config: dict, show_progress: bool = False) -> TargetFiles:
    """Get the list of target files from a config

    :param config: Config dictionary
    :param show_progress: Show progress bar
    :return: List of target files
    """
    from itertools import chain

    from sonusai.utils import dataclass_from_dict
    from sonusai.utils import par_track
    from sonusai.utils import track

    from .datatypes import TargetFiles

    class_indices = config["class_indices"]
    if not isinstance(class_indices, list):
        class_indices = [class_indices]

    target_files = list(
        chain.from_iterable(
            [
                append_target_files(
                    entry=entry,
                    class_indices=class_indices,
                    truth_configs=config["truth_configs"],
                    level_type=config["target_level_type"],
                )
                for entry in config["targets"]
            ]
        )
    )

    progress = track(total=len(target_files), disable=not show_progress)
    target_files = par_track(_get_num_samples, target_files, progress=progress)
    progress.close()

    num_classes = config["num_classes"]
    for target_file in target_files:
        if any(class_index < 0 for class_index in target_file["class_indices"]):
            raise ValueError("class indices must contain only positive elements")

        if any(class_index > num_classes for class_index in target_file["class_indices"]):
            raise ValueError(f"class index elements must not be greater than {num_classes}")

    return dataclass_from_dict(TargetFiles, target_files)


def append_target_files(
    entry: dict | str,
    class_indices: list[int],
    truth_configs: dict,
    level_type: str,
    tokens: dict | None = None,
) -> list[dict]:
    """Process target files list and append as needed

    :param entry: Target file entry to append to the list
    :param class_indices: Class indices
    :param truth_configs: Truth configs
    :param level_type: Target level type
    :param tokens: Tokens used for variable expansion
    :return: List of target files
    """
    from copy import deepcopy
    from glob import glob
    from os import listdir
    from os.path import dirname
    from os.path import isabs
    from os.path import isdir
    from os.path import join
    from os.path import splitext

    from sonusai.utils import dataclass_from_dict

    from .audio import validate_input_file
    from .constants import REQUIRED_TRUTH_CONFIGS
    from .datatypes import TruthConfig
    from .tokenized_shell_vars import tokenized_expand
    from .tokenized_shell_vars import tokenized_replace

    if tokens is None:
        tokens = {}

    if isinstance(entry, dict):
        if "name" in entry:
            in_name = entry["name"]
        else:
            raise AttributeError("Target list contained record without name")

        if "class_indices" in entry:
            if isinstance(entry["class_indices"], list):
                class_indices = entry["class_indices"]
            else:
                class_indices = [entry["class_indices"]]

        truth_configs_override = entry.get("truth_configs", {})
        for key in truth_configs_override:
            if key not in truth_configs:
                raise AttributeError(
                    f"Truth config '{key}' override specified for {entry['name']} is not defined at top level"
                )
        truth_configs_merged = {}
        for key in truth_configs_override:
            truth_configs_merged[key] = deepcopy(truth_configs[key])
            if truth_configs_override[key] is not None:
                truth_configs_merged[key] |= truth_configs_override[key]
        level_type = entry.get("level_type", level_type)
    else:
        in_name = entry
        truth_configs_merged = deepcopy(truth_configs)

    in_name, new_tokens = tokenized_expand(in_name)
    tokens.update(new_tokens)
    names = sorted(glob(in_name))
    if not names:
        raise OSError(f"Could not find {in_name}. Make sure path exists")

    target_files: list[dict] = []
    for name in names:
        ext = splitext(name)[1].lower()
        dir_name = dirname(name)
        if isdir(name):
            for file in listdir(name):
                child = file
                if not isabs(child):
                    child = join(dir_name, child)
                target_files.extend(
                    append_target_files(
                        entry=child,
                        class_indices=class_indices,
                        truth_configs=truth_configs_merged,
                        level_type=level_type,
                        tokens=tokens,
                    )
                )
        else:
            try:
                if ext == ".txt":
                    with open(file=name) as txt_file:
                        for line in txt_file:
                            # strip comments
                            child = line.partition("#")[0]
                            child = child.rstrip()
                            if child:
                                child, new_tokens = tokenized_expand(child)
                                tokens.update(new_tokens)
                                if not isabs(child):
                                    child = join(dir_name, child)
                                target_files.extend(
                                    append_target_files(
                                        entry=child,
                                        class_indices=class_indices,
                                        truth_configs=truth_configs_merged,
                                        level_type=level_type,
                                        tokens=tokens,
                                    )
                                )
                elif ext == ".yml":
                    try:
                        yml_config = raw_load_config(name)

                        if "targets" in yml_config:
                            for record in yml_config["targets"]:
                                target_files.extend(
                                    append_target_files(
                                        entry=record,
                                        class_indices=class_indices,
                                        truth_configs=truth_configs_merged,
                                        level_type=level_type,
                                        tokens=tokens,
                                    )
                                )
                    except Exception as e:
                        raise OSError(f"Error processing {name}: {e}") from e
                else:
                    validate_input_file(name)
                    target_file: dict = {
                        "expanded_name": name,
                        "name": tokenized_replace(name, tokens),
                        "class_indices": class_indices,
                        "level_type": level_type,
                        "truth_configs": {},
                    }
                    if len(truth_configs_merged) > 0:
                        for tc_key, tc_value in truth_configs_merged.items():
                            config = deepcopy(tc_value)
                            truth_config: dict = {}
                            for key in REQUIRED_TRUTH_CONFIGS:
                                truth_config[key] = config[key]
                                del config[key]
                            truth_config["config"] = config
                            target_file["truth_configs"][tc_key] = dataclass_from_dict(TruthConfig, truth_config)
                        for tc_key in target_file["truth_configs"]:
                            if (
                                "function" in truth_configs_merged[tc_key]
                                and truth_configs_merged[tc_key]["function"] == "file"
                            ):
                                truth_configs_merged[tc_key]["file"] = splitext(target_file["name"])[0] + ".h5"
                    target_files.append(target_file)
            except Exception as e:
                raise OSError(f"Error processing {name}: {e}") from e

    return target_files


def get_noise_files(config: dict, show_progress: bool = False) -> NoiseFiles:
    """Get the list of noise files from a config

    :param config: Config dictionary
    :param show_progress: Show progress bar
    :return: List of noise file
    """
    from itertools import chain

    from sonusai.utils import dataclass_from_dict
    from sonusai.utils import par_track
    from sonusai.utils import track

    from .datatypes import NoiseFiles

    noise_files = list(chain.from_iterable([append_noise_files(entry=entry) for entry in config["noises"]]))

    progress = track(total=len(noise_files), disable=not show_progress)
    noise_files = par_track(_get_num_samples, noise_files, progress=progress)
    progress.close()

    return dataclass_from_dict(NoiseFiles, noise_files)


def append_noise_files(entry: dict | str, tokens: dict | None = None) -> list[dict]:
    """Process noise files list and append as needed

    :param entry: Noise file entry to append to the list
    :param tokens: Tokens used for variable expansion
    :return: List of noise files
    """
    from glob import glob
    from os import listdir
    from os.path import dirname
    from os.path import isabs
    from os.path import isdir
    from os.path import join
    from os.path import splitext

    from .audio import validate_input_file
    from .tokenized_shell_vars import tokenized_expand
    from .tokenized_shell_vars import tokenized_replace

    if tokens is None:
        tokens = {}

    if isinstance(entry, dict):
        if "name" in entry:
            in_name = entry["name"]
        else:
            raise AttributeError("Noise list contained record without name")
    else:
        in_name = entry

    in_name, new_tokens = tokenized_expand(in_name)
    tokens.update(new_tokens)
    names = sorted(glob(in_name))
    if not names:
        raise OSError(f"Could not find {in_name}. Make sure path exists")

    noise_files: list[dict] = []
    for name in names:
        ext = splitext(name)[1].lower()
        dir_name = dirname(name)
        if isdir(name):
            for file in listdir(name):
                child = file
                if not isabs(child):
                    child = join(dir_name, child)
                noise_files.extend(append_noise_files(entry=child, tokens=tokens))
        else:
            try:
                if ext == ".txt":
                    with open(file=name) as txt_file:
                        for line in txt_file:
                            # strip comments
                            child = line.partition("#")[0]
                            child = child.rstrip()
                            if child:
                                child, new_tokens = tokenized_expand(child)
                                tokens.update(new_tokens)
                                if not isabs(child):
                                    child = join(dir_name, child)
                                noise_files.extend(append_noise_files(entry=child, tokens=tokens))
                elif ext == ".yml":
                    try:
                        yml_config = raw_load_config(name)

                        if "noises" in yml_config:
                            for record in yml_config["noises"]:
                                noise_files.extend(append_noise_files(entry=record, tokens=tokens))
                    except Exception as e:
                        raise OSError(f"Error processing {name}: {e}") from e
                else:
                    validate_input_file(name)
                    noise_file: dict = {
                        "expanded_name": name,
                        "name": tokenized_replace(name, tokens),
                    }
                    noise_files.append(noise_file)
            except Exception as e:
                raise OSError(f"Error processing {name}: {e}") from e

    return noise_files


def get_impulse_response_files(config: dict) -> ImpulseResponseFiles:
    """Get the list of impulse response files from a config

    :param config: Config dictionary
    :return: List of impulse response files
    """
    return [ImpulseResponseFile(entry["name"], entry["tags"]) for entry in config["impulse_responses"]]
    # from itertools import chain
    #
    # return list(
    #     chain.from_iterable(
    #         [
    #             append_impulse_response_files(entry=ImpulseResponseFile(entry["name"], entry["tags"]))
    #             for entry in config["impulse_responses"]
    #         ]
    #     )
    # )


def append_impulse_response_files(entry: ImpulseResponseFile, tokens: dict | None = None) -> list[str]:
    """Process impulse response files list and append as needed

    :param entry: Impulse response file entry to append to the list
    :param tokens: Tokens used for variable expansion
    :return: List of impulse response files
    """
    from glob import glob
    from os import listdir
    from os.path import dirname
    from os.path import isabs
    from os.path import isdir
    from os.path import join
    from os.path import splitext

    from .audio import validate_input_file
    from .tokenized_shell_vars import tokenized_expand
    from .tokenized_shell_vars import tokenized_replace

    if tokens is None:
        tokens = {}

    in_name, new_tokens = tokenized_expand(entry.file)
    tokens.update(new_tokens)
    names = sorted(glob(in_name))
    if not names:
        raise OSError(f"Could not find {in_name}. Make sure path exists")

    impulse_response_files: list[str] = []
    for name in names:
        ext = splitext(name)[1].lower()
        dir_name = dirname(name)
        if isdir(name):
            for file in listdir(name):
                if not isabs(file):
                    file = join(dir_name, file)
                child = ImpulseResponseFile(file, entry.tags)
                impulse_response_files.extend(append_impulse_response_files(entry=child, tokens=tokens))
        else:
            try:
                if ext == ".txt":
                    with open(file=name) as txt_file:
                        for line in txt_file:
                            # strip comments
                            file = line.partition("#")[0]
                            file = file.rstrip()
                            if file:
                                file, new_tokens = tokenized_expand(file)
                                tokens.update(new_tokens)
                                if not isabs(file):
                                    file = join(dir_name, file)
                                child = ImpulseResponseFile(file, entry.tags)
                                impulse_response_files.extend(append_impulse_response_files(entry=child, tokens=tokens))
                elif ext == ".yml":
                    try:
                        yml_config = raw_load_config(name)

                        if "impulse_responses" in yml_config:
                            for record in yml_config["impulse_responses"]:
                                impulse_response_files.extend(
                                    append_impulse_response_files(entry=record, tokens=tokens)
                                )
                    except Exception as e:
                        raise OSError(f"Error processing {name}: {e}") from e
                else:
                    validate_input_file(name)
                    impulse_response_files.append(tokenized_replace(name, tokens))
            except Exception as e:
                raise OSError(f"Error processing {name}: {e}") from e

    return impulse_response_files


def get_spectral_masks(config: dict) -> SpectralMasks:
    """Get the list of spectral masks from a config

    :param config: Config dictionary
    :return: List of spectral masks
    """
    from sonusai.utils import dataclass_from_dict

    try:
        return dataclass_from_dict(SpectralMasks, config["spectral_masks"])
    except Exception as e:
        raise ValueError(f"Error in spectral_masks: {e}") from e


def get_truth_parameters(config: dict) -> TruthParameters:
    """Get the list of truth parameters from a config

    :param config: Config dictionary
    :return: List of truth parameters
    """
    from copy import deepcopy

    from sonusai.mixture import truth_functions
    from sonusai.mixture.truth_functions.datatypes import TruthFunctionConfig

    from .constants import REQUIRED_TRUTH_CONFIGS
    from .datatypes import TruthParameter

    truth_parameters: TruthParameters = []
    for name, truth_config in config["truth_configs"].items():
        optional_config = deepcopy(truth_config)
        for key in REQUIRED_TRUTH_CONFIGS:
            del optional_config[key]

        t_config = TruthFunctionConfig(
            feature=config["feature"],
            num_classes=config["num_classes"],
            class_indices=[1],
            target_gain=1,
            config=optional_config,
        )

        parameters = getattr(truth_functions, truth_config["function"] + "_parameters")(t_config)
        truth_parameters.append(TruthParameter(name, parameters))

    return truth_parameters


def _get_num_samples(entry: dict) -> dict:
    from .audio import get_num_samples

    entry["samples"] = get_num_samples(entry["expanded_name"])
    del entry["expanded_name"]
    return entry
