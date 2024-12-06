# ruff: noqa: S608
from .datatypes import AudiosT
from .datatypes import AudioT
from .datatypes import Augmentation
from .datatypes import AugmentationRules
from .datatypes import AugmentedTargets
from .datatypes import GenMixData
from .datatypes import ImpulseResponseFiles
from .datatypes import Mixture
from .datatypes import Mixtures
from .datatypes import NoiseFiles
from .datatypes import SpectralMasks
from .datatypes import TargetFiles
from .datatypes import Targets
from .datatypes import UniversalSNRGenerator
from .mixdb import MixtureDatabase


def config_file(location: str) -> str:
    from os.path import join

    return join(location, "config.yml")


def initialize_db(location: str, test: bool = False) -> None:
    from .mixdb import db_connection

    con = db_connection(location=location, create=True, test=test)

    con.execute("""
    CREATE TABLE truth_config(
    id INTEGER PRIMARY KEY NOT NULL,
    config TEXT NOT NULL)
    """)

    con.execute("""
    CREATE TABLE truth_parameters(
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    parameters INTEGER NOT NULL)
    """)

    con.execute("""
    CREATE TABLE target_file (
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    samples INTEGER NOT NULL,
    class_indices TEXT NOT NULL,
    level_type TEXT NOT NULL,
    speaker_id INTEGER,
    FOREIGN KEY(speaker_id) REFERENCES speaker (id))
    """)

    con.execute("""
    CREATE TABLE speaker (
    id INTEGER PRIMARY KEY NOT NULL,
    parent TEXT NOT NULL)
    """)

    con.execute("""
    CREATE TABLE noise_file (
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    samples INTEGER NOT NULL)
    """)

    con.execute("""
    CREATE TABLE top (
    id INTEGER PRIMARY KEY NOT NULL,
    version INTEGER NOT NULL,
    asr_configs TEXT NOT NULL,
    class_balancing BOOLEAN NOT NULL,
    feature TEXT NOT NULL,
    noise_mix_mode TEXT NOT NULL,
    num_classes INTEGER NOT NULL,
    seed INTEGER NOT NULL,
    mixid_width INTEGER NOT NULL,
    speaker_metadata_tiers TEXT NOT NULL,
    textgrid_metadata_tiers TEXT NOT NULL)
    """)

    con.execute("""
    CREATE TABLE class_label (
    id INTEGER PRIMARY KEY NOT NULL,
    label TEXT NOT NULL)
    """)

    con.execute("""
    CREATE TABLE class_weights_threshold (
    id INTEGER PRIMARY KEY NOT NULL,
    threshold FLOAT NOT NULL)
    """)

    con.execute("""
    CREATE TABLE impulse_response_file (
    id INTEGER PRIMARY KEY NOT NULL,
    file TEXT NOT NULL,
    tags TEXT NOT NULL)
    """)

    con.execute("""
    CREATE TABLE spectral_mask (
    id INTEGER PRIMARY KEY NOT NULL,
    f_max_width INTEGER NOT NULL,
    f_num INTEGER NOT NULL,
    t_max_width INTEGER NOT NULL,
    t_num INTEGER NOT NULL,
    t_max_percent INTEGER NOT NULL)
    """)

    con.execute("""
    CREATE TABLE target_file_truth_config (
    target_file_id INTEGER,
    truth_config_id INTEGER,
    FOREIGN KEY(target_file_id) REFERENCES target_file (id),
    FOREIGN KEY(truth_config_id) REFERENCES truth_config (id))
    """)

    con.execute("""
    CREATE TABLE target (
    id INTEGER PRIMARY KEY NOT NULL,
    file_id INTEGER NOT NULL,
    augmentation TEXT NOT NULL,
    gain FLOAT,
    FOREIGN KEY(file_id) REFERENCES target_file (id))
    """)

    con.execute("""
    CREATE TABLE mixture (
    id INTEGER PRIMARY KEY NOT NULL,
    name VARCHAR NOT NULL,
    noise_file_id INTEGER NOT NULL,
    noise_augmentation TEXT NOT NULL,
    noise_offset INTEGER NOT NULL,
    noise_snr_gain FLOAT,
    random_snr BOOLEAN NOT NULL,
    snr FLOAT NOT NULL,
    samples INTEGER NOT NULL,
    spectral_mask_id INTEGER NOT NULL,
    spectral_mask_seed INTEGER NOT NULL,
    target_snr_gain FLOAT,
    FOREIGN KEY(noise_file_id) REFERENCES noise_file (id),
    FOREIGN KEY(spectral_mask_id) REFERENCES spectral_mask (id))
    """)

    con.execute("""
    CREATE TABLE mixture_target (
    mixture_id INTEGER,
    target_id INTEGER,
    FOREIGN KEY(mixture_id) REFERENCES mixture (id),
    FOREIGN KEY(target_id) REFERENCES target (id))
    """)

    con.commit()
    con.close()


