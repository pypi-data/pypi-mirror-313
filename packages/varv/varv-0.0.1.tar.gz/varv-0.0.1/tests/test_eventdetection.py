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

import pandas as pd
import pytest
import numpy as np

from varv import base
from varv.preprocessing import eventdetection

DATA_FILE_CV = pathlib.Path(__file__).parent.joinpath('assets', 'test_data_constant_voltage.h5')
DATA_FILE_VV = pathlib.Path(__file__).parent.joinpath('assets', 'test_data_variable_voltage.h5')

@pytest.fixture
def raw_cv():
    data = pd.read_hdf(DATA_FILE_CV, 'df')
    info = base.Info(5000, 'ABC', base.BiasVoltage(180, 0, 0))
    raw = base.Raw(data, info)
    raw.reset_states()
    return raw


@pytest.fixture
def raw_vv():
    data = pd.read_hdf(DATA_FILE_VV, 'df')
    info = base.Info(5000, 'ABC', base.BiasVoltage(150, 50, 200))
    raw = base.Raw(data, info)
    raw.reset_states()
    return raw


class TestEventDetection:

    def test_get_open_state(self, raw_cv):

        open_state, std, weight = eventdetection.get_open_state_current_distr(
            raw_cv.get_i(), 220, 250)

        # fig, ax = raw.plot()
        # ax.axhline(open_state, c="r", label="Open State")
        # ax.legend(loc=3)
        # fig.show()

        assert open_state == pytest.approx(243.6, abs=1)
        assert std == pytest.approx(1.1, abs=0.1)
        assert weight == pytest.approx(0.189, abs=0.1)

    def test_mark_open_state(self, raw_cv):

        eventdetection.find_open_state(raw_cv)

        # fig, ax = raw.plot()
        # ax.legend(loc=3)
        # fig.show()

        np.testing.assert_array_equal(np.unique(raw_cv.get_states()),
                                      np.array([base.GOOD_STATE, base.OPEN_STATE]))

    def test_mark_open_state_varv(self, raw_vv):

        eventdetection.find_open_state(raw_vv, lower_bound=170, upper_bound=200,
                                       lowpass=100)

        # fig, ax = raw_vv.plot()
        # ax.legend(loc=3)
        # fig.show()

        np.testing.assert_array_equal(np.unique(raw_vv.get_states()),
                                      np.array([base.GOOD_STATE, base.OPEN_STATE]))

    def test_get_voltage_states(self, raw_cv):

        distrs = eventdetection.get_voltage_distrs(raw_cv.get_v())


        assert distrs[0].mean() == pytest.approx(181.8, abs=1) # On
        assert distrs[1].mean() == pytest.approx(1.6, abs=1) # Off
        assert distrs[2].mean() == pytest.approx(-181.6, abs=1) # Reversed bias

        # fig, axs = eventdetection.plot_voltage_state(raw)
        # fig.show()

    def test_get_voltage_states_with_a_priori_varv(self, raw_vv):
        distrs = eventdetection.get_voltage_distrs(raw_vv.get_v(),
                                                   known_good_voltage=(90, 210))

        assert distrs[0].mean() == pytest.approx(150, abs=1) # On (DC component)
        assert distrs[1].mean() == pytest.approx(-5, abs=1) # Off
        assert distrs[2].mean() == pytest.approx(-143, abs=1) # Reversed bias

    def test_mark_voltage_states(self, raw_cv):
        eventdetection.find_bad_voltages(raw_cv)

        np.testing.assert_array_equal(np.unique(raw_cv.get_states()),
                                      np.array([base.GOOD_STATE, base.BAD_VOLTAGE_STATE]))

    def test_mark_voltage_states_with_a_priori_varv(self, raw_vv):
        eventdetection.find_bad_voltages(raw_vv, known_good_voltage=(90, 210))

        np.testing.assert_array_equal(np.unique(raw_vv.get_states()),
                                      np.array([base.GOOD_STATE, base.BAD_VOLTAGE_STATE]))


    def test_get_open_state_segments(self, raw_cv):
        eventdetection.find_open_state(raw_cv)
        eventdetection.find_bad_voltages(raw_cv)

        segments = eventdetection.get_open_state_segments(raw_cv)

        assert segments.shape[0] == pytest.approx(694, abs=1)
        assert segments.shape[1] == 2


    def test_get_open_state_fit(self, raw_cv):

        eventdetection.find_open_state(raw_cv)
        eventdetection.find_bad_voltages(raw_cv)

        poly = eventdetection.get_open_pore_fit(raw_cv)

        # fig, ax = raw.plot()
        # t = raw.get_time()[::100]
        # ax.plot(t, poly(t), "r", label="Fit")
        #
        # ax.legend(loc=3)
        # fig.show()

        assert poly.coef[0] == pytest.approx(243, abs=1)
        assert poly.coef[1] == pytest.approx(0.216, abs=0.1)


if __name__ == "__main__":
    sys.exit(pytest.main(["-qq"]))

