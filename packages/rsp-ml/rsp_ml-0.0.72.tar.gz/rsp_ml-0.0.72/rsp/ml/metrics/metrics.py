import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sn
import pandas as pd
import cv2 as cv
from typing import List

#__example__ #import rsp.ml.metrics as m
#__example__ #import torch
#__example__ 
#__example__ Y = torch.tensor([
#__example__ \t[0.1, 0.1, 0.8],
#__example__ \t[0.03, 0.95, 0.02],
#__example__ \t[0.05, 0.9, 0.05],
#__example__ \t[0.01, 0.87, 0.12],
#__example__ \t[0.04, 0.03, 0.93],
#__example__ \t[0.94, 0.02, 0.06]
#__example__ ])
#__example__ T = torch.tensor([
#__example__ \t[0, 0, 1],
#__example__ \t[1, 0, 0],
#__example__ \t[0, 1, 0],
#__example__ \t[0, 1, 0],
#__example__ \t[0, 0, 1],
#__example__ \t[1, 0, 0]
#__example__ ])
#__example__ 
#__example__ conf_mat = m.confusion_matrix(Y, T)
#__example__ print(conf_mat) -> tensor([\n\t[1, 1, 0],\n\t[0, 2, 0],\n\t[0, 0, 2]\n])
def confusion_matrix(Y:torch.Tensor, T:torch.Tensor) -> torch.Tensor:
    """
    Calculates the confusion matrix. Expected input shape: (batch_size, num_classes)

    Parameters
    ----------
    Y : torch.Tensor
        Prediction
    T : torch.Tensor
        True values

    Returns
    -------
    torch.Tensor
        Confusion matrix
    """
    assert Y.shape == T.shape, f'Expected Y and T to have the same shape.'
    assert torch.all(Y >= 0) and torch.all(Y <= 1), f'Expected 0 <= Y <= 1'
    assert torch.all(T >= 0) and torch.all(T <= 1), f'Expected 0 <= T <= 1'
    assert len(T.shape) == 2, f'Expected shape (batch_size, num_classes), but got shape of {T.shape}'

    num_classes = T.shape[1]
    classes_Y = torch.argmax(Y, dim=1)
    classes_T = torch.argmax(T, dim=1)

    cm = torch.zeros((num_classes, num_classes), dtype=torch.int64)

    for cy, ct in zip(classes_Y, classes_T):
        cm[ct, cy] += 1

    return cm

#__example__ #import rsp.ml.metrics as m
#__example__ #import torch
#__example__ 
#__example__ Y = torch.tensor([
#__example__ \t[0.1, 0.1, 0.8],
#__example__ \t[0.03, 0.95, 0.02],
#__example__ \t[0.05, 0.9, 0.05],
#__example__ \t[0.01, 0.87, 0.12],
#__example__ \t[0.04, 0.03, 0.93],
#__example__ \t[0.94, 0.02, 0.06]
#__example__ ])
#__example__ T = torch.tensor([
#__example__ \t[0, 0, 1],
#__example__ \t[1, 0, 0],
#__example__ \t[0, 1, 0],
#__example__ \t[0, 1, 0],
#__example__ \t[0, 0, 1],
#__example__ \t[1, 0, 0]
#__example__ ])
#__example__ 
#__example__ tp = m.TP(Y, T)
#__example__ print(tp) -> 5
def TP(Y:torch.Tensor, T:torch.Tensor, threshold:float = 0.5) -> int:
    """
    True positives. Expected input shape: (batch_size, num_classes)
    
    Parameters
    ----------
    Y : torch.Tensor
        Prediction
    T : torch.Tensor
        True values
    threshold : float
        All values that are greater than or equal to the threshold are considered a positive class.

    Returns
    -------
    int
        True positives
    """
    assert Y.shape == T.shape, f'Expected Y and T to have the same shape.'
    assert torch.all(Y >= 0) and torch.all(Y <= 1), f'Expected 0 <= Y <= 1'
    assert torch.all(T >= 0) and torch.all(T <= 1), f'Expected 0 <= T <= 1'
    assert len(T.shape) == 2, f'Expected shape (batch_size, num_classes), but got shape of {T.shape}'
    
    Y_pos = Y >= threshold
    T_pos = T >= threshold

    mask = torch.bitwise_and(Y_pos, T_pos)
    tp = mask.sum().item()
    return tp

#__example__ #import rsp.ml.metrics as m
#__example__ #import torch
#__example__ 
#__example__ Y = torch.tensor([
#__example__ \t[0.1, 0.1, 0.8],
#__example__ \t[0.03, 0.95, 0.02],
#__example__ \t[0.05, 0.9, 0.05],
#__example__ \t[0.01, 0.87, 0.12],
#__example__ \t[0.04, 0.03, 0.93],
#__example__ \t[0.94, 0.02, 0.06]
#__example__ ])
#__example__ T = torch.tensor([
#__example__ \t[0, 0, 1],
#__example__ \t[1, 0, 0],
#__example__ \t[0, 1, 0],
#__example__ \t[0, 1, 0],
#__example__ \t[0, 0, 1],
#__example__ \t[1, 0, 0]
#__example__ ])
#__example__ 
#__example__ tn = m.TN(Y, T)
#__example__ print(tn) -> 11
def TN(Y:torch.Tensor, T:torch.Tensor, threshold:float = 0.5) -> int:
    """
    True negatives. Expected input shape: (batch_size, num_classes)
    
    Parameters
    ----------
    Y : torch.Tensor
        Prediction
    T : torch.Tensor
        True values
    threshold : float
        All values that are greater than or equal to the threshold are considered a positive class.

    Returns
    -------
    int
        True negatives
    """
    assert Y.shape == T.shape, f'Expected Y and T to have the same shape.'
    assert torch.all(Y >= 0) and torch.all(Y <= 1), f'Expected 0 <= Y <= 1'
    assert torch.all(T >= 0) and torch.all(T <= 1), f'Expected 0 <= T <= 1'
    assert len(T.shape) == 2, f'Expected shape (batch_size, num_classes), but got shape of {T.shape}'
    
    Y_neg = Y < threshold
    T_neg = T < threshold

    mask = torch.bitwise_and(Y_neg, T_neg)
    tn = mask.sum().item()
    return tn