def populate_top_table(location: str, config: dict, test: bool = False) -> None:
    """Populate top table"""
    import json

    from .constants import MIXDB_VERSION
    from .mixdb import db_connection

    con = db_connection(location=location, readonly=False, test=test)
    con.execute(
        """
    INSERT INTO top (version, asr_configs, class_balancing, feature, noise_mix_mode, num_classes,
    seed, mixid_width, speaker_metadata_tiers, textgrid_metadata_tiers)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            MIXDB_VERSION,
            json.dumps(config["asr_configs"]),
            config["class_balancing"],
            config["feature"],
            config["noise_mix_mode"],
            config["num_classes"],
            config["seed"],
            0,
            "",
            "",
        ),
    )
    con.commit()
    con.close()


def populate_class_label_table(location: str, config: dict, test: bool = False) -> None:
    """Populate class_label table"""
    from .mixdb import db_connection

    con = db_connection(location=location, readonly=False, test=test)
    con.executemany(
        "INSERT INTO class_label (label) VALUES (?)",
        [(item,) for item in config["class_labels"]],
    )
    con.commit()
    con.close()


def populate_class_weights_threshold_table(location: str, config: dict, test: bool = False) -> None:
    """Populate class_weights_threshold table"""
    from .mixdb import db_connection

    class_weights_threshold = config["class_weights_threshold"]
    num_classes = config["num_classes"]

    if not isinstance(class_weights_threshold, list):
        class_weights_threshold = [class_weights_threshold]

    if len(class_weights_threshold) == 1:
        class_weights_threshold = [class_weights_threshold[0]] * num_classes

    if len(class_weights_threshold) != num_classes:
        raise ValueError(f"invalid class_weights_threshold length: {len(class_weights_threshold)}")

    con = db_connection(location=location, readonly=False, test=test)
    con.executemany(
        "INSERT INTO class_weights_threshold (threshold) VALUES (?)",
        [(item,) for item in class_weights_threshold],
    )
    con.commit()
    con.close()


def populate_spectral_mask_table(location: str, config: dict, test: bool = False) -> None:
    """Populate spectral_mask table"""
    from .config import get_spectral_masks
    from .mixdb import db_connection

    con = db_connection(location=location, readonly=False, test=test)
    con.executemany(
        """
    INSERT INTO spectral_mask (f_max_width, f_num, t_max_width, t_num, t_max_percent) VALUES (?, ?, ?, ?, ?)
    """,
        [
            (
                item.f_max_width,
                item.f_num,
                item.t_max_width,
                item.t_num,
                item.t_max_percent,
            )
            for item in get_spectral_masks(config)
        ],
    )
    con.commit()
    con.close()


def populate_truth_parameters_table(location: str, config: dict, test: bool = False) -> None:
    """Populate truth_parameters table"""
    from .config import get_truth_parameters
    from .mixdb import db_connection

    con = db_connection(location=location, readonly=False, test=test)
    con.executemany(
        """
    INSERT INTO truth_parameters (name, parameters) VALUES (?, ?)
    """,
        [
            (
                item.name,
                item.parameters,
            )
            for item in get_truth_parameters(config)
        ],
    )
    con.commit()
    con.close()


def populate_target_file_table(location: str, target_files: TargetFiles, test: bool = False) -> None:
    """Populate target file table"""
    import json
    from pathlib import Path

    from .mixdb import db_connection

    _populate_truth_config_table(location, target_files, test)
    _populate_speaker_table(location, target_files, test)

    con = db_connection(location=location, readonly=False, test=test)

    cur = con.cursor()
    textgrid_metadata_tiers: set[str] = set()
    for target_file in target_files:
        # Get TextGrid tiers for target file and add to collection
        tiers = _get_textgrid_tiers_from_target_file(target_file.name)
        for tier in tiers:
            textgrid_metadata_tiers.add(tier)

        # Get truth settings for target file
        truth_config_ids: list[int] = []
        for name, config in target_file.truth_configs.items():
            ts = json.dumps({"name": name} | config.to_dict())
            cur.execute(
                "SELECT truth_config.id FROM truth_config WHERE ? = truth_config.config",
                (ts,),
            )
            truth_config_ids.append(cur.fetchone()[0])

        # Get speaker_id for target file
        cur.execute(
            "SELECT speaker.id FROM speaker WHERE ? = speaker.parent",
            (Path(target_file.name).parent.as_posix(),),
        )
        result = cur.fetchone()
        speaker_id = None
        if result is not None:
            speaker_id = result[0]

        # Add entry
        cur.execute(
            "INSERT INTO target_file (name, samples, class_indices, level_type, speaker_id) VALUES (?, ?, ?, ?, ?)",
            (
                target_file.name,
                target_file.samples,
                json.dumps(target_file.class_indices),
                target_file.level_type,
                speaker_id,
            ),
        )
        target_file_id = cur.lastrowid
        for truth_config_id in truth_config_ids:
            cur.execute(
                "INSERT INTO target_file_truth_config (target_file_id, truth_config_id) VALUES (?, ?)",
                (target_file_id, truth_config_id),
            )

    # Update textgrid_metadata_tiers in the top table
    con.execute(
        "UPDATE top SET textgrid_metadata_tiers=? WHERE top.id = ?",
        (json.dumps(sorted(textgrid_metadata_tiers)), 1),
    )

    con.commit()
    con.close()


def populate_noise_file_table(location: str, noise_files: NoiseFiles, test: bool = False) -> None:
    """Populate noise file table"""
    from .mixdb import db_connection

    con = db_connection(location=location, readonly=False, test=test)
    con.executemany(
        "INSERT INTO noise_file (name, samples) VALUES (?, ?)",
        [(noise_file.name, noise_file.samples) for noise_file in noise_files],
    )
    con.commit()
    con.close()


def populate_impulse_response_file_table(
    location: str, impulse_response_files: ImpulseResponseFiles, test: bool = False
) -> None:
    """Populate impulse response file table"""
    import json

    from .mixdb import db_connection

    con = db_connection(location=location, readonly=False, test=test)
    con.executemany(
        "INSERT INTO impulse_response_file (file, tags) VALUES (?, ?)",
        [
            (
                impulse_response_file.file,
                json.dumps(impulse_response_file.tags),
            )
            for impulse_response_file in impulse_response_files
        ],
    )
    con.commit()
    con.close()


def update_mixid_width(location: str, num_mixtures: int, test: bool = False) -> None:
    """Update the mixid width"""
    from sonusai.utils import max_text_width

    from .mixdb import db_connection

    con = db_connection(location=location, readonly=False, test=test)
    con.execute(
        "UPDATE top SET mixid_width=? WHERE top.id = ?",
        (max_text_width(num_mixtures), 1),
    )
    con.commit()
    con.close()


def populate_mixture_table(location: str, mixtures: Mixtures, test: bool = False) -> None:
    """Populate mixture table"""
    from .helpers import from_mixture
    from .helpers import from_target
    from .mixdb import db_connection

    con = db_connection(location=location, readonly=False, test=test)

    # Populate target table
    targets: list[tuple[int, str, float]] = []
    for mixture in mixtures:
        for target in mixture.targets:
            entry = from_target(target)
            if entry not in targets:
                targets.append(entry)

    con.executemany("INSERT INTO target (file_id, augmentation, gain) VALUES (?, ?, ?)", targets)

    # Populate mixture table
    cur = con.cursor()
    for mixture in mixtures:
        cur.execute(
            """
        INSERT INTO mixture (name, noise_file_id, noise_augmentation, noise_offset, noise_snr_gain, random_snr,
        snr, samples, spectral_mask_id, spectral_mask_seed, target_snr_gain)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            from_mixture(mixture),
        )

        mixture_id = cur.lastrowid
        for target in mixture.targets:
            target_id = con.execute(
                """
            SELECT target.id
            FROM target
            WHERE ? = target.file_id AND ? = target.augmentation AND ? = target.gain
            """,
                from_target(target),
            ).fetchone()[0]
            con.execute(
                "INSERT INTO mixture_target (mixture_id, target_id) VALUES (?, ?)",
                (mixture_id, target_id),
            )

    con.commit()
    con.close()


