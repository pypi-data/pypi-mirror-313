# ruff: noqa: F821
import numpy as np
import pandas as pd

from sonusai.mixture import GeneralizedIDs
from sonusai.mixture import MixtureDatabase
from sonusai.mixture import Predict
from sonusai.mixture import Truth


def confusion_matrix_summary(
    mixdb: MixtureDatabase,
    mixids: GeneralizedIDs,
    truth_f: Truth,
    predict: Predict,
    class_idx: int,
    predict_thr: float | np.ndarray = 0,
    truth_thr: float = 0.5,
    timesteps: int = 0,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Calculate confusion matrix for specified class, using truth and prediction
    data [features, num_classes].

    predict_thr sets the decision threshold(s) applied to predict data, thus allowing
    predict to be continuous probabilities.

    Default predict_thr=0 will infer 0.5 for multi-label mode (truth_mutex = False), or
    if single-label mode (truth_mutex == True) then ignore and use argmax mode, and
    the confusion matrix is calculated for all classes.

    Returns pandas dataframes of confusion matrix cmdf and normalized confusion matrix cmndf.
    """
    from sonusai.metrics import one_hot

    num_classes = truth_f.shape[1]
    # TODO: re-work for modern mixdb API
    ytrue, ypred = get_mixids_data(mixdb=mixdb, mixids=mixids, truth_f=truth_f, predict=predict)  # type: ignore[name-defined]

    # Check predict_thr array or scalar and return final scalar predict_thr value
    if not mixdb.truth_mutex and num_classes > 1:
        if not isinstance(predict_thr, np.ndarray):
            if predict_thr == 0:
                # multi-label predict_thr scalar 0 force to 0.5 default
                predict_thr = np.atleast_1d(0.5)
            else:
                predict_thr = np.atleast_1d(predict_thr)
        else:
            if predict_thr.ndim == 1:
                if predict_thr[0] == 0:
                    # multi-label predict_thr array scalar 0 force to 0.5 default
                    predict_thr = np.atleast_1d(0.5)
                else:
                    # multi-label predict_thr array set to scalar = array[0]
                    predict_thr = predict_thr[0]
            else:
                # multi-label predict_thr array scalar set = array[class_idx]
                predict_thr = predict_thr[class_idx]

    if len(mixdb.class_labels) == num_classes:
        class_names = mixdb.class_labels
    else:
        class_names = [f"Class {i}" for i in range(1, num_classes + 1)]

    class_nums = [f"{i}" for i in range(1, num_classes + 1)]

    if mixdb.truth_mutex:
        # single-label mode force to argmax mode
        predict_thr = np.array(0, dtype=np.float32)
        _, _, cm, cmn, _, _ = one_hot(ytrue, ypred, predict_thr, truth_thr, timesteps)
        row_n = class_names
        row_n[-1] = "Other"
        # mux = pd.MultiIndex.from_product([['Single-label/mutex mode, truth thr = {}'.format(truth_thr)],
        #                                   class_nums])
        # mux = pd.MultiIndex.from_product([['truth thr = {}'.format(truth_thr)], class_nums])

        cmdf = pd.DataFrame(cm, index=row_n, columns=class_nums, dtype=np.int32)
        cmndf = pd.DataFrame(cmn, index=row_n, columns=class_nums, dtype=np.float32)

    else:
        _, _, cm, cmn, _, _ = one_hot(ytrue[:, class_idx], ypred[:, class_idx], predict_thr, truth_thr, timesteps)
        cname = class_names[class_idx]
        row_n = ["TrueN", "TrueP"]
        col_n = ["N-" + cname, "P-" + cname]
        cmdf = pd.DataFrame(cm, index=row_n, columns=col_n, dtype=np.int32)
        cmndf = pd.DataFrame(cmn, index=row_n, columns=col_n, dtype=np.float32)
        # add thresholds in 3rd row
        pdnote = pd.DataFrame(np.atleast_2d([predict_thr, truth_thr]), index=["p/t thr:"], columns=col_n)
        cmdf = pd.concat([cmdf, pdnote])
        cmndf = pd.concat([cmndf, pdnote])

    return cmdf, cmndf
