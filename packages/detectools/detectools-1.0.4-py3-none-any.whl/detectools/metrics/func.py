import torch
from torch import Tensor


# functionnals metrics
def f1score(tp, fp, tn, fn):
    return (2 * tp) / (2 * tp + fp + fn)


def precision(tp, fp, tn, fn):
    # if tp + fp == 0:
    #     return torch.tensor(torch.nan)
    return (tp) / (tp + fp)


def recall(tp, fp, tn, fn):
    # if tp + fn == 0:
    #     return torch.tensor(torch.nan)
    return (tp) / (tp + fn)


def iou(tp: Tensor, fp: Tensor, tn: Tensor, fn: Tensor) -> Tensor:
    """Compute IoU from statistics."""
    # if tp + fp + fn == 0:
    #     return torch.tensor(torch.nan)
    return tp / (tp + fp + fn)


def accuracy(tp: Tensor, fp: Tensor, tn: Tensor, fn: Tensor):
    """Compute accuracy from statistics. In case of detection, tn is none : -> 0 for computation"""
    if tn == None:
        return tp / (tp + fp + fn)
    else:
        return (tp + tn) / (tn + tp + fp + fn)
