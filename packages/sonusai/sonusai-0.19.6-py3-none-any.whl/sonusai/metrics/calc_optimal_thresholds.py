import numpy as np

from sonusai.mixture.datatypes import Predict
from sonusai.mixture.datatypes import Truth


def calc_optimal_thresholds(
    truth: Truth, predict: Predict, timesteps: int = 0, truth_thr: float = 0.5
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Calculates optimal thresholds for each class from one-hot prediction and truth data where both are
    one-hot probabilities (or quantized decisions) with size [frames, num_classes] or [frames, timesteps, num_classes].

    Returns:
      thresholds_opt_pr     [num_classes, 1] optimal thresholds for PR-curve (F1) performance
      thresholds_opt_roc    [num_classes, 1] optimal thresholds for ROC-curve (TPR/FPR) performance
      AP                    [num_classes, 1]
      AUC                   [num_classes, 1]

    Optional truth_thr is the decision threshold(s) applied to truth one-hot input allowing truth to optionally be
    continuous probabilities. Default is 0.5.
    """
    from sklearn.metrics import average_precision_score
    from sklearn.metrics import precision_recall_curve
    from sklearn.metrics import roc_auc_score
    from sklearn.metrics import roc_curve

    from sonusai.utils import get_num_classes_from_predict
    from sonusai.utils import reshape_outputs

    if truth.shape != predict.shape:
        raise ValueError("truth and predict are not the same shape")

    predict, truth = reshape_outputs(predict=predict, truth=truth, timesteps=timesteps)  # type: ignore[assignment]
    num_classes = get_num_classes_from_predict(predict=predict, timesteps=timesteps)

    # Apply decision to truth input
    truth_binary = np.array(truth >= truth_thr).astype(np.int8)

    AP = np.zeros((num_classes, 1))
    AUC = np.zeros((num_classes, 1))
    thresholds_opt_pr = np.zeros((num_classes, 1))
    thresholds_opt_roc = np.zeros((num_classes, 1))
    eps = np.finfo(float).eps
    for nci in range(num_classes):
        # Average Precision also called area under the PR curve AUCPR and
        # AUC ROC curve using binary-ized truth and continuous prediction probabilities
        # sklearn returns nan if no active truth in a class but w/un-suppressible div-by-zero warning
        if sum(truth_binary[:, nci]) == 0:  # no active truth must be NaN
            thresholds_opt_pr[nci] = np.NaN
            thresholds_opt_roc[nci] = np.NaN
            AUC[nci] = np.NaN
            AP[nci] = np.NaN
        else:
            AP[nci] = average_precision_score(truth_binary[:, nci], predict[:, nci], average=None)
            AUC[nci] = roc_auc_score(truth_binary[:, nci], predict[:, nci], average=None)

            # Optimal threshold from PR curve, optimizes f-score
            precision, recall, thrpr = precision_recall_curve(truth_binary[:, nci], predict[:, nci])
            fscore = (2 * precision * recall) / (precision + recall + eps)
            ix = np.argmax(fscore)  # index of largest f1 score
            thresholds_opt_pr[nci] = thrpr[ix]

            # Optimal threshold from ROC curve, optimizes J-statistic (TPR-FPR) or gmean
            fpr, tpr, thrroc = roc_curve(truth_binary[:, nci], predict[:, nci])
            # J = tpr - fpr                  # J can result in thr > 1
            gmeans = np.sqrt(tpr * (1 - fpr))  # gmean seems better behaved
            ix = np.argmax(gmeans)
            thresholds_opt_roc[nci] = thrroc[ix]

    return thresholds_opt_pr, thresholds_opt_roc, AP, AUC
