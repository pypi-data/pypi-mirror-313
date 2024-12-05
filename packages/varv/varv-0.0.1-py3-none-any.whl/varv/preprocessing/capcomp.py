#
#      Copyright (C) 2024 Thijn Hoekstra
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

"""
Capacitance compensation for variable voltage sequencing of peptides.

Based on: Noakes, M.period., Brinkerhoff, H., Laszlo, A.H. et al.
Increasing the accuracy of nanopore DNA sequencing using a time-varying
cross membrane voltage. Nat Biotechnol 37, 651–656 (2019).
https://doi.org/10.1038/s41587-019-0096-0

TODO: Write checks for long matrices etc.
TODO: Find better name for long matrix
"""

import scipy
import numpy as np

from varv import utils


def get_compensated_current(v_data, i_data, period,
                            low_voltage: float = 95,
                            high_voltage: float = 205,
                            phase_offset: int = 2):
    v_data = v_data.copy()
    i_data = i_data.copy()

    phase = utils.get_phase_of_period(v_data, period) + phase_offset

    # Grab only data where voltage sweep is in range
    v_data[(v_data < low_voltage) | (v_data > high_voltage)] = np.nan

    # Examine to make sure the in-sweep region is at least one period long
    if np.sum(~np.isnan(v_data)) < period:
        raise ValueError('Warning, level does not have full cycle in bounds.')

    v_data = align_data_to_periods(v_data, period, phase)
    i_data = align_data_to_periods(i_data, period, phase)

    cyc = get_number_of_cycles(v_data, period)

    # Reshape v_data into a matrix where each column is the data for one
    # complete cycle
    v_mat = v_data.reshape((cyc, period)).T
    i_mat = i_data.reshape((cyc, period)).T

    # Create long matrices where each row now corresponds to a single voltage,
    # as opposed to a single phase point (each voltage point corresponds to two
    # phase points, one for up, one for down)

    v_mat_long = get_half_cycle_mat(v_mat, period)
    i_mat_long = get_half_cycle_mat(i_mat, period)

    # Average voltage by voltage point is median along the 2nd dim of long
    # matrix
    v = np.nanmedian(v_mat_long, axis=1)

    # Up slope entries are contained in the top half of the matrix
    # Down slope entries are contained in the bottom half of the matrix
    i_avg_up = np.nanmedian(i_mat[:period // 2, :], axis=1)
    i_avg_do = np.nanmedian(i_mat[-period // 2:, :], axis=1)

    # Calculate the correction function from the averaged data
    # Grab voltage, up slope current, and down slope current, and put all three
    # in the same ordering
    h_v = np.flip(i_avg_do) - i_avg_up

    # q1, q2, q3 are the first, second, and third voltage quartiles
    # idx_q1, idx_q2, idx_q3 are the indices of the 1st, 2nd, and 3rd voltage
    # quartiles
    q1, q2, q3 = scipy.stats.mstats.mquantiles(v)
    idx_q1 = np.argmin(np.abs(v - q1))
    idx_q2 = np.argmin(np.abs(v - q2))
    idx_q3 = np.argmin(np.abs(v - q3))

    params = fit_centered_parabola(v[idx_q1:idx_q3], h_v[idx_q1:idx_q3])

    m = get_parabola_vertex_y(*params)

    corrector = get_corrector(h_v, m)

    # Tile corrector function
    corrector = np.tile(corrector, (i_mat.shape[1], 1)).T

    # Apply the correction function to all of the data
    i_comp_mat = i_mat + corrector

    return i_comp_mat, v_mat


def get_conductance(i_comp_mat_long: np.ndarray,
                    v_mat_long: np.ndarray) -> np.ndarray:
    """Gets conductance

    Args:
        i_comp_mat_long:
        v_mat_long:

    Returns:

    """
    assert i_comp_mat_long.shape[0] == v_mat_long.shape[0], (
        'Unequal number of rows in voltage and current data. Please check '
        'whether both are half-cycle arrays.')

    return i_comp_mat_long / v_mat_long


def get_corrector(h_v, m):
    # Calculate right half of c_up and left half of c_do
    c_up = np.full_like(h_v, m / 2)
    c_do = np.full_like(h_v, m / 2)
    # Calculate left half of c_up and right half of c_do
    half = len(h_v) // 2
    c_up[:half] = h_v[:half] - m / 2
    c_do[half:] = h_v[half:] - m / 2

    # put correction function into the right order to be added into current
    # matrix directly
    c_do = -np.flip(c_do)
    corrector = np.concatenate([c_up, c_do])
    return corrector


def get_number_of_cycles(v_data, period):
    """Find how many cycles we have

    Args:
        v_data:
        period:

    Returns:

    """
    return np.ceil(len(v_data) / period).astype(np.int64)


def align_data_to_periods(v_data, period, phase):
    """Make into full cycles by appending NaNs to front and back

    Args:
        v_data:
        period:
        phase:

    Returns:

    """
    assert 0 <= phase <= period, f'Error, need phase between 0 and {period}'

    v_data = np.concatenate([
        np.full(phase, np.nan),
        v_data,
        np.full((period - phase - len(v_data) % period) % period, np.nan)
    ])
    return v_data


def get_half_cycle_mat(data_mat, period):
    utils.check_if_array_is_full_cycle(data_mat, period)

    data_mat_long = np.hstack([
        data_mat[:period // 2, :],
        np.flip(data_mat[-period // 2:, :], axis=0)
    ])
    return data_mat_long


def fit_centered_parabola(x, y):
    """Fits parabola with a fixed vertex.

    Fits a parabola to the events with its peak fixed at the midpoint of the x
    events.

    This function fits a parabola of the form y = a * x^2 + bx + c to the
    given `x` and `y` events, with the vertex of the parabola constrained to lie
    at the midpoint of the `x` events. It assumes that the events points are evenly
    distributed along the `x` axis.

    Args:
        x (np.ndarray): The x-values of the events points.
        y (np.ndarray): The y-values of the events points.

    Returns:
        float: The coefficient `a` of the quadratic term.
        float: The coefficient `b` of the linear term.
        float: The coefficient `c` of the constant term.
    """

    vertex_x = (x[0] + x[-1]) / 2

    def parabola(x, a, c):
        return a * x ** 2 + -2 * a * vertex_x * x + c

    popt, pcov = scipy.optimize.curve_fit(parabola, x, y)

    a, c = popt

    return a, -2 * a * vertex_x, c


def get_parabola_vertex_y(a, b, c):
    return -b ** 2 / 4 / a + c


def full_cycle_mat_to_array(mat: np.ndarray) -> np.ndarray:
    data = mat.T.flatten()
    return data[~np.isnan(data)]


def capacitance_compensation(v, i, period, low_voltage: float = 95, high_voltage: float = 205, phase_offset=2):
    """Master function for capacitance compensation

    Returns:
        np.ndarray:
    """
    i_mat_comp, v_mat = get_compensated_current(
        v, i, period,
        low_voltage=low_voltage,
        high_voltage=high_voltage,
        phase_offset=phase_offset,
    )
    i_mat_comp_long = get_half_cycle_mat(i_mat_comp, period)
    v_mat_long = get_half_cycle_mat(v_mat, period)
    g_mat_long = get_conductance(i_mat_comp_long, v_mat_long)
    return g_mat_long