def update_mixture(mixdb: MixtureDatabase, mixture: Mixture, with_data: bool = False) -> tuple[Mixture, GenMixData]:
    """Update mixture record with name and gains

    :param mixdb: Mixture database
    :param mixture: Mixture record
    :param with_data: Return audio data
    :return: Generated audio data (if requested)
    """
    from .audio import get_next_noise
    from .augmentation import apply_gain
    from .datatypes import GenMixData
    from .helpers import get_target

    mixture, targets_audio = _initialize_targets_audio(mixdb, mixture)

    noise_audio = _augmented_noise_audio(mixdb, mixture)
    noise_audio = get_next_noise(audio=noise_audio, offset=mixture.noise.offset, length=mixture.samples)

    # Apply IR and sum targets audio before initializing the mixture SNR gains
    target_audio = get_target(mixdb, mixture, targets_audio)

    mixture = _initialize_mixture_gains(
        mixdb=mixdb, mixture=mixture, target_audio=target_audio, noise_audio=noise_audio
    )

    mixture.name = f"{int(mixture.name):0{mixdb.mixid_width}}"

    if not with_data:
        return mixture, GenMixData()

    # Apply SNR gains
    targets_audio = [apply_gain(audio=target_audio, gain=mixture.target_snr_gain) for target_audio in targets_audio]
    noise_audio = apply_gain(audio=noise_audio, gain=mixture.noise_snr_gain)

    # Apply IR and sum targets audio after applying the mixture SNR gains
    target_audio = get_target(mixdb, mixture, targets_audio)
    mixture_audio = target_audio + noise_audio

    return mixture, GenMixData(
        mixture=mixture_audio,
        targets=targets_audio,
        target=target_audio,
        noise=noise_audio,
    )


