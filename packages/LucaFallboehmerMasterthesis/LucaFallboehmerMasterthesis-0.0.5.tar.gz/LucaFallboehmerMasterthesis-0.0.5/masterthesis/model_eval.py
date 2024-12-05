import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import time
from tqdm.notebook import trange

# from dataset import *
# from models import *

from .dataset import *
from .models import *

#
# Performance Evaluation Functions
#


def true_positive(ground_truth, prediction):
    tp = 0
    for gt, pred in zip(ground_truth, prediction):
        if gt == 1 and pred == 1:
            tp += 1
    return tp


def true_negative(ground_truth, prediction):
    tn = 0
    for gt, pred in zip(ground_truth, prediction):
        if gt == 0 and pred == 0:
            tn += 1
    return tn


def false_positive(ground_truth, prediction):  # type 1 error
    fp = 0
    for gt, pred in zip(ground_truth, prediction):
        if gt == 0 and pred == 1:
            fp += 1
    return fp


def false_negative(ground_truth, prediction):  # type 2 error
    fn = 0
    for gt, pred in zip(ground_truth, prediction):
        if gt == 1 and pred == 0:
            fn += 1
    return fn


def recall(ground_truth, prediction):  # also called true positive rate / sensitivity
    tp = true_positive(ground_truth, prediction)
    fn = false_negative(ground_truth, prediction)
    rec = tp / (tp + fn)
    return rec


def fallout(ground_truth, prediction):  # also called false positive rate
    fp = false_positive(ground_truth, prediction)
    tn = true_negative(ground_truth, prediction)
    # if fp + tn > 0.0:
    #     fpr = fp / (fp + tn)
    # else:
    #     fpr = 0
    fpr = fp / (fp + tn)
    return fpr


def precision(ground_truth, prediction):
    tp = true_positive(ground_truth, prediction)
    fp = false_positive(ground_truth, prediction)
    if tp + fp > 0:
        prec = tp / (tp + fp)
    else:
        prec = 0
    return prec


def accuracy(ground_truth, prediction):
    tp = true_positive(ground_truth, prediction)
    tn = true_negative(ground_truth, prediction)
    fp = false_positive(ground_truth, prediction)
    fn = false_negative(ground_truth, prediction)
    acc = (tp + tn) / (tp + tn + fp + fn)
    return acc


def f1(ground_truth, prediction):
    p = precision(ground_truth, prediction)
    r = recall(ground_truth, prediction)
    if p + r > 0.0:
        f1_score = 2 * p * r / (p + r)
    else:
        f1_score = 0
    return f1_score


def eval_by_threshold(model, threshold_list, X_test, y_test, device="cpu"):
    """Choose different evaluation thresholds. Used e.g. to create a ROC curve of the model"""
    # want to evaluate model on dataset of certain size:
    # dataset_size = int(X_test.shape[0] / 10)

    score_df_list = []

    # calculate score for model on whole dataset for different thresholds
    with trange(threshold_list, unit="treshold") as iterable:
        for count, threshold in enumerate(iterable):
            score = model.eval_simple(
                threshold_pred=threshold,
                X_validation=X_test,
                y_validation=y_test,
                plot=False,
                losses_training=False,
                losses_validation=False,
                device=device,
            )
            score_df = pd.DataFrame(score, index=[count])
            score_df_list.append(score_df)

    return pd.concat(score_df_list)


def plot_eval_by_threshold(score_by_threshold, dpi=200):
    """
    Plots various evaluation metrics against threshold values.

    Parameters:
    score_by_threshold (dict): Dictionary containing threshold values and evaluation metrics.

    Returns:
    None
    """
    # Extract max values and corresponding thresholds for accuracy, f1, and recall
    max_acc, thr_max_acc = (
        score_by_threshold["accuracy"].max(),
        score_by_threshold["threshold_roc"][np.argmax(score_by_threshold["accuracy"])],
    )
    max_f1, thr_max_f1 = (
        score_by_threshold["f1"].max(),
        score_by_threshold["threshold_roc"][np.argmax(score_by_threshold["f1"])],
    )
    max_rec, thr_max_rec = (
        score_by_threshold["recall"].max(),
        score_by_threshold["threshold_roc"][np.argmax(score_by_threshold["recall"])],
    )

    # Set up subplots
    fig, ax = plt.subplots(3, 2, figsize=(20, 20), dpi=dpi)

    # Plot accuracy by threshold
    ax[0][0].plot(
        score_by_threshold["threshold_roc"],
        score_by_threshold["accuracy"],
        marker="o",
        linestyle="-",
        markersize=6,
        alpha=0.75,
    )
    ax[0][0].axvline(
        x=thr_max_acc,
        color="purple",
        label=f"max value {max_acc:.3f} at {thr_max_acc:.3f}",
    )
    ax[0][0].set_xlabel("Threshold")
    ax[0][0].set_ylabel("Accuracy")
    ax[0][0].set_title("Accuracy by Threshold", weight="bold")
    ax[0][0].legend()

    # Plot F1 score by threshold
    ax[0][1].plot(
        score_by_threshold["threshold_roc"],
        score_by_threshold["f1"],
        marker="o",
        linestyle="-",
        markersize=6,
        alpha=0.75,
    )
    ax[0][1].axvline(
        x=thr_max_f1,
        color="purple",
        label=f"max value {max_f1:.3f} at {thr_max_f1:.3f}",
    )
    ax[0][1].set_xlabel("Threshold")
    ax[0][1].set_ylabel("F1 Score")
    ax[0][1].set_title("F1 Score by Threshold", weight="bold")
    ax[0][1].legend()

    # Plot recall (sensitivity) by threshold
    ax[1][0].plot(
        score_by_threshold["threshold_roc"],
        score_by_threshold["recall"],
        marker="o",
        linestyle="-",
        markersize=6,
        alpha=0.75,
    )
    # Uncomment the following line if you want to show the max recall threshold line:
    # ax[1][0].axvline(x=thr_max_rec, color="purple", label=f"max value {max_rec:.3f} at {thr_max_rec:.3f}")
    ax[1][0].set_xlabel("Threshold")
    ax[1][0].set_ylabel("Recall (Sensitivity)")
    ax[1][0].set_title("Recall (Sensitivity) by Threshold", weight="bold")

    # Plot fallout (false positive rate) by threshold
    ax[1][1].plot(
        score_by_threshold["threshold_roc"],
        score_by_threshold["fall-out"],
        marker="o",
        linestyle="-",
        markersize=6,
        alpha=0.75,
    )

    ax[1][1].set_xlabel("Threshold")
    ax[1][1].set_ylabel("Fallout (False Positive Rate)")
    ax[1][1].set_title("Fallout by Threshold", weight="bold")

    # Plot ROC Curve (recall vs. fallout)
    ax[2][0].plot(
        score_by_threshold["fall-out"],
        score_by_threshold["recall"],
        marker="o",
        linestyle="-",
        markersize=6,
        alpha=0.75,
    )
    ax[2][0].set_xlabel("Fallout (False Positive Rate)")
    ax[2][0].set_ylabel("Recall (Sensitivity)")
    ax[2][0].set_title("ROC Curve", weight="bold")

    # Plot Precision-Recall Curve
    ax[2][1].plot(
        score_by_threshold["recall"],
        score_by_threshold["precision"],
        marker="o",
        linestyle="-",
        markersize=6,
        alpha=0.75,
    )
    ax[2][1].set_xlabel("Recall (Sensitivity)")
    ax[2][1].set_ylabel("Precision")
    ax[2][1].set_title("Precision-Recall Curve", weight="bold")

    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------------------------------------------------
