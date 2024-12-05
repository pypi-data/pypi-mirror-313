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

import pathlib
import sys

import scipy
import pytest
import numpy as np

from varv import utils
from varv.preprocessing import capcomp



DATA_FILE = pathlib.Path(__file__).parent.joinpath('assets', 'test_data_capcomp.npz')


@pytest.fixture()
def period():
    return 250

class TestUtilities:

    @pytest.fixture(scope="class")
    def full_cycle_array(self):
        return np.zeros((250, 10))

    @pytest.fixture(scope="class")
    def half_cycle_array(self):
        return np.zeros((125, 10))




    def test_half_cycle_array_check_good(self, half_cycle_array, period):
        assert utils.check_if_array_is_half_cycle(half_cycle_array, period) is None

    def test_half_cycle_array_check_bad(self, full_cycle_array, period):
        with pytest.raises(ValueError):
              utils.check_if_array_is_half_cycle(full_cycle_array, period)

    def test_full_cycle_array_check_good(self, full_cycle_array, period):
        assert utils.check_if_array_is_full_cycle(full_cycle_array, period) is None

    def test_full_cycle_array_check_bad(self, half_cycle_array, period):
        with pytest.raises(ValueError):
            utils.check_if_array_is_full_cycle(half_cycle_array, period)


@pytest.fixture
def data():
    return np.load(DATA_FILE)


@pytest.fixture
def i(data):
    return data['i']


@pytest.fixture
def v(data):
    return data['v']



class TestCapacitanceCompensation:

    def test_fit_parabola(self):

        x = np.linspace(-7, 5, 30)

        y = 1 * x ** 2 + 2 * x - 3

        a, b, c = capcomp.fit_centered_parabola(x, y)

        assert a == pytest.approx(1)
        assert b == pytest.approx(2)
        assert c == pytest.approx(-3)

    def test_fit_parabola_off_center(self):

        x = np.linspace(-10, 4, 30)

        y = 1 * x ** 2 + 2 * x - 3

        a, b, c = capcomp.fit_centered_parabola(x, y)

        # assert a != pytest.approx(1)
        assert b != pytest.approx(2)
        assert c != pytest.approx(-3)

    def test_align_data_to_period_no_change(self, v, period):
        v_data = capcomp.align_data_to_periods(v, period, 0)

        np.testing.assert_array_equal(v_data, v)

    def test_align_data_to_period_with_padding(self, v, period):
        v_data = capcomp.align_data_to_periods(v, period, 10)

        np.testing.assert_array_equal(v_data[10:3760], v)
        assert np.sum(np.isnan(v_data)) == period

    def test_align_data_to_period_indivisible_length(self, v, period):
        v_data = capcomp.align_data_to_periods(v[:3001], period, 0)

        assert len(v_data) == 3250

    def test_align_data_to_period_with_padding_indivisible_length(self, v, period):
        v_data = capcomp.align_data_to_periods(v[:3001], period, 10)

        np.testing.assert_array_equal(v_data[10:3011], v[:3001])
        assert len(v_data) == 3250
        assert np.sum(np.isnan(v_data)) == period - 1

    def test_capacitance_compensation_shape(self, i, v, period):
        comp_mat, _ = capcomp.get_compensated_current(
            v, i, period)

        assert comp_mat.shape == (period, 16)


    def test_capacitance_compensation_shape_indivisible_length(self, i, v, period):

        comp_mat, _ = capcomp.get_compensated_current(
            v[:3001], i[:3001], period)

        assert comp_mat.shape == (period, 13)

    def test_capacitance_compensation_long_shape(self, i, v, period):

        comp_mat, _ = capcomp.get_compensated_current(
            v, i, period)
        comp_mat_long = capcomp.get_half_cycle_mat(comp_mat, period)

        assert comp_mat_long.shape == (125, 32)

    def test_capacitance_compensation_slope_up(self, i, v, period):
        comp_mat, _ = capcomp.get_compensated_current(
            v, i, period)

        comp_mat_long = capcomp.get_half_cycle_mat(comp_mat, period)
        x = np.arange(125)
        for _, y in enumerate(comp_mat_long.T):
            if np.sum(np.isnan(y)):  # Only check full arrays
                continue
            res = scipy.stats.linregress(x, y)
            assert res.slope > 0

    def test_capacitance_compensation_mat_to_array(self, i, v, period):
        comp_mat, _ = capcomp.get_compensated_current(
            v, i, period)

        i_data = capcomp.full_cycle_mat_to_array(comp_mat)

        assert len(i_data) == 3750

    def test_get_conductance(self):
        i_comp_mat_long = np.tile(np.arange(0, 100, 10), (3, 1)).T
        v_mat_long = np.tile(np.arange(100, 200, 10), (3, 1)).T


        g_true = np.arange(0, 100, 10) / np.arange(100, 200, 10)
        g_true = np.tile(g_true, (3, 1)).T

        g = capcomp.get_conductance(i_comp_mat_long, v_mat_long)

        np.testing.assert_array_equal(g, g_true)

if __name__ == "__main__":
    sys.exit(pytest.main(["-qq"]))