#__example__ #import rsp.ml.metrics as m
#__example__ #import torch
#__example__ 
#__example__ Y = torch.tensor([
#__example__ \t[0.1, 0.1, 0.8],
#__example__ \t[0.03, 0.95, 0.02],
#__example__ \t[0.05, 0.9, 0.05],
#__example__ \t[0.01, 0.87, 0.12],
#__example__ \t[0.04, 0.03, 0.93],
#__example__ \t[0.94, 0.02, 0.06]
#__example__ ])
#__example__ T = torch.tensor([
#__example__ \t[0, 0, 1],
#__example__ \t[1, 0, 0],
#__example__ \t[0, 1, 0],
#__example__ \t[0, 1, 0],
#__example__ \t[0, 0, 1],
#__example__ \t[1, 0, 0]
#__example__ ])
#__example__ 
#__example__ fp = m.FP(Y, T)
#__example__ print(fp) -> 1
def FP(Y:torch.Tensor, T:torch.Tensor, threshold:float = 0.5) -> int:
    """
    False positives. Expected input shape: (batch_size, num_classes)
    
    Parameters
    ----------
    Y : torch.Tensor
        Prediction
    T : torch.Tensor
        True values
    threshold : float
        All values that are greater than or equal to the threshold are considered a positive class.

    Returns
    -------
    int
        False positives
    """
    assert Y.shape == T.shape, f'Expected Y and T to have the same shape.'
    assert torch.all(Y >= 0) and torch.all(Y <= 1), f'Expected 0 <= Y <= 1'
    assert torch.all(T >= 0) and torch.all(T <= 1), f'Expected 0 <= T <= 1'
    assert len(T.shape) == 2, f'Expected shape (batch_size, num_classes), but got shape of {T.shape}'
    
    Y_pos = Y >= threshold
    T_neg = T < threshold

    mask = torch.bitwise_and(Y_pos, T_neg)
    fp = mask.sum().item()
    return fp

#__example__ #import rsp.ml.metrics as m
#__example__ #import torch
#__example__ 
#__example__ Y = torch.tensor([
#__example__ \t[0.1, 0.1, 0.8],
#__example__ \t[0.03, 0.95, 0.02],
#__example__ \t[0.05, 0.9, 0.05],
#__example__ \t[0.01, 0.87, 0.12],
#__example__ \t[0.04, 0.03, 0.93],
#__example__ \t[0.94, 0.02, 0.06]
#__example__ ])
#__example__ T = torch.tensor([
#__example__ \t[0, 0, 1],
#__example__ \t[1, 0, 0],
#__example__ \t[0, 1, 0],
#__example__ \t[0, 1, 0],
#__example__ \t[0, 0, 1],
#__example__ \t[1, 0, 0]
#__example__ ])
#__example__ 
#__example__ fn = m.FN(Y, T)
#__example__ print(fn) -> 1
def FN(Y:torch.Tensor, T:torch.Tensor, threshold:float = 0.5) -> int:
    """
    False negatives. Expected input shape: (batch_size, num_classes)
    
    Parameters
    ----------
    Y : torch.Tensor
        Prediction
    T : torch.Tensor
        True values
    threshold : float
        All values that are greater than or equal to the threshold are considered a positive class.

    Returns
    -------
    int
        False negatives
    """
    assert Y.shape == T.shape, f'Expected Y and T to have the same shape.'
    assert torch.all(Y >= 0) and torch.all(Y <= 1), f'Expected 0 <= Y <= 1'
    assert torch.all(T >= 0) and torch.all(T <= 1), f'Expected 0 <= T <= 1'
    assert len(T.shape) == 2, f'Expected shape (batch_size, num_classes), but got shape of {T.shape}'
    
    Y_neg = Y < threshold
    T_pos = T >= threshold

    mask = torch.bitwise_and(Y_neg, T_pos)
    fn = mask.sum().item()
    return fn

