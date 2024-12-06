# ruff: noqa: F821
import numpy as np
import pandas as pd

from sonusai.mixture import GeneralizedIDs
from sonusai.mixture import MixtureDatabase
from sonusai.mixture import Predict
from sonusai.mixture import Truth


def class_summary(
    mixdb: MixtureDatabase,
    mixids: GeneralizedIDs,
    truth_f: Truth,
    predict: Predict,
    predict_thr: float | np.ndarray = 0,
    truth_thr: float = 0.5,
    timesteps: int = 0,
) -> pd.DataFrame:
    """Calculate table of metrics per class, and averages for a list
    of mixtures using truth and prediction data [features, num_classes]
    Example:
    Generate multi-class metric summary into table, for example:
                    PPV     TPR      F1     FPR     ACC   AP  AUC  Support
        Class 1     0.71    0.80    0.75    0.00    0.99            44
        Class 2     0.90    0.76    0.82    0.00    0.99            128
        Class 3     0.86    0.82    0.84    0.04    0.93            789
        Other       0.94    0.96    0.95    0.18    0.92            2807

      micro-avg                     0.92    0.027                   3768
      macro avg     0.85    0.83    0.84    0.05    0.96            3768
      micro-avgwo
    """
    from sonusai.metrics import one_hot

    num_classes = truth_f.shape[1]

    # TODO: re-work for modern mixdb API
    y_truth_f, y_predict = get_mixids_data(mixdb, mixids, truth_f, predict)  # type: ignore[name-defined]

    if not mixdb.truth_mutex and num_classes > 1:
        if not isinstance(predict_thr, np.ndarray):
            if predict_thr == 0:
                predict_thr = np.atleast_1d(0.5)
            else:
                predict_thr = np.atleast_1d(predict_thr)
        else:
            if predict_thr.ndim == 1 and predict_thr[0] == 0:
                predict_thr = np.atleast_1d(0.5)

    _, metrics, _, _, _, metavg = one_hot(y_truth_f, y_predict, predict_thr, truth_thr, timesteps)

    # [ACC, TPR, PPV, TNR, FPR, HITFA, F1, MCC, NT, PT, TP, FP, AP, AUC]
    table_idx = np.array([2, 1, 6, 4, 0, 12, 13, 9])
    col_n = ["PPV", "TPR", "F1", "FPR", "ACC", "AP", "AUC", "Support"]
    if mixdb.truth_mutex:
        if len(mixdb.class_labels) >= num_classes - 1:  # labels exist with or without Other
            row_n = mixdb.class_labels
            if len(mixdb.class_labels) == num_classes - 1:  # Other label does not exist, so add it
                row_n.append("Other")
        else:
            row_n = [f"Class {i}" for i in range(1, num_classes)]
            row_n.append("Other")
    else:
        if len(mixdb.class_labels) == num_classes:
            row_n = mixdb.class_labels
        else:
            row_n = [f"Class {i}" for i in range(1, num_classes + 1)]

    df = pd.DataFrame(metrics[:, table_idx], columns=col_n, index=row_n)

    # [miPPV, miTPR, miF1, miFPR, miACC, miAP, miAUC, TPSUM]
    avg_row_n = ["Macro-avg", "Micro-avg", "Weighted-avg"]
    dfavg = pd.DataFrame(metavg, columns=col_n, index=avg_row_n)

    # dfblank = pd.DataFrame([''])
    # pd.concat([df, dfblank, dfblank, dfavg])

    classdf = pd.concat([df, dfavg])
    # classdf = classdf.round(2)
    classdf["Support"] = classdf["Support"].astype(int)

    return classdf