# OLD (kept for convenience) ------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------


def normal_approx_interval(
    model, metric, confidence_level, X_val, y_val, threshold, device="cpu"
):
    z_value = scipy.stats.norm.ppf((1 + confidence_level) / 2.0)

    score = model.eval_simple(
        X_validation=X_val,
        y_validation=y_val,
        plot=False,
        losses_training=False,
        losses_validation=False,
        threshold_pred=threshold,
        device=device,
    )

    ci_length = z_value * np.sqrt(
        (score[metric] * (1 - score[metric])) / y_val.shape[0]
    )

    return score[metric], ci_length


def train_bootstraping(
    model_untrained,
    b_rounds,
    epochs_per_round,
    X_train,
    y_train,
    X_val,
    y_val,
    random_state,
    status=True,
    device="cpu",
):
    rng = np.random.RandomState(random_state)
    bootstrap_train_scores_list = []
    for count, i in enumerate(range(b_rounds)):
        if count == 0:
            t_start = time.time()
        idxs_train = rng.choice(
            np.arange(X_train.shape[0]), size=int(X_train.shape[0] / 5), replace=True
        )
        x_t_b, y_t_b = X_train[idxs_train], y_train[idxs_train]

        idxs_val = rng.choice(
            np.arange(X_val.shape[0]), size=int(X_val.shape[0] / 5), replace=True
        )
        x_v_b, y_v_b = X_train[idxs_val], y_train[idxs_val]

        l, l_val = model_untrained.train_simple(
            epochs=epochs_per_round,
            X_train=x_t_b,
            y_train=y_t_b,
            X_validation=x_v_b,
            y_validation=y_v_b,
            batch_size=model_untrained.batch_size,
            device=device,
            lr=model_untrained.learning_rate,
            random_state=random_state,
        )
        score = model_untrained.eval_simple(
            X_validation=x_v_b,
            y_validation=y_v_b,
            losses_training=False,
            losses_validation=False,
            plot=False,
            device=device,
        )
        score_df = pd.DataFrame(score, index=[count])
        bootstrap_train_scores_list.append(score_df)
        init_weights(model_untrained, bias=True)
        if count == 0:
            t_end = time.time()
        if status:
            print(
                f"round [{count} | {b_rounds}], time/round: {t_end - t_start}, approx time left: {(b_rounds -count) * (t_end-t_start)}"
            )

    bootstrap_train_scores = pd.concat(bootstrap_train_scores_list)
    return bootstrap_train_scores


def test_bootstrapping(
    model_trained, b_rounds, X_val, y_val, random_state, status=True, device="cpu"
):
    rng = np.random.RandomState(seed=random_state)
    idx = np.arange(y_val.shape[0])

    test_scores_list = []

    for count, i in enumerate(range(b_rounds)):
        if count == 0:
            t_start = time.time()
        pred_idx = rng.choice(idx, size=idx.shape[0], replace=True)
        scores_test_boot = model_trained.eval_simple(
            X_validation=X_val[pred_idx],
            y_validation=y_val[pred_idx],
            plot=False,
            losses_training=False,
            losses_validation=False,
            threshold_pred=0.5,
            device=device,
        )
        scores_test_boot_df = pd.DataFrame(scores_test_boot, index=[count])
        test_scores_list.append(scores_test_boot_df)
        if count == 0:
            t_end = time.time()
        if status:
            print(
                f"round [{count} / {b_rounds}], time/round: {t_end - t_start}, approx time left: {(b_rounds-count) * (t_end-t_start)}"
            )

    test_scores = pd.concat(test_scores_list)
    return test_scores