#__example__ #import rsp.ml.metrics as m
#__example__ #import torch
#__example__ 
#__example__ Y = torch.tensor([
#__example__ \t[0.1, 0.1, 0.8],
#__example__ \t[0.03, 0.95, 0.02],
#__example__ \t[0.05, 0.9, 0.05],
#__example__ \t[0.01, 0.87, 0.12],
#__example__ \t[0.04, 0.03, 0.93],
#__example__ \t[0.94, 0.02, 0.06]
#__example__ ])
#__example__ T = torch.tensor([
#__example__ \t[0, 0, 1],
#__example__ \t[1, 0, 0],
#__example__ \t[0, 1, 0],
#__example__ \t[0, 1, 0],
#__example__ \t[0, 0, 1],
#__example__ \t[1, 0, 0]
#__example__ ])
#__example__ 
#__example__ fpr = m.FPR(Y, T)
#__example__ print(fpr) -> 0.08333333333333333
def FPR(Y:torch.Tensor, T:torch.Tensor, threshold:float = 0.5) -> float:
    """
    False positive rate. Expected input shape: (batch_size, num_classes)
    
    Parameters
    ----------
    Y : torch.Tensor
        Prediction
    T : torch.Tensor
        True values
    threshold : float
        All values that are greater than or equal to the threshold are considered a positive class.

    Returns
    -------
    float
        False positive rate
    """
    assert Y.shape == T.shape, f'Expected Y and T to have the same shape.'
    assert torch.all(Y >= 0) and torch.all(Y <= 1), f'Expected 0 <= Y <= 1'
    assert torch.all(T >= 0) and torch.all(T <= 1), f'Expected 0 <= T <= 1'
    assert len(T.shape) == 2, f'Expected shape (batch_size, num_classes), but got shape of {T.shape}'

    fp = FP(Y, T, threshold)
    tn = TN(Y, T, threshold)
    if fp + tn == 0:
        return np.nan
    fpr = fp / (fp + tn)
    return fpr

#__example__ #import rsp.ml.metrics as m
#__example__ #import torch
#__example__ 
#__example__ Y = torch.tensor([
#__example__ \t[0.1, 0.1, 0.8],
#__example__ \t[0.03, 0.95, 0.02],
#__example__ \t[0.05, 0.9, 0.05],
#__example__ \t[0.01, 0.87, 0.12],
#__example__ \t[0.04, 0.03, 0.93],
#__example__ \t[0.94, 0.02, 0.06]
#__example__ ])
#__example__ T = torch.tensor([
#__example__ \t[0, 0, 1],
#__example__ \t[1, 0, 0],
#__example__ \t[0, 1, 0],
#__example__ \t[0, 1, 0],
#__example__ \t[0, 0, 1],
#__example__ \t[1, 0, 0]
#__example__ ])
#__example__ 
#__example__ tpr = m.TPR(Y, T)
#__example__ print(tpr) -> 0.8333333333333334
def TPR(Y:torch.Tensor, T:torch.Tensor, threshold:float = 0.5) -> float:
    """
    True positive rate. Expected input shape: (batch_size, num_classes)
    
    Parameters
    ----------
    Y : torch.Tensor
        Prediction
    T : torch.Tensor
        True values
    threshold : float
        All values that are greater than or equal to the threshold are considered a positive class.

    Returns
    -------
    float
        True positive rate
    """
    assert Y.shape == T.shape, f'Expected Y and T to have the same shape.'
    assert torch.all(Y >= 0) and torch.all(Y <= 1), f'Expected 0 <= Y <= 1'
    assert torch.all(T >= 0) and torch.all(T <= 1), f'Expected 0 <= T <= 1'
    assert len(T.shape) == 2, f'Expected shape (batch_size, num_classes), but got shape of {T.shape}'

    tp = TP(Y, T, threshold)
    fn = FN(Y, T, threshold)
    if tp + fn == 0:
        return np.nan
    tpr = tp / (tp + fn)
    return tpr

#__example__ #import rsp.ml.metrics as m
#__example__ #import torch
#__example__ 
#__example__ Y = torch.tensor([
#__example__ \t[0.1, 0.1, 0.8],
#__example__ \t[0.03, 0.95, 0.02],
#__example__ \t[0.05, 0.9, 0.05],
#__example__ \t[0.01, 0.87, 0.12],
#__example__ \t[0.04, 0.03, 0.93],
#__example__ \t[0.94, 0.02, 0.06]
#__example__ ])
#__example__ T = torch.tensor([
#__example__ \t[0, 0, 1],
#__example__ \t[1, 0, 0],
#__example__ \t[0, 1, 0],
#__example__ \t[0, 1, 0],
#__example__ \t[0, 0, 1],
#__example__ \t[1, 0, 0]
#__example__ ])
#__example__ 
#__example__ precision = m.precision(Y, T)
#__example__ print(precision) -> 0.8333333333333334
#__equation__ $precision = \frac{TP}{TP + FP}$
def precision(Y:torch.Tensor, T:torch.Tensor, threshold:float = 0.5) -> float:
    """
    Precision. Expected input shape: (batch_size, num_classes)

    Parameters
    ----------
    Y : torch.Tensor
        Prediction
    T : torch.Tensor
        True values
    threshold : float
        All values that are greater than or equal to the threshold are considered a positive class.

    Returns
    -------
    float
        Precision
    """
    assert Y.shape == T.shape, f'Expected Y and T to have the same shape.'
    assert torch.all(Y >= 0) and torch.all(Y <= 1), f'Expected 0 <= Y <= 1'
    assert torch.all(T >= 0) and torch.all(T <= 1), f'Expected 0 <= T <= 1'
    assert len(T.shape) == 2, f'Expected shape (batch_size, num_classes), but got shape of {T.shape}'

    tp = TP(Y, T, threshold)
    fp = FP(Y, T, threshold)
    if tp + fp == 0:
        return np.nan
    prec = tp / (tp + fp)
    return prec

