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

import numpy as np
import pytest
import matplotlib.pyplot as plt

from varv.preprocessing import changepoint





def create_timeseries(step_heights, step_durations, snr):
    a = np.zeros(0)
    for step_height, steps_length in zip(step_heights, step_durations):
        a = np.append(a, np.full(steps_length, step_height))

    amp_signal = np.max(a) - np.min(a)

    if snr:
        a += np.random.normal(scale=amp_signal / snr, size=a.shape)

    return a

@pytest.fixture
def step_heights():
    return [0, 1, 0.5, 0.25, 0.75, 1]


@pytest.fixture
def step_durations():
    return [500, 600, 150, 400, 200, 250]


@pytest.fixture
def snr():
    """Signal-to-noise ratio.

    Returns:
        A floating point number describing the signal to noise ratio.

    """
    return 10


@pytest.fixture
def stepped_timeseries(step_heights, step_durations, snr):
    return create_timeseries(step_heights, step_durations, snr)


class TestChangePoint:

    def test_base_change_point_const_voltage(self, stepped_timeseries,
                                             step_heights, step_durations):
        results = changepoint.step_finder(stepped_timeseries, sensitivity=1.5)
        df = changepoint.format_steps_df(*results, sfreq=5000)

        np.testing.assert_allclose(df['mean'].to_numpy(), step_heights,
                                   atol=0.1)
        np.testing.assert_allclose(df['n_pts'].to_numpy(), step_durations,
                                   atol=5)

    def test_plot_steps(self, stepped_timeseries):
        results = changepoint.step_finder(stepped_timeseries, sensitivity=1.5)
        df = changepoint.format_steps_df(*results, sfreq=5000)

        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(stepped_timeseries)
        fig, ax = changepoint.plot_steps(df, fig=fig, ax=ax)

        assert isinstance(fig, plt.Figure)
        assert isinstance(ax, plt.Axes)

    def test_plot_steps_with_time_axis(self, stepped_timeseries):
        results = changepoint.step_finder(stepped_timeseries, sensitivity=1.5)
        df = changepoint.format_steps_df(*results, sfreq=5000)

        t = np.arange(len(stepped_timeseries)) * 5 + 100

        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(t, stepped_timeseries)
        fig, _ = changepoint.plot_steps(df, x_range=(t.min(), t.max()),
                                        fig=fig, ax=ax)

        # fig.show()


if __name__ == "__main__":
    sys.exit(pytest.main(["-qq"]))
