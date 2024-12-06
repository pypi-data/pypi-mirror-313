"""sonusai genft

usage: genft [-hvs] [-i MIXID] LOC

options:
    -h, --help
    -v, --verbose                   Be verbose.
    -i MIXID, --mixid MIXID         Mixture ID(s) to generate. [default: *].
    -s, --segsnr                    Save segsnr. [default: False].

Generate SonusAI feature/truth data from a SonusAI mixture database.

Inputs:
    LOC         A SonusAI mixture database directory.
    MIXID       A glob of mixture ID(s) to generate.

Outputs the following to the mixture database directory:
    <id>
        feature.pkl
        truth_f.pkl
        segsnr.pkl (optional)
        metadata.txt
    genft.log

"""

import signal

from sonusai.mixture import GeneralizedIDs
from sonusai.mixture import GenFTData


def signal_handler(_sig, _frame):
    import sys

    from sonusai import logger

    logger.info("Canceled due to keyboard interrupt")
    sys.exit(1)


signal.signal(signal.SIGINT, signal_handler)


def genft(
    location: str,
    mixids: GeneralizedIDs = "*",
    compute_truth: bool = True,
    compute_segsnr: bool = False,
    write: bool = False,
    show_progress: bool = False,
    force: bool = True,
) -> list[GenFTData]:
    from functools import partial

    from sonusai.mixture import MixtureDatabase
    from sonusai.utils import par_track
    from sonusai.utils import track

    mixdb = MixtureDatabase(location)
    mixids = mixdb.mixids_to_list(mixids)

    progress = track(total=len(mixids), disable=not show_progress)
    results = par_track(
        partial(_genft_kernel, location=location, compute_truth=compute_truth, compute_segsnr=compute_segsnr, force=force, write=write),
        mixids,
        progress=progress,
    )
    progress.close()

    return results


def _genft_kernel(m_id: int, location: str, compute_truth: bool, compute_segsnr: bool, force: bool, write: bool) -> GenFTData:
    from typing import Any

    from sonusai.mixture import MixtureDatabase
    from sonusai.mixture import write_cached_data
    from sonusai.mixture import write_mixture_metadata

    mixdb = MixtureDatabase(location)

    result = GenFTData()

    feature, truth_f = mixdb.mixture_ft(m_id=m_id, force=force)
    write_data: list[tuple[str, Any]] = [("feature", feature)]
    result.feature = feature

    if compute_truth:
        write_data.append(("truth_f", truth_f))
        result.truth_f = truth_f

    if compute_segsnr:
        segsnr = mixdb.mixture_segsnr(m_id=m_id, force=force)
        write_data.append(("segsnr", segsnr))
        result.segsnr = segsnr

    if write:
        write_cached_data(mixdb.location, "mixture", mixdb.mixture(m_id).name, write_data)
        write_mixture_metadata(mixdb, mixdb.mixture(m_id))

    return result


def main() -> None:
    from docopt import docopt

    import sonusai
    from sonusai.utils import trim_docstring

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    import time
    from os.path import join

    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import logger
    from sonusai import update_console_handler
    from sonusai.mixture import MixtureDatabase
    from sonusai.mixture import check_audio_files_exist
    from sonusai.utils import human_readable_size
    from sonusai.utils import seconds_to_hms

    verbose = args["--verbose"]
    mixids = args["--mixid"]
    compute_segsnr = args["--segsnr"]
    location = args["LOC"]

    start_time = time.monotonic()

    create_file_handler(join(location, "genft.log"))
    update_console_handler(verbose)
    initial_log_messages("genft")

    logger.info(f"Load mixture database from {location}")
    mixdb = MixtureDatabase(location)
    mixids = mixdb.mixids_to_list(mixids)

    total_samples = mixdb.total_samples(mixids)
    duration = total_samples / sonusai.mixture.SAMPLE_RATE
    total_transform_frames = total_samples // mixdb.ft_config.overlap
    total_feature_frames = total_samples // mixdb.feature_step_samples

    logger.info("")
    logger.info(f"Found {len(mixids):,} mixtures to process")
    logger.info(
        f"{total_samples:,} samples, "
        f"{total_transform_frames:,} transform frames, "
        f"{total_feature_frames:,} feature frames"
    )

    check_audio_files_exist(mixdb)

    try:
        genft(
            location=location,
            mixids=mixids,
            compute_segsnr=compute_segsnr,
            write=True,
            show_progress=True,
        )
    except Exception as e:
        logger.debug(e)
        raise

    logger.info(f"Wrote {len(mixids)} mixtures to {location}")
    logger.info("")
    logger.info(f"Duration: {seconds_to_hms(seconds=duration)}")
    logger.info(
        f"feature:  {human_readable_size(total_feature_frames * mixdb.fg_stride * mixdb.feature_parameters * 4, 1)}"
    )
    logger.info(f"truth_f:  {human_readable_size(total_feature_frames * mixdb.num_classes * 4, 1)}")
    if compute_segsnr:
        logger.info(f"segsnr:   {human_readable_size(total_transform_frames * 4, 1)}")

    end_time = time.monotonic()
    logger.info(f"Completed in {seconds_to_hms(seconds=end_time - start_time)}")
    logger.info("")


if __name__ == "__main__":
    main()