#__example__ #import rsp.ml.metrics as m
#__example__ #import torch
#__example__ 
#__example__ Y = torch.tensor([
#__example__ \t[0.1, 0.1, 0.8],
#__example__ \t[0.03, 0.95, 0.02],
#__example__ \t[0.05, 0.9, 0.05],
#__example__ \t[0.01, 0.87, 0.12],
#__example__ \t[0.04, 0.03, 0.93],
#__example__ \t[0.94, 0.02, 0.06]
#__example__ ])
#__example__ T = torch.tensor([
#__example__ \t[0, 0, 1],
#__example__ \t[1, 0, 0],
#__example__ \t[0, 1, 0],
#__example__ \t[0, 1, 0],
#__example__ \t[0, 0, 1],
#__example__ \t[1, 0, 0]
#__example__ ])
#__example__ 
#__example__ recall = m.recall(Y, T)
#__example__ print(recall) -> 0.8333333333333334
#__equation__ $recall = \frac{TP}{TP + FN}$
def recall(Y:torch.Tensor, T:torch.Tensor, threshold:float = 0.5) -> float:
    """
    Recall. Expected input shape: (batch_size, num_classes)

    Parameters
    ----------
    Y : torch.Tensor
        Prediction
    T : torch.Tensor
        True values
    threshold : float
        All values that are greater than or equal to the threshold are considered a positive class.

    Returns
    -------
    float
        Recall
    """
    assert Y.shape == T.shape, f'Expected Y and T to have the same shape.'
    assert torch.all(Y >= 0) and torch.all(Y <= 1), f'Expected 0 <= Y <= 1'
    assert torch.all(T >= 0) and torch.all(T <= 1), f'Expected 0 <= T <= 1'
    assert len(T.shape) == 2, f'Expected shape (batch_size, num_classes), but got shape of {T.shape}'

    tp = TP(Y, T, threshold)
    fn = FN(Y, T, threshold)
    if tp + fn == 0:
        return np.nan
    rec = tp / (tp + fn)
    return rec

#__equation__ $precision = \frac{TP}{TP + FP}$
#__equation__ $recall = \frac{TP}{TP + FN}$
#__equation__ $F_1 = \frac{2 \cdot precision \cdot recall}{precision + recall} = \frac{2 \cdot TP}{2 \cdot TP + FP + FN}$
#__example__ import rsp.ml.metrics as m\n
#__example__ Y = torch.tensor([
#__example__ \t[0.1, 0.1, 0.8],
#__example__ \t[0.03, 0.95, 0.02],
#__example__ \t[0.05, 0.9, 0.05],
#__example__ \t[0.01, 0.87, 0.12],
#__example__ \t[0.04, 0.03, 0.93],
#__example__ \t[0.94, 0.02, 0.06]
#__example__ ])
#__example__ T = torch.tensor([
#__example__ \t[0, 0, 1],
#__example__ \t[1, 0, 0],
#__example__ \t[0, 1, 0],
#__example__ \t[0, 1, 0],
#__example__ \t[0, 0, 1],
#__example__ \t[1, 0, 0]
#__example__ ])
#__example__ \nf1score = m.F1_Score(Y, T)
#__example__ \nprint(f1score) --> 0.5
def F1_Score(Y:torch.Tensor, T:torch.Tensor, threshold:float = 0.5) -> float:
    """
    F1 Score. Expected input shape: (batch_size, num_classes)

    Parameters
    ----------
    Y : torch.Tensor
        Prediction
    T : torch.Tensor
        True values
    threshold : float
        All values that are greater than or equal to the threshold are considered a positive class.

    Returns
    -------
    float
        F1 Score
    """
    # Formular

    assert Y.shape == T.shape, f'Expected Y and T to have the same shape.'
    assert torch.all(Y >= 0) and torch.all(Y <= 1), f'Expected 0 <= Y <= 1'
    assert torch.all(T >= 0) and torch.all(T <= 1), f'Expected 0 <= T <= 1'
    assert len(T.shape) == 2, f'Expected shape (batch_size, num_classes), but got shape of {T.shape}'

    tp = TP(Y, T, threshold)
    fp = FP(Y, T, threshold)
    fn = FN(Y, T, threshold)
    if tp + fp + fn == 0:
        return np.nan
    f1score = 2 * tp / (2 * tp + fp + fn)
    return f1score