def _augmented_noise_audio(mixdb: MixtureDatabase, mixture: Mixture) -> AudioT:
    from .audio import read_audio
    from .audio import read_ir
    from .augmentation import apply_augmentation
    from .augmentation import apply_impulse_response

    noise = mixdb.noise_file(mixture.noise.file_id)
    noise_augmentation = mixture.noise.augmentation

    audio = read_audio(noise.name)
    audio = apply_augmentation(audio, noise_augmentation)
    if noise_augmentation.ir is not None:
        audio = apply_impulse_response(audio, read_ir(mixdb.impulse_response_file(noise_augmentation.ir)))

    return audio


def _initialize_targets_audio(mixdb: MixtureDatabase, mixture: Mixture) -> tuple[Mixture, AudiosT]:
    from .augmentation import apply_augmentation
    from .augmentation import pad_audio_to_length

    targets_audio = []
    for target in mixture.targets:
        target_audio = mixdb.read_target_audio(target.file_id)
        targets_audio.append(
            apply_augmentation(
                audio=target_audio,
                augmentation=target.augmentation,
                frame_length=mixdb.feature_step_samples,
            )
        )

        # target_gain is used to back out the gain augmentation in order to return the target audio
        # to its normalized level when calculating truth (if needed).
        if target.augmentation.gain is not None:
            target.gain = round(10 ** (target.augmentation.gain / 20), ndigits=5)
        else:
            target.gain = 1

    mixture.samples = max([len(item) for item in targets_audio])

    for idx in range(len(targets_audio)):
        targets_audio[idx] = pad_audio_to_length(audio=targets_audio[idx], length=mixture.samples)

    return mixture, targets_audio


def _initialize_mixture_gains(
    mixdb: MixtureDatabase, mixture: Mixture, target_audio: AudioT, noise_audio: AudioT
) -> Mixture:
    import numpy as np

    from sonusai.utils import asl_p56
    from sonusai.utils import db_to_linear

    if mixture.snr < -96:
        # Special case for zeroing out target data
        mixture.target_snr_gain = 0
        mixture.noise_snr_gain = 1
        # Setting target_gain to zero will cause the truth to be all zeros.
        for target in mixture.targets:
            target.gain = 0
    elif mixture.snr > 96:
        # Special case for zeroing out noise data
        mixture.target_snr_gain = 1
        mixture.noise_snr_gain = 0
    else:
        target_level_types = [
            target_file.level_type for target_file in [mixdb.target_file(target.file_id) for target in mixture.targets]
        ]
        if not all(level_type == target_level_types[0] for level_type in target_level_types):
            raise ValueError("Not all target_level_types in mixup are the same")

        level_type = target_level_types[0]
        match level_type:
            case "default":
                target_energy = np.mean(np.square(target_audio))
            case "speech":
                target_energy = asl_p56(target_audio)
            case _:
                raise ValueError(f"Unknown level_type: {level_type}")

        noise_energy = np.mean(np.square(noise_audio))
        if noise_energy == 0:
            noise_gain = 1
        else:
            noise_gain = np.sqrt(target_energy / noise_energy) / db_to_linear(mixture.snr)

        # Check for noise_gain > 1 to avoid clipping
        if noise_gain > 1:
            mixture.target_snr_gain = 1 / noise_gain
            mixture.noise_snr_gain = 1
        else:
            mixture.target_snr_gain = 1
            mixture.noise_snr_gain = noise_gain

    # Check for clipping in mixture
    gain_adjusted_target_audio = target_audio * mixture.target_snr_gain
    gain_adjusted_noise_audio = noise_audio * mixture.noise_snr_gain
    mixture_audio = gain_adjusted_target_audio + gain_adjusted_noise_audio
    max_abs_audio = max(abs(mixture_audio))
    clip_level = db_to_linear(-0.25)
    if max_abs_audio > clip_level:
        # Clipping occurred; lower gains to bring audio within +/-1
        gain_adjustment = clip_level / max_abs_audio
        mixture.target_snr_gain *= gain_adjustment
        mixture.noise_snr_gain *= gain_adjustment

    mixture.target_snr_gain = round(mixture.target_snr_gain, ndigits=5)
    mixture.noise_snr_gain = round(mixture.noise_snr_gain, ndigits=5)
    return mixture


