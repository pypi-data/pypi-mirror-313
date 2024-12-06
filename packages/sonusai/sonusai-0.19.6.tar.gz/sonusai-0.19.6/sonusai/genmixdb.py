"""sonusai genmixdb

usage: genmixdb [-hvmfsdj] LOC

options:
   -h, --help
   -v, --verbose    Be verbose.
   -m, --mix        Save mixture data. [default: False].
   -f, --ft         Save feature/truth_f data. [default: False].
   -s, --segsnr     Save segsnr data. [default: False].
   -d, --dryrun     Perform a dry run showing the processed config. [default: False].
   -j, --json       Save JSON version of database. [default: False].

Create mixture database data for training and evaluation. Optionally, also create mixture audio and feature/truth data.

genmixdb creates a database of training and evaluation feature and truth data generation information. It allows the
choice of audio neural-network feature types that are supported by the Aaware real-time front-end and truth data that is
synchronized frame-by-frame with the feature data.

Here are some examples:

#### Adding target data
Suppose you have an audio file which is an example, or target, of what you want to recognize or detect. Of course, for
training a NN you also need truth data for that file (also called parameters/labels/classes). If you don't already have
it, genmixdb can create truth using a variety of generation functions on each frame of the feature data. You can also
select different feature types. Here's an example:

genmixdb target_gfr32ts2

where target_gfr32ts2 contains config.yml with the following inside:
---
feature: gfr32ts2

targets:
  - name: data/target.wav

target_augmentations:
  - normalize: -3.5
...

The mixture database is written to a SQLite file (mixdb.db) in the same directory that contains the config.yml file.

#### Target data mix with noise and augmentation

genmixdb mix_gfr32ts2.yml

where mix_gfr32ts2.yml contains:
---
feature: gfr32ts2

targets:
  - name: data/target.wav

target_augmentations:
  - normalize: -3.5
    pitch: [-3, 0, 3]
    tempo: [0.8, 1, 1.2]

noises:
  - name: data/noise.wav

noise_augmentations:
  - normalize: -3.5

snrs:
  - 20
...

In this example a time-domain mixture is created and feature data is calculated as specified by 'feature: gfr32ts2'.
Various feature types are available which vary in spectral and temporal resolution (4 ms or higher), and other feature
algorithm parameters. The total feature size, dimension, and #frames for mixture is reported in the log file (the log
file name is genmixdb.log).

Truth (parameters/labels/classes) can be automatically created per feature output frame based on a variety of truth
generation functions. By default, these are included with the feature data in a single HDF5 output file. By default,
truth generation is turned on with default settings (see truth section) and a single class, i.e., detecting a single
type of sound. The truth format is a single float per class representing the probability of activity/presence, and
multi-class truth is possible by specifying the number of classes and either a scalar index or a vector of indices in
which to put the truth result. For example, 'num_class: 3' and 'class_indices: [ 2 ]' adds a 1x3 vector to the feature
data with truth put in index 2 (others would be 0) for data/target.wav being an audio clip from sound type of class 2.

The mixture is created with potential data augmentation functions in the following way:
1. apply noise augmentation rule
2. apply target augmentation rule to each target in the mixture (multiple targets may be used in mixup)
3. adjust noise and target gains for specified SNR
4. add augmented noise to augmented target(s)

Note: If an impulse response is part of the target augmentation, truth generation is performed on the targets before
applying the IRs. In this way, the truth is not impacted by the IR.

The mixture length is the length of the longest target in the mixture, and the noise signal is repeated if it is
shorter, or trimmed if longer.

#### Target and noise using path lists

Target and noise audio is specified as a list containing text files, audio files, and file globs. Text files are
processed with items on each line where each item can be a text file, an audio file, or a file glob. Each item will be
searched for audio files which can be WAV, MP3, FLAC, AIFF, or OGG format with any sample rate, bit depth, or channel
count. All audio files will be converted to 16 kHz, float32, single channel (only the first channel is used) format
before processing.

For example,

genmixdb dog-bark.yml

where dog-bark.yml contains:
---
targets:
  - name: slib/dog-outside/*.wav
  - name: slib/dog-inside/*.wav

will find all .wav files in the specified directories and process them as targets.

"""

import signal

from sonusai.mixture import Mixture


def signal_handler(_sig, _frame):
    import sys

    from sonusai import logger

    logger.info("Canceled due to keyboard interrupt")
    sys.exit(1)


signal.signal(signal.SIGINT, signal_handler)