#__example__ import rsp.ml.metrics as m\n
#__example__ Y = torch.tensor([
#__example__ \t[0.1, 0.1, 0.8],
#__example__ \t[0.03, 0.95, 0.02],
#__example__ \t[0.05, 0.9, 0.05],
#__example__ \t[0.01, 0.87, 0.12],
#__example__ \t[0.04, 0.03, 0.93],
#__example__ \t[0.94, 0.02, 0.06]
#__example__ ])
#__example__ T = torch.tensor([
#__example__ \t[0, 0, 1],
#__example__ \t[1, 0, 0],
#__example__ \t[0, 1, 0],
#__example__ \t[0, 1, 0],
#__example__ \t[0, 0, 1],
#__example__ \t[1, 0, 0]
#__example__ ])
#__example__ \ntop_k_accuracy = m.top_k_accuracy(Y, T, k = 3)
#__example__ \nprint(top_k_accuracy) --> 1.0
def top_k_accuracy(Y:torch.Tensor, T:torch.Tensor, k:int) -> float:
    """
    Top k accuracy. Expected input shape: (batch_size, num_classes)
    
    Parameters
    ----------
    Y : torch.Tensor
        Prediction
    T : torch.Tensor
        True values

    Returns
    -------
    float
        Top k accuracy
    """
    assert Y.shape == T.shape, f'Expected Y and T to have the same shape.'
    assert torch.all(Y >= 0) and torch.all(Y <= 1), f'Expected 0 <= Y <= 1'
    assert torch.all(T >= 0) and torch.all(T <= 1), f'Expected 0 <= T <= 1'
    assert len(T.shape) == 2, f'Expected shape (batch_size, num_classes), but got shape of {T.shape}'

    top_k_prediction = torch.argsort(Y, dim=1, descending=True)[:, :k]
    top_1_target = torch.argmax(T, dim=1)

    tp = 0
    for y, t in zip(top_k_prediction, top_1_target):
        if t in y:
            tp += 1
        pass

    acc = tp / T[:, 0].numel()
    return acc

#__example__ import rsp.ml.metrics as m\n
#__example__ Y = torch.tensor([
#__example__ \t[0.1, 0.1, 0.8],
#__example__ \t[0.03, 0.95, 0.02],
#__example__ \t[0.05, 0.9, 0.05],
#__example__ \t[0.01, 0.87, 0.12],
#__example__ \t[0.04, 0.03, 0.93],
#__example__ \t[0.94, 0.02, 0.06]
#__example__ ])
#__example__ T = torch.tensor([
#__example__ \t[0, 0, 1],
#__example__ \t[1, 0, 0],
#__example__ \t[0, 1, 0],
#__example__ \t[0, 1, 0],
#__example__ \t[0, 0, 1],
#__example__ \t[1, 0, 0]
#__example__ ])
#__example__ \ntop_1_accuracy = m.top_1_accuracy(Y, T, k = 3)
#__example__ \nprint(top_1_accuracy) --> 0.8333333333333334
def top_1_accuracy(Y:torch.Tensor, T:torch.Tensor) -> float:
    """
    Top 1 accuracy. Expected input shape: (batch_size, num_classes)
    
    Parameters
    ----------
    Y : torch.Tensor
        Prediction
    T : torch.Tensor
        True values

    Returns
    -------
    float
        Top 1 accuracy -> top k accuracy | k = 1
    """
    assert Y.shape == T.shape, f'Expected Y and T to have the same shape, but got Y.shape {Y.shape}, T.shape {T.shape}'
    assert torch.all(Y >= 0) and torch.all(Y <= 1), f'Expected 0 <= Y <= 1'
    assert torch.all(T >= 0) and torch.all(T <= 1), f'Expected 0 <= T <= 1'
    assert len(T.shape) == 2, f'Expected shape (batch_size, num_classes), but got shape of {T.shape}'

    return top_k_accuracy(Y, T, 1)

#__example__ import rsp.ml.metrics as m\n
#__example__ Y = torch.tensor([
#__example__ \t[0.1, 0.1, 0.8],
#__example__ \t[0.03, 0.95, 0.02],
#__example__ \t[0.05, 0.9, 0.05],
#__example__ \t[0.01, 0.87, 0.12],
#__example__ \t[0.04, 0.03, 0.93],
#__example__ \t[0.94, 0.02, 0.06]
#__example__ ])
#__example__ T = torch.tensor([
#__example__ \t[0, 0, 1],
#__example__ \t[1, 0, 0],
#__example__ \t[0, 1, 0],
#__example__ \t[0, 1, 0],
#__example__ \t[0, 0, 1],
#__example__ \t[1, 0, 0]
#__example__ ])
#__example__ \ntop_2_accuracy = m.top_2_accuracy(Y, T, k = 3)
#__example__ \nprint(top_2_accuracy) --> 1.0
def top_2_accuracy(Y:torch.Tensor, T:torch.Tensor) -> float:
    """
    Top 2 accuracy. Expected input shape: (batch_size, num_classes)
    
    Parameters
    ----------
    Y : torch.Tensor
        Prediction
    T : torch.Tensor
        True values

    Returns
    -------
    float
        Top 2 accuracy -> top k accuracy | k = 2
    """
    assert Y.shape == T.shape, f'Expected Y and T to have the same shape.'
    assert torch.all(Y >= 0) and torch.all(Y <= 1), f'Expected 0 <= Y <= 1'
    assert torch.all(T >= 0) and torch.all(T <= 1), f'Expected 0 <= T <= 1'
    assert len(T.shape) == 2, f'Expected shape (batch_size, num_classes), but got shape of {T.shape}'

    return top_k_accuracy(Y, T, 2)

