# ruff: noqa: S608
from functools import cached_property
from functools import lru_cache
from functools import partial
from sqlite3 import Connection
from sqlite3 import Cursor
from typing import Any

from .datatypes import ASRConfigs
from .datatypes import AudioF
from .datatypes import AudiosF
from .datatypes import AudiosT
from .datatypes import AudioT
from .datatypes import ClassCount
from .datatypes import Feature
from .datatypes import FeatureGeneratorConfig
from .datatypes import FeatureGeneratorInfo
from .datatypes import GeneralizedIDs
from .datatypes import ImpulseResponseFiles
from .datatypes import MetricDoc
from .datatypes import MetricDocs
from .datatypes import Mixture
from .datatypes import Mixtures
from .datatypes import NoiseFile
from .datatypes import NoiseFiles
from .datatypes import Segsnr
from .datatypes import SpectralMask
from .datatypes import SpectralMasks
from .datatypes import SpeechMetadata
from .datatypes import TargetFile
from .datatypes import TargetFiles
from .datatypes import TransformConfig
from .datatypes import TruthConfigs
from .datatypes import TruthDict
from .datatypes import UniversalSNR


def db_file(location: str, test: bool = False) -> str:
    from os.path import join

    if test:
        name = "mixdb_test.db"
    else:
        name = "mixdb.db"

    return join(location, name)


def db_connection(location: str, create: bool = False, readonly: bool = True, test: bool = False) -> Connection:
    import sqlite3
    from os import remove
    from os.path import exists

    name = db_file(location, test)
    if create and exists(name):
        remove(name)

    if not create and not exists(name):
        raise OSError(f"Could not find mixture database in {location}")

    if not create and readonly:
        name += "?mode=ro"

    connection = sqlite3.connect("file:" + name, uri=True)
    # connection.set_trace_callback(print)
    return connection


class SQLiteContextManager:
    def __init__(self, location: str, test: bool = False) -> None:
        self.location = location
        self.test = test

    def __enter__(self) -> Cursor:
        self.con = db_connection(location=self.location, test=self.test)
        self.cur = self.con.cursor()
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.con.close()


