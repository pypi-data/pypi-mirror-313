# Created by Henry Brinkerhoff
# Written for Python by Thijn Hoekstra

"""Change point detection

"""
import re
import typing
from importlib import resources as impresources

import scipy
import numpy as np
import pandas as pd

from varv import utils
from varv.preprocessing import assets, cpic, capcomp, dimreduction

COV_VEC_FORMAT = "Sigma_{}"

AMPS_FORMAT = "x_{}"

inp_file_level_finding = impresources.files(
    assets) / 'principal_components_for_level_finding.npy'

BASIS_FNS_LEVEL_FINDING = np.load(inp_file_level_finding)



def get_bias_period_and_phase(v_data: np.ndarray,
                              max_length_to_check: int = 10000,
                              verbose=False) -> tuple:
    """

    Gets the bias frequency period in samples and its phase from samples
    without the need for knowing the bias frequency *a priori*. Assumes that
    the bias frequency is the frequency in the signal with the largest
    amplitude.

    Args:
        v_data (np.ndarray): A numpy array containing the time series of bias
            voltage.
        max_length_to_check (int): Maximum number of samples in which to find a
            period and phase. Defaults to 10,000 samples. Speeds up Fourier
            transform.
        verbose (bool): Whether to print information on the found frequency.
            Defaults to False.

    Returns:
        A tuple containing the period and the phase of the most prominent
        frequency in the signal.

    """
    # Find the phase from the voltage assets
    N = min(max_length_to_check, len(v_data))

    y = v_data[:N]
    yf = scipy.fft.fft(y)[:N // 2]
    xf = scipy.fft.fftfreq(N)[:N // 2]
    idx = np.argmax(np.abs(yf)[1:]) + 1  # Skip DC component
    fourier_component = yf[idx]

    period = round(1 / xf[idx])

    if verbose:
        print(f'Found a frequency component with a period of '
              f'{period} samples.')

    if np.abs(fourier_component) < np.mean(np.abs(yf)):
        raise ValueError(
            f'No AC voltage applied in first {N} points of file - could not '
            f'determine phase.')

    phase = utils.get_phase_from_fourier_component(fourier_component, period)
    return period, phase


def find_levels_pc(i_data: np.ndarray, vdata: np.ndarray,
                   period: int,
                   basis_fns: np.ndarray = None,
                   num_basis_fns: int = 5,
                   sensitivity: float = 1.0, verbose=False) -> np.ndarray:
    """
    Finds step transitions in a time series using a combination of basis
    functions and statistical fitting.

    Args:
        i_data (np.ndarray): A numpy array containing the time series of ionic
            current.
        vdata (np.ndarray): A numpy array containing the time series of bias
            voltage.
        period (int): Period of the bias frequency in samples.
        basis_fns (np.ndarray): An (M, N) numpy array containing N 1D basis
            functions of length M that describe the signal in between steps.
        sensitivity (float, optional): Sensitivity of the step finder. Default
            is 1.0.

    Returns:
        np.ndarray: An array of indices where the transitions occur.


    TODO: Allow for variable period size.
    """

    assert isinstance(period, int)

    if basis_fns is None:
        basis_fns = BASIS_FNS_LEVEL_FINDING[:, :num_basis_fns]  # First 5 Bfs

    # define the number determining level finder sensitivity
    cpic_multiplier = 4 * sensitivity

    # the shortest level length allowed. Equal to the period
    min_level_length = period

    # The number of basis functions
    num_bf = basis_fns.shape[1]

    phase = utils.get_phase_of_period(vdata, period)
    if verbose:
        print(f'Found frequency with period {period} with a phase {phase}.')

    # Remove spikes. TODO: figure out how this works.
    original_length = len(i_data)  # Length of original arrays
    delete_x = np.arange(phase - period, original_length, period // 2)
    delete_x = delete_x.reshape((len(delete_x), 1))
    delete_y = np.arange(21)
    pts_to_delete = delete_x + delete_y  # Using NumPy broadcasting
    pts_to_delete = pts_to_delete.flatten()
    pts_to_delete = pts_to_delete[(pts_to_delete >= 1) & (pts_to_delete <= original_length)]
    original_indices = np.arange(original_length)
    i_data = np.delete(i_data, pts_to_delete)
    original_indices = np.delete(original_indices, pts_to_delete)
    period = period - 42
    phase = phase - np.sum(pts_to_delete < phase)

    if verbose:
        print('Removed spikes.')

    # Call the recursive level finding function

    N = len(i_data)

    x = np.concatenate([np.zeros(1), i_data])
    t = np.arange(-1, N)

    # define basis functions
    bf = add_phase_to_bf(basis_fns.T, phase)
    bf = tile_bf_to_match_signal(bf, len(t))

    if verbose:
        print('Generating cumulative sums...', end='')
    BB, XB, Xsq = get_cumulative_sums(bf, num_bf, x)
    if verbose:
        print('Done!\nFinding transitions...', end='')

    transition_list = find_transitions(1, len(x) - 1,
                                       Xsq, XB, BB,
                                       min_level_length,
                                       cpic_multiplier,
                                       num_bf)

    if verbose:
        print('Done!')

    transitions = np.sort(np.unique(transition_list)) - 1
    transitions_with_ends = np.concatenate(
        [[0], transitions, [len(i_data)]])

    some_change = True

    while some_change:
        some_change = False

        transition_cpic = np.full(len(transitions_with_ends), -np.inf)

        for i in range(1, len(transitions_with_ends) - 2):

            #  score the transition.
            left = max(transitions_with_ends[i - 1], 1)
            right = transitions_with_ends[i + 1]

            N_T = right - left + 1
            N_L = transitions_with_ends[i] - left + 1
            N_R = right - transitions_with_ends[i]

            B_matrix_L = BB[:, left + N_L - 1] - BB[:, left - 1]
            B_matrix_R = BB[:, right] - BB[:, right - N_R]
            B_matrix_T = BB[:, right] - BB[:, left - 1]

            XB_L = XB[:, left + N_L - 1] - XB[:, left - 1]
            XB_R = XB[:, right] - XB[:, right - N_R]
            XB_T = XB[:, right] - XB[:, left - 1]

            Xsq_L = Xsq[left + N_L - 1] - Xsq[left - 1]
            Xsq_R = Xsq[right] - Xsq[right - N_R]
            Xsq_T = Xsq[right] - Xsq[left - 1]

            var_L = get_var_value(num_bf, N_L, B_matrix_L, XB_L, Xsq_L)
            var_R = get_var_value(num_bf, N_R, B_matrix_R, XB_R, Xsq_R)
            var_T = get_var_value(num_bf, N_T, B_matrix_T, XB_T, Xsq_T)

            p_cpic = cpic.get_cpic_penalty(N_T)

            transition_cpic[i] = get_cpic(N_L, N_R, N_T,
                     var_L, var_R, var_T,
                     cpic_multiplier, num_bf, p_cpic)

        max_cpic = np.max(transition_cpic)
        wheremax = np.argmax(transition_cpic)

        if max_cpic > 0:
            transitions_with_ends = np.delete(transitions_with_ends, wheremax)
            some_change = True

    if not len(transitions_with_ends[1:-1]):
        raise ValueError("Cannot find steps in data. Try adjusting sensitivity.")

    # Append 0 and the end
    transitions = np.concatenate(
        [np.zeros(1), original_indices[transitions_with_ends[1:-1]], [original_length]])
    return transitions.astype(np.int64)


def get_cumulative_sums(bf: np.ndarray, num_bf: int, x: np.ndarray) -> tuple:
    """Gets necessary cumulates

    Args:
        bf:
        num_bf:
        x:

    Returns:

    """
    # cumulate of x^2
    Xsq = np.cumsum(x ** 2)

    # Vector of cumulates of x*b_i
    XB = np.cumsum(np.tile(x, (len(bf), 1)) * bf, axis=1)

    # matrix of cumulates of b_i*b_j, the cumulate for each entry of the matrix
    # is a row of BB
    BB = np.zeros((num_bf ** 2, len(x)))
    for cbf in range(num_bf):
        BB[cbf * num_bf:(cbf + 1) * num_bf, :] = np.cumsum(
            np.tile(bf[cbf, :], (num_bf, 1)) * bf, axis=1)
    return BB, XB, Xsq


def tile_bf_to_match_signal(bf: np.ndarray, n: int) -> np.ndarray:
    """Repeats the basis functions.

    Tiles the basis functions so as to lengthen the array to a length equal
    to the current arrays.

    Args:
        bf (np.ndarray): An array containing the basis functions.
        n (int): The length of the current arrays.

    Returns:
        np.ndarray: An array containing repats of the basis functions that
            matches the length of the ionic current arrays.

    """
    return np.tile(bf, (1, (n // bf.shape[0]) + 1))[:, :n]


def add_phase_to_bf(basis_fns: np.ndarray, phase: int,
                    seg: int = 0) -> np.ndarray:
    """Applies a phase shift to the basis functions.

    Shifts the basis functions by a certain phase so that they are corrected
    for the phase of the signal.

    Args:
        basis_fns (np.ndarray): An array containing the basis functions.
        phase (int): Phase shift of the current and voltage arrays in samples.
            Phase is zero corresponds to the voltage rising exactly at the
            first sample.
        seg: Reference point for phase. Defaults to zero. Not used. Originally
            used for dealing with arrays chunks.

    Returns:
        np.ndarray: The basis functions array corrected for phase.

    """
    bf = np.roll(basis_fns, phase - seg, axis=1)
    return bf


def find_transitions(left: int, right: int,
                     Xsq: np.ndarray, XB: np.ndarray, BB: np.ndarray,
                     period: int,
                     cpic_multiplier: float, num_bf: int) -> list:
    """
    Recursive function to find transitions by dividing the assets into regions and scoring potential transitions.

    Args:
        left (int): Left bound of the current segment.
        right (int): Right bound of the current segment.
        Xsq (np.ndarray): Cumulative sum of squared assets.
        XB (np.ndarray): Cumulative sum of assets multiplied by basis functions.
        BB (np.ndarray): Cumulative sum of basis functions.
        period (int): Minimum length of a level.
        cpic_multiplier (float): Multiplier for CPIC penalty to control sensitivity.
        num_bf (int): Number of basis functions.

    Returns:
        list: List of transition points found within the segment.
    """
    transitions = []

    # The number of points total, to the left of the transition point, and to
    # the right of the transition point. N_L and N_R are vectors, since we
    # simultaneously calculate the likelihood for all candidate points.
    N_T = right - left + 1
    N_L = np.arange(period, N_T - period)
    N_R = np.flip(N_L)

    if len(N_L) == 0:
        return []

    # Calculate the mean of the left, the right, and the entire interval. THE
    # TRANSITION POINT IS THE LAST POINT OF THE LEFT PARTITION.
    B_matrix_L, B_matrix_R, B_matrix_T = get_flanking_matrices(
        BB, N_L, N_R, left, right)
    XB_L, XB_R, XB_T = get_flanking_matrices(
        XB, N_L, N_R, left, right)
    Xsq_L, Xsq_R, Xsq_T = get_flanking_matrices(
        Xsq, N_L, N_R, left, right)

    var_L, var_R, var_T = get_var(
        N_L, N_R, N_T,
        B_matrix_L, B_matrix_R, B_matrix_T,
        XB_L, XB_R, XB_T,
        Xsq_L, Xsq_R, Xsq_T,
        period,
        for_range=np.arange(0, len(N_L), period)
    )

    p_cpic = cpic.get_cpic_penalty(N_T)

    # The total CPIC is the negative log likelihood plus the CPIC penalty times
    # a multiplier that determines the algorithm's sensitivity. A higher
    # multiplier means a less-sensitive level finder. Totally naïve level
    # finding should see cpic_multiplier = 1.
    CPIC = get_cpic(N_L, N_R, N_T,
                    var_L, var_R, var_T,
                    cpic_multiplier, num_bf, p_cpic)

    # Find the best possible transition point
    where_min = np.nanargmin(CPIC)

    # Calculate the summed variance from the model of each side
    var_L, var_R, _ = get_var(
        N_L, N_R, N_T,
        B_matrix_L, B_matrix_R, B_matrix_T,
        XB_L, XB_R, XB_T,
        Xsq_L, Xsq_R, Xsq_T,
        period,
        for_range=np.arange(
            max(where_min - period, 0),
            min(where_min + period, len(N_L) - 1)
        )
    )
    # Recalculate the CPIC
    CPIC = get_cpic(N_L, N_R, N_T,
                    var_L, var_R, var_T,
                    cpic_multiplier, num_bf, p_cpic)

    # Find the best possible transition point
    where_min = np.nanargmin(CPIC)
    min_cpic = np.nanmin(CPIC)

    # Correct the index from the location in the edge-chopped interval to the
    # location in the arrays x and xsq.
    min_index = where_min + period + left - 2

    # CPIC < 0 means that encoding is better if we make the partition
    if min_cpic < 0:

        # Return the found transition, together with any found by repeating the
        # search on the intervals left and right of the transition.
        transitions = ([min_index]
                       + find_transitions(left, min_index,
                                          Xsq, XB, BB,
                                          period, cpic_multiplier,
                                          num_bf)
                       + find_transitions(min_index + 1, right,
                                          Xsq, XB, BB,
                                          period, cpic_multiplier,
                                          num_bf))
    return transitions


def get_cpic(N_L, N_R, N_T, var_L, var_R, var_T, cpic_multiplier, num_bf,
             p_cpic):
    CPIC = 0.5 * (
            N_L * np.log(var_L)
            + N_R * np.log(var_R)
            - N_T * np.log(var_T)
    ) + num_bf + cpic_multiplier * p_cpic
    return CPIC


def get_var(N_L, N_R, N_T,
            B_matrix_L, B_matrix_R, B_matrix_T,
            XB_L, XB_R, XB_T,
            Xsq_L, Xsq_R, Xsq_T,
            period: int,
            for_range: typing.Iterable = None):

    if for_range is None:
        for_range = range(0, len(N_L), period)

    var_L = np.zeros_like(N_L)
    var_R = np.zeros_like(N_R)

    num_bf = XB_L.shape[0]

    for ct in for_range:
        var_L[ct] = get_var_value(num_bf, N_L[ct], B_matrix_L[:, [ct]], XB_L[:, [ct]], Xsq_L[0, ct])
        var_R[ct] = get_var_value(num_bf, N_R[ct], B_matrix_R[:, [ct]], XB_R[:, [ct]], Xsq_R[0, ct])

    var_T = (Xsq_T - (mrdivide(XB_T.T, B_matrix_T.reshape(
        (num_bf, num_bf))) @ XB_T)) / N_T

    var_L = var_L.astype(np.float64)
    var_R = var_R.astype(np.float64)
    var_L[var_L <= 0] = np.nan
    var_R[var_R <= 0] = np.nan

    var_T = var_T[0, 0]

    return var_L, var_R, var_T


def get_var_value(num_bf, N_side, B_matrix_side, XB_side, Xsq_side):
    s = (mrdivide(XB_side.T,B_matrix_side.reshape((num_bf, num_bf))) @ XB_side)
    return (Xsq_side - np.squeeze(s)) / N_side


def mrdivide(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """Matrix right division

    x = B/A is the solution to the equation xA = B. Matrices A and B must have
    the same number of columns. In terms of the left division operator,
    B/A = (A'\\B')'.

    Args:
        A (np.ndarray): An array.
        B (np.ndarray): An array.

    Returns:
        np.ndarray: The matrix right division.
    """
    return A @ np.linalg.inv(B)


def get_flanking_matrices(cumulate, N_L, N_R, left, right):
    # TODO rename and docs
    if N_L.ndim == 0:
        pass
    cumulate = np.atleast_2d(cumulate)
    left_result = cumulate[:, left + N_L - 1] - cumulate[:, [left - 1]]  # Using array broadcasting
    right_result = cumulate[:, [right]] - cumulate[:, right - N_R]
    t_result = cumulate[:, [right]] - cumulate[:, [left - 1]]

    return left_result, right_result, t_result


def step_finder(i_data, v_data, period=250, sensitivity=1, verbose=False,
                num_bf_cp: int = 5, num_bf_dr: int = 3, low_voltage: float = 95,
                high_voltage: float = 205, phase_offset: int = 2) -> tuple:
    transitions = find_levels_pc(i_data, v_data,
                                 period=period,
                                 verbose=verbose,
                                 num_basis_fns=num_bf_cp,
                                 sensitivity=sensitivity)

    feat_dim = dimreduction.get_cov_vec_size(num_bf_dr) + num_bf_dr
    feat_vecs = np.zeros((feat_dim, len(transitions) - 1))
    for ct in range(1, len(transitions)):
        i_step = i_data[transitions[ct - 1]: transitions[ct]]
        v_step = v_data[transitions[ct - 1]: transitions[ct]]

        g_step_long = capcomp.capacitance_compensation(v_step, i_step, period, low_voltage, high_voltage, phase_offset)

        feat_vecs[:, ct - 1] = dimreduction.dimreduction(g_step_long, num_bf_dr)

    return transitions, feat_vecs

def format_steps_df(transitions, features, sfreq, num_bf_dr: int = 3):
    cov_vec_size = dimreduction.get_cov_vec_size(num_bf_dr)
    steps_df = pd.DataFrame({
        "start_idx": transitions[:-1],
        "end_idx": transitions[1:],
    })
    steps_df["n_pts"] = steps_df["end_idx"] - steps_df["start_idx"]
    steps_df["dwell_time_s"] = steps_df["n_pts"] / sfreq

    for i in range(num_bf_dr):
        steps_df[AMPS_FORMAT.format(i)] = features[i, :]

    for i in range(cov_vec_size):
        steps_df[COV_VEC_FORMAT.format(i)] = features[i, :]

    return steps_df


def get_xs_and_cov_vecs_from_steps_df(steps_df, num_bf_dr: int = None):
    if num_bf_dr is None:
        num_bf_dr = sum([re.match(r'x_\d', col) is not None
                      for col in steps_df.columns])
    cov_vec_length = dimreduction.get_cov_vec_size(num_bf_dr)

    xs = np.zeros((len(steps_df), num_bf_dr))
    cov_vec = np.zeros((len(steps_df), cov_vec_length))

    xs[:, :] = steps_df[[AMPS_FORMAT.format(i) for i in range(num_bf_dr)]]
    cov_vec[:, :] = steps_df[[COV_VEC_FORMAT.format(i)
                        for i in range(cov_vec_length)]].to_numpy()

    return xs, cov_vec

def get_traces_and_stds_from_steps_df(steps_df, get_errors: bool = True, num_bf_dr: int = None):
    xs, cov_vecs = get_xs_and_cov_vecs_from_steps_df(steps_df, num_bf_dr)

    covs = dimreduction.get_cov_from_vector(cov_vecs)
    traces = dimreduction.reconstitute_signal(xs.T).T

    if get_errors:
        stds = dimreduction.get_std_from_cov(xs, covs)
    else:
        stds = None

    return traces, stds