def generate_mixtures(
    noise_mix_mode: str,
    augmented_targets: AugmentedTargets,
    target_files: TargetFiles,
    target_augmentations: AugmentationRules,
    noise_files: NoiseFiles,
    noise_augmentations: AugmentationRules,
    spectral_masks: SpectralMasks,
    all_snrs: list[UniversalSNRGenerator],
    mixups: list[int],
    num_classes: int,
    feature_step_samples: int,
    num_ir: int,
) -> tuple[int, int, Mixtures]:
    """Generate mixtures

    :param noise_mix_mode: Noise mix mode
    :param augmented_targets: List of augmented targets
    :param target_files: List of target files
    :param target_augmentations: List of target augmentations
    :param noise_files: List of noise files
    :param noise_augmentations: List of noise augmentations
    :param spectral_masks: List of spectral masks
    :param all_snrs: List of all SNRs
    :param mixups: List of mixup values
    :param num_classes: Number of classes
    :param feature_step_samples: Number of samples in a feature step
    :param num_ir: Number of impulse response files
    :return: (Number of noise files used, number of noise samples used, list of mixture records)
    """
    if noise_mix_mode == "exhaustive":
        return _exhaustive_noise_mix(
            augmented_targets=augmented_targets,
            target_files=target_files,
            target_augmentations=target_augmentations,
            noise_files=noise_files,
            noise_augmentations=noise_augmentations,
            spectral_masks=spectral_masks,
            all_snrs=all_snrs,
            mixups=mixups,
            num_classes=num_classes,
            feature_step_samples=feature_step_samples,
            num_ir=num_ir,
        )

    if noise_mix_mode == "non-exhaustive":
        return _non_exhaustive_noise_mix(
            augmented_targets=augmented_targets,
            target_files=target_files,
            target_augmentations=target_augmentations,
            noise_files=noise_files,
            noise_augmentations=noise_augmentations,
            spectral_masks=spectral_masks,
            all_snrs=all_snrs,
            mixups=mixups,
            num_classes=num_classes,
            feature_step_samples=feature_step_samples,
            num_ir=num_ir,
        )

    if noise_mix_mode == "non-combinatorial":
        return _non_combinatorial_noise_mix(
            augmented_targets=augmented_targets,
            target_files=target_files,
            target_augmentations=target_augmentations,
            noise_files=noise_files,
            noise_augmentations=noise_augmentations,
            spectral_masks=spectral_masks,
            all_snrs=all_snrs,
            mixups=mixups,
            num_classes=num_classes,
            feature_step_samples=feature_step_samples,
            num_ir=num_ir,
        )

    raise ValueError(f"invalid noise_mix_mode: {noise_mix_mode}")


def _exhaustive_noise_mix(
    augmented_targets: AugmentedTargets,
    target_files: TargetFiles,
    target_augmentations: AugmentationRules,
    noise_files: NoiseFiles,
    noise_augmentations: AugmentationRules,
    spectral_masks: SpectralMasks,
    all_snrs: list[UniversalSNRGenerator],
    mixups: list[int],
    num_classes: int,
    feature_step_samples: int,
    num_ir: int,
) -> tuple[int, int, Mixtures]:
    """Use every noise/augmentation with every target/augmentation"""
    from random import randint

    import numpy as np

    from .augmentation import augmentation_from_rule
    from .augmentation import estimate_augmented_length_from_length
    from .datatypes import Mixture
    from .datatypes import Mixtures
    from .datatypes import Noise
    from .datatypes import UniversalSNR
    from .targets import get_augmented_target_ids_for_mixup

    mixtures: Mixtures = []
    m_id = 0
    used_noise_files = len(noise_files) * len(noise_augmentations)
    used_noise_samples = 0

    augmented_target_ids_for_mixups = [
        get_augmented_target_ids_for_mixup(
            augmented_targets=augmented_targets,
            targets=target_files,
            target_augmentations=target_augmentations,
            mixup=mixup,
            num_classes=num_classes,
        )
        for mixup in mixups
    ]
    for noise_file_id in range(len(noise_files)):
        for noise_augmentation_rule in noise_augmentations:
            noise_augmentation = augmentation_from_rule(noise_augmentation_rule, num_ir)
            noise_offset = 0
            noise_length = estimate_augmented_length_from_length(
                length=noise_files[noise_file_id].samples,
                tempo=noise_augmentation.tempo,
            )

            for augmented_target_ids_for_mixup in augmented_target_ids_for_mixups:
                for augmented_target_ids in augmented_target_ids_for_mixup:
                    targets, target_length = _get_target_info(
                        augmented_target_ids=augmented_target_ids,
                        augmented_targets=augmented_targets,
                        target_files=target_files,
                        target_augmentations=target_augmentations,
                        feature_step_samples=feature_step_samples,
                        num_ir=num_ir,
                    )

                    for spectral_mask_id in range(len(spectral_masks)):
                        for snr in all_snrs:
                            mixtures.append(
                                Mixture(
                                    targets=targets,
                                    name=str(m_id),
                                    noise=Noise(
                                        file_id=noise_file_id + 1,
                                        augmentation=noise_augmentation,
                                        offset=noise_offset,
                                    ),
                                    samples=target_length,
                                    snr=UniversalSNR(value=snr.value, is_random=snr.is_random),
                                    spectral_mask_id=spectral_mask_id + 1,
                                    spectral_mask_seed=randint(0, np.iinfo("i").max),  # noqa: S311
                                )
                            )
                            m_id += 1

                            noise_offset = int((noise_offset + target_length) % noise_length)
                            used_noise_samples += target_length

    return used_noise_files, used_noise_samples, mixtures


