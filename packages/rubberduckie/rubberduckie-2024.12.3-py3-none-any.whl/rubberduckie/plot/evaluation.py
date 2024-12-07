import numpy as np
from sklearn.metrics import (
    f1_score,
    precision_score,
    recall_score,
    accuracy_score,
    confusion_matrix,
)
from matplotlib import pyplot as plt

DEBUG = False
if DEBUG:
    print("Evalution tools are loaded!")


def prepare_confusion_matrix(
    y, y_hat, model_name="", average="weighted", save_fig_to=None
):
    """Prepare confusion matrix for model evaluation

    Author:
        Colin Li @ 2023-05

    Args:
        y (iterable): actual y
        y_hat (iterable): predicted y
        model_name (str, optional): Name of the model. Defaults to ''.
        average (str, optional): average method. Defaults to 'weighted'.
        save_fig_to (str, optional): file path for output. Defaults to None.
    """
    f1 = f1_score(y, y_hat, average=average)
    precision = precision_score(y, y_hat, average=average)
    recall = recall_score(y, y_hat, average=average)
    accuracy = accuracy_score(y, y_hat)
    cm = confusion_matrix(y_true=y, y_pred=y_hat)
    eval_str = (
        f"Model Evaluation Metrics:\nF1: {f1:.4f}\n"
        + f"Precision: {precision:.4f}\n"
        + f"Recall: {recall:.4f}\n"
        + f"Accuracy: {accuracy:.4f}"
    )
    fig1, axe1 = plt.subplots(figsize=(5, 5), dpi=100, nrows=1, ncols=1)
    axe1.matshow(cm, aspect=1, cmap="Blues", alpha=0.8)
    axe1.set_xlabel("Predicted")
    axe1.set_ylabel("Actual")
    axe1.set_title(f"Confusion Matrix\n{model_name}", fontsize=10)
    for (i, j), z in np.ndenumerate(cm):
        axe1.text(j, i, f"{z:,}", ha="center", va="center", weight="bold")
    fig1.text(
        0.5,
        -0.05,
        eval_str,
        ha="center",
        va="center",
        fontsize=10,
        bbox={"facecolor": "lightblue", "alpha": 0.75, "pad": 5},
    )
    if save_fig_to is not None:
        fig1.savefig(save_fig_to, bbox_inches="tight")
