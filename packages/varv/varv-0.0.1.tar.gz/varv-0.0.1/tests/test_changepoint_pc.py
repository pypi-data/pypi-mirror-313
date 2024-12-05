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

import sys
import pathlib

import scipy
import pytest
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from varv import utils
from varv.preprocessing import changepoint_pc

CUMULATES_FILE = pathlib.Path(__file__).parent.joinpath('assets', 'test_cumulates.npz')

def create_timeseries(step_heights, step_durations, snr):
    a = np.zeros(0)
    for step_height, steps_length in zip(step_heights, step_durations):
        a = np.append(a, np.full(steps_length, step_height))

    amp_signal = np.max(a) - np.min(a)

    if snr:
        a += np.random.normal(scale=amp_signal / snr, size=a.shape)

    return a

def create_stepped_timeseries_varv(stepped_timeseries, step_heights, step_durations,
                            sfreq, trifreq, triamp, snr, phase):
    """Creates a stepped time series with a triangle wave component added on.

    Returns:
        A tuple containing the stepped time series combined the triangle wave
        component, along with the triangle wave on its own. The former models
        the current time series, while the latter models the voltage time
        series.
    """
    steps = create_timeseries(step_heights, step_durations, snr)

    t = (np.arange(len(steps)) + phase) / sfreq
    triangle_wave = (scipy.signal.sawtooth(2 * np.pi * t * trifreq, width=0.5)
                     * triamp)

    i = steps + triangle_wave
    return i + triangle_wave, triangle_wave

@pytest.fixture
def step_heights():
    return [0, 30, 60, 10, 30, 0]


@pytest.fixture
def step_durations():
    return [5000, 6000, 1500, 4000, 2000, 2500]


@pytest.fixture
def snr():
    """Signal-to-noise ratio."""
    return 100

@pytest.fixture
def period():
    return 250

@pytest.fixture
def amplitude():
    """Triangle wave."""
    return 200

def create_timeseries_varv(step_heights, step_durations,
                            period, amplitude, snr, phase):
    """Creates a stepped time series with a triangle wave component added on.

    Returns:
        A tuple containing the stepped time series combined the triangle wave
        component, along with the triangle wave on its own. The former models
        the current time series, while the latter models the voltage time
        series.
    """
    steps = create_timeseries(step_heights, step_durations, snr)

    t = (np.arange(len(steps)) + phase)
    triangle_wave = (scipy.signal.sawtooth(2 * np.pi * t / period, width=0.5)
                     * amplitude)

    i = steps + triangle_wave
    return i + triangle_wave, triangle_wave

@pytest.fixture
def phase():
    return 0

@pytest.fixture
def stepped_timeseries_varv(step_heights, step_durations,
                            period, amplitude, snr, phase):
    return create_timeseries_varv(step_heights, step_durations,
                            period, amplitude, snr, phase)


class TestGetPhase:

    @pytest.mark.parametrize("phase_input, phase_expected", [
        (0, 0),
        (250, 0), # One period shift
        (125, 125), # Half period
        (8, 8), # Arbitrary shift
        (-8, 242), # Negative shift
    ])
    def test_get_phase(self, step_heights, step_durations,
                            period, amplitude, snr, phase_input, phase_expected):
        _, v = create_timeseries_varv(step_heights, step_durations,
                                      period, amplitude, snr, phase_input)

        phase_found = utils.get_phase_of_period(v, period)

        assert phase_found == phase_expected

    def test__get_phase_zero_phase_low_amp(self, stepped_timeseries_varv):
        _, v = stepped_timeseries_varv
        v /= 15 # Signal with amplitude smaller than 1

        with pytest.raises(ValueError):
            utils.get_phase_of_period(v, 50)


class TestGetPeriodAndPhase:

    @pytest.mark.parametrize("period_input", [10, 25, 2, 8])
    def test_get_period_and_phase(self, step_heights, step_durations,
                            period, amplitude, snr, phase, period_input):
        _, v = create_timeseries_varv(step_heights, step_durations,
                                      period_input, amplitude, snr, phase)

        period_found, _ = changepoint_pc.get_bias_period_and_phase(v)

        assert period_found == period_input