#__example__ import rsp.ml.metrics as m\n
#__example__ Y = torch.tensor([
#__example__ \t[0.1, 0.1, 0.8],
#__example__ \t[0.03, 0.95, 0.02],
#__example__ \t[0.05, 0.9, 0.05],
#__example__ \t[0.01, 0.87, 0.12],
#__example__ \t[0.04, 0.03, 0.93],
#__example__ \t[0.94, 0.02, 0.06]
#__example__ ])
#__example__ T = torch.tensor([
#__example__ \t[0, 0, 1],
#__example__ \t[1, 0, 0],
#__example__ \t[0, 1, 0],
#__example__ \t[0, 1, 0],
#__example__ \t[0, 0, 1],
#__example__ \t[1, 0, 0]
#__example__ ])
#__example__ \ntop_3_accuracy = m.top_3_accuracy(Y, T, k = 3)
#__example__ \nprint(top_3_accuracy) --> 1.0
def top_3_accuracy(Y:torch.Tensor, T:torch.Tensor) -> float:
    """
    Top 3 accuracy. Expected input shape: (batch_size, num_classes)
    
    Parameters
    ----------
    Y : torch.Tensor
        Prediction
    T : torch.Tensor
        True values

    Returns
    -------
    float
        Top 3 accuracy -> top k accuracy | k = 3
    """
    assert Y.shape == T.shape, f'Expected Y and T to have the same shape.'
    assert torch.all(Y >= 0) and torch.all(Y <= 1), f'Expected 0 <= Y <= 1'
    assert torch.all(T >= 0) and torch.all(T <= 1), f'Expected 0 <= T <= 1'
    assert len(T.shape) == 2, f'Expected shape (batch_size, num_classes), but got shape of {T.shape}'

    return top_k_accuracy(Y, T, 3)

#__example__ import rsp.ml.metrics as m\n
#__example__ Y = torch.tensor([
#__example__ \t[0.1, 0.1, 0.8],
#__example__ \t[0.03, 0.95, 0.02],
#__example__ \t[0.05, 0.9, 0.05],
#__example__ \t[0.01, 0.87, 0.12],
#__example__ \t[0.04, 0.03, 0.93],
#__example__ \t[0.94, 0.02, 0.06]
#__example__ ])
#__example__ T = torch.tensor([
#__example__ \t[0, 0, 1],
#__example__ \t[1, 0, 0],
#__example__ \t[0, 1, 0],
#__example__ \t[0, 1, 0],
#__example__ \t[0, 0, 1],
#__example__ \t[1, 0, 0]
#__example__ ])
#__example__ \ntop_5_accuracy = m.top_5_accuracy(Y, T, k = 3)
#__example__ \nprint(top_5_accuracy) --> 1.0
def top_5_accuracy(Y:torch.Tensor, T:torch.Tensor) -> float:
    """
    Top 5 accuracy. Expected input shape: (batch_size, num_classes)
    
    Parameters
    ----------
    Y : torch.Tensor
        Prediction
    T : torch.Tensor
        True values

    Returns
    -------
    float
        Top 5 accuracy -> top k accuracy | k = 5
    """
    assert Y.shape == T.shape, f'Expected Y and T to have the same shape.'
    assert torch.all(Y >= 0) and torch.all(Y <= 1), f'Expected 0 <= Y <= 1'
    assert torch.all(T >= 0) and torch.all(T <= 1), f'Expected 0 <= T <= 1'
    assert len(T.shape) == 2, f'Expected shape (batch_size, num_classes), but got shape of {T.shape}'

    return top_k_accuracy(Y, T, 5)

#__example__ import rsp.ml.metrics as m\n
#__example__ Y = torch.tensor([
#__example__ \t[0.1, 0.1, 0.8],
#__example__ \t[0.03, 0.95, 0.02],
#__example__ \t[0.05, 0.9, 0.05],
#__example__ \t[0.01, 0.87, 0.12],
#__example__ \t[0.04, 0.03, 0.93],
#__example__ \t[0.94, 0.02, 0.06]
#__example__ ])
#__example__ T = torch.tensor([
#__example__ \t[0, 0, 1],
#__example__ \t[1, 0, 0],
#__example__ \t[0, 1, 0],
#__example__ \t[0, 1, 0],
#__example__ \t[0, 0, 1],
#__example__ \t[1, 0, 0]
#__example__ ])
#__example__ \ntop_10_accuracy = m.top_10_accuracy(Y, T, k = 3)
#__example__ \nprint(top_10_accuracy) --> 1.0
def top_10_accuracy(Y:torch.Tensor, T:torch.Tensor) -> float:
    """
    Top 10 accuracy. Expected input shape: (batch_size, num_classes)
    
    Parameters
    ----------
    Y : torch.Tensor
        Prediction
    T : torch.Tensor
        True values

    Returns
    -------
    float
        Top 10 accuracy -> top k accuracy | k = 10
    """
    assert Y.shape == T.shape, f'Expected Y and T to have the same shape.'
    assert torch.all(Y >= 0) and torch.all(Y <= 1), f'Expected 0 <= Y <= 1'
    assert torch.all(T >= 0) and torch.all(T <= 1), f'Expected 0 <= T <= 1'
    assert len(T.shape) == 2, f'Expected shape (batch_size, num_classes), but got shape of {T.shape}'

    return top_k_accuracy(Y, T, 10)

