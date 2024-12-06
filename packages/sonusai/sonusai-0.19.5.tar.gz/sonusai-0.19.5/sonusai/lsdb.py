"""sonusai lsdb

usage: lsdb [-hta] [-i MIXID] [-c CID] LOC

Options:
    -h, --help
    -i MIXID, --mixid MIXID         Mixture ID(s) to analyze. [default: *].
    -c CID, --class_index CID       Analyze mixtures that contain this class index.
    -t, --targets                   List all target files.
    -a, --all_class_counts          List all class counts.

List mixture data information from a SonusAI mixture database.

Inputs:
    LOC     A SonusAI mixture database directory.

"""

import signal

from sonusai import logger
from sonusai.mixture import GeneralizedIDs
from sonusai.mixture import MixtureDatabase


def signal_handler(_sig, _frame):
    import sys

    from sonusai import logger

    logger.info("Canceled due to keyboard interrupt")
    sys.exit(1)


signal.signal(signal.SIGINT, signal_handler)


def lsdb(
    mixdb: MixtureDatabase,
    mixids: GeneralizedIDs = "*",
    class_index: int | None = None,
    list_targets: bool = False,
    all_class_counts: bool = False,
) -> None:
    from sonusai.mixture import SAMPLE_RATE
    from sonusai.queries import get_mixids_from_class_indices
    from sonusai.utils import consolidate_range
    from sonusai.utils import max_text_width
    from sonusai.utils import print_mixture_details
    from sonusai.utils import seconds_to_hms

    desc_len = 24

    total_samples = mixdb.total_samples()
    total_duration = total_samples / SAMPLE_RATE

    logger.info(f'{"Mixtures":{desc_len}} {mixdb.num_mixtures}')
    logger.info(f'{"Duration":{desc_len}} {seconds_to_hms(seconds=total_duration)}')
    logger.info(f'{"Targets":{desc_len}} {mixdb.num_target_files}')
    logger.info(f'{"Noises":{desc_len}} {mixdb.num_noise_files}')
    logger.info(f'{"Feature":{desc_len}} {mixdb.feature}')
    logger.info(
        f'{"Feature shape":{desc_len}} {mixdb.fg_stride} x {mixdb.feature_parameters} '
        f'({mixdb.fg_stride * mixdb.feature_parameters} total params)'
    )
    logger.info(f'{"Feature samples":{desc_len}} {mixdb.feature_samples} samples ({mixdb.feature_ms} ms)')
    logger.info(
        f'{"Feature step samples":{desc_len}} {mixdb.feature_step_samples} samples ' f'({mixdb.feature_step_ms} ms)'
    )
    logger.info(f'{"Feature overlap":{desc_len}} {mixdb.fg_step / mixdb.fg_stride} ({mixdb.feature_step_ms} ms)')
    logger.info(f'{"SNRs":{desc_len}} {mixdb.snrs}')
    logger.info(f'{"Random SNRs":{desc_len}} {mixdb.random_snrs}')
    logger.info(f'{"Classes":{desc_len}} {mixdb.num_classes}')
    # TODO: fix class count
    logger.info(f'{"Class count":{desc_len}} not supported')
    # print_class_count(class_count=class_count, length=desc_len, print_fn=logger.info)
    # TODO: add class weight calculations here
    logger.info("")

    if list_targets:
        logger.info("Target details:")
        idx_len = max_text_width(mixdb.num_target_files)
        for idx, target in enumerate(mixdb.target_files):
            desc = f"  {idx:{idx_len}} Name"
            logger.info(f"{desc:{desc_len}} {target.name}")
            desc = f"  {idx:{idx_len}} Truth index"
            logger.info(f"{desc:{desc_len}} {target.class_indices}")
        logger.info("")

    if class_index is not None:
        if 0 <= class_index > mixdb.num_classes:
            raise ValueError(f"Given class_index is outside valid range of 1-{mixdb.num_classes}")
        ids = get_mixids_from_class_indices(mixdb=mixdb, predicate=lambda x: x in [class_index])[class_index]
        logger.info(f"Mixtures with class index {class_index}: {ids}")
        logger.info("")

    mixids = mixdb.mixids_to_list(mixids)

    if len(mixids) == 1:
        print_mixture_details(mixdb=mixdb, mixid=mixids[0], desc_len=desc_len, print_fn=logger.info)
        if all_class_counts:
            # TODO: fix class count
            logger.info("All class count not supported")
            # print_class_count(class_count=class_count, length=desc_len, print_fn=logger.info, all_class_counts=True)
    else:
        logger.info(
            f"Calculating statistics from truth_f files for {len(mixids):,} mixtures" f" ({consolidate_range(mixids)})"
        )
        logger.info("Not supported")


def main() -> None:
    from docopt import docopt

    import sonusai
    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import update_console_handler
    from sonusai.utils import trim_docstring

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    mixid = args["--mixid"]
    class_index = args["--class_index"]
    list_targets = args["--targets"]
    all_class_counts = args["--all_class_counts"]
    location = args["LOC"]

    if class_index is not None:
        class_index = int(class_index)

    create_file_handler("lsdb.log")
    update_console_handler(False)
    initial_log_messages("lsdb")

    logger.info(f"Analyzing {location}")

    mixdb = MixtureDatabase(location)
    lsdb(
        mixdb=mixdb,
        mixids=mixid,
        class_index=class_index,
        list_targets=list_targets,
        all_class_counts=all_class_counts,
    )


if __name__ == "__main__":
    main()