def _non_exhaustive_noise_mix(
    augmented_targets: AugmentedTargets,
    target_files: TargetFiles,
    target_augmentations: AugmentationRules,
    noise_files: NoiseFiles,
    noise_augmentations: AugmentationRules,
    spectral_masks: SpectralMasks,
    all_snrs: list[UniversalSNRGenerator],
    mixups: list[int],
    num_classes: int,
    feature_step_samples: int,
    num_ir: int,
) -> tuple[int, int, Mixtures]:
    """Cycle through every target/augmentation without necessarily using all noise/augmentation combinations
    (reduced data set).
    """
    from random import randint

    import numpy as np

    from .datatypes import Mixture
    from .datatypes import Mixtures
    from .datatypes import Noise
    from .datatypes import UniversalSNR
    from .targets import get_augmented_target_ids_for_mixup

    mixtures: Mixtures = []
    m_id = 0
    used_noise_files = set()
    used_noise_samples = 0
    noise_file_id = None
    noise_augmentation_id = None
    noise_offset = None

    augmented_target_indices_for_mixups = [
        get_augmented_target_ids_for_mixup(
            augmented_targets=augmented_targets,
            targets=target_files,
            target_augmentations=target_augmentations,
            mixup=mixup,
            num_classes=num_classes,
        )
        for mixup in mixups
    ]
    for mixup in augmented_target_indices_for_mixups:
        for augmented_target_indices in mixup:
            targets, target_length = _get_target_info(
                augmented_target_ids=augmented_target_indices,
                augmented_targets=augmented_targets,
                target_files=target_files,
                target_augmentations=target_augmentations,
                feature_step_samples=feature_step_samples,
                num_ir=num_ir,
            )

            for spectral_mask_id in range(len(spectral_masks)):
                for snr in all_snrs:
                    (
                        noise_file_id,
                        noise_augmentation_id,
                        noise_augmentation,
                        noise_offset,
                    ) = _get_next_noise_offset(
                        noise_file_id=noise_file_id,
                        noise_augmentation_id=noise_augmentation_id,
                        noise_offset=noise_offset,
                        target_length=target_length,
                        noise_files=noise_files,
                        noise_augmentations=noise_augmentations,
                        num_ir=num_ir,
                    )
                    used_noise_samples += target_length

                    used_noise_files.add(f"{noise_file_id}_{noise_augmentation_id}")

                    mixtures.append(
                        Mixture(
                            targets=targets,
                            name=str(m_id),
                            noise=Noise(
                                file_id=noise_file_id + 1,
                                augmentation=noise_augmentation,
                                offset=noise_offset,
                            ),
                            samples=target_length,
                            snr=UniversalSNR(value=snr.value, is_random=snr.is_random),
                            spectral_mask_id=spectral_mask_id + 1,
                            spectral_mask_seed=randint(0, np.iinfo("i").max),  # noqa: S311
                        )
                    )
                    m_id += 1

    return len(used_noise_files), used_noise_samples, mixtures


