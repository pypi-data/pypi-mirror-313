from __future__ import annotations

import warnings
from sys import float_info

import numpy as np
import pandas as pd

eps = float_info.epsilon


def compute_tr(damage_index: np.ndarray | pd.Series, threshold: float) -> float:
    """
    Compute the Trigger Rate (TPR/FPR) given anomaly scores and a threshold.

    Parameters:
    - damage_index (array-like): Anomaly index scores.
    - threshold (float): Threshold above which scores are considered anomalies.

    Returns:
    - float: Trigger Rate.
    """
    if isinstance(damage_index, pd.Series):
        damage_index = damage_index.values
    if isinstance(damage_index, list):
        damage_index = np.array(damage_index)

    return np.sum(damage_index > threshold) / len(damage_index)


def mean_ratio(
    damage_index_healthy: np.ndarray | pd.Series,
    damage_index_damaged: np.ndarray | pd.Series,
) -> float:
    """
    Compute the mean ratio of anomaly scores between healthy and damaged states.

    Parameters:
    - damage_index_healthy (array-like): Anomaly index scores for healthy state.
    - damage_indexs_damaged (array-like): Anomaly index scores for damaged state.

    Returns:
    - float: Mean ratio of anomaly scores.
    """
    if isinstance(damage_index_healthy, pd.Series):
        damage_index_healthy = damage_index_healthy.values
    if isinstance(damage_index_damaged, pd.Series):
        damage_index_damaged = damage_index_damaged.values

    if isinstance(damage_index_healthy, list):
        damage_index_healthy = np.array(damage_index_healthy)
    if isinstance(damage_index_damaged, list):
        damage_index_damaged = np.array(damage_index_damaged)

    # Compute the range of healthy scores
    range_healthy = np.max(damage_index_healthy) - np.min(damage_index_healthy)

    # Handle zero range by raising a warning and using a range of 1
    if range_healthy == 0:
        warnings.warn(
            "Range of healthy anomaly scores is 0. Using a fallback range of 1.",
            UserWarning,
        )
        range_healthy = 1

    # Compute the mean ratio
    res = (
        np.mean(damage_index_damaged)
        / (np.mean(damage_index_healthy) + eps)
        / (range_healthy + eps)
    )
    return res