#__image__ ![](documentation/image/confusion_matrix.jpg)
def plot_confusion_matrix(
        confusion_matrix:torch.Tensor,
        labels:List[str] = None,
        cmap:str = 'Blues',
        xlabel:str = 'Predicted label',
        ylabel:str = 'True label',
        title:str = 'Confusion Matrix',
        plt_show:bool = False,
        save_file_name:str = None) -> np.array:
    """
    Plot the confusion matrix
    
    Parameters
    ----------
    confusion_matrix : torch.Tensor
        Confusion matrix
    labels : str, optional, default = None
        Class labels -> automatic labeling C000, ..., CXXX if labels is None
    cmap : str, optional, default = 'Blues'
        Seaborn cmap, see https://r02b.github.io/seaborn_palettes/
    xlabel : str, optional, default = 'Predicted label'
        X-Axis label
    ylabel : str, optional, default = 'True label'
        Y-Axis label
    title : str, optional, default = 'Confusion Matrix'
        Title of the plot
    plt_show : bool, optional, default = False
        Set to True to show the plot
    save_file_name : str, optional, default = None
        If not None, the plot is saved under the specified save_file_name.

    Returns
    -------
    np.array
        Image of the confusion matrix
    """
    # test
    if labels is None:
        labels = [f'Class {i+1}' for i in range(confusion_matrix.shape[0])]

    df_cm = pd.DataFrame(confusion_matrix, index = [i for i in labels],
                  columns = [i for i in labels])
    fig = plt.figure(figsize = (10,7))

    sn.heatmap(df_cm, annot=len(labels) <= 20, cmap=cmap, fmt='g')
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0, ha="right")
    if title is not None:
        plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if plt_show:
        plt.show()

    fig.canvas.draw()

    s, (width, height) = fig.canvas.print_to_buffer()

    # Option 2a: Convert to a NumPy array.
    img = np.fromstring(s, np.uint8).reshape((height, width, 4))
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    if save_file_name is not None:
        cv.imwrite(save_file_name, img)

    plt.close()

    return img

#__example__ import rsp.ml.metrics as m
#__example__ import torch
#__example__ import torch.nn.functional as F
#__example__ 
#__example__ num_elements = 100000
#__example__ num_classes = 7
#__example__ 
#__example__ T = []
#__example__ for i in range(num_elements):
#__example__ \ttrue_class = torch.randint(0, num_classes, (1,))
#__example__ \tt = F.one_hot(true_class, num_classes=num_classes)
#__example__ \tT.append(t)
#__example__ T = torch.cat(T)
#__example__ 
#__example__ dist = torch.normal(T.float(), 1.5)
#__example__ Y = F.softmax(dist, dim = 1)
#__example__ FPRs, TPRs = m.ROC(Y, T)
def ROC(Y:torch.Tensor, T:torch.Tensor, num_thresholds:int = 100):
    """
    Calculates the receiver operating characteristic: computes False Positive Rates and True positive Rates for `num_thresholds` aligned between 0 and 1

    Parameters
    ----------
    Y : torch.Tensor
        Prediction
    T : torch.Tensor
        True values
    num_thresholds : int, default = 100
        Number of thresholds to compute.
    
    Returns
    -------
    (List[float], List[float])
        (False Positive Rates, True Positive Rates) for 100 different thresholds
    """
    FPRs = []
    TPRs = []
    thresholds = np.linspace(0, 1 + 1 / num_thresholds, num_thresholds)**2
    for threshold in thresholds:
        fpr = FPR(Y, T, threshold)
        tpr = TPR(Y, T, threshold)
        FPRs.append(fpr)
        TPRs.append(tpr)

    FPRs = np.array(FPRs)
    TPRs = np.array(TPRs)
    indices = np.argsort(FPRs)
    FPRs = FPRs[indices]
    TPRs = TPRs[indices]
    return FPRs, TPRs

#__image__ ![](documentation/image/ROC_AUC.jpg)
def plot_ROC(
        Y:torch.Tensor,
        T:torch.Tensor, 
        num_thresholds:int = 100,
        title:str = 'ROC Curve',
        class_curves:bool = False,
        labels:List[str] = None,
        plt_show:bool = False,
        save_file_name:str = None) -> np.array:
    """
    Plot the receiver operating characteristic.
    
    Parameters
    ----------
    Y : torch.Tensor
        Prediction
    T : torch.Tensor
        True values
    num_thresholds : int, default = 100
        Number of thresholds to compute.
    title : str, optional, default = 'Confusion Matrix'
        Title of the plot
    class_curves : bool, default = False
        Plot ROC curve for each class
    labels : str, optional, default = None
        Class labels -> automatic labeling C000, ..., CXXX if labels is None
    plt_show : bool, optional, default = False
        Set to True to show the plot
    save_file_name : str, optional, default = None
        If not None, the plot is saved under the specified save_file_name.

    Returns
    -------
    np.array
        Image of the confusion matrix
    """
    fig = plt.figure(figsize = (10, 7))

    if title is not None:
        plt.title(title)

    if class_curves:
        cmap = plt.get_cmap('Pastel1')
        colors = cmap(np.linspace(0, 1, T.shape[1]))
        
        class_data = {}
        for i in range(T.shape[1]):
            class_data[i] = [], []
        for y, t in zip(Y, T):
            c = torch.argmax(t, dim = 0).item()

            class_data[c][0].append(y)
            class_data[c][1].append(t)
        for c in class_data:
            Y_c, T_c = class_data[c]
            if len(Y_c) == 0:
                continue
            Y_c = torch.stack(Y_c, dim = 0)
            T_c = torch.stack(T_c, dim = 0)
            FPRs, TPRs = ROC(Y_c, T_c, num_thresholds)
            roc_auc_c = AUROC(Y_c, T_c, num_thresholds)
            if labels is None:
                class_str = f'C{c:0>3}'
            else:
                class_str = labels[c]
            label_str = '$AUROC_{' + class_str + '} = ' + f'{roc_auc_c:0.4f}' + '$'
            plt.plot(FPRs, TPRs, label=label_str, linewidth = 1, color = colors[c])

    FPRs, TPRs = ROC(Y, T, num_thresholds)
    roc_auc = AUROC(Y, T, num_thresholds)
    label_str = '$ROC\,AUC_ = ' + f'{roc_auc:0.4f}' + '$'
    plt.plot(FPRs, TPRs, label = label_str, linewidth=1.2)
    plt.fill_between(FPRs, TPRs, 0, alpha = 0.2)

    plt.plot([0, 1], [0, 1], linestyle = ':', color='gray', alpha = 0.8)

    plt.xlim(0, 1)
    plt.ylim(0, 1)

    plt.minorticks_on()
    plt.grid(which='minor', color='lightgray', linewidth=0.2)
    plt.grid(which='major', linewidth=.6)

    plt.xlabel('FPR')
    plt.ylabel('TPR')

    plt.legend()

    
    #plt.text(0.82, 1.02, f'ROC AUC = {roc_auc:0.4f}')

    if plt_show:
        plt.show()

    fig.canvas.draw()

    s, (width, height) = fig.canvas.print_to_buffer()

    # Option 2a: Convert to a NumPy array.
    img = np.fromstring(s, np.uint8).reshape((height, width, 4))
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    plt.close()

    if save_file_name is not None:
        cv.imwrite(save_file_name, img)

    return img