### Fixtures for cumulates ###

@pytest.fixture
def data():
    return np.load(CUMULATES_FILE)

@pytest.fixture
def bf_true(data):
    return data['bb_small']

@pytest.fixture
def bf_true_phase_10(data):
    return data['bb_small_10_phase']

@pytest.fixture
def bf_true_offset_7(data):
    return data['bb_small_7_seg']

@pytest.fixture
def BB_true(data):
    return data['BB_big']

class TestBasisFunctions:

    def test_basis_func_tiling(self, bf_true):
        basis_fns = changepoint_pc.BASIS_FNS_LEVEL_FINDING[:, :5]  # First 5 Bfs
        bf = changepoint_pc.add_phase_to_bf(basis_fns.T, 0, 0)
        bf = changepoint_pc.tile_bf_to_match_signal(bf, 17474)
        BB, _, _ = changepoint_pc.get_cumulative_sums(bf, 5, np.zeros(17474))

        assert bf.shape == (5, 17474)
        np.testing.assert_allclose(bf, bf_true, atol=1e-5)

    def test_basis_func_tiling_with_zero_phase(self, bf_true):
        basis_fns = changepoint_pc.BASIS_FNS_LEVEL_FINDING[:, :5]  # First 5 Bfs

        bf = changepoint_pc.add_phase_to_bf(basis_fns.T, 0, 0)
        bf = changepoint_pc.tile_bf_to_match_signal(bf, 17474)

        assert bf.shape == (5, 17474)
        np.testing.assert_allclose(bf, bf_true, atol=1e-5)

    def test_basis_func_tiling_with_ten_phase(self, bf_true_phase_10):
        basis_fns = changepoint_pc.BASIS_FNS_LEVEL_FINDING[:, :5]  # First 5 Bfs

        bf = changepoint_pc.add_phase_to_bf(basis_fns.T, 10, 0)
        bf = changepoint_pc.tile_bf_to_match_signal(bf, 17474)

        assert bf.shape == (5, 17474)
        np.testing.assert_allclose(bf, bf_true_phase_10, atol=1e-5)

    def test_basis_func_tiling_with_seven_segment_offset(self, bf_true_offset_7):
        basis_fns = changepoint_pc.BASIS_FNS_LEVEL_FINDING[:, :5]  # First 5 Bfs

        bf = changepoint_pc.add_phase_to_bf(basis_fns.T, 0, 7)
        bf = changepoint_pc.tile_bf_to_match_signal(bf, 17474)

        assert bf.shape == (5, 17474)
        np.testing.assert_allclose(bf, bf_true_offset_7, atol=1e-5)

    def test_basis_func_cumulative(self, BB_true):
        basis_fns = changepoint_pc.BASIS_FNS_LEVEL_FINDING[:, :5]  # First 5 Bfs

        bf = changepoint_pc.add_phase_to_bf(basis_fns.T, 0, 0)
        bf = changepoint_pc.tile_bf_to_match_signal(bf, 17474)

        BB, _, _ = changepoint_pc.get_cumulative_sums(bf, 5, np.zeros(17474))

        np.testing.assert_allclose(BB, BB_true, atol=1e-3)

@pytest.fixture
def b_matrix_L_true(data):
    return data['B_matrix_L']

@pytest.fixture
def b_matrix_R_true(data):
    return data['B_matrix_R']

@pytest.fixture
def b_matrix_T_true(data):
    return data['B_matrix_T']


@pytest.fixture
def XB_L_true(data):
    return data['XB_L']

@pytest.fixture
def XB_R_true(data):
    return data['XB_R']

@pytest.fixture
def XB_T_true(data):
    return data['XB_T']

@pytest.fixture
def XB_true(data):
    return data['XB']


@pytest.fixture
def Xsq_L_true(data):
    return data['Xsq_L']

@pytest.fixture
def Xsq_R_true(data):
    return data['Xsq_R']

@pytest.fixture
def Xsq_T_true(data):
    return data['Xsq_T']

