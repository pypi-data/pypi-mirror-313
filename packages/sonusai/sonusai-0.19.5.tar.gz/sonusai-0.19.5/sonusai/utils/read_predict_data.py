import numpy as np

from sonusai.mixture.datatypes import Predict


def read_predict_data(filename: str) -> Predict:
    """Read predict data from given HDF5 file and return it."""
    import h5py

    from sonusai import logger

    logger.debug(f"Reading prediction data from {filename}")
    with h5py.File(filename, "r") as f:
        # prediction data is either [frames, num_classes], or [frames, timesteps, num_classes]
        predict = np.array(f["predict"])

        if predict.ndim == 2:
            return predict

        if predict.ndim == 3:
            frames, timesteps, num_classes = predict.shape

            logger.debug(
                f"Reshaping prediction data in {filename} "
                f""
                f"from [{frames}, {timesteps}, {num_classes}] "
                f"to [{frames * timesteps}, {num_classes}]"
            )
            predict = np.reshape(predict, [frames * timesteps, num_classes], order="F")
            return predict

        raise RuntimeError(f"Invalid prediction data dimensions in {filename}")