class MixtureDatabase:
    def __init__(self, location: str, test: bool = False) -> None:
        self.location = location
        self.db = partial(SQLiteContextManager, self.location, test)

    @cached_property
    def json(self) -> str:
        from .datatypes import MixtureDatabaseConfig

        config = MixtureDatabaseConfig(
            asr_configs=self.asr_configs,
            class_balancing=self.class_balancing,
            class_labels=self.class_labels,
            class_weights_threshold=self.class_weights_thresholds,
            feature=self.feature,
            impulse_response_files=self.impulse_response_files,
            mixtures=self.mixtures,
            noise_mix_mode=self.noise_mix_mode,
            noise_files=self.noise_files,
            num_classes=self.num_classes,
            spectral_masks=self.spectral_masks,
            target_files=self.target_files,
        )
        return config.to_json(indent=2)

    def save(self) -> None:
        """Save the MixtureDatabase as a JSON file"""
        from os.path import join

        json_name = join(self.location, "mixdb.json")
        with open(file=json_name, mode="w") as file:
            file.write(self.json)

    @cached_property
    def fg_config(self) -> FeatureGeneratorConfig:
        return FeatureGeneratorConfig(
            feature_mode=self.feature,
            truth_parameters=self.truth_parameters,
        )

    @cached_property
    def fg_info(self) -> FeatureGeneratorInfo:
        from .helpers import get_feature_generator_info

        return get_feature_generator_info(self.fg_config)

    @cached_property
    def truth_parameters(self) -> dict[str, int]:
        with self.db() as c:
            rows = c.execute("SELECT * FROM truth_parameters").fetchall()
            truth_parameters: dict[str, int] = {}
            for row in rows:
                truth_parameters[row[1]] = row[2]
            return truth_parameters

    @cached_property
    def num_classes(self) -> int:
        with self.db() as c:
            return int(c.execute("SELECT top.num_classes FROM top").fetchone()[0])

    @cached_property
    def noise_mix_mode(self) -> str:
        with self.db() as c:
            return str(c.execute("SELECT top.noise_mix_mode FROM top").fetchone()[0])

    @cached_property
    def asr_configs(self) -> ASRConfigs:
        import json

        with self.db() as c:
            return json.loads(c.execute("SELECT top.asr_configs FROM top").fetchone()[0])

    @cached_property
    def supported_metrics(self) -> MetricDocs:
        metrics = MetricDocs(
            [
                MetricDoc("Mixture Metrics", "mxsnr", "SNR specification in dB"),
                MetricDoc(
                    "Mixture Metrics",
                    "mxssnr_avg",
                    "Segmental SNR average over all frames",
                ),
                MetricDoc(
                    "Mixture Metrics",
                    "mxssnr_std",
                    "Segmental SNR standard deviation over all frames",
                ),
                MetricDoc(
                    "Mixture Metrics",
                    "mxssnrdb_avg",
                    "Segmental SNR average of the dB frame values over all frames",
                ),
                MetricDoc(
                    "Mixture Metrics",
                    "mxssnrdb_std",
                    "Segmental SNR standard deviation of the dB frame values over all frames",
                ),
                MetricDoc(
                    "Mixture Metrics",
                    "mxssnrf_avg",
                    "Per-bin segmental SNR average over all frames (using feature transform)",
                ),
                MetricDoc(
                    "Mixture Metrics",
                    "mxssnrf_std",
                    "Per-bin segmental SNR standard deviation over all frames (using feature transform)",
                ),
                MetricDoc(
                    "Mixture Metrics",
                    "mxssnrdbf_avg",
                    "Per-bin segmental average of the dB frame values over all frames (using feature transform)",
                ),
                MetricDoc(
                    "Mixture Metrics",
                    "mxssnrdbf_std",
                    "Per-bin segmental standard deviation of the dB frame values over all frames (using feature transform)",
                ),
                MetricDoc("Mixture Metrics", "mxpesq", "PESQ of mixture versus true target[0]"),
                MetricDoc(
                    "Mixture Metrics",
                    "mxwsdr",
                    "Weighted signal distorion ratio of mixture versus true target[0]",
                ),
                MetricDoc(
                    "Mixture Metrics",
                    "mxpd",
                    "Phase distance between mixture and true target[0]",
                ),
                MetricDoc(
                    "Mixture Metrics",
                    "mxstoi",
                    "Short term objective intelligibility of mixture versus true target[0]",
                ),
                MetricDoc(
                    "Mixture Metrics",
                    "mxcsig",
                    "Predicted rating of speech distortion of mixture versus true target[0]",
                ),
                MetricDoc(
                    "Mixture Metrics",
                    "mxcbak",
                    "Predicted rating of background distortion of mixture versus true target[0]",
                ),
                MetricDoc(
                    "Mixture Metrics",
                    "mxcovl",
                    "Predicted rating of overall quality of mixture versus true target[0]",
                ),
                MetricDoc("Mixture Metrics", "ssnr", "Segmental SNR"),
                MetricDoc("Target Metrics", "tdco", "Target[0] DC offset"),
                MetricDoc("Target Metrics", "tmin", "Target[0] min level"),
                MetricDoc("Target Metrics", "tmax", "Target[0] max levl"),
                MetricDoc("Target Metrics", "tpkdb", "Target[0] Pk lev dB"),
                MetricDoc("Target Metrics", "tlrms", "Target[0] RMS lev dB"),
                MetricDoc("Target Metrics", "tpkr", "Target[0] RMS Pk dB"),
                MetricDoc("Target Metrics", "ttr", "Target[0] RMS Tr dB"),
                MetricDoc("Target Metrics", "tcr", "Target[0] Crest factor"),
                MetricDoc("Target Metrics", "tfl", "Target[0] Flat factor"),
                MetricDoc("Target Metrics", "tpkc", "Target[0] Pk count"),
                MetricDoc("Noise Metrics", "ndco", "Noise DC offset"),
                MetricDoc("Noise Metrics", "nmin", "Noise min level"),
                MetricDoc("Noise Metrics", "nmax", "Noise max levl"),
                MetricDoc("Noise Metrics", "npkdb", "Noise Pk lev dB"),
                MetricDoc("Noise Metrics", "nlrms", "Noise RMS lev dB"),
                MetricDoc("Noise Metrics", "npkr", "Noise RMS Pk dB"),
                MetricDoc("Noise Metrics", "ntr", "Noise RMS Tr dB"),
                MetricDoc("Noise Metrics", "ncr", "Noise Crest factor"),
                MetricDoc("Noise Metrics", "nfl", "Noise Flat factor"),
                MetricDoc("Noise Metrics", "npkc", "Noise Pk count"),
                MetricDoc(
                    "Truth Metrics",
                    "sedavg",
                    "(not implemented) Average SED activity over all frames [truth_parameters, 1]",
                ),
                MetricDoc(
                    "Truth Metrics",
                    "sedcnt",
                    "(not implemented) Count in number of frames that SED is active [truth_parameters, 1]",
                ),
                MetricDoc(
                    "Truth Metrics",
                    "sedtop3",
                    "(not implemented) 3 most active by largest sedavg [3, 1]",
                ),
                MetricDoc(
                    "Truth Metrics",
                    "sedtopn",
                    "(not implemented) N most active by largest sedavg [N, 1]",
                ),
            ]
        )
        for name in self.asr_configs:
            metrics.append(
                MetricDoc(
                    "Target Metrics",
                    f"tasr.{name}",
                    f"Target[0] ASR text using {name} ASR as defined in mixdb asr_configs parameter",
                )
            )
            metrics.append(
                MetricDoc(
                    "Mixture Metrics",
                    f"mxasr.{name}",
                    f"ASR text using {name} ASR as defined in mixdb asr_configs parameter",
                )
            )
            metrics.append(
                MetricDoc(
                    "Target Metrics",
                    f"basewer.{name}",
                    f"Word error rate of tasr.{name} vs. speech text metadata for the target",
                )
            )
            metrics.append(
                MetricDoc(
                    "Mixture Metrics",
                    f"mxwer.{name}",
                    f"Word error rate of mxasr.{name} vs. tasr.{name}",
                )
            )

        return metrics

    @cached_property
    def class_balancing(self) -> bool:
        with self.db() as c:
            return bool(c.execute("SELECT top.class_balancing FROM top").fetchone()[0])

    @cached_property
    def feature(self) -> str:
        with self.db() as c:
            return str(c.execute("SELECT top.feature FROM top").fetchone()[0])

    @cached_property
    def fg_decimation(self) -> int:
        return self.fg_info.decimation

    @cached_property
    def fg_stride(self) -> int:
        return self.fg_info.stride

    @cached_property
    def fg_step(self) -> int:
        return self.fg_info.step

    @cached_property
    def feature_parameters(self) -> int:
        return self.fg_info.feature_parameters

    @cached_property
    def ft_config(self) -> TransformConfig:
        return self.fg_info.ft_config

    @cached_property
    def eft_config(self) -> TransformConfig:
        return self.fg_info.eft_config

    @cached_property
    def it_config(self) -> TransformConfig:
        return self.fg_info.it_config

    @cached_property
    def transform_frame_ms(self) -> float:
        from .constants import SAMPLE_RATE

        return float(self.ft_config.overlap) / float(SAMPLE_RATE / 1000)

    @cached_property
    def feature_ms(self) -> float:
        return self.transform_frame_ms * self.fg_decimation * self.fg_stride

    @cached_property
    def feature_samples(self) -> int:
        return self.ft_config.overlap * self.fg_decimation * self.fg_stride

    @cached_property
    def feature_step_ms(self) -> float:
        return self.transform_frame_ms * self.fg_decimation * self.fg_step

    @cached_property
    def feature_step_samples(self) -> int:
        return self.ft_config.overlap * self.fg_decimation * self.fg_step

    def total_samples(self, m_ids: GeneralizedIDs = "*") -> int:
        samples = 0
        for m_id in self.mixids_to_list(m_ids):
            s = self.mixture(m_id).samples
            if s is not None:
                samples += s
        return samples

    def total_transform_frames(self, m_ids: GeneralizedIDs = "*") -> int:
        return self.total_samples(m_ids) // self.ft_config.overlap

    def total_feature_frames(self, m_ids: GeneralizedIDs = "*") -> int:
        return self.total_samples(m_ids) // self.feature_step_samples

    def mixture_transform_frames(self, m_id: int) -> int:
        from .helpers import frames_from_samples

        return frames_from_samples(self.mixture(m_id).samples, self.ft_config.overlap)

    def mixture_feature_frames(self, m_id: int) -> int:
        from .helpers import frames_from_samples

        return frames_from_samples(self.mixture(m_id).samples, self.feature_step_samples)

    def mixids_to_list(self, m_ids: GeneralizedIDs = "*") -> list[int]:
        """Resolve generalized mixture IDs to a list of integers

        :param m_ids: Generalized mixture IDs
        :return: List of mixture ID integers
        """
        from .helpers import generic_ids_to_list

        return generic_ids_to_list(self.num_mixtures, m_ids)

    @cached_property
    def class_labels(self) -> list[str]:
        """Get class labels from db

        :return: Class labels
        """
        with self.db() as c:
            return [
                str(item[0])
                for item in c.execute("SELECT class_label.label FROM class_label ORDER BY class_label.id").fetchall()
            ]

    @cached_property
    def class_weights_thresholds(self) -> list[float]:
        """Get class weights thresholds from db

        :return: Class weights thresholds
        """
        with self.db() as c:
            return [
                float(item[0])
                for item in c.execute(
                    "SELECT class_weights_threshold.threshold FROM class_weights_threshold"
                ).fetchall()
            ]

    @cached_property
    def truth_configs(self) -> TruthConfigs:
        """Get truth configs from db

        :return: Truth configs
        """
        import json

        from .datatypes import TruthConfig

        with self.db() as c:
            truth_configs: TruthConfigs = {}
            for truth_config_record in c.execute("SELECT truth_config.config FROM truth_config").fetchall():
                truth_config = json.loads(truth_config_record[0])
                if truth_config["name"] not in truth_configs:
                    truth_configs[truth_config["name"]] = TruthConfig(
                        function=truth_config["function"],
                        stride_reduction=truth_config["stride_reduction"],
                        config=truth_config["config"],
                    )
            return truth_configs

    def target_truth_configs(self, t_id: int) -> TruthConfigs:
        return _target_truth_configs(self.db, t_id)

    @cached_property
    def random_snrs(self) -> list[float]:
        """Get random snrs from db

        :return: Random SNRs
        """
        with self.db() as c:
            return list(
                {
                    float(item[0])
                    for item in c.execute("SELECT mixture.snr FROM mixture WHERE mixture.random_snr == 1").fetchall()
                }
            )

    @cached_property
    def snrs(self) -> list[float]:
        """Get snrs from db

        :return: SNRs
        """
        with self.db() as c:
            return list(
                {
                    float(item[0])
                    for item in c.execute("SELECT mixture.snr FROM mixture WHERE mixture.random_snr == 0").fetchall()
                }
            )

    @cached_property
    def all_snrs(self) -> list[UniversalSNR]:
        return sorted(
            set(
                [UniversalSNR(is_random=False, value=snr) for snr in self.snrs]
                + [UniversalSNR(is_random=True, value=snr) for snr in self.random_snrs]
            )
        )

    @cached_property
    def spectral_masks(self) -> SpectralMasks:
        """Get spectral masks from db

        :return: Spectral masks
        """
        from .db_datatypes import SpectralMaskRecord

        with self.db() as c:
            spectral_masks = [
                SpectralMaskRecord(*result) for result in c.execute("SELECT * FROM spectral_mask").fetchall()
            ]
            return [
                SpectralMask(
                    f_max_width=spectral_mask.f_max_width,
                    f_num=spectral_mask.f_num,
                    t_max_width=spectral_mask.t_max_width,
                    t_num=spectral_mask.t_num,
                    t_max_percent=spectral_mask.t_max_percent,
                )
                for spectral_mask in spectral_masks
            ]

    def spectral_mask(self, sm_id: int) -> SpectralMask:
        """Get spectral mask with ID from db

        :param sm_id: Spectral mask ID
        :return: Spectral mask
        """
        return _spectral_mask(self.db, sm_id)

    @cached_property
    def target_files(self) -> TargetFiles:
        """Get target files from db

        :return: Target files
        """
        import json

        from .datatypes import TruthConfig
        from .datatypes import TruthConfigs
        from .db_datatypes import TargetFileRecord

        with self.db() as c:
            target_files: TargetFiles = []
            target_file_records = [
                TargetFileRecord(*result) for result in c.execute("SELECT * FROM target_file").fetchall()
            ]
            for target_file_record in target_file_records:
                truth_configs: TruthConfigs = {}
                for truth_config_records in c.execute(
                    "SELECT truth_config.config "
                    + "FROM truth_config, target_file_truth_config "
                    + "WHERE ? = target_file_truth_config.target_file_id "
                    + "AND truth_config.id = target_file_truth_config.truth_config_id",
                    (target_file_record.id,),
                ).fetchall():
                    truth_config = json.loads(truth_config_records[0])
                    truth_configs[truth_config["name"]] = TruthConfig(
                        function=truth_config["function"],
                        stride_reduction=truth_config["stride_reduction"],
                        config=truth_config["config"],
                    )
                target_files.append(
                    TargetFile(
                        name=target_file_record.name,
                        samples=target_file_record.samples,
                        class_indices=json.loads(target_file_record.class_indices),
                        level_type=target_file_record.level_type,
                        truth_configs=truth_configs,
                        speaker_id=target_file_record.speaker_id,
                    )
                )
            return target_files

    @cached_property
    def target_file_ids(self) -> list[int]:
        """Get target file IDs from db

        :return: List of target file IDs
        """
        with self.db() as c:
            return [int(item[0]) for item in c.execute("SELECT target_file.id FROM target_file").fetchall()]

    def target_file(self, t_id: int) -> TargetFile:
        """Get target file with ID from db

        :param t_id: Target file ID
        :return: Target file
        """
        return _target_file(self.db, t_id)

    @cached_property
    def num_target_files(self) -> int:
        """Get number of target files from db

        :return: Number of target files
        """
        with self.db() as c:
            return int(c.execute("SELECT count(target_file.id) FROM target_file").fetchone()[0])

    @cached_property
    def noise_files(self) -> NoiseFiles:
        """Get noise files from db

        :return: Noise files
        """
        with self.db() as c:
            return [
                NoiseFile(name=noise[0], samples=noise[1])
                for noise in c.execute("SELECT noise_file.name, samples FROM noise_file").fetchall()
            ]

    @cached_property
    def noise_file_ids(self) -> list[int]:
        """Get noise file IDs from db

        :return: List of noise file IDs
        """
        with self.db() as c:
            return [int(item[0]) for item in c.execute("SELECT noise_file.id FROM noise_file").fetchall()]

    def noise_file(self, n_id: int) -> NoiseFile:
        """Get noise file with ID from db

        :param n_id: Noise file ID
        :return: Noise file
        """
        return _noise_file(self.db, n_id)

    @cached_property
    def num_noise_files(self) -> int:
        """Get number of noise files from db

        :return: Number of noise files
        """
        with self.db() as c:
            return int(c.execute("SELECT count(noise_file.id) FROM noise_file").fetchone()[0])

    @cached_property
    def impulse_response_files(self) -> ImpulseResponseFiles:
        """Get impulse response files from db

        :return: Impulse response files
        """
        import json

        from .datatypes import ImpulseResponseFile

        with self.db() as c:
            # for impulse_response in c.execute(
            #         "SELECT impulse_response_file.* FROM impulse_response_file"
            # ).fetchall():
            #     print(impulse_response)
            return [
                ImpulseResponseFile(impulse_response[1], json.loads(impulse_response[2]))
                for impulse_response in c.execute(
                    "SELECT impulse_response_file.* FROM impulse_response_file"
                ).fetchall()
            ]

    @cached_property
    def impulse_response_file_ids(self) -> list[int]:
        """Get impulse response file IDs from db

        :return: List of impulse response file IDs
        """
        with self.db() as c:
            return [
                int(item[0])
                for item in c.execute("SELECT impulse_response_file.id FROM impulse_response_file").fetchall()
            ]

    def impulse_response_file(self, ir_id: int | None) -> str | None:
        """Get impulse response file with ID from db

        :param ir_id: Impulse response file ID
        :return: Noise
        """
        if ir_id is None:
            return None
        return _impulse_response_file(self.db, ir_id)

    @cached_property
    def num_impulse_response_files(self) -> int:
        """Get number of impulse response files from db

        :return: Number of impulse response files
        """
        with self.db() as c:
            return int(c.execute("SELECT count(impulse_response_file.id) FROM impulse_response_file").fetchone()[0])

    @cached_property
    def mixtures(self) -> Mixtures:
        """Get mixtures from db

        :return: Mixtures
        """
        from .db_datatypes import MixtureRecord
        from .db_datatypes import TargetRecord
        from .helpers import to_mixture
        from .helpers import to_target

        with self.db() as c:
            mixtures: Mixtures = []
            for mixture in [MixtureRecord(*record) for record in c.execute("SELECT * FROM mixture").fetchall()]:
                targets = [
                    to_target(TargetRecord(*target))
                    for target in c.execute(
                        "SELECT target.* FROM target, mixture_target "
                        + "WHERE ? = mixture_target.mixture_id AND target.id = mixture_target.target_id",
                        (mixture.id,),
                    ).fetchall()
                ]
                mixtures.append(to_mixture(mixture, targets))
            return mixtures

    @cached_property
    def mixture_ids(self) -> list[int]:
        """Get mixture IDs from db

        :return: List of zero-based mixture IDs
        """
        with self.db() as c:
            return [int(item[0]) - 1 for item in c.execute("SELECT mixture.id FROM mixture").fetchall()]

    def mixture(self, m_id: int) -> Mixture:
        """Get mixture record with ID from db

        :param m_id: Zero-based mixture ID
        :return: Mixture record
        """
        return _mixture(self.db, m_id)

    @cached_property
    def mixid_width(self) -> int:
        with self.db() as c:
            return int(c.execute("SELECT top.mixid_width FROM top").fetchone()[0])

    def mixture_location(self, m_id: int) -> str:
        """Get the file location for the give mixture ID

        :param m_id: Zero-based mixture ID
        :return: File location
        """
        from os.path import join

        return join(self.location, self.mixture(m_id).name)

    @cached_property
    def num_mixtures(self) -> int:
        """Get number of mixtures from db

        :return: Number of mixtures
        """
        with self.db() as c:
            return int(c.execute("SELECT count(mixture.id) FROM mixture").fetchone()[0])

    def read_mixture_data(self, m_id: int, items: list[str] | str) -> Any:
        """Read mixture data from a mixture HDF5 file

        :param m_id: Zero-based mixture ID
        :param items: String(s) of dataset(s) to retrieve
        :return: Data (or tuple of data)
        """
        from sonusai.mixture import read_cached_data

        return read_cached_data(self.location, "mixture", self.mixture(m_id).name, items)

    def read_target_audio(self, t_id: int) -> AudioT:
        """Read target audio

        :param t_id: Target ID
        :return: Target audio
        """
        from .audio import read_audio

        return read_audio(self.target_file(t_id).name)

    def augmented_noise_audio(self, mixture: Mixture) -> AudioT:
        """Get augmented noise audio

        :param mixture: Mixture
        :return: Augmented noise audio
        """
        from .audio import read_audio
        from .audio import read_ir
        from .augmentation import apply_augmentation
        from .augmentation import apply_impulse_response

        noise = self.noise_file(mixture.noise.file_id)
        audio = read_audio(noise.name)
        audio = apply_augmentation(audio, mixture.noise.augmentation)
        if mixture.noise.augmentation.ir is not None:
            audio = apply_impulse_response(
                audio,
                read_ir(self.impulse_response_file(mixture.noise.augmentation.ir)),
            )

        return audio

    def mixture_class_indices(self, m_id: int) -> list[int]:
        class_indices: list[int] = []
        for t_id in self.mixture(m_id).target_ids:
            class_indices.extend(self.target_file(t_id).class_indices)
        return sorted(set(class_indices))

    def mixture_targets(self, m_id: int, force: bool = False) -> AudiosT:
        """Get the list of augmented target audio data (one per target in the mixup) for the given mixture ID

        :param m_id: Zero-based mixture ID
        :param force: Force computing data from original sources regardless of whether cached data exists
        :return: List of augmented target audio data (one per target in the mixup)
        """
        from .augmentation import apply_augmentation
        from .augmentation import apply_gain
        from .augmentation import pad_audio_to_length

        if not force:
            targets_audio = self.read_mixture_data(m_id, "targets")
            if targets_audio is not None:
                return list(targets_audio)

        mixture = self.mixture(m_id)
        if mixture is None:
            raise ValueError(f"Could not find mixture for m_id: {m_id}")

        targets_audio = []
        for target in mixture.targets:
            target_audio = self.read_target_audio(target.file_id)
            target_audio = apply_augmentation(
                audio=target_audio,
                augmentation=target.augmentation,
                frame_length=self.feature_step_samples,
            )
            target_audio = apply_gain(audio=target_audio, gain=mixture.target_snr_gain)
            target_audio = pad_audio_to_length(audio=target_audio, length=mixture.samples)
            targets_audio.append(target_audio)

        return targets_audio

    def mixture_targets_f(self, m_id: int, targets: AudiosT | None = None, force: bool = False) -> AudiosF:
        """Get the list of augmented target transform data (one per target in the mixup) for the given mixture ID

        :param m_id: Zero-based mixture ID
        :param targets: List of augmented target audio data (one per target in the mixup)
        :param force: Force computing data from original sources regardless of whether cached data exists
        :return: List of augmented target transform data (one per target in the mixup)
        """
        from .helpers import forward_transform

        if force or targets is None:
            targets = self.mixture_targets(m_id, force)

        return [forward_transform(target, self.ft_config) for target in targets]

    def mixture_target(self, m_id: int, targets: AudiosT | None = None, force: bool = False) -> AudioT:
        """Get the augmented target audio data for the given mixture ID

        :param m_id: Zero-based mixture ID
        :param targets: List of augmented target audio data (one per target in the mixup)
        :param force: Force computing data from original sources regardless of whether cached data exists
        :return: Augmented target audio data
        """
        from .helpers import get_target

        if not force:
            target = self.read_mixture_data(m_id, "target")
            if target is not None:
                return target

        if force or targets is None:
            targets = self.mixture_targets(m_id, force)

        return get_target(self, self.mixture(m_id), targets)

    def mixture_target_f(
        self,
        m_id: int,
        targets: AudiosT | None = None,
        target: AudioT | None = None,
        force: bool = False,
    ) -> AudioF:
        """Get the augmented target transform data for the given mixture ID

        :param m_id: Zero-based mixture ID
        :param targets: List of augmented target audio data (one per target in the mixup)
        :param target: Augmented target audio for the given m_id
        :param force: Force computing data from original sources regardless of whether cached data exists
        :return: Augmented target transform data
        """
        from .helpers import forward_transform

        if force or target is None:
            target = self.mixture_target(m_id, targets, force)

        return forward_transform(target, self.ft_config)

    def mixture_noise(self, m_id: int, force: bool = False) -> AudioT:
        """Get the augmented noise audio data for the given mixture ID

        :param m_id: Zero-based mixture ID
        :param force: Force computing data from original sources regardless of whether cached data exists
        :return: Augmented noise audio data
        """
        from .audio import get_next_noise
        from .augmentation import apply_gain

        if not force:
            noise = self.read_mixture_data(m_id, "noise")
            if noise is not None:
                return noise

        mixture = self.mixture(m_id)
        noise = self.augmented_noise_audio(mixture)
        noise = get_next_noise(audio=noise, offset=mixture.noise.offset, length=mixture.samples)
        return apply_gain(audio=noise, gain=mixture.noise_snr_gain)

    def mixture_noise_f(self, m_id: int, noise: AudioT | None = None, force: bool = False) -> AudioF:
        """Get the augmented noise transform for the given mixture ID

        :param m_id: Zero-based mixture ID
        :param noise: Augmented noise audio data
        :param force: Force computing data from original sources regardless of whether cached data exists
        :return: Augmented noise transform data
        """
        from .helpers import forward_transform

        if force or noise is None:
            noise = self.mixture_noise(m_id, force)

        return forward_transform(noise, self.ft_config)

    def mixture_mixture(
        self,
        m_id: int,
        targets: AudiosT | None = None,
        target: AudioT | None = None,
        noise: AudioT | None = None,
        force: bool = False,
    ) -> AudioT:
        """Get the mixture audio data for the given mixture ID

        :param m_id: Zero-based mixture ID
        :param targets: List of augmented target audio data (one per target in the mixup)
        :param target: Augmented target audio data
        :param noise: Augmented noise audio data
        :param force: Force computing data from original sources regardless of whether cached data exists
        :return: Mixture audio data
        """
        if not force:
            mixture = self.read_mixture_data(m_id, "mixture")
            if mixture is not None:
                return mixture

        if force or target is None:
            target = self.mixture_target(m_id, targets, force)

        if force or noise is None:
            noise = self.mixture_noise(m_id, force)

        return target + noise

    def mixture_mixture_f(
        self,
        m_id: int,
        targets: AudiosT | None = None,
        target: AudioT | None = None,
        noise: AudioT | None = None,
        mixture: AudioT | None = None,
        force: bool = False,
    ) -> AudioF:
        """Get the mixture transform for the given mixture ID

        :param m_id: Zero-based mixture ID
        :param targets: List of augmented target audio data (one per target in the mixup)
        :param target: Augmented target audio data
        :param noise: Augmented noise audio data
        :param mixture: Mixture audio data
        :param force: Force computing data from original sources regardless of whether cached data exists
        :return: Mixture transform data
        """
        from .helpers import forward_transform
        from .spectral_mask import apply_spectral_mask

        if force or mixture is None:
            mixture = self.mixture_mixture(m_id, targets, target, noise, force)

        mixture_f = forward_transform(mixture, self.ft_config)

        m = self.mixture(m_id)
        if m.spectral_mask_id is not None:
            mixture_f = apply_spectral_mask(
                audio_f=mixture_f,
                spectral_mask=self.spectral_mask(int(m.spectral_mask_id)),
                seed=m.spectral_mask_seed,
            )

        return mixture_f

    def mixture_truth_t(
        self,
        m_id: int,
        targets: AudiosT | None = None,
        noise: AudioT | None = None,
        mixture: AudioT | None = None,
        force: bool = False,
    ) -> TruthDict:
        """Get the truth_t data for the given mixture ID

        :param m_id: Zero-based mixture ID
        :param targets: List of augmented target audio data (one per target in the mixup) for the given mixture ID
        :param noise: Augmented noise audio data for the given mixture ID
        :param mixture: Mixture audio data for the given mixture ID
        :param force: Force computing data from original sources regardless of whether cached data exists
        :return: truth_t data
        """
        from .helpers import get_truth

        if not force:
            truth_t = self.read_mixture_data(m_id, "truth_t")
            if truth_t is not None:
                return truth_t

        if force or targets is None:
            targets = self.mixture_targets(m_id, force)

        if force or noise is None:
            noise = self.mixture_noise(m_id, force)

        if force or mixture is None:
            mixture = self.mixture_mixture(m_id, targets=targets, noise=noise, force=force)

        return get_truth(self, self.mixture(m_id), targets, noise, mixture)

    def mixture_segsnr_t(
        self,
        m_id: int,
        targets: AudiosT | None = None,
        target: AudioT | None = None,
        noise: AudioT | None = None,
        force: bool = False,
    ) -> Segsnr:
        """Get the segsnr_t data for the given mixture ID

        :param m_id: Zero-based mixture ID
        :param targets: List of augmented target audio data (one per target in the mixup)
        :param target: Augmented target audio data
        :param noise: Augmented noise audio data
        :param force: Force computing data from original sources regardless of whether cached data exists
        :return: segsnr_t data
        """
        from .helpers import get_segsnr_t

        if not force:
            segsnr_t = self.read_mixture_data(m_id, "segsnr_t")
            if segsnr_t is not None:
                return segsnr_t

        if force or target is None:
            target = self.mixture_target(m_id, targets, force)

        if force or noise is None:
            noise = self.mixture_noise(m_id, force)

        return get_segsnr_t(self, self.mixture(m_id), target, noise)

    def mixture_segsnr(
        self,
        m_id: int,
        segsnr_t: Segsnr | None = None,
        targets: AudiosT | None = None,
        target: AudioT | None = None,
        noise: AudioT | None = None,
        force: bool = False,
    ) -> Segsnr:
        """Get the segsnr data for the given mixture ID

        :param m_id: Zero-based mixture ID
        :param segsnr_t: segsnr_t data
        :param targets: List of augmented target audio data (one per target in the mixup)
        :param target: Augmented target audio data
        :param noise: Augmented noise audio data
        :param force: Force computing data from original sources regardless of whether cached data exists
        :return: segsnr data
        """
        if not force:
            segsnr = self.read_mixture_data(m_id, "segsnr")
            if segsnr is not None:
                return segsnr

            segsnr_t = self.read_mixture_data(m_id, "segsnr_t")
            if segsnr_t is not None:
                return segsnr_t[0 :: self.ft_config.overlap]

        if force or segsnr_t is None:
            segsnr_t = self.mixture_segsnr_t(m_id, targets, target, noise, force)

        return segsnr_t[0 :: self.ft_config.overlap]

    def mixture_ft(
        self,
        m_id: int,
        targets: AudiosT | None = None,
        target: AudioT | None = None,
        noise: AudioT | None = None,
        mixture_f: AudioF | None = None,
        mixture: AudioT | None = None,
        truth_t: TruthDict | None = None,
        force: bool = False,
    ) -> tuple[Feature, TruthDict]:
        """Get the feature and truth_f data for the given mixture ID

        :param m_id: Zero-based mixture ID
        :param targets: List of augmented target audio data (one per target in the mixup)
        :param target: Augmented target audio data
        :param noise: Augmented noise audio data
        :param mixture_f: Mixture transform data
        :param mixture: Mixture audio data
        :param truth_t: truth_t
        :param force: Force computing data from original sources regardless of whether cached data exists
        :return: Tuple of (feature, truth_f) data
        """
        from pyaaware import FeatureGenerator

        from .truth import truth_stride_reduction

        if not force:
            feature, truth_f = self.read_mixture_data(m_id, ["feature", "truth_f"])
            if feature is not None and truth_f is not None:
                return feature, truth_f

        if force or mixture_f is None:
            mixture_f = self.mixture_mixture_f(
                m_id=m_id,
                targets=targets,
                target=target,
                noise=noise,
                mixture=mixture,
                force=force,
            )

        if force or truth_t is None:
            truth_t = self.mixture_truth_t(m_id=m_id, targets=targets, noise=noise, force=force)

        fg = FeatureGenerator(self.fg_config.feature_mode, self.fg_config.truth_parameters)

        feature, truth_f = fg.execute_all(mixture_f, truth_t)
        for key in self.truth_configs:
            truth_f[key] = truth_stride_reduction(truth_f[key], self.truth_configs[key].stride_reduction)

        return feature, truth_f

    def mixture_feature(
        self,
        m_id: int,
        targets: AudiosT | None = None,
        noise: AudioT | None = None,
        mixture: AudioT | None = None,
        truth_t: TruthDict | None = None,
        force: bool = False,
    ) -> Feature:
        """Get the feature data for the given mixture ID

        :param m_id: Zero-based mixture ID
        :param targets: List of augmented target audio data (one per target in the mixup)
        :param noise: Augmented noise audio data
        :param mixture: Mixture audio data
        :param truth_t: truth_t
        :param force: Force computing data from original sources regardless of whether cached data exists
        :return: Feature data
        """
        feature, _ = self.mixture_ft(
            m_id=m_id,
            targets=targets,
            noise=noise,
            mixture=mixture,
            truth_t=truth_t,
            force=force,
        )
        return feature

    def mixture_truth_f(
        self,
        m_id: int,
        targets: AudiosT | None = None,
        noise: AudioT | None = None,
        mixture: AudioT | None = None,
        truth_t: TruthDict | None = None,
        force: bool = False,
    ) -> TruthDict:
        """Get the truth_f data for the given mixture ID

        :param m_id: Zero-based mixture ID
        :param targets: List of augmented target audio data (one per target in the mixup)
        :param noise: Augmented noise audio data
        :param mixture: Mixture audio data
        :param truth_t: truth_t
        :param force: Force computing data from original sources regardless of whether cached data exists
        :return: truth_f data
        """
        _, truth_f = self.mixture_ft(
            m_id=m_id,
            targets=targets,
            noise=noise,
            mixture=mixture,
            truth_t=truth_t,
            force=force,
        )
        return truth_f

    def mixture_class_count(
        self,
        m_id: int,
        targets: AudiosT | None = None,
        noise: AudioT | None = None,
        truth_t: TruthDict | None = None,
    ) -> ClassCount:
        """Compute the number of frames for which each class index is active for the given mixture ID

        :param m_id: Zero-based mixture ID
        :param targets: List of augmented target audio (one per target in the mixup)
        :param noise: Augmented noise audio
        :param truth_t: truth_t
        :return: List of class counts
        """
        import numpy as np

        if truth_t is None:
            truth_t = self.mixture_truth_t(m_id, targets, noise)

        class_count = [0] * self.num_classes
        num_classes = self.num_classes
        if "sed" in self.truth_configs:
            for cl in range(num_classes):
                class_count[cl] = int(np.sum(truth_t["sed"][:, cl] >= self.class_weights_thresholds[cl]))

        return class_count

    @cached_property
    def speaker_metadata_tiers(self) -> list[str]:
        import json

        with self.db() as c:
            return json.loads(c.execute("SELECT speaker_metadata_tiers FROM top WHERE 1 = id").fetchone()[0])

    @cached_property
    def textgrid_metadata_tiers(self) -> list[str]:
        import json

        with self.db() as c:
            return json.loads(c.execute("SELECT textgrid_metadata_tiers FROM top WHERE 1 = id").fetchone()[0])

    @cached_property
    def speech_metadata_tiers(self) -> list[str]:
        return sorted(set(self.speaker_metadata_tiers + self.textgrid_metadata_tiers))

    def speaker(self, s_id: int | None, tier: str) -> str | None:
        return _speaker(self.db, s_id, tier)

    def speech_metadata(self, tier: str) -> list[str]:
        from .helpers import get_textgrid_tier_from_target_file

        results: set[str] = set()
        if tier in self.textgrid_metadata_tiers:
            for target_file in self.target_files:
                data = get_textgrid_tier_from_target_file(target_file.name, tier)
                if data is None:
                    continue
                if isinstance(data, list):
                    for item in data:
                        results.add(item.label)
                else:
                    results.add(data)
        elif tier in self.speaker_metadata_tiers:
            for target_file in self.target_files:
                data = self.speaker(target_file.speaker_id, tier)
                if data is not None:
                    results.add(data)

        return sorted(results)

    def mixture_speech_metadata(self, mixid: int, tier: str) -> list[SpeechMetadata]:
        from praatio.utilities.constants import Interval

        from .helpers import get_textgrid_tier_from_target_file

        results: list[SpeechMetadata] = []
        is_textgrid = tier in self.textgrid_metadata_tiers
        if is_textgrid:
            for target in self.mixture(mixid).targets:
                data = get_textgrid_tier_from_target_file(self.target_file(target.file_id).name, tier)
                if isinstance(data, list):
                    # Check for tempo augmentation and adjust Interval start and end data as needed
                    entries = []
                    for entry in data:
                        if target.augmentation.tempo is not None:
                            entries.append(
                                Interval(
                                    entry.start / target.augmentation.tempo,
                                    entry.end / target.augmentation.tempo,
                                    entry.label,
                                )
                            )
                        else:
                            entries.append(entry)
                    results.append(entries)
                else:
                    results.append(data)
        else:
            for target in self.mixture(mixid).targets:
                results.append(self.speaker(self.target_file(target.file_id).speaker_id, tier))

        return results

    def mixids_for_speech_metadata(self, tier: str, value: str | None = None, where: str | None = None) -> list[int]:
        """Get a list of mixture IDs for the given speech metadata tier.

        If 'where' is None, then include mixture IDs whose tier values are equal to the given 'value'.
        If 'where' is not None, then ignore 'value' and use the given SQL where clause to determine
        which entries to include.

        Examples:
        >>> mixdb = MixtureDatabase('/mixdb_location')

        >>> mixids = mixdb.mixids_for_speech_metadata('speaker_id', 'TIMIT_ARC0')
        Get mixutre IDs for mixtures with speakers whose speaker_ids are 'TIMIT_ARC0'.

        >>> mixids = mixdb.mixids_for_speech_metadata('age', where='age < 25')
        Get mixture IDs for mixtures with speakers whose ages are less than 25.

        >>> mixids = mixdb.mixids_for_speech_metadata('dialect', where="dialect in ('New York City', 'Northern')")
        Get mixture IDs for mixtures with speakers whose dialects are either 'New York City' or 'Northern'.
        """
        if value is None and where is None:
            raise ValueError("Must provide either value or where")

        if where is None:
            where = f"{tier} = '{value}'"

        if tier in self.textgrid_metadata_tiers:
            raise ValueError(f"TextGrid tier data, '{tier}', is not supported in mixids_for_speech_metadata().")

        with self.db() as c:
            speaker_ids = [
                speaker_id[0] for speaker_id in c.execute(f"SELECT id FROM speaker WHERE {where}").fetchall()
            ]
            results = c.execute(
                "SELECT id FROM target_file " + f"WHERE speaker_id IN ({','.join(map(str, speaker_ids))})"
            ).fetchall()
            target_file_ids = [target_file_id[0] for target_file_id in results]
            results = c.execute(
                "SELECT mixture_id FROM mixture_target "
                + f"WHERE mixture_target.target_id IN ({','.join(map(str, target_file_ids))})"
            ).fetchall()

        return [mixture_id[0] - 1 for mixture_id in results]

    def mixture_all_speech_metadata(self, m_id: int) -> list[dict[str, SpeechMetadata]]:
        from .helpers import mixture_all_speech_metadata

        return mixture_all_speech_metadata(self, self.mixture(m_id))

    def mixture_metrics(
        self, m_id: int, metrics: list[str], force: bool = False
    ) -> list[float | int | str | Segsnr | None]:
        """Get metrics data for the given mixture ID

        :param m_id: Zero-based mixture ID
        :param metrics: List of metrics to get
        :param force: Force computing data from original sources regardless of whether cached data exists
        :return: List of metric data
        """
        from collections.abc import Callable

        import numpy as np
        from pystoi import stoi

        from sonusai.metrics import calc_audio_stats
        from sonusai.metrics import calc_phase_distance
        from sonusai.metrics import calc_segsnr_f
        from sonusai.metrics import calc_segsnr_f_bin
        from sonusai.metrics import calc_speech
        from sonusai.metrics import calc_wer
        from sonusai.metrics import calc_wsdr
        from sonusai.mixture import SAMPLE_RATE
        from sonusai.mixture import AudioStatsMetrics
        from sonusai.mixture import SpeechMetrics
        from sonusai.utils import calc_asr

        def create_target_audio() -> Callable[[], np.ndarray]:
            state = None

            def get() -> np.ndarray:
                nonlocal state
                if state is None:
                    state = self.mixture_target(m_id)
                return state

            return get

        target_audio = create_target_audio()

        def create_target_f() -> Callable[[], np.ndarray]:
            state = None

            def get() -> np.ndarray:
                nonlocal state
                if state is None:
                    state = self.mixture_targets_f(m_id)[0]
                return state

            return get

        target_f = create_target_f()

        def create_noise_audio() -> Callable[[], np.ndarray]:
            state = None

            def get() -> np.ndarray:
                nonlocal state
                if state is None:
                    state = self.mixture_noise(m_id)
                return state

            return get

        noise_audio = create_noise_audio()

        def create_noise_f() -> Callable[[], np.ndarray]:
            state = None

            def get() -> np.ndarray:
                nonlocal state
                if state is None:
                    state = self.mixture_noise_f(m_id)
                return state

            return get

        noise_f = create_noise_f()

        def create_mixture_audio() -> Callable[[], np.ndarray]:
            state = None

            def get() -> np.ndarray:
                nonlocal state
                if state is None:
                    state = self.mixture_mixture(m_id)
                return state

            return get

        mixture_audio = create_mixture_audio()

        def create_segsnr_f() -> Callable[[], np.ndarray]:
            state = None

            def get() -> np.ndarray:
                nonlocal state
                if state is None:
                    state = self.mixture_segsnr(m_id)
                return state

            return get

        segsnr_f = create_segsnr_f()

        def create_speech() -> Callable[[], SpeechMetrics]:
            state = None

            def get() -> SpeechMetrics:
                nonlocal state
                if state is None:
                    state = calc_speech(hypothesis=mixture_audio(), reference=target_audio())
                return state

            return get

        speech = create_speech()

        def create_target_stats() -> Callable[[], AudioStatsMetrics]:
            state = None

            def get() -> AudioStatsMetrics:
                nonlocal state
                if state is None:
                    state = calc_audio_stats(target_audio(), self.fg_info.ft_config.length / SAMPLE_RATE)
                return state

            return get

        target_stats = create_target_stats()

        def create_noise_stats() -> Callable[[], AudioStatsMetrics]:
            state = None

            def get() -> AudioStatsMetrics:
                nonlocal state
                if state is None:
                    state = calc_audio_stats(noise_audio(), self.fg_info.ft_config.length / SAMPLE_RATE)
                return state

            return get

        noise_stats = create_noise_stats()

        def create_asr_config() -> Callable[[str], dict]:
            state: dict[str, dict] = {}

            def get(asr_name) -> dict:
                nonlocal state
                if asr_name not in state:
                    value = self.asr_configs.get(asr_name, None)
                    if value is None:
                        raise ValueError(f"Unrecognized ASR name: '{asr_name}'")
                    state[asr_name] = value
                return state[asr_name]

            return get

        asr_config = create_asr_config()

        def create_target_asr() -> Callable[[str], str]:
            state: dict[str, str] = {}

            def get(asr_name) -> str:
                nonlocal state
                if asr_name not in state:
                    state[asr_name] = calc_asr(target_audio(), **asr_config(asr_name)).text
                return state[asr_name]

            return get

        target_asr = create_target_asr()

        def create_mixture_asr() -> Callable[[str], str]:
            state: dict[str, str] = {}

            def get(asr_name) -> str:
                nonlocal state
                if asr_name not in state:
                    state[asr_name] = calc_asr(mixture_audio(), **asr_config(asr_name)).text
                return state[asr_name]

            return get

        mixture_asr = create_mixture_asr()

        def get_asr_name(m: str) -> str:
            parts = m.split(".")
            if len(parts) != 2:
                raise ValueError(f"Unrecognized format: '{m}'; must be of the form: '<metric>.<name>'")
            asr_name = parts[1]
            return asr_name

        def calc(m: str) -> float | int | str | Segsnr | None:
            if m == "mxsnr":
                return self.mixture(m_id).snr

            # Get cached data first, if exists
            if not force:
                value = self.read_mixture_data(m_id, m)
                if value is not None:
                    return value

            # Otherwise, generate data as needed
            if m.startswith("mxwer"):
                asr_name = get_asr_name(m)

                if self.mixture(m_id).snr < -96:
                    # noise only, ignore/reset target asr
                    return float("nan")

                if target_asr(asr_name):
                    return calc_wer(mixture_asr(asr_name), target_asr(asr_name)).wer * 100

                # TODO: should this be NaN like above?
                return float(0)

            if m.startswith("basewer"):
                asr_name = get_asr_name(m)

                text = self.mixture_speech_metadata(m_id, "text")[0]
                if text is not None:
                    return calc_wer(target_asr(asr_name), text).wer * 100

                # TODO: should this be NaN like above?
                return float(0)

            if m.startswith("mxasr"):
                return mixture_asr(get_asr_name(m))

            if m == "mxssnr_avg":
                return calc_segsnr_f(segsnr_f()).avg

            if m == "mxssnr_std":
                return calc_segsnr_f(segsnr_f()).std

            if m == "mxssnrdb_avg":
                return calc_segsnr_f(segsnr_f()).db_avg

            if m == "mxssnrdb_std":
                return calc_segsnr_f(segsnr_f()).db_std

            if m == "mxssnrf_avg":
                return calc_segsnr_f_bin(target_f(), noise_f()).avg

            if m == "mxssnrf_std":
                return calc_segsnr_f_bin(target_f(), noise_f()).std

            if m == "mxssnrdbf_avg":
                return calc_segsnr_f_bin(target_f(), noise_f()).db_avg

            if m == "mxssnrdbf_std":
                return calc_segsnr_f_bin(target_f(), noise_f()).db_std

            if m == "mxpesq":
                if self.mixture(m_id).snr < -96:
                    return 0
                return speech().pesq

            if m == "mxcsig":
                if self.mixture(m_id).snr < -96:
                    return 0
                return speech().csig

            if m == "mxcbak":
                if self.mixture(m_id).snr < -96:
                    return 0
                return speech().cbak

            if m == "mxcovl":
                if self.mixture(m_id).snr < -96:
                    return 0
                return speech().covl

            if m == "mxwsdr":
                mixture = mixture_audio()[:, np.newaxis]
                target = target_audio()[:, np.newaxis]
                noise = noise_audio()[:, np.newaxis]
                return calc_wsdr(
                    hypothesis=np.concatenate((mixture, noise), axis=1),
                    reference=np.concatenate((target, noise), axis=1),
                    with_log=True,
                )[0]

            if m == "mxpd":
                mixture_f = self.mixture_mixture_f(m_id)
                return calc_phase_distance(hypothesis=mixture_f, reference=target_f())[0]

            if m == "mxstoi":
                return stoi(
                    x=target_audio(),
                    y=mixture_audio(),
                    fs_sig=SAMPLE_RATE,
                    extended=False,
                )

            if m == "tdco":
                return target_stats().dco

            if m == "tmin":
                return target_stats().min

            if m == "tmax":
                return target_stats().max

            if m == "tpkdb":
                return target_stats().pkdb

            if m == "tlrms":
                return target_stats().lrms

            if m == "tpkr":
                return target_stats().pkr

            if m == "ttr":
                return target_stats().tr

            if m == "tcr":
                return target_stats().cr

            if m == "tfl":
                return target_stats().fl

            if m == "tpkc":
                return target_stats().pkc

            if m.startswith("tasr"):
                return target_asr(get_asr_name(m))

            if m == "ndco":
                return noise_stats().dco

            if m == "nmin":
                return noise_stats().min

            if m == "nmax":
                return noise_stats().max

            if m == "npkdb":
                return noise_stats().pkdb

            if m == "nlrms":
                return noise_stats().lrms

            if m == "npkr":
                return noise_stats().pkr

            if m == "ntr":
                return noise_stats().tr

            if m == "ncr":
                return noise_stats().cr

            if m == "nfl":
                return noise_stats().fl

            if m == "npkc":
                return noise_stats().pkc

            if m == "sedavg":
                return 0

            if m == "sedcnt":
                return 0

            if m == "sedtop3":
                return np.zeros(3, dtype=np.float32)

            if m == "sedtopn":
                return 0

            if m == "ssnr":
                return segsnr_f()

            raise AttributeError(f"Unrecognized metric: '{m}'")

        result: list[float | int | str | Segsnr | None] = []
        for metric in metrics:
            result.append(calc(metric))

        return result


