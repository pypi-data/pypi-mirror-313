"""sonusai genmetrics

usage: genmetrics [-hvs] [-i MIXID] [-n INCLUDE] [-x EXCLUDE] LOC

options:
    -h, --help
    -v, --verbose                   Be verbose.
    -i MIXID, --mixid MIXID         Mixture ID(s) to generate. [default: *].
    -n INCLUDE, --include INCLUDE   Metrics to include. [default: all]
    -x EXCLUDE, --exclude EXCLUDE   Metrics to exclude. [default: none]
    -s, --supported                 Show list of supported metrics.

Calculate speech enhancement metrics of SonusAI mixture data in LOC.

Inputs:
    LOC         A SonusAI mixture database directory.
    MIXID       A glob of mixture ID(s) to generate.
    INCLUDE     Comma separated list of metrics to include. Can be 'all' or
                any of the supported metrics.
    EXCLUDE     Comma separated list of metrics to exclude. Can be 'none' or
                any of the supported metrics.

Examples:

Generate all available mxwer metrics (as determined by mixdb asr_configs parameter):
> sonusai genmetrics -n"mxwer" mixdb_loc

Generate only mxwer.faster metrics:
> sonusai genmetrics -n"mxwer.faster" mixdb_loc

Generate all available metrics except for mxwer.faster:
> sonusai genmetrics -x"mxwer.faster" mixdb_loc

"""

import signal


def signal_handler(_sig, _frame):
    import sys

    from sonusai import logger

    logger.info("Canceled due to keyboard interrupt")
    sys.exit(1)


signal.signal(signal.SIGINT, signal_handler)


def _process_mixture(mixid: int, location: str, metrics: list[str]) -> None:
    from sonusai.mixture import MixtureDatabase
    from sonusai.mixture import write_cached_data

    mixdb = MixtureDatabase(location)

    values = mixdb.mixture_metrics(m_id=mixid, metrics=metrics, force=True)
    write_data = list(zip(metrics, values, strict=False))

    write_cached_data(mixdb.location, "mixture", mixdb.mixture(mixid).name, write_data)


def main() -> None:
    from docopt import docopt

    import sonusai
    from sonusai.mixture import MixtureDatabase
    from sonusai.utils import trim_docstring

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    verbose = args["--verbose"]
    mixids = args["--mixid"]
    includes = [x.strip() for x in args["--include"].lower().split(",")]
    excludes = [x.strip() for x in args["--exclude"].lower().split(",")]
    show_supported = args["--supported"]
    location = args["LOC"]

    import sys
    import time
    from functools import partial
    from os.path import join

    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import logger
    from sonusai import update_console_handler
    from sonusai.utils import par_track
    from sonusai.utils import seconds_to_hms
    from sonusai.utils import track

    # TODO: Check config.yml for changes to asr_configs and update mixdb
    # TODO: Support globs for metrics (includes and excludes)

    start_time = time.monotonic()

    # Setup logging file
    create_file_handler(join(location, "genmetrics.log"))
    update_console_handler(verbose)
    initial_log_messages("genmetrics")

    logger.info(f"Load mixture database from {location}")

    mixdb = MixtureDatabase(location)
    supported = mixdb.supported_metrics
    if show_supported:
        logger.info(f"\nSupported metrics:\n\n{supported.pretty}")
        sys.exit(0)

    if includes is None or "all" in includes:
        metrics = supported.names
    else:
        metrics = set(includes)
        if "mxwer" in metrics:
            metrics.remove("mxwer")
            for name in mixdb.asr_configs:
                metrics.add(f"mxwer.{name}")

    diff = metrics.difference(supported.names)
    if diff:
        logger.error(f"Unrecognized metric: {', '.join(diff)}")
        sys.exit(1)

    if excludes is None or "none" in excludes:
        _excludes = set()
    else:
        _excludes = set(excludes)
        if "mxwer" in _excludes:
            _excludes.remove("mxwer")
            for name in mixdb.asr_configs:
                _excludes.add(f"mxwer.{name}")

    diff = _excludes.difference(supported.names)
    if diff:
        logger.error(f"Unrecognized metric: {', '.join(diff)}")
        sys.exit(1)

    for exclude in _excludes:
        metrics.discard(exclude)

    logger.info(f"Generating metrics: {', '.join(metrics)}")

    mixids = mixdb.mixids_to_list(mixids)
    logger.info("")
    logger.info(f"Found {len(mixids):,} mixtures to process")

    progress = track(total=len(mixids), desc="genmetrics")
    par_track(
        partial(_process_mixture, location=location, metrics=list(metrics)),
        mixids,
        progress=progress,
    )
    progress.close()

    logger.info(f"Wrote metrics for {len(mixids)} mixtures to {location}")
    logger.info("")

    end_time = time.monotonic()
    logger.info(f"Completed in {seconds_to_hms(seconds=end_time - start_time)}")
    logger.info("")


if __name__ == "__main__":
    main()
