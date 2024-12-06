"""sonusai gentcst

usage: gentcst [-hvru] [-o OUTPUT] [-f FOLD] [-y ONTOLOGY]

options:
    -h, --help
    -v, --verbose                       Be verbose.
    -o OUTPUT, --output OUTPUT          Output file name.
    -f FOLD, --fold FOLD                Fold(s) to include. [default: *].
    -y ONTOLOGY, --ontology ONTOLOGY    Reference ontology JSON file for cross-check and adding metadata.
                                        [default: ontology.json].
    -r, --hierarchical                  Generate hierarchical multiclass truth for non-leaf nodes.
    -u, --update                        Write JSON metadata into the tree.

Generate a target SonusAI configuration file from a hierarchical subdirectory tree
under the local directory. Leaves in the subdirectory tree define classes by providing SonusAI list
.txt files for class data and additional truth config definitions. This offers a way to simplify and
more clearly manage hierarchical class structure similar to the Audioset ontology.

Features:
    - automatically compiles the target configuration with the number of classes and each truth
      index and the associated files (note: files should use absolute path with env variable)
    - supports hierarchical multilabel class truth generation, where higher nodes in the tree
      are included with leaf truth index, and different leaves with the same name will have the
      same index (i.e. door/squeak, chair/squeak, and brief-tone/squeak)
    - support config overrides for class config.yml or filename.yml for specific file config
    - manages folds via file prefix naming convention, i.e. 1-*.txt, 2-*.txt, etc.
      specifies data for fold 1, 2, etc.
    - cross-check node definitions with the reference ontology and auto copy class metadata into
      the tree to help define/collect data
    - class label is also generated (in the .yml or referencing a .csv)

Inputs:
    The local subdirectory tree with expected top-level configuration file config.yml. This
    file must at least define the feature and can have additional parameters treated as default
    (for truth, augmentation, etc.) which will be included in the generated output yaml file.
    An entire class dataset config parameter can be overridden by including it in a config.yml
    file in the class subdirectory. Individual file config parameters can be further overridden
    or specified in a file of the same name but with .yml (i.e. 1-data.yml with the 1-data.txt)

Outputs:
    output.yml
    output.csv
    gentcst.log

"""

import signal
from dataclasses import dataclass


def signal_handler(_sig, _frame):
    import sys

    from sonusai import logger

    logger.info("Canceled due to keyboard interrupt")
    sys.exit(1)


signal.signal(signal.SIGINT, signal_handler)

CONFIG_FILE = "config.yml"


@dataclass
class FileInfo:
    file: str
    classes: list[str]
    leaf: str
    labels: list[str]
    fold: int
    truth_index: list[int] | None = None


@dataclass(frozen=True)
class DirInfo:
    file: str
    classes: list[str]


@dataclass(frozen=True)
class LabelInfo:
    index: int
    display_name: str


@dataclass(frozen=True)
class OntologyInfo:
    id: str
    name: list[str]
    description: str
    citation_uri: str
    positive_examples: list[str]
    child_ids: list[str]
    restrictions: list[str]


