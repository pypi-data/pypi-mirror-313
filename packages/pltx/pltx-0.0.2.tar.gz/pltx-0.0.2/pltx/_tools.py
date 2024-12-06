import itertools
from typing import Union, Tuple
import numpy as np
from matplotlib import pyplot as plt
from sklearn.calibration import label_binarize
from sklearn.metrics import roc_curve, auc, confusion_matrix


def plot_confusion_matrix(
    cm: np.ndarray,
    classes: list = None,
    figsize: Tuple[int, int] = None,
    title="Confusion matrix",
    cmap=plt.cm.Blues,
):
    """
    绘制预测结果与真实结果的混淆矩阵
    """
    # 增加图像尺寸，设置更大的底部边距
    if figsize:
        plt.figure(figsize=figsize)
    plt.imshow(cm, interpolation="nearest", cmap=cmap)
    plt.title(title)
    plt.colorbar()

    # 设置刻度标签
    classes = classes or [i for i in range(cm.shape[0])]
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45, ha="right")  # 将标签旋转45度，右对齐
    plt.yticks(tick_marks, classes)

    # 添加数值标注
    thresh = cm.max() / 2.0
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(
            j,
            i,
            cm[i, j],
            horizontalalignment="center",
            color="white" if cm[i, j] > thresh else "black",
        )

    # 调整布局，确保所有元素都显示完整
    plt.tight_layout()

    # 添加标签，并调整位置
    plt.ylabel("True label")
    plt.xlabel("Predicted label")

    # 调整底部边距，确保x轴标签完全显示
    plt.subplots_adjust(bottom=0.15)
    plt.show()


def plot_confusion_matrix2(
    y_true: Union[np.ndarray, list],
    y_pred: Union[np.ndarray, list],
    classes: list = None,
    figsize: Tuple[int, int] = None,
    title="Confusion matrix",
    cmap=plt.cm.Blues,
):
    y_true = y_true if isinstance(y_true, np.ndarray) else np.array(y_true)
    y_pred = y_pred if isinstance(y_pred, np.ndarray) else np.array(y_pred)
    cm = confusion_matrix(y_true, y_pred)
    plot_confusion_matrix(cm, classes, figsize, title, cmap)


def plot_roc(
    y_true: Union[np.ndarray, list],
    y_prob: Union[np.ndarray, list],
    figsize: Tuple[int, int] = None,
    title="Receiver Operating Characteristic",
    xlabel="False Positive Rate",
    ylabel="True Positive Rate",
):
    y_true = y_true if isinstance(y_true, np.ndarray) else np.array(y_true)
    y_prob = y_prob if isinstance(y_prob, np.ndarray) else np.array(y_prob)
    fpr, tpr, thesholds_ = roc_curve(y_true, y_prob)
    roc_auc = auc(fpr, tpr)  # 曲线下面积

    # 绘制 ROC曲线
    if figsize:
        plt.figure(figsize=figsize)
    plt.title(title)
    plt.plot(fpr, tpr, "b", label="AUC = %0.5f" % roc_auc)
    plt.legend(loc="lower right")
    plt.plot([0, 1], [0, 1], "r--")
    plt.xlim([-0.1, 1.0])
    plt.ylim([-0.1, 1.01])
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.show()


def plot_multi_class_roc(
    y_true: Union[np.ndarray, list],
    y_prob: Union[np.ndarray, list],
    classes: list = None,
    figsize: Tuple[int, int] = None,
    title="Receiver Operating Characteristic",
    xlabel="False Positive Rate",
    ylabel="True Positive Rate",
):
    """
    绘制宏平均ROC曲线
    参数:
    y_true: 真实标签
    y_pred: 预测概率
    classes: 类别列表
    """
    # 计算每个类别的ROC曲线和AUC
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    y_true = y_true if isinstance(y_true, np.ndarray) else np.array(y_true)
    y_prob = y_prob if isinstance(y_prob, np.ndarray) else np.array(y_prob)
    classes = classes or [i for i in range(y_prob.shape[1])]
    if len(y_true.shape) == 1:
        y_true = label_binarize(y_true, classes=[i for i in range(len(classes))])
 
    # 计算每个类别的假阳性率和真阳性率
    for i in range(y_true.shape[1]):
        fpr[i], tpr[i], _ = roc_curve(y_true[:, i], y_prob[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    # 绘制ROC曲线
    if figsize:
        plt.figure(figsize=figsize)
    for i, cls in enumerate(classes):
        plt.plot(
            fpr[i],
            tpr[i],
            color="#1f77b4",
            linestyle="-",
            label="Class {} ROC  AUC={:.4f}".format(cls, roc_auc[i]),
            lw=2,
        )
    plt.plot([0, 1], [0, 1], color="r", linestyle="--")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend(loc="lower right")
    plt.show()