@pytest.fixture
def Xsq_true(data):
    return data['Xsq']

@pytest.fixture
def var_L_true(data):
    return data['var_L']

@pytest.fixture
def var_R_true(data):
    return data['var_R']

@pytest.fixture
def var_T_true(data):
    return data['var_T']

class TestFindTransitions:

    @pytest.fixture(scope='class')
    def period(self):
        return 250

    def test_b_matrix(self, b_matrix_L_true, b_matrix_R_true, b_matrix_T_true, BB_true, period):
        N_L = np.arange(period - 1, 1001 - period)
        N_R = np.flip(N_L)

        B_matrix_L, B_matrix_R, B_matrix_T = changepoint_pc.get_flanking_matrices(
            BB_true, N_L, N_R, 1000, 2000)

        assert B_matrix_L.shape == (25, 502)
        assert B_matrix_R.shape == (25, 502)
        assert B_matrix_T.shape == (25, 1)

        # Lots of rounding errors so large tolerance
        np.testing.assert_allclose(B_matrix_L, b_matrix_L_true, atol=0.3)
        np.testing.assert_allclose(B_matrix_R, b_matrix_R_true, atol=0.3)
        np.testing.assert_allclose(B_matrix_T, b_matrix_T_true, atol=0.3)

    def test_xb(self, XB_L_true, XB_R_true, XB_T_true, XB_true, period):

        N_L = np.arange(period - 1, 1001 - period)
        N_R = np.flip(N_L)

        XB_L, XB_R, XB_T = changepoint_pc.get_flanking_matrices(
            XB_true, N_L, N_R, 1000, 2000)

        assert XB_L.shape == (5, 502)
        assert XB_R.shape == (5, 502)
        assert XB_T.shape == (5, 1)

        # Lots of rounding errors so large tolerance
        np.testing.assert_allclose(XB_L, XB_L_true, atol=1000)
        np.testing.assert_allclose(XB_R, XB_R_true, atol=1000)
        np.testing.assert_allclose(XB_T, XB_T_true, atol=1000)

    def test_Xsq_2d(self, Xsq_L_true, Xsq_R_true, Xsq_T_true, Xsq_true, period):
        N_L = np.arange(period - 1, 1001 - period)
        N_R = np.flip(N_L)

        Xsq_L, Xsq_R, Xsq_T = changepoint_pc.get_flanking_matrices(
            Xsq_true, N_L, N_R, 1000, 2000)

        assert Xsq_L.shape == (1, 502)
        assert Xsq_R.shape == (1, 502)
        assert Xsq_T.shape == (1, 1)

        # Lots of rounding errors so large tolerance
        np.testing.assert_allclose(Xsq_L, Xsq_L_true, rtol=0.01)
        np.testing.assert_allclose(Xsq_R, Xsq_R_true, rtol=0.01)
        np.testing.assert_allclose(Xsq_T, Xsq_T_true, rtol=0.01)

    def test_get_var(self,
                     var_L_true, var_R_true, var_T_true,
                     b_matrix_L_true, b_matrix_R_true, b_matrix_T_true,
                     XB_L_true, XB_R_true, XB_T_true,
                     Xsq_L_true, Xsq_R_true, Xsq_T_true,
                     period,):

        args = (b_matrix_L_true, b_matrix_R_true, b_matrix_T_true,
                XB_L_true, XB_R_true, XB_T_true,
                Xsq_L_true, Xsq_R_true, Xsq_T_true)

        N_L = np.arange(period - 1, 1001 - period)
        N_R = np.flip(N_L)
        N_T = 1001

        var_L, var_R, var_T = changepoint_pc.get_var(
            N_L, N_R, N_T, *args, period, for_range=range(0, len(N_L), period))

        assert var_L.shape == (502,)
        assert var_R.shape == (502,)
        assert isinstance(var_T, float)

        # Lots of rounding errors so large tolerance
        np.testing.assert_allclose(var_L, var_L_true.flatten(), rtol=0.01)
        np.testing.assert_allclose(var_R, var_R_true.flatten(), rtol=0.01)
        assert var_T == pytest.approx(var_T_true, rel=0.01)

    def test_find_single_step(self, stepped_timeseries_varv, bf_true, period):
        basis_fns = changepoint_pc.BASIS_FNS_LEVEL_FINDING[:, :5]  # First 5 Bfs
        min_level_length = period
        cpic_multiplier = 3
        num_bf = 5

        i_data, _ = stepped_timeseries_varv
        i_data = i_data[:11000] # Only first step

        # Remove spikes
        n = len(i_data)  # Length of original arrays
        delete_x = np.arange(0 - 250, n, 250 // 2)
        delete_x = delete_x.reshape((len(delete_x), 1))
        delete_y = np.arange(21)
        pts_to_delete = delete_x + delete_y  # Using NumPy broadcasting
        pts_to_delete = pts_to_delete.flatten()
        pts_to_delete = pts_to_delete[
            (pts_to_delete >= 1) & (pts_to_delete <= n)]

        original_indices = np.arange(n)
        i_data = np.delete(i_data, pts_to_delete)
        original_indices = np.delete(original_indices, pts_to_delete)
        period = 250 - 42
        phase = 0 - np.sum(pts_to_delete < 0)

        start_point = 0
        end_point = len(i_data)

        x = np.concatenate([np.zeros(1), i_data])
        t = np.arange(start_point - 1, end_point)

        bf = changepoint_pc.add_phase_to_bf(basis_fns.T, 0, 0)
        bf = changepoint_pc.tile_bf_to_match_signal(bf, len(t))

        BB, XB, Xsq = changepoint_pc.get_cumulative_sums(bf, num_bf, x)

        transitions = changepoint_pc.find_transitions(1, len(x) - 1,
                                                      Xsq, XB, BB,
                                                      min_level_length,
                                                      cpic_multiplier,
                                                      num_bf)

        # fig, ax = plt.subplots(figsize=(12, 4))
        # ax.plot(i_data)
        #
        # for s in transitions:
        #     ax.axvline(s, color="r")
        #
        # fig.show()

        assert len(transitions) == 1
        assert transitions[0] == pytest.approx(5000, abs=1000)
        # Big margin because of spike removal shifting indices



class TestVarVChangePoint:

    def test_changepoint_pc_for_varv(self, stepped_timeseries_varv,
                                     step_heights, period):
        i, v = stepped_timeseries_varv

        results = changepoint_pc.find_levels_pc(i, v, period=period,
                                                verbose=False, sensitivity=1)

        # fig, ax = plt.subplots(figsize=(12, 4))
        # ax.plot(i)
        # for s in results:
        #     ax.axvline(s, c="r")
        #
        # ax.set_xlabel("Sample number")
        # ax.set_ylabel("Mock current")
        # ax.set_title("Step finding on mock arrays")
        #
        # fig.show()

        assert len(results) == len(step_heights) - 1 + 2
        # Also "transitions" at start and end of array.


class TestStepsDataFrame:

    @pytest.fixture(scope='class')
    def steps_df(self):
        return pd.DataFrame(np.array(
            [[1, 2, 1, 2, 3],
             [2, 3, 2, 3, 4]]),
            columns=['x_0', 'x_1', 'Sigma_0', 'Sigma_1', 'Sigma_2']
        )

    @pytest.fixture(scope='class')
    def comp_amps_true(self):
        return np.array([[1, 2], [2, 3]])

    @pytest.fixture(scope='class')
    def cov_vecs_true(self):
        return np.array([
            [1, 2, 3],
            [2, 3, 4]
        ])


    def test_x_and_cov_from_steps_df(self, steps_df,
                                     comp_amps_true, cov_vecs_true):
        xs, cov_vecs = changepoint_pc.get_xs_and_cov_vecs_from_steps_df(steps_df)

        np.testing.assert_array_equal(cov_vecs, cov_vecs_true)
        np.testing.assert_array_equal(xs, comp_amps_true)

if __name__ == "__main__":
    sys.exit(pytest.main(["-qq"]))