def gentcst(
    fold: str = "*",
    ontology: str = "ontology.json",
    hierarchical: bool = False,
    update: bool = False,
    verbose: bool = False,
) -> tuple[dict, list[LabelInfo]]:
    from copy import deepcopy
    from os import getcwd
    from os.path import dirname
    from os.path import exists
    from os.path import splitext

    from sonusai import SonusAIError
    from sonusai import initial_log_messages
    from sonusai import logger
    from sonusai import update_console_handler
    from sonusai.mixture import get_default_config
    from sonusai.mixture import raw_load_config
    from sonusai.mixture import update_config_from_hierarchy
    from sonusai.mixture import validate_truth_configs

    update_console_handler(verbose)
    initial_log_messages("gentcst")

    if update:
        logger.info("Updating tree with JSON metadata")
        logger.info("")

    logger.debug(f"fold:         {fold}")
    logger.debug(f"ontology:     {ontology}")
    logger.debug(f"hierarchical: {hierarchical}")
    logger.debug(f"update:       {update}")
    logger.debug("")

    config = get_config()

    if config["truth_mode"] == "mutex" and hierarchical:
        raise SonusAIError("Multi-class truth is incompatible with truth_mode mutex")

    all_files = get_all_files(hierarchical)
    all_folds = get_folds_from_files(all_files)
    use_folds = get_use_folds(all_folds, fold)
    use_files = get_files_from_folds(all_files, use_folds)
    report_leaf_fold_data_usage(all_files, use_files)

    ontology_data = validate_ontology(ontology, use_files)

    labels = get_labels_from_files(all_files)
    logger.debug("Truth indices:")
    for item in labels:
        logger.debug(f" {item.index:3} {item.display_name}")
    logger.debug("")

    gen_truth_indices(use_files, labels)

    config["num_classes"] = len(labels)
    if config["truth_mode"] == "mutex":
        config["num_classes"] = config["num_classes"] + 1

    config["targets"] = []

    logger.info(f"gentcst {len(use_files)} entries in tree")
    root = getcwd()
    for file in use_files:
        leaf = dirname(file.file)
        local_config = get_default_config()
        local_config = update_config_from_hierarchy(root=root, leaf=leaf, config=local_config)
        if not isinstance(local_config["truth_settings"], list):
            local_config["truth_settings"] = [local_config["truth_settings"]]

        specific_name = splitext(file.file)[0] + ".yml"
        if exists(specific_name):
            specific_config = raw_load_config(specific_name)

            for key in specific_config:
                if key != "truth_settings":
                    local_config[key] = specific_config[key]
                else:
                    local_config["truth_settings"] = validate_truth_configs(
                        given=specific_config["truth_settings"],
                        default=local_config["truth_settings"],
                    )

        truth_settings = deepcopy(local_config["truth_settings"])
        for idx, val in enumerate(truth_settings):
            val["index"] = file.truth_index
            for key in ["function", "config"]:
                if key in val and val[key] == config["truth_settings"][idx][key]:
                    del val[key]

        target = {"name": file.file, "truth_settings": truth_settings}

        config["targets"].append(target)

        if update:
            write_metadata_to_tree(ontology_data, file)

    return config, labels


def get_ontology(ontology: str) -> list[OntologyInfo]:
    import json
    from os.path import exists

    raw_ontology_data = []
    if exists(ontology):
        with open(file=ontology, encoding="utf-8") as f:
            raw_ontology_data = json.load(f)

    return [
        OntologyInfo(
            id=item["id"],
            name=convert_ontology_name(item["name"]),
            description=item["description"],
            citation_uri=item["citation_uri"],
            positive_examples=item["positive_examples"],
            child_ids=item["child_ids"],
            restrictions=item["restrictions"],
        )
        for item in raw_ontology_data
    ]


def convert_ontology_name(name: str) -> list[str]:
    """Convert names to lowercase, convert spaces to '-', split into lists on ','."""
    text = name.lower()
    # Need to find ', ' before converting spaces so that we don't convert ', ' to ',-'
    text = text.replace(", ", ",")
    text = text.replace(" ", "-")
    return text.split(",")


def get_dirs() -> list[DirInfo]:
    from os import getcwd
    from os import walk
    from os.path import join

    match: list[str] = []
    cwd = getcwd()
    for root, ds, _ in walk(cwd):
        for d in ds:
            match.append(join(root, d).replace(cwd, "."))
    match = sorted(match)

    dirs: list[DirInfo] = []
    for m in match:
        if not m.startswith("./gentcst") and m != ".":
            classes = m.split("/")
            # Remove first element because it is '.'
            classes.pop(0)
            dirs.append(DirInfo(file=m, classes=classes))

    return dirs


def get_leaf_from_classes(classes: list[str]) -> str:
    return "/".join(classes)


def get_all_files(hierarchical: bool) -> list[FileInfo]:
    import re
    from os import getcwd
    from os import walk
    from os.path import join

    file_list: list[str] = []
    cwd = getcwd()
    regex = re.compile(r"^\d+-.*\.txt$")
    for root, _, fs in walk(cwd):
        for f in fs:
            if regex.match(f):
                file_list.append(join(root, f).replace(cwd, "."))

    files: list[FileInfo] = []
    fold_pattern = re.compile(r".*/(\d+)-.*\.txt")
    for file in file_list:
        fold_match = fold_pattern.match(file)
        if fold_match:
            fold = int(fold_match.group(1))

            classes = file.split("/")
            # Remove first element because it is '.'
            classes.pop(0)
            # Remove last element because it is the file name
            classes.pop()

            leaf = get_leaf_from_classes(classes)

            if hierarchical:
                labels = classes
            else:
                labels = [leaf]

            files.append(FileInfo(file=file, classes=classes, leaf=leaf, labels=labels, fold=fold))

    return files


def get_use_folds(all_folds: list[int], fold: str) -> list[int]:
    import numpy as np

    from sonusai import logger

    req_folds: list[int] = get_req_folds(all_folds, fold)
    use_folds: list[int] = list(set(req_folds).intersection(all_folds))

    logger.debug("Fold information")
    logger.debug(f" Available: {all_folds}")
    logger.debug(f" Requested: {req_folds}")
    logger.debug(f" Used:      {use_folds}")
    logger.debug(f" Unused:    {list(set(use_folds).symmetric_difference(all_folds))}")
    logger.debug(f" Missing:   {list(np.setdiff1d(req_folds, all_folds))}")
    logger.debug("")

    return use_folds


