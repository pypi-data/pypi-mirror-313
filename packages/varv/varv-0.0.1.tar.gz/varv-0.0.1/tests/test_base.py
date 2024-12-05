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

import sys

import pytest
import numpy as np
from matplotlib import pyplot as plt

from varv.base import Raw, Info



class TestInfo:

    def test_print(self):
        info = Info(5e3, 'ABC')

        s_true = (
            '                                  \n'
            'Name                           ABC\n'
            'Channel No.                      0\n'
            'Start Index                      0\n'
             'Label                            0\n'
             'Sampling Rate           5000.00 Hz\n'
             'Bias Voltage DC            0.00 Hz\n'
             'Bias Voltage Amplitude     0.00 pA\n'
             'Bias Voltage Frequency     0.00 Hz\n'
             'Open Channel Current       0.00 pA')
        s = info.__str__()

        assert s == s_true


@pytest.fixture
def raw():
    return Raw.from_arrays(np.arange(1000), np.zeros(1000), 5e3, 'ABC', bdc=180, bamp=0, bfreq=0)


class TestRaw:

    def test_print(self, raw):
        s_true = (
 '                                  \n'
 'Duration                    0.20 s\n'
 'No. Samples                   1000\n'
 'Name                           ABC\n'
 'Channel No.                      0\n'
 'Start Index                      0\n'
 'Label                            0\n'
 'Sampling Rate           5000.00 Hz\n'
 'Bias Voltage DC          180.00 Hz\n'
 'Bias Voltage Amplitude     0.00 pA\n'
 'Bias Voltage Frequency     0.00 Hz\n'
 'Open Channel Current       0.00 pA')

        assert raw.__str__() == s_true

    def test_base_init(self, raw):
        assert raw.info.sfreq == 5e3
        assert raw.info.name, 'ABC'
        assert raw.info.bv.dc, 180

        np.testing.assert_array_equal(raw.data['v'].to_numpy(), np.zeros(1000))
        np.testing.assert_array_equal(raw.data['i'].to_numpy(), np.arange(1000))

    def test_save(self, raw, tmp_path):
        raw.save(directory=tmp_path)

    def test_get_i(self, raw):
        np.testing.assert_array_equal(raw.get_i(), np.arange(1000))

    def test_get_i_stop(self, raw):
        np.testing.assert_array_equal(raw.get_i(stop=10), np.arange(10))

    def test_get_i_start_stop(self, raw):
        np.testing.assert_array_equal(raw.get_i(start=10, stop=20),
                                      np.arange(10, 20))

    def test_get_i_resampled(self, raw):
        assert len(raw.get_i(resample_to_freq=500)) == 100

    def test_get_i_resampled_same_rate(self, raw):
        i_original = raw.get_i()
        i = raw.get_i(resample_to_freq=5e3)

        np.testing.assert_array_equal(i, i_original)

    def test_plot(self, raw):
        fig, ax = raw.plot()

        assert isinstance(fig, plt.Figure)
        assert isinstance(ax, plt.Axes)

if __name__ == "__main__":
    sys.exit(pytest.main(["-qq"]))