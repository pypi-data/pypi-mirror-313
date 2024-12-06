"""sonusai mkwav

usage: mkwav [-hvtn] [-i MIXID] LOC

options:
    -h, --help
    -v, --verbose                   Be verbose.
    -i MIXID, --mixid MIXID         Mixture ID(s) to generate. [default: *].
    -t, --target                    Write target file.
    -n, --noise                     Write noise file.

The mkwav command creates WAV files from a SonusAI database.

Inputs:
    LOC         A SonusAI mixture database directory.
    MIXID       A glob of mixture ID(s) to generate.

Outputs the following to the mixture database directory:
    <id>
        mixture.wav:   mixture
        target.wav:    target (optional)
        noise.wav:     noise (optional)
        metadata.txt
    mkwav.log

"""

import signal


def signal_handler(_sig, _frame):
    import sys

    from sonusai import logger

    logger.info("Canceled due to keyboard interrupt")
    sys.exit(1)


signal.signal(signal.SIGINT, signal_handler)


def _process_mixture(m_id: int, location: str, write_target: bool, write_noise: bool) -> None:
    from os.path import join

    from sonusai.mixture import MixtureDatabase
    from sonusai.mixture import write_mixture_metadata
    from sonusai.utils import float_to_int16
    from sonusai.utils import write_audio

    mixdb = MixtureDatabase(location)

    mixture = mixdb.mixture(m_id)
    location = join(mixdb.location, mixture.name)

    write_audio(name=join(location, "mixture.wav"), audio=float_to_int16(mixdb.mixture_mixture(m_id)))
    if write_target:
        write_audio(name=join(location, "target.wav"), audio=float_to_int16(mixdb.mixture_target(m_id)))
    if write_noise:
        write_audio(name=join(location, "noise.wav"), audio=float_to_int16(mixdb.mixture_noise(m_id)))

    write_mixture_metadata(mixdb, mixture)


def main() -> None:
    from docopt import docopt

    import sonusai
    from sonusai.utils import trim_docstring

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    verbose = args["--verbose"]
    mixid = args["--mixid"]
    write_target = args["--target"]
    write_noise = args["--noise"]
    location = args["LOC"]

    import time
    from functools import partial
    from os.path import join

    import sonusai
    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import logger
    from sonusai import update_console_handler
    from sonusai.mixture import MixtureDatabase
    from sonusai.mixture import check_audio_files_exist
    from sonusai.utils import human_readable_size
    from sonusai.utils import par_track
    from sonusai.utils import seconds_to_hms
    from sonusai.utils import track

    start_time = time.monotonic()

    create_file_handler(join(location, "mkwav.log"))
    update_console_handler(verbose)
    initial_log_messages("mkwav")

    logger.info(f"Load mixture database from {location}")
    mixdb = MixtureDatabase(location)
    mixid = mixdb.mixids_to_list(mixid)

    total_samples = mixdb.total_samples(mixid)
    duration = total_samples / sonusai.mixture.SAMPLE_RATE

    logger.info("")
    logger.info(f"Found {len(mixid):,} mixtures to process")
    logger.info(f"{total_samples:,} samples")

    check_audio_files_exist(mixdb)

    progress = track(total=len(mixid))
    par_track(
        partial(_process_mixture, location=location, write_target=write_target, write_noise=write_noise),
        mixid,
        progress=progress,
    )
    progress.close()

    logger.info(f"Wrote {len(mixid)} mixtures to {location}")
    logger.info("")
    logger.info(f"Duration: {seconds_to_hms(seconds=duration)}")
    logger.info(f"mixture:  {human_readable_size(total_samples * 2, 1)}")
    if write_target:
        logger.info(f"target:   {human_readable_size(total_samples * 2, 1)}")
    if write_noise:
        logger.info(f"noise:    {human_readable_size(total_samples * 2, 1)}")

    end_time = time.monotonic()
    logger.info(f"Completed in {seconds_to_hms(seconds=end_time - start_time)}")
    logger.info("")


if __name__ == "__main__":
    main()