def _non_combinatorial_noise_mix(
    augmented_targets: AugmentedTargets,
    target_files: TargetFiles,
    target_augmentations: AugmentationRules,
    noise_files: NoiseFiles,
    noise_augmentations: AugmentationRules,
    spectral_masks: SpectralMasks,
    all_snrs: list[UniversalSNRGenerator],
    mixups: list[int],
    num_classes: int,
    feature_step_samples: int,
    num_ir: int,
) -> tuple[int, int, Mixtures]:
    """Combine a target/augmentation with a single cut of a noise/augmentation non-exhaustively
    (each target/augmentation does not use each noise/augmentation). Cut has random start and loop back to
    beginning if end of noise/augmentation is reached.
    """
    from random import choice
    from random import randint

    import numpy as np

    from .datatypes import Mixture
    from .datatypes import Mixtures
    from .datatypes import Noise
    from .datatypes import UniversalSNR
    from .targets import get_augmented_target_ids_for_mixup

    mixtures: Mixtures = []
    m_id = 0
    used_noise_files = set()
    used_noise_samples = 0
    noise_file_id = None
    noise_augmentation_id = None

    augmented_target_indices_for_mixups = [
        get_augmented_target_ids_for_mixup(
            augmented_targets=augmented_targets,
            targets=target_files,
            target_augmentations=target_augmentations,
            mixup=mixup,
            num_classes=num_classes,
        )
        for mixup in mixups
    ]
    for mixup in augmented_target_indices_for_mixups:
        for augmented_target_indices in mixup:
            targets, target_length = _get_target_info(
                augmented_target_ids=augmented_target_indices,
                augmented_targets=augmented_targets,
                target_files=target_files,
                target_augmentations=target_augmentations,
                feature_step_samples=feature_step_samples,
                num_ir=num_ir,
            )

            for spectral_mask_id in range(len(spectral_masks)):
                for snr in all_snrs:
                    (
                        noise_file_id,
                        noise_augmentation_id,
                        noise_augmentation,
                        noise_length,
                    ) = _get_next_noise_indices(
                        noise_file_id=noise_file_id,
                        noise_augmentation_id=noise_augmentation_id,
                        noise_files=noise_files,
                        noise_augmentations=noise_augmentations,
                        num_ir=num_ir,
                    )
                    used_noise_samples += target_length

                    used_noise_files.add(f"{noise_file_id}_{noise_augmentation_id}")

                    mixtures.append(
                        Mixture(
                            targets=targets,
                            name=str(m_id),
                            noise=Noise(
                                file_id=noise_file_id + 1,
                                augmentation=noise_augmentation,
                                offset=choice(range(noise_length)),  # noqa: S311
                            ),
                            samples=target_length,
                            snr=UniversalSNR(value=snr.value, is_random=snr.is_random),
                            spectral_mask_id=spectral_mask_id + 1,
                            spectral_mask_seed=randint(0, np.iinfo("i").max),  # noqa: S311
                        )
                    )
                    m_id += 1

    return len(used_noise_files), used_noise_samples, mixtures


def _get_next_noise_indices(
    noise_file_id: int | None,
    noise_augmentation_id: int | None,
    noise_files: NoiseFiles,
    noise_augmentations: AugmentationRules,
    num_ir: int,
) -> tuple[int, int, Augmentation, int]:
    from .augmentation import augmentation_from_rule
    from .augmentation import estimate_augmented_length_from_length

    if noise_file_id is None or noise_augmentation_id is None:
        noise_file_id = 0
        noise_augmentation_id = 0
    else:
        noise_augmentation_id += 1
        if noise_augmentation_id == len(noise_augmentations):
            noise_augmentation_id = 0
            noise_file_id += 1
            if noise_file_id == len(noise_files):
                noise_file_id = 0

    noise_augmentation = augmentation_from_rule(noise_augmentations[noise_augmentation_id], num_ir)
    noise_length = estimate_augmented_length_from_length(
        length=noise_files[noise_file_id].samples, tempo=noise_augmentation.tempo
    )
    return noise_file_id, noise_augmentation_id, noise_augmentation, noise_length


def _get_next_noise_offset(
    noise_file_id: int | None,
    noise_augmentation_id: int | None,
    noise_offset: int | None,
    target_length: int,
    noise_files: NoiseFiles,
    noise_augmentations: AugmentationRules,
    num_ir: int,
) -> tuple[int, int, Augmentation, int]:
    from .augmentation import augmentation_from_rule
    from .augmentation import estimate_augmented_length_from_length

    if noise_file_id is None or noise_augmentation_id is None or noise_offset is None:
        noise_file_id = 0
        noise_augmentation_id = 0
        noise_offset = 0

    noise_augmentation = augmentation_from_rule(noise_augmentations[noise_file_id], num_ir)
    noise_length = estimate_augmented_length_from_length(
        length=noise_files[noise_file_id].samples, tempo=noise_augmentation.tempo
    )
    if noise_offset + target_length >= noise_length:
        if noise_offset == 0:
            raise ValueError("Length of target audio exceeds length of noise audio")

        noise_offset = 0
        noise_augmentation_id += 1
        if noise_augmentation_id == len(noise_augmentations):
            noise_augmentation_id = 0
            noise_file_id += 1
            if noise_file_id == len(noise_files):
                noise_file_id = 0
        noise_augmentation = augmentation_from_rule(noise_augmentations[noise_augmentation_id], num_ir)

    return noise_file_id, noise_augmentation_id, noise_augmentation, noise_offset


