# ruff: noqa: F821
import numpy as np
import pandas as pd

from sonusai.mixture import GeneralizedIDs
from sonusai.mixture import MixtureDatabase
from sonusai.mixture import Predict
from sonusai.mixture import Segsnr
from sonusai.mixture import Truth


def snr_summary(
    mixdb: MixtureDatabase,
    mixid: GeneralizedIDs,
    truth_f: Truth,
    predict: Predict,
    segsnr: Segsnr | None = None,
    predict_thr: float | np.ndarray = 0,
    truth_thr: float = 0.5,
    timesteps: int = 0,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    """Calculate average-over-class metrics per SNR over specified mixture list.
    Inputs:
      mixdb        Mixture database
      mixid
      truth_f      Truth/labels [features, num_classes]
      predict      Prediction data / neural net model one-hot out [features, num_classes]
      segsnr       Segmental SNR from SonusAI genft  [transform_frames, 1]
      predict_thr  Decision threshold(s) applied to predict data, allowing predict to be
                   continuous probabilities or decisions
      truth_thr    Decision threshold(s) applied to truth data, allowing truth to be
                   continuous probabilities or decisions
      timesteps

    Default predict_thr=0 will infer 0.5 for multi-label mode (truth_mutex = False), or
    if single-label mode (truth_mutex == True) then ignore and use argmax mode, and
    the confusion matrix is calculated for all classes.

    Returns pandas dataframe (snrdf) of metrics per SNR.
    """
    import warnings

    from sonusai.metrics import one_hot
    from sonusai.queries import get_mixids_from_snr

    num_classes = truth_f.shape[1]

    snr_mixids = get_mixids_from_snr(mixdb=mixdb, mixids=mixid)

    # Check predict_thr array or scalar and return final scalar predict_thr value
    if not mixdb.truth_mutex and num_classes > 1:
        if not isinstance(predict_thr, np.ndarray):
            if predict_thr == 0:
                # multi-label predict_thr scalar 0 force to 0.5 default
                predict_thr = np.atleast_1d(0.5)
            else:
                predict_thr = np.atleast_1d(predict_thr)
        else:
            if predict_thr.ndim == 1 and len(predict_thr) == 1:
                if predict_thr[0] == 0:
                    # multi-label predict_thr array scalar 0 force to 0.5 default
                    predict_thr = np.atleast_1d(0.5)
                else:
                    # multi-label predict_thr array set to scalar = array[0]
                    predict_thr = predict_thr[0]

    macro_avg = np.zeros((len(snr_mixids), 7), dtype=np.float32)
    micro_avg = np.zeros((len(snr_mixids), 7), dtype=np.float32)
    wghtd_avg = np.zeros((len(snr_mixids), 7), dtype=np.float32)
    ssnr_stats = None
    segsnr_f = None

    if segsnr is not None:
        # prep segsnr if provided, transform frames to feature frames via mean()
        # expected to always be an integer
        feature_frames = int(segsnr.shape[0] / truth_f.shape[0])
        segsnr_f = np.mean(
            np.reshape(segsnr, (truth_f.shape[0], feature_frames)),
            axis=1,
            keepdims=True,
        )
        ssnr_stats = np.zeros((len(snr_mixids), 3), dtype=np.float32)

    for ii, snr in enumerate(snr_mixids):
        # TODO: re-work for modern mixdb API
        y_truth, y_predict = get_mixids_data(mixdb, snr_mixids[snr], truth_f, predict)  # type: ignore[name-defined]
        _, metrics, _, _, _, mavg = one_hot(y_truth, y_predict, predict_thr, truth_thr, timesteps)

        # mavg macro, micro, weighted: [PPV, TPR, F1, FPR, ACC, mAP, mAUC, TPSUM]
        macro_avg[ii, :] = mavg[0, 0:7]
        micro_avg[ii, :] = mavg[1, 0:7]
        wghtd_avg[ii, :] = mavg[2, 0:7]
        if segsnr is not None:
            # TODO: re-work for modern mixdb API
            y_truth, y_segsnr = get_mixids_data(mixdb, snr_mixids[snr], truth_f, segsnr_f)  # type: ignore[name-defined]
            with warnings.catch_warnings():
                warnings.filterwarnings(action="ignore", message="divide by zero encountered in log10")
                # segmental SNR mean = mixture_snr and target_snr
                ssnr_stats[ii, 0] = 10 * np.log10(np.mean(y_segsnr))  # type: ignore[index]
                # segmental SNR 80% percentile
                ssnr_stats[ii, 1] = 10 * np.log10(np.percentile(y_segsnr, 80, method="midpoint"))  # type: ignore[index]
                # segmental SNR max
                ssnr_stats[ii, 2] = 10 * np.log10(max(y_segsnr))  # type: ignore[index]

    # SNR format: PPV, TPR, F1, FPR, ACC, AP, AUC
    col_n = ["PPV", "TPR", "F1", "FPR", "ACC", "AP", "AUC"]
    snr_macrodf = pd.DataFrame(macro_avg, index=list(snr_mixids.keys()), columns=col_n)
    snr_macrodf.sort_index(ascending=False, inplace=True)

    snr_microdf = pd.DataFrame(micro_avg, index=list(snr_mixids.keys()), columns=col_n)
    snr_microdf.sort_index(ascending=False, inplace=True)

    snr_wghtdf = pd.DataFrame(wghtd_avg, index=list(snr_mixids.keys()), columns=col_n)
    snr_wghtdf.sort_index(ascending=False, inplace=True)

    # Add segmental SNR columns if provided
    if segsnr is not None:
        ssnrdf = pd.DataFrame(
            ssnr_stats,
            index=list(snr_mixids.keys()),
            columns=["SSNRavg", "SSNR80p", "SSNRmax"],
        )
        ssnrdf.sort_index(ascending=False, inplace=True)
        snr_macrodf = pd.concat([snr_macrodf, ssnrdf], axis=1)
        snr_microdf = pd.concat([snr_microdf, ssnrdf], axis=1)
        snr_wghtdf = pd.concat([snr_wghtdf, ssnrdf], axis=1)

    return snr_macrodf, snr_microdf, snr_wghtdf, snr_mixids