def genmixdb(
    location: str,
    save_mix: bool = False,
    save_ft: bool = False,
    save_segsnr: bool = False,
    logging: bool = True,
    show_progress: bool = False,
    test: bool = False,
    save_json: bool = False,
) -> None:
    from functools import partial
    from random import seed

    import yaml

    from sonusai import logger
    from sonusai.mixture import SAMPLE_BYTES
    from sonusai.mixture import SAMPLE_RATE
    from sonusai.mixture import AugmentationRule
    from sonusai.mixture import MixtureDatabase
    from sonusai.mixture import balance_targets
    from sonusai.mixture import generate_mixtures
    from sonusai.mixture import get_all_snrs_from_config
    from sonusai.mixture import get_augmentation_rules
    from sonusai.mixture import get_augmented_targets
    from sonusai.mixture import get_impulse_response_files
    from sonusai.mixture import get_mixups
    from sonusai.mixture import get_noise_files
    from sonusai.mixture import get_target_augmentations_for_mixup
    from sonusai.mixture import get_target_files
    from sonusai.mixture import initialize_db
    from sonusai.mixture import load_config
    from sonusai.mixture import log_duration_and_sizes
    from sonusai.mixture import populate_class_label_table
    from sonusai.mixture import populate_class_weights_threshold_table
    from sonusai.mixture import populate_impulse_response_file_table
    from sonusai.mixture import populate_mixture_table
    from sonusai.mixture import populate_noise_file_table
    from sonusai.mixture import populate_spectral_mask_table
    from sonusai.mixture import populate_target_file_table
    from sonusai.mixture import populate_top_table
    from sonusai.mixture import populate_truth_parameters_table
    from sonusai.mixture import update_mixid_width
    from sonusai.utils import dataclass_from_dict
    from sonusai.utils import human_readable_size
    from sonusai.utils import par_track
    from sonusai.utils import seconds_to_hms
    from sonusai.utils import track

    config = load_config(location)
    initialize_db(location=location, test=test)

    mixdb = MixtureDatabase(location=location, test=test)

    populate_top_table(location, config, test)
    populate_class_label_table(location, config, test)
    populate_class_weights_threshold_table(location, config, test)
    populate_spectral_mask_table(location, config, test)
    populate_truth_parameters_table(location, config, test)

    seed(config["seed"])

    if logging:
        logger.debug(f"Seed: {config['seed']}")
        logger.debug("Configuration:")
        logger.debug(yaml.dump(config))

    if logging:
        logger.info("Collecting targets")

    target_files = get_target_files(config, show_progress=show_progress)

    if len(target_files) == 0:
        raise RuntimeError("Canceled due to no targets")

    populate_target_file_table(location, target_files, test)

    if logging:
        logger.debug("List of targets:")
        logger.debug(yaml.dump([target.name for target in mixdb.target_files], default_flow_style=False))
        logger.debug("")

    if logging:
        logger.info("Collecting noises")

    noise_files = get_noise_files(config, show_progress=show_progress)

    populate_noise_file_table(location, noise_files, test)

    if logging:
        logger.debug("List of noises:")
        logger.debug(yaml.dump([noise.name for noise in mixdb.noise_files], default_flow_style=False))
        logger.debug("")

    if logging:
        logger.info("Collecting impulse responses")

    impulse_response_files = get_impulse_response_files(config)

    populate_impulse_response_file_table(location, impulse_response_files, test)

    if logging:
        logger.debug("List of impulse responses:")
        logger.debug(
            yaml.dump(
                [entry.file for entry in mixdb.impulse_response_files],
                default_flow_style=False,
            )
        )
        logger.debug("")

    if logging:
        logger.info("Collecting target augmentations")

    target_augmentations = get_augmentation_rules(
        rules=config["target_augmentations"], num_ir=mixdb.num_impulse_response_files
    )
    mixups = get_mixups(target_augmentations)

    if logging:
        for mixup in mixups:
            logger.debug(f"Expanded list of target augmentation rules for mixup of {mixup}:")
            for target_augmentation in get_target_augmentations_for_mixup(target_augmentations, mixup):
                ta_dict = target_augmentation.to_dict()
                del ta_dict["mixup"]
                logger.debug(f"- {ta_dict}")
            logger.debug("")

    if logging:
        logger.info("Collecting noise augmentations")

    noise_augmentations = get_augmentation_rules(
        rules=config["noise_augmentations"], num_ir=mixdb.num_impulse_response_files
    )

    if logging:
        logger.debug("Expanded list of noise augmentations:")
        for noise_augmentation in noise_augmentations:
            na_dict = noise_augmentation.to_dict()
            del na_dict["mixup"]
            logger.debug(f"- {na_dict}")
        logger.debug("")

    if logging:
        logger.debug(f"SNRs: {config['snrs']}\n")
        logger.debug(f"Random SNRs: {config['random_snrs']}\n")
        logger.debug(f"Noise mix mode: {mixdb.noise_mix_mode}\n")
        logger.debug("Spectral masks:")
        for spectral_mask in mixdb.spectral_masks:
            logger.debug(f"- {spectral_mask}")
        logger.debug("")

    if logging:
        logger.info("Collecting augmented targets")

    augmented_targets = get_augmented_targets(target_files, target_augmentations, mixups)

    if config["class_balancing"]:
        class_balancing_augmentation = dataclass_from_dict(AugmentationRule, config["class_balancing_augmentation"])
        augmented_targets, target_augmentations = balance_targets(
            augmented_targets=augmented_targets,
            targets=target_files,
            target_augmentations=target_augmentations,
            class_balancing_augmentation=class_balancing_augmentation,
            num_classes=mixdb.num_classes,
            num_ir=mixdb.num_impulse_response_files,
            mixups=mixups,
        )

    target_audio_samples = sum([targets.samples for targets in mixdb.target_files])
    target_audio_duration = target_audio_samples / SAMPLE_RATE
    noise_audio_duration = sum([noises.duration for noises in mixdb.noise_files])
    noise_audio_samples = noise_audio_duration * SAMPLE_RATE

    if logging:
        logger.info("")
        logger.info(
            f"Target audio: {mixdb.num_target_files} files, "
            f"{human_readable_size(target_audio_samples * SAMPLE_BYTES, 1)}, "
            f"{seconds_to_hms(seconds=target_audio_duration)}"
        )
        logger.info(
            f"Noise audio: {mixdb.num_noise_files} files, "
            f"{human_readable_size(noise_audio_samples * SAMPLE_BYTES, 1)}, "
            f"{seconds_to_hms(seconds=noise_audio_duration)}"
        )

    used_noise_files, used_noise_samples, mixtures = generate_mixtures(
        noise_mix_mode=mixdb.noise_mix_mode,
        augmented_targets=augmented_targets,
        target_files=target_files,
        target_augmentations=target_augmentations,
        noise_files=noise_files,
        noise_augmentations=noise_augmentations,
        spectral_masks=mixdb.spectral_masks,
        all_snrs=get_all_snrs_from_config(config),
        mixups=mixups,
        num_classes=mixdb.num_classes,
        feature_step_samples=mixdb.feature_step_samples,
        num_ir=mixdb.num_impulse_response_files,
    )

    num_mixtures = len(mixtures)
    update_mixid_width(location, num_mixtures, test)

    if logging:
        logger.info("")
        logger.info(f"Found {num_mixtures:,} mixtures to process")

    total_duration = float(sum([mixture.samples for mixture in mixtures])) / SAMPLE_RATE

    if logging:
        log_duration_and_sizes(
            total_duration=total_duration,
            num_classes=mixdb.num_classes,
            feature_step_samples=mixdb.feature_step_samples,
            feature_parameters=mixdb.feature_parameters,
            stride=mixdb.fg_stride,
            desc="Estimated",
        )
        logger.info(
            f"Feature shape:        "
            f"{mixdb.fg_stride} x {mixdb.feature_parameters} "
            f"({mixdb.fg_stride * mixdb.feature_parameters} total params)"
        )
        logger.info(f"Feature samples:      {mixdb.feature_samples} samples ({mixdb.feature_ms} ms)")
        logger.info(f"Feature step samples: {mixdb.feature_step_samples} samples ({mixdb.feature_step_ms} ms)")
        logger.info("")

    # Fill in the details
    if logging:
        logger.info("Generating mixtures")
    progress = track(total=num_mixtures, disable=not show_progress)
    mixtures = par_track(
        partial(
            _process_mixture,
            location=location,
            save_mix=save_mix,
            save_ft=save_ft,
            save_segsnr=save_segsnr,
            test=test,
        ),
        mixtures,
        progress=progress,
    )
    progress.close()

    populate_mixture_table(location, mixtures, test)

    total_noise_files = len(noise_files)

    total_samples = mixdb.total_samples()
    total_duration = float(total_samples / SAMPLE_RATE)

    noise_files_percent = (float(used_noise_files) / float(total_noise_files)) * 100
    noise_samples_percent = (float(used_noise_samples) / float(noise_audio_samples)) * 100

    if logging:
        log_duration_and_sizes(
            total_duration=total_duration,
            num_classes=mixdb.num_classes,
            feature_step_samples=mixdb.feature_step_samples,
            feature_parameters=mixdb.feature_parameters,
            stride=mixdb.fg_stride,
            desc="Actual",
        )
        logger.info("")
        logger.info(f"Used {noise_files_percent:,.0f}% of noise files")
        logger.info(f"Used {noise_samples_percent:,.0f}% of noise audio")
        logger.info("")

    if not test and save_json:
        if logging:
            logger.info(f"Writing JSON version of database to {location}")
        mixdb = MixtureDatabase(location)
        mixdb.save()