def _get_target_info(
    augmented_target_ids: list[int],
    augmented_targets: AugmentedTargets,
    target_files: TargetFiles,
    target_augmentations: AugmentationRules,
    feature_step_samples: int,
    num_ir: int,
) -> tuple[Targets, int]:
    from .augmentation import augmentation_from_rule
    from .augmentation import estimate_augmented_length_from_length
    from .datatypes import Target
    from .datatypes import Targets

    mixups: Targets = []
    target_length = 0
    for idx in augmented_target_ids:
        tfi = augmented_targets[idx].target_id
        target_augmentation_rule = target_augmentations[augmented_targets[idx].target_augmentation_id]
        target_augmentation = augmentation_from_rule(target_augmentation_rule, num_ir)

        mixups.append(Target(file_id=tfi + 1, augmentation=target_augmentation))

        target_length = max(
            estimate_augmented_length_from_length(
                length=target_files[tfi].samples,
                tempo=target_augmentation.tempo,
                frame_length=feature_step_samples,
            ),
            target_length,
        )
    return mixups, target_length


def get_all_snrs_from_config(config: dict) -> list[UniversalSNRGenerator]:
    from .datatypes import UniversalSNRGenerator

    return [UniversalSNRGenerator(is_random=False, _raw_value=snr) for snr in config["snrs"]] + [
        UniversalSNRGenerator(is_random=True, _raw_value=snr) for snr in config["random_snrs"]
    ]


def _get_textgrid_tiers_from_target_file(target_file: str) -> list[str]:
    from pathlib import Path

    from praatio import textgrid

    from sonusai.mixture import tokenized_expand

    textgrid_file = Path(tokenized_expand(target_file)[0]).with_suffix(".TextGrid")
    if not textgrid_file.exists():
        return []

    tg = textgrid.openTextgrid(str(textgrid_file), includeEmptyIntervals=False)

    return sorted(tg.tierNames)


def _populate_speaker_table(location: str, target_files: TargetFiles, test: bool = False) -> None:
    """Populate speaker table"""
    import json
    from pathlib import Path

    import yaml

    from .mixdb import db_connection
    from .tokenized_shell_vars import tokenized_expand

    # Determine columns for speaker table
    all_parents = {Path(target_file.name).parent for target_file in target_files}
    speaker_parents = (parent for parent in all_parents if Path(tokenized_expand(parent / "speaker.yml")[0]).exists())

    speakers: dict[Path, dict[str, str]] = {}
    for parent in sorted(speaker_parents):
        with open(tokenized_expand(parent / "speaker.yml")[0]) as f:
            speakers[parent] = yaml.safe_load(f)

    new_columns: list[str] = []
    for keys in speakers:
        for column in speakers[keys]:
            new_columns.append(column)
    new_columns = sorted(set(new_columns))

    con = db_connection(location=location, readonly=False, test=test)

    for new_column in new_columns:
        con.execute(f"ALTER TABLE speaker ADD COLUMN {new_column} TEXT")

    # Populate speaker table
    speaker_rows: list[tuple[str, ...]] = []
    for key in speakers:
        entry = (speakers[key].get(column, None) for column in new_columns)
        speaker_rows.append((key.as_posix(), *entry))  # type: ignore[arg-type]

    column_ids = ", ".join(["parent", *new_columns])
    column_values = ", ".join(["?"] * (len(new_columns) + 1))
    con.executemany(f"INSERT INTO speaker ({column_ids}) VALUES ({column_values})", speaker_rows)

    con.execute("CREATE INDEX speaker_parent_idx ON speaker (parent)")

    # Update speaker_metadata_tiers in the top table
    tiers = [
        description[0]
        for description in con.execute("SELECT * FROM speaker").description
        if description[0] not in ("id", "parent")
    ]
    con.execute(
        "UPDATE top SET speaker_metadata_tiers=? WHERE top.id = ?",
        (json.dumps(tiers), 1),
    )

    if "speaker_id" in tiers:
        con.execute("CREATE INDEX speaker_speaker_id_idx ON speaker (speaker_id)")

    con.commit()
    con.close()


def _populate_truth_config_table(location: str, target_files: TargetFiles, test: bool = False) -> None:
    """Populate truth_config table"""
    import json

    from .mixdb import db_connection

    con = db_connection(location=location, readonly=False, test=test)

    # Populate truth_config table
    truth_configs: list[str] = []
    for target_file in target_files:
        for name, config in target_file.truth_configs.items():
            ts = json.dumps({"name": name} | config.to_dict())
            if ts not in truth_configs:
                truth_configs.append(ts)
    con.executemany(
        "INSERT INTO truth_config (config) VALUES (?)",
        [(item,) for item in truth_configs],
    )

    con.commit()
    con.close()