def get_files_from_folds(files: list[FileInfo], folds: list[int]) -> list[FileInfo]:
    return [file for file in files if file.fold in folds]


def get_item_from_name(ontology_data: list[OntologyInfo], name: str) -> OntologyInfo | None:
    return next((item for item in ontology_data if name in item.name), None)


def get_item_from_id(ontology_data: list[OntologyInfo], identity: str) -> OntologyInfo | None:
    return next((item for item in ontology_data if item.id == identity), None)


def get_name_from_id(ontology_data: list[OntologyInfo], identity: str) -> list[str] | None:
    from sonusai import SonusAIError

    name = None
    found = False

    for item in ontology_data:
        if item.id == identity:
            if found:
                raise SonusAIError(f"id {identity} appears multiple times in ontology")

            name = item.name
            found = True

    return name


def get_id_from_name(ontology_data: list[OntologyInfo], name: str) -> str | None:
    from sonusai import SonusAIError

    identity = None
    found = False

    for item in ontology_data:
        if name in item.name:
            if found:
                raise SonusAIError(f"name {name} appears multiple times in ontology")

            identity = item.id
            found = True

    return identity


def is_valid_name(ontology_data: list[OntologyInfo], name: str) -> bool:
    return any(name in item.name for item in ontology_data)


def is_valid_child(ontology_data: list[OntologyInfo], parent: str, child: str) -> bool:
    valid = False
    parent_item = get_item_from_name(ontology_data, parent)
    child_id = get_id_from_name(ontology_data, child)

    if child_id is not None and parent_item is not None and child_id in parent_item.child_ids:
        valid = True

    return valid


def is_valid_hierarchy(ontology_data: list[OntologyInfo], classes: list[str]) -> bool:
    from itertools import pairwise
    valid = True

    for parent, child in pairwise(classes):
        if not is_valid_child(ontology_data, parent, child):
            valid = False

    return valid


def validate_class(ontology_data: list[OntologyInfo], item: FileInfo | DirInfo) -> bool:
    from sonusai import logger

    valid = True

    for c in item.classes:
        if not is_valid_name(ontology_data, c):
            logger.warning(f" Could not find {c} in ontology for {item.file}")
            valid = False

    if valid and not is_valid_hierarchy(ontology_data, item.classes):
        logger.warning(f" Invalid parent/child relationship for {item.file}")
        valid = False

    return valid


def get_req_folds(folds: list[int], fold: str) -> list[int]:
    from sonusai.utils import expand_range

    if fold == "*":
        return folds

    return expand_range(fold)


def get_folds_from_files(files: list[FileInfo]) -> list[int]:
    result: list[int] = [file.fold for file in files]
    # Converting to set and back to list ensures uniqueness
    return sorted(set(result))


def get_leaves_from_files(files: list[FileInfo]) -> list[str]:
    result: list[str] = [file.leaf for file in files]
    # Converting to set and back to list ensures uniqueness
    return sorted(set(result))


def get_labels_from_files(files: list[FileInfo]) -> list[LabelInfo]:
    all_labels = [file.labels for file in files]

    # Get labels by depth
    labels_by_depth: list[list[str]] = [[] for _ in range(max([len(label) for label in all_labels]))]
    for label in all_labels:
        for index, name in enumerate(label):
            labels_by_depth[index].append(name)

    for n in range(len(labels_by_depth)):
        # Converting to set and back to list ensures uniqueness
        labels_by_depth[n] = sorted(set(labels_by_depth[n]))

    # We want the deepest leaves first
    labels_by_depth.reverse()

    # Now flatten the list
    flattened_labels_by_depth = [item for sublist in labels_by_depth for item in sublist]

    # Generate index, name pairs
    # labels = []
    # for index, file in enumerate(flattened_labels_by_depth):
    #     labels.append({'index': index + 1, 'display_name': file})
    return [LabelInfo(index=index + 1, display_name=file) for index, file in enumerate(flattened_labels_by_depth)]


def gen_truth_indices(files: list[FileInfo], labels: list[LabelInfo]):
    for file in files:
        file.truth_index = sorted([get_index_from_label(labels, label) for label in file.labels])


def get_index_from_label(labels: list[LabelInfo], label: str) -> int:
    return next((item for item in labels if item.display_name == label), None).index