@lru_cache
def _spectral_mask(db: partial, sm_id: int) -> SpectralMask:
    """Get spectral mask with ID from db

    :param db: Database context
    :param sm_id: Spectral mask ID
    :return: Spectral mask
    """
    from .db_datatypes import SpectralMaskRecord

    with db() as c:
        spectral_mask = SpectralMaskRecord(
            *c.execute("SELECT * FROM spectral_mask WHERE ? = spectral_mask.id", (sm_id,)).fetchone()
        )
        return SpectralMask(
            f_max_width=spectral_mask.f_max_width,
            f_num=spectral_mask.f_num,
            t_max_width=spectral_mask.t_max_width,
            t_num=spectral_mask.t_num,
            t_max_percent=spectral_mask.t_max_percent,
        )


@lru_cache
def _target_file(db: partial, t_id: int) -> TargetFile:
    """Get target file with ID from db

    :param db: Database context
    :param t_id: Target file ID
    :return: Target file
    """
    import json

    from .db_datatypes import TargetFileRecord

    with db() as c:
        target_file = TargetFileRecord(
            *c.execute("SELECT * FROM target_file WHERE ? = target_file.id", (t_id,)).fetchone()
        )

        return TargetFile(
            name=target_file.name,
            samples=target_file.samples,
            class_indices=json.loads(target_file.class_indices),
            level_type=target_file.level_type,
            truth_configs=_target_truth_configs(db, t_id),
            speaker_id=target_file.speaker_id,
        )