def AUROC(Y:torch.Tensor, T:torch.Tensor, num_thresholds:int = 100):
    """
    Calculates the Area under the Receiver Operation Chracteristic Curve.
    
    Parameters
    ----------
    Y : torch.Tensor
        Prediction
    T : torch.Tensor
        True values
    num_thresholds : int, default = 100
        Number of thresholds to compute.

    Returns
    -------
    float
        Receiver Operation Chracteristic Area under the Curve
    """
    FPRs, TPRs = ROC(Y, T, num_thresholds)

    roc_auc = 0.

    last_fpr = 0
    i = 0
    while i < len(FPRs):
        while FPRs[i] == last_fpr:
            i += 1
            if i == len(FPRs):
                break
        if i == len(FPRs):
            break

        if np.isnan(TPRs[i]):
            last_fpr = FPRs[i]
            continue

        diff = TPRs[i] * (FPRs[i] - last_fpr)
        if np.isnan(diff):
            i+= 1
            continue

        roc_auc += diff
        
        
        last_fpr = FPRs[i]
        last_tpr = TPRs[i]
        
        i += 1

    return roc_auc

if __name__ == '__main__':
    Y = torch.tensor([
        [0.1, 0.1, 0.8],
        [0.03, 0.95, 0.02],
        [0.05, 0.9, 0.05],
        [0.01, 0.87, 0.12],
        [0.04, 0.03, 0.93],
        [0.94, 0.02, 0.06]
    ])
    T = torch.tensor([
        [0, 0, 1],
        [1, 0, 0],
        [0, 1, 0],
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 0]
    ])

    conf_mat = confusion_matrix(Y, T)
    print(conf_mat)

    tp = TP(Y, T)
    tn = TN(Y, T)
    fp = FP(Y, T)
    fn = FN(Y, T)

    fpr = FPR(Y, T)
    tpr = TPR(Y, T)

    prec = precision(Y, T)
    rec = recall(Y, T)

    t1a = top_1_accuracy(Y, T)
    t1a = top_1_accuracy(Y, T)

    f1 = F1_Score(Y, T)

    # confusion matrix
    epsilon = 0.2
    num_elements = 10000
    num_classes = 7

    T = []
    for i in range(num_elements):
        true_class = torch.randint(0, num_classes, (1,))
        t = F.one_hot(true_class, num_classes=num_classes)
        T.append(t)
    T = torch.cat(T)

    dist = torch.normal(T.float(), 0.5)
    Y = torch.argmax(dist, dim=1)
    Y = F.one_hot(Y, num_classes=num_classes)

    conf_m = confusion_matrix(Y, T)
    print(conf_m)

    labels = []
    for a in range(num_classes):
        a_str = str(a)
        while len(a_str) < 3:
            a_str = '0' + a_str
        a_str = 'A' + a_str
        labels.append(a_str)

    img = plot_confusion_matrix(conf_m, labels=labels, plt_show=False)
    cv.imwrite('documentation/image/confusion_matrix.jpg', img)

    # ROC AUC
    num_elements = 100000
    num_classes = 7

    T = []
    for i in range(num_elements):
        true_class = torch.randint(0, num_classes, (1,))
        t = F.one_hot(true_class, num_classes=num_classes)
        T.append(t)
    T = torch.cat(T)

    dist = torch.normal(T.float(), 1.5)
    Y = F.softmax(dist, dim = 1)
    #Y = F.sigmoid(dist)

    img = plot_ROC(Y, T, save_file_name='ROC_AUC.jpg', class_curves=True)
    cv.imshow('ROC', img)
    cv.waitKey()
    pass