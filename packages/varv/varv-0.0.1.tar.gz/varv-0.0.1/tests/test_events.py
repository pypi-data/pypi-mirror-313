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

import pytest
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from varv import base
from varv import events
from varv.events import Events


DATA_FILE_CV = pathlib.Path(__file__).parent.joinpath(
    'assets', 'test_data_constant_voltage.h5')


@pytest.fixture
def info():
    """Info with open pore current"""
    return base.Info(5000, 'ABC', base.BiasVoltage(180, 0, 0), open_pore_current=200)

@pytest.fixture
def info_no_open_pore_current():
    """Info with open pore current"""
    return base.Info(5000, 'ABC')

@pytest.fixture
def raw(info):
    data = pd.read_hdf(DATA_FILE_CV, 'df')
    raw = base.Raw(data, info)
    raw.reset_states()
    return raw

@pytest.fixture
def data():
    return pd.DataFrame({
        'i': np.full(10, 100),
        'v': np.full(10, 180)})


@pytest.fixture
def data_low_current():
    return pd.DataFrame({
        'i': np.full(10, 10),
        'v': np.full(10, 180)})

@pytest.fixture
def event(data, info):
    return events.Event(data, info)

@pytest.fixture
def event_low_current(data_low_current, info):
    return events.Event(data_low_current, info)

@pytest.fixture
def event_no_open_pore_current(data, info_no_open_pore_current):
    return events.Event(data, info_no_open_pore_current)

@pytest.fixture
def eves_a(info, event):
    properties = pd.DataFrame(
        {'dur_s': [3, 1, 2, 5],
         'start_idx': [1, 2, 3, 4],
         'end_idx': [11, 12, 13, 14]})
    eves = [event for _ in range(4)]
    return Events(info, properties, eves)

@pytest.fixture
def eves_b(info, event, event_low_current, event_no_open_pore_current):
    properties = pd.DataFrame(
        {'dur_s': [2, 3, 3, 6],
         'start_idx': [2, 3, 4, 5],
         'end_idx': [12, 13, 14, 15]})
    eves = [event_no_open_pore_current, event, event_low_current, event]
    return Events(info, properties, eves)

class TestEvent:

    def test_event_save_and_load(self, event, tmp_path):
        event.save('event_a', tmp_path)
        event_a_loaded = events.Event.from_h5(tmp_path / 'event_a.h5')

        assert len(event_a_loaded) == 10

    def test_event_change_point(self, event):
        event.find_steps()

        assert len(event.steps) == 1
        assert event.steps['mean'][0] == 100

class TestEvents:

    def test_events_creation(self, raw):
        eves = events.Events.from_raw(raw)

        assert len(eves) == pytest.approx(110, abs=5)
        assert len(eves.properties.columns) == 6

    def test_events_save_and_load(self, eves_a, tmp_path):
        eves_a.save('events_a', tmp_path)
        eves_a_loaded = Events.from_h5(tmp_path / 'events_a.h5')

        assert len(eves_a_loaded) == 4
        assert len(eves_a_loaded.properties) == 4

    def test_events_plot(self, eves_a):
        fig, ax = eves_a.plot(0)

        assert isinstance(fig, plt.Figure)
        assert isinstance(ax, plt.Axes)

        # fig.show()

    def test_events_plot_with_filtering(self, eves_a):
        fig, ax = eves_a.plot(0, lowpass=100)

        assert isinstance(fig, plt.Figure)
        assert isinstance(ax, plt.Axes)

    def test_event_concatenation(self, eves_a, eves_b):
        eves = eves_a + eves_b

        assert len(eves) == 8
        assert eves.properties.shape == (8, 3)
        assert eves.info.sfreq == 5000

    def test_event_creation_error(self, info, event):
        d = {'dur_s': [3, 1, 2, 5],
             'start_idx': [1, 2, 3, 4],
             'end_idx': [11, 12, 13, 14]}
        properties = pd.DataFrame(data=d)

        eves = [event for _ in range(3)]

        with pytest.raises(ValueError):
            events.Events(info, properties, eves)

    def test_event_filtering_by_mask(self, eves_a):

        eves_a.filter_with_mask([1, 0, 1, 1])

        assert len(eves_a) == 3
        np.testing.assert_array_equal(
            eves_a.properties['dur_s'].to_numpy(), np.array([3, 2, 5]))
        np.testing.assert_array_equal(
            eves_a.properties['start_idx'].to_numpy(), np.array([1, 3, 4]))
        np.testing.assert_array_equal(
            eves_a.properties['end_idx'].to_numpy(), np.array([11, 13, 14]))

    def test_event_slice_by_idxs_list(self, eves_a):

        eves_a = eves_a[[0, 3]]

        assert len(eves_a) == 2
        np.testing.assert_array_equal(eves_a.properties['dur_s'].to_numpy(),
                                      np.array([3, 5]))
        np.testing.assert_array_equal(eves_a.properties['start_idx'].to_numpy(),
                                      np.array([1, 4]))
        np.testing.assert_array_equal(eves_a.properties['end_idx'].to_numpy(),
                                      np.array([11, 14]))

    def test_event_filtering_by_length(self, eves_a):

        eves_a.filter_by_event_length(min_duration=2)

        assert len(eves_a) == 3
        np.testing.assert_array_equal(
            eves_a.properties['dur_s'].to_numpy(), np.array([3, 2, 5]))
        np.testing.assert_array_equal(
            eves_a.properties['start_idx'].to_numpy(), np.array([1, 3, 4]))
        np.testing.assert_array_equal(
            eves_a.properties['end_idx'].to_numpy(), np.array([11, 13, 14]))

    def test_event_filtering_by_current_error(self, eves_b):
        """Error because no open pore current"""
        with pytest.raises(Exception):
            eves_b.filter_by_current_range()

    def test_event_filtering_by_current(self, eves_b):

        eves_b.filter_by_current_range(strict=False)
        assert len(eves_b) == 3

    def test_event_change_point(self, eves_a):
        eves_a.find_steps()

        for eve in eves_a:
            assert len(eve.steps) == 1
            assert eve.steps['mean'][0] == 100

    def test_event_change_point_plot(self, eves_a):
        eves_a.find_steps()

        fig, ax = eves_a.plot(0)
        assert isinstance(fig, plt.Figure)
        assert isinstance(ax, plt.Axes)

if __name__ == "__main__":
    sys.exit(pytest.main(["-qq"]))