@lru_cache
def _noise_file(db: partial, n_id: int) -> NoiseFile:
    """Get noise file with ID from db

    :param db: Database context
    :param n_id: Noise file ID
    :return: Noise file
    """
    with db() as c:
        noise = c.execute(
            "SELECT noise_file.name, samples FROM noise_file WHERE ? = noise_file.id",
            (n_id,),
        ).fetchone()
        return NoiseFile(name=noise[0], samples=noise[1])


@lru_cache
def _impulse_response_file(db: partial, ir_id: int) -> str:
    """Get impulse response file with ID from db

    :param db: Database context
    :param ir_id: Impulse response file ID
    :return: Noise
    """
    with db() as c:
        return str(
            c.execute(
                "SELECT impulse_response_file.file FROM impulse_response_file WHERE ? = impulse_response_file.id",
                (ir_id + 1,),
            ).fetchone()[0]
        )


@lru_cache
def _mixture(db: partial, m_id: int) -> Mixture:
    """Get mixture record with ID from db

    :param db: Database context
    :param m_id: Zero-based mixture ID
    :return: Mixture record
    """
    from .db_datatypes import MixtureRecord
    from .db_datatypes import TargetRecord
    from .helpers import to_mixture
    from .helpers import to_target

    with db() as c:
        mixture = MixtureRecord(*c.execute("SELECT * FROM mixture WHERE ? = mixture.id", (m_id + 1,)).fetchone())
        targets = [
            to_target(TargetRecord(*target))
            for target in c.execute(
                "SELECT target.* "
                + "FROM target, mixture_target "
                + "WHERE ? = mixture_target.mixture_id AND target.id = mixture_target.target_id",
                (mixture.id,),
            ).fetchall()
        ]

        return to_mixture(mixture, targets)


@lru_cache
def _speaker(db: partial, s_id: int | None, tier: str) -> str | None:
    if s_id is None:
        return None

    with db() as c:
        data = c.execute(f"SELECT {tier} FROM speaker WHERE ? = id", (s_id,)).fetchone()
        if data is None:
            return None
        if data[0] is None:
            return None
        return data[0]


@lru_cache
def _target_truth_configs(db: partial, t_id: int) -> TruthConfigs:
    import json

    from .datatypes import TruthConfig

    truth_configs: TruthConfigs = {}
    with db() as c:
        for truth_config_record in c.execute(
            "SELECT truth_config.config "
            + "FROM truth_config, target_file_truth_config "
            + "WHERE ? = target_file_truth_config.target_file_id "
            + "AND truth_config.id = target_file_truth_config.truth_config_id",
            (t_id,),
        ).fetchall():
            truth_config = json.loads(truth_config_record[0])
            truth_configs[truth_config["name"]] = TruthConfig(
                function=truth_config["function"],
                stride_reduction=truth_config["stride_reduction"],
                config=truth_config["config"],
            )
    return truth_configs
