# Created by Cees Dekker Lab at the Delft University of Technology
# Refactored by Thijn Hoekstra

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from varv.preprocessing import cpic

def plot_steps(steps: pd.DataFrame,
               x_range: tuple = None,
               fig: plt.Figure = None,
               ax: plt.Axes = None,
               color='black',
               line_at_step=True,
               **kwargs) -> tuple:


    if fig is None and ax is None:
        fig, ax = plt.subplots(figsize=(12, 4))

    values = steps['mean']
    std = steps['std']

    edges = steps['start_idx']
    edges = np.concatenate([edges, [steps['end_idx'][len(steps) - 1]]])

    if x_range:
        assert len(x_range) == 2
        edges = np.interp(edges, (edges.min(), edges.max()), x_range)

    if line_at_step:
        for edge in edges:
            ax.axvline(edge, color=color, alpha=0.1, linestyle='dashed')

    ax.stairs(values + std, edges, baseline=values - std, fill=True,
              color=color, alpha=0.2, **kwargs)
    ax.stairs(values, edges, baseline=None, color=color, **kwargs)

    return fig, ax


def _find_transitions(x, xsq, left, right, min_level_length, cpic_multiplier):
    transitions = []
    N_T = right - left + 1
    N_L = np.arange(min_level_length, N_T - min_level_length + 1, dtype=int)
    N_R = N_T - N_L

    if N_T < 2 * min_level_length:
        return transitions


    CPIC = calculate_cpic(N_L, N_R, N_T, cpic_multiplier, left, right, x, xsq)

    min_CPIC_index = np.argmin(CPIC)
    min_index = min_CPIC_index + min_level_length + left - 1

    if CPIC[min_CPIC_index] < 0:
        transitions = ([min_index]
                       + _find_transitions(x, xsq, left, min_index,
                                           min_level_length, cpic_multiplier)
                       + _find_transitions(x, xsq, min_index + 1, right,
                                           min_level_length, cpic_multiplier))

    return transitions


def step_finder(data: np.ndarray, sensitivity: float = 1,
                min_level_length: int = 2,
                return_errors = False,
                return_stiffnesses = False) -> tuple:
    original_data_mapping = np.arange(len(data))
    data_length = len(data)
    original_data_mapping = original_data_mapping[~np.isnan(data)]
    data = data[~np.isnan(data)]

    cpic_multiplier = sensitivity
    min_level_length = min_level_length

    x = np.concatenate((np.zeros(1), np.cumsum(data)))
    xsq = np.concatenate((np.zeros(1), np.cumsum(data ** 2)))

    transitions = sorted(
        _find_transitions(x, xsq, 1, len(data), min_level_length,
                          cpic_multiplier))
    transitions = [t for t in transitions
                   if min_level_length < t < len(data) - min_level_length]
    transitions_with_ends = [0] + transitions + [len(data)]

    some_change = True
    while some_change:
        some_change = False
        transition_CPIC = -np.inf * np.ones(len(transitions_with_ends))

        for i in range(1, len(transitions_with_ends) - 1):
            left = max(transitions_with_ends[i - 1], 1)
            right = transitions_with_ends[i + 1]

            N_T = right - left + 1
            N_L = transitions_with_ends[i] - left + 1
            N_R = right - transitions_with_ends[i]

            if N_T < 2 * min_level_length:
                continue

            transition_CPIC[i] = calculate_cpic(N_L, N_R, N_T, cpic_multiplier, left, right,
                                  x, xsq)

        max_CPIC_index = np.argmax(transition_CPIC)
        if transition_CPIC[max_CPIC_index] > 0:
            transitions_with_ends.pop(max_CPIC_index)
            some_change = True

    features = np.zeros((2, len(transitions_with_ends) - 1))

    if return_errors:
        errors = np.zeros((2, len(transitions_with_ends) - 1))
    else:
        errors = None

    if return_stiffnesses:
        stiffnesses = [None] * (len(transitions_with_ends) - 1)
    else:
        stiffnesses = None

    for ct in range(1, len(transitions_with_ends)):
        features[:, ct - 1] = [np.median(
            data[transitions_with_ends[ct - 1]:transitions_with_ends[ct]]),
            np.std(data[transitions_with_ends[ct - 1]:
                        transitions_with_ends[ct]])]

        if return_errors:
            errors[:, ct - 1] = [features[1, ct - 1] / np.sqrt(
                transitions_with_ends[ct] - transitions_with_ends[ct - 1] - 1),
                                 features[1, ct - 1] / np.sqrt(2 * (
                                         transitions_with_ends[ct] -
                                         transitions_with_ends[ct - 1] - 1))]

        if return_stiffnesses:
            stiffnesses[ct - 1] = np.diag(errors[:, ct - 1] ** -2)

    transitions = [0] + [original_data_mapping[t] for t in
                         transitions_with_ends[1:-1]] + [data_length]

    return np.array(transitions), np.array(features), errors, stiffnesses


def calculate_cpic(N_L, N_R, N_T, cpic_multiplier, left, right, x, xsq):
    x_mean_L, x_mean_R, x_mean_T = get_means(N_L, N_R, N_T, left, right, x)

    xsq_mean_L, xsq_mean_R, xsq_mean_T = get_means(N_L, N_R, N_T, left, right, xsq)

    var_L = np.maximum(xsq_mean_L - x_mean_L ** 2, 0.0003)
    var_R = np.maximum(xsq_mean_R - x_mean_R ** 2, 0.0003)
    var_T = np.maximum(xsq_mean_T - x_mean_T ** 2, 0.0003)

    if N_T >= 1e6:
        p_cpic = cpic.cpic_greater_than_1000(1e6)
    elif N_T > 1000 and N_T < 1e6:
        p_cpic = cpic.cpic_greater_than_1000(N_T)
    else:
        p_cpic = cpic.cpic_less_than_1000(N_T)

    return 0.5 * (N_L * np.log(var_L) + N_R * np.log(
        var_R) - N_T * np.log(
        var_T)) + 1 + cpic_multiplier * p_cpic


def get_means(n_l, n_r, n_t, left, right, x):
    x_mean_L = (x[left + n_l - 1] - x[left - 1]) / n_l
    x_mean_R = (x[right] - x[right - n_r]) / n_r
    x_mean_T = (x[right] - x[left - 1]) / n_t
    return x_mean_L, x_mean_R, x_mean_T


def format_steps_df(transitions, features, errors, stiffnesses, sfreq):
    steps_df = pd.DataFrame({
        "start_idx": transitions[:-1],
        "end_idx": transitions[1:],
    })
    steps_df["n_pts"] = steps_df["end_idx"] - steps_df["start_idx"]
    steps_df["dwell_time_s"] = steps_df["n_pts"] / sfreq
    steps_df["mean"] = features[0, :]
    steps_df["std"] = features[1, :]

    return steps_df