def _process_mixture(
    mixture: Mixture,
    location: str,
    save_mix: bool,
    save_ft: bool,
    save_segsnr: bool,
    test: bool,
) -> Mixture:
    from typing import Any

    from sonusai.mixture import MixtureDatabase
    from sonusai.mixture import get_ft
    from sonusai.mixture import get_segsnr
    from sonusai.mixture import get_truth
    from sonusai.mixture import update_mixture
    from sonusai.mixture import write_cached_data
    from sonusai.mixture import write_mixture_metadata

    with_data = save_mix or save_ft
    mixdb = MixtureDatabase(location, test)

    mixture, genmix_data = update_mixture(mixdb, mixture, with_data)

    if with_data:
        write_data: list[tuple[str, Any]] = []

        if save_mix:
            write_data.append(("targets", genmix_data.targets))
            write_data.append(("noise", genmix_data.noise))
            write_data.append(("mixture", genmix_data.mixture))

        if save_ft:
            if genmix_data.targets is None or genmix_data.noise is None or genmix_data.mixture is None:
                raise RuntimeError("Mixture data was not generated properly")
            truth_t = get_truth(
                mixdb=mixdb,
                mixture=mixture,
                targets_audio=genmix_data.targets,
                noise_audio=genmix_data.noise,
                mixture_audio=genmix_data.mixture,
            )
            feature, truth_f = get_ft(
                mixdb=mixdb,
                mixture=mixture,
                mixture_audio=genmix_data.mixture,
                truth_t=truth_t,
            )
            write_data.append(("feature", feature))
            write_data.append(("truth_f", truth_f))

            if save_segsnr:
                if genmix_data.target is None:
                    raise RuntimeError("Target data was not generated properly")
                segsnr = get_segsnr(
                    mixdb=mixdb,
                    mixture=mixture,
                    target_audio=genmix_data.target,
                    noise=genmix_data.noise,
                )
                write_data.append(("segsnr", segsnr))

        write_cached_data(mixdb.location, "mixture", mixture.name, write_data)
        write_mixture_metadata(mixdb, mixture)

    return mixture