def get_config() -> dict:
    from os.path import exists

    from sonusai import SonusAIError
    from sonusai.mixture import raw_load_config

    if not exists(CONFIG_FILE):
        raise SonusAIError(f"No {CONFIG_FILE} at top level")

    config = raw_load_config(CONFIG_FILE)

    if "feature" not in config:
        raise SonusAIError("feature not in top level config")

    if "truth_mode" not in config:
        raise SonusAIError("truth_mode not in top level config")

    if config["truth_mode"] not in ["normal", "mutex"]:
        raise SonusAIError("Invalid truth_mode in top level config")

    if "truth_settings" in config and not isinstance(config["truth_settings"], list):
        config["truth_settings"] = [config["truth_settings"]]

    return config


def validate_ontology(ontology: str, items: list[FileInfo] | list[DirInfo]) -> list[OntologyInfo]:
    from os.path import exists

    from sonusai import logger

    if exists(ontology):
        ontology_data = get_ontology(ontology)
        logger.debug(f"Reference ontology in {ontology} has {len(ontology_data)} classes")
        logger.debug("")

        logger.info("Checking tree against reference ontology")
        all_dirs = get_dirs()
        valid = True
        for file in all_dirs:
            if not validate_class(ontology_data, file):
                valid = False
        if valid:
            logger.info("PASS")
        logger.info("")

        logger.info("Checking files against reference ontology")
        valid = True
        for item in items:
            if not validate_class(ontology_data, item):
                valid = False
        if valid:
            logger.info("PASS")
        logger.info("")

        return ontology_data

    return []


def get_node_from_name(ontology_data: list[OntologyInfo], name: str) -> OntologyInfo | None:
    from sonusai import logger

    nodes = [item for item in ontology_data if name in item.name]
    if len(nodes) == 1:
        return nodes[0]

    if nodes:
        logger.warning(f"Found multiple entries in reference ontology that match {name}")
    else:
        logger.warning(f"Could not find entry for {name} in reference ontology")

    return None


def write_metadata_to_tree(ontology_data: list[OntologyInfo], file: FileInfo):
    import json
    from dataclasses import asdict
    from os.path import basename
    from os.path import dirname

    if ontology_data:
        node = get_node_from_name(ontology_data, file.classes[-1])
        if node is not None:
            dir_name = dirname(file.file)
            json_name = dir_name + "/" + basename(dir_name) + ".json"
            with open(file=json_name, mode="w") as f:
                json.dump(asdict(node), f)


def get_folds_from_leaf(all_files: list[FileInfo], leaf: str) -> list[int]:
    files = [item for item in all_files if item.leaf == leaf]
    return get_folds_from_files(files)


def report_leaf_fold_data_usage(all_files: list[FileInfo], use_files: list[FileInfo]):
    from sonusai import logger

    use_leaves = get_leaves_from_files(use_files)
    all_leaves = get_leaves_from_files(all_files)

    logger.debug("Data folds present in each leaf")
    leaf_len = len(max(all_leaves, key=len))
    for leaf in all_leaves:
        folds = get_folds_from_leaf(all_files, leaf)
        logger.debug(f" {leaf:{leaf_len}} {folds}")
    logger.debug("")

    dif_leaves = set(all_leaves).symmetric_difference(use_leaves)
    if dif_leaves:
        logger.warning("This fold selection is missing data from the following leaves")
        for c in dif_leaves:
            logger.warning(f" {c}")
        logger.warning("")


def main() -> None:
    from docopt import docopt

    import sonusai
    from sonusai.utils import trim_docstring

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    verbose = args["--verbose"]
    output_name = args["--output"]
    fold = args["--fold"]
    ontology = args["--ontology"]
    hierarchical = args["--hierarchical"]
    update = args["--update"]

    import csv
    from dataclasses import asdict
    from os import getcwd
    from os.path import basename
    from os.path import splitext

    import yaml

    from sonusai import create_file_handler
    from sonusai import logger

    if not output_name:
        output_name = basename(getcwd()) + ".yml"

    create_file_handler("gentcst.log")

    config, labels = gentcst(
        fold=fold,
        ontology=ontology,
        hierarchical=hierarchical,
        update=update,
        verbose=verbose,
    )

    with open(file=output_name, mode="w") as f:
        yaml.dump(config, f)
        logger.info(f"Wrote config to {output_name}")

    csv_fields = ["index", "display_name"]
    csv_name = splitext(output_name)[0] + ".csv"

    with open(file=csv_name, mode="w") as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields)
        writer.writeheader()
        writer.writerows([asdict(label) for label in labels])
        logger.info(f"Wrote labels to {csv_name}")


if __name__ == "__main__":
    main()
