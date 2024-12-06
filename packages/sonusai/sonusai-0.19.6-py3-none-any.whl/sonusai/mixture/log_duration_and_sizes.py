def log_duration_and_sizes(
    total_duration: float,
    num_classes: int,
    feature_step_samples: int,
    feature_parameters: int,
    stride: int,
    desc: str,
) -> None:
    from sonusai import logger
    from sonusai.utils import human_readable_size
    from sonusai.utils import seconds_to_hms

    from .constants import FLOAT_BYTES
    from .constants import SAMPLE_BYTES
    from .constants import SAMPLE_RATE

    total_samples = int(total_duration * SAMPLE_RATE)
    mixture_bytes = total_samples * SAMPLE_BYTES
    truth_t_bytes = total_samples * num_classes * FLOAT_BYTES
    feature_bytes = total_samples / feature_step_samples * stride * feature_parameters * FLOAT_BYTES
    truth_f_bytes = total_samples / feature_step_samples * num_classes * FLOAT_BYTES

    logger.info("")
    logger.info(f"{desc} duration:   {seconds_to_hms(seconds=total_duration)}")
    logger.info(f"{desc} sizes:")
    logger.info(f" mixture:             {human_readable_size(mixture_bytes, 1)}")
    logger.info(f" truth_t:             {human_readable_size(truth_t_bytes, 1)}")
    logger.info(f" feature:             {human_readable_size(feature_bytes, 1)}")
    logger.info(f" truth_f:             {human_readable_size(truth_f_bytes, 1)}")
