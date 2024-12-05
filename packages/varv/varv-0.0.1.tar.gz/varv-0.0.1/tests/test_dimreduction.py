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

import pathlib
import sys

import pytest
import numpy as np

from varv.preprocessing import dimreduction

DATA_FILE = pathlib.Path(__file__).parent.joinpath('assets', 'test_data_dimreduction.npy')

@pytest.fixture()
def repeats():
    return 10

@pytest.fixture
def g_mat_long_from_data():
    """Conductance matrix from actual data"""
    return np.load(DATA_FILE)

@pytest.fixture
def g_mat_long_three_bfs(repeats):
    """Toy conductance matrix created using equal parts of all three basis
    functions of the dimension reduction. Equivalent to a signal that
    exactly matches the sum of the three basis functions."""
    return np.repeat(dimreduction.BASIS_FNS_DIM_RED, repeats, axis=1)

@pytest.fixture
def p_true_three_bfs(repeats):
    """Component amplitudes from toy conductance matrix created with all three
    basis functions."""
    return np.repeat(np.eye(3, 3), repeats, axis=1)

@pytest.fixture
def x_true_three_bfs():
    """Mean component amplitudes from toy conductance matrix created with all
    three basis functions."""
    return np.full(3, 1/3)

@pytest.fixture
def g_mat_long_first_bf(repeats):
    """Toy conductance matrix created using only the first basis function of
    the dimension reduction method. Equivalent to a signal that
    exactly matches first basis function."""
    return np.tile(dimreduction.BASIS_FNS_DIM_RED[:, 0], (repeats, 1)).T

@pytest.fixture
def x_true_first_bf():
    """Mean component amplitudes from toy conductance matrix created with the
    first basis function."""
    return np.array([1, 0, 0])


class TestDimensionReduction:

    def test_design_matrix(self):
        M = dimreduction.BASIS_FNS_DIM_RED

        assert M.shape == (125, 3)

    def test_weights(self, g_mat_long_three_bfs, p_true_three_bfs):
        p, _ = dimreduction.get_comp_amps_and_cov(g_mat_long_three_bfs)

        np.testing.assert_allclose(p_true_three_bfs, p, atol=1e-6)

    def test_covariance(self, g_mat_long_three_bfs):
        _, cov = dimreduction.get_comp_amps_and_cov(g_mat_long_three_bfs)

        assert cov.shape == (3, 3)

    def test_on_dataset(self, g_mat_long_from_data):
        p, cov = dimreduction.get_comp_amps_and_cov(g_mat_long_from_data)

        assert cov.shape == (3, 3)
        assert p.shape == (3, g_mat_long_from_data.shape[1])

    def test_mean_component_amps_three_bfs(
            self, g_mat_long_three_bfs, x_true_three_bfs):
        p, _ = dimreduction.get_comp_amps_and_cov(g_mat_long_three_bfs)
        x = dimreduction.get_mean_comp_amp(p)

        np.testing.assert_allclose(x_true_three_bfs, x)

    def test_mean_component_amps_one_bf(
            self, g_mat_long_first_bf, x_true_first_bf):
        p, _ = dimreduction.get_comp_amps_and_cov(g_mat_long_first_bf)
        x = dimreduction.get_mean_comp_amp(p)

        np.testing.assert_allclose(x_true_first_bf, x, atol=1e-6)

    def test_reconstitute(self):
        true_sig = dimreduction.BASIS_FNS_DIM_RED[:, 2]
        g_mat_long = np.tile(true_sig, (10, 1)).T
        g_mat_long += np.random.randn(125, 10) * 0.05
        p, _ = dimreduction.get_comp_amps_and_cov(g_mat_long)
        x = dimreduction.get_mean_comp_amp(p)
        sig = dimreduction.reconstitute_signal(x)

        # plt.plot(g_mat_long, alpha=0.5, c='black')
        # plt.plot(true_sig, c='b', label='Ground truth')
        # plt.plot(sig, c='r', label='Reconstituted')
        # plt.xlabel('Voltage index')
        # plt.ylabel('Conductance [nS]')
        # plt.show()

        np.testing.assert_allclose(true_sig, sig, atol=0.1)

    def test_reconstitute_std(self):
        NUM_SAMPLES = 100
        np.random.seed(0)
        true_sig = dimreduction.BASIS_FNS_DIM_RED[:, 2]
        true_std = 0.05
        g_mat_long = np.tile(true_sig, (NUM_SAMPLES, 1)).T
        g_mat_long += np.random.randn(125, NUM_SAMPLES) * true_std
        p, cov = dimreduction.get_comp_amps_and_cov(g_mat_long)
        mean = dimreduction.get_mean_comp_amp(p)
        std = dimreduction.get_std_from_cov(mean, cov)

        # sig = dimreduction.reconstitute_signal(x)
        # plt.plot(g_mat_long, alpha=0.5, c='black')
        # plt.fill_between(np.arange(len(sig)), sig - std, sig + std, alpha=0.5, color='r', zorder=10)
        # plt.plot(sig, c='r', label='Reconstituted')
        # plt.xlabel('Voltage index')
        # plt.ylabel('Conductance [nS]')
        # plt.show()

        # Stdev of the dimension-reduced data should be less
        # than of the original dataset.
        assert np.all(std < true_std)

    def test_get_vec_from_cov(self):
        cov = np.arange(9).reshape((3, 3))

        vec = dimreduction.get_vector_from_cov(cov)

        np.testing.assert_array_equal(vec, np.array([0, 1, 2, 4, 5, 8]))

    def test_get_cov_from_vec(self):
        true_cov = np.array([
            [0, 1, 2],
            [1, 4, 5],
            [2, 5, 8],
        ])
        cov = dimreduction.get_cov_from_vector(np.array([0, 1, 2, 4, 5, 8]))

        np.testing.assert_array_equal(cov, true_cov)

    def test_get_cov_from_vec_2d(self):
        true_cov = np.array([
            [[0, 1, 2],
             [1, 4, 5],
             [2, 5, 8]],
            [[0, 1, 2],
             [1, 4, 5],
             [2, 5, 8]],
        ])
        cov = dimreduction.get_cov_from_vector(np.array([
            [0, 1, 2, 4, 5, 8],
            [0, 1, 2, 4, 5, 8],
        ]))

        np.testing.assert_array_equal(cov, true_cov)

if __name__ == "__main__":
    sys.exit(pytest.main(["-qq"]))