def main() -> None:
    from docopt import docopt

    import sonusai
    from sonusai.utils import trim_docstring

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    import time
    from os import makedirs
    from os import remove
    from os.path import exists
    from os.path import isdir
    from os.path import join

    import yaml

    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import logger
    from sonusai import update_console_handler
    from sonusai.mixture import load_config
    from sonusai.utils import seconds_to_hms

    verbose = args["--verbose"]
    save_mix = args["--mix"]
    save_ft = args["--ft"]
    save_segsnr = args["--segsnr"]
    dryrun = args["--dryrun"]
    save_json = args["--json"]
    location = args["LOC"]

    start_time = time.monotonic()

    if exists(location) and not isdir(location):
        remove(location)

    makedirs(location, exist_ok=True)

    create_file_handler(join(location, "genmixdb.log"))
    update_console_handler(verbose)
    initial_log_messages("genmixdb")

    if dryrun:
        config = load_config(location)
        logger.info("Dryrun configuration:")
        logger.info(yaml.dump(config))
        return

    logger.info(f"Creating mixture database for {location}")
    logger.info("")

    try:
        genmixdb(
            location=location,
            save_mix=save_mix,
            save_ft=save_ft,
            save_segsnr=save_segsnr,
            show_progress=True,
            save_json=save_json,
        )
    except Exception as e:
        logger.debug(e)
        raise

    end_time = time.monotonic()
    logger.info(f"Completed in {seconds_to_hms(seconds=end_time - start_time)}")
    logger.info("")


if __name__ == "__main__":
    main()
