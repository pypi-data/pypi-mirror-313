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

import os
import copy
import typing
import itertools
from operator import itemgetter

import numpy as np
import pandas as pd
from tqdm import tqdm
from matplotlib import pyplot as plt


from varv import utils, base
from varv.preprocessing import changepoint_pc, changepoint, eventdetection


class Event(base.BaseData):

    def __init__(self, data: pd.DataFrame, info: base.Info = None,
                 steps: typing.Optional[pd.DataFrame] = None,
                 event_num: int = None):
        super().__init__(info, data)
        self.steps = steps
        self.event_num = event_num

    def set_event_num(self, event_num: int):
        self.event_num = event_num

    def find_steps(self, sensitivity: float = 1, min_level_length: int = 2,
                   verbose=False):

        i = self.get_i()

        if self.is_varv():
            period = self.get_bv_period()
            transitions, feat_vecs = changepoint_pc.step_finder(
                i, self.get_v(), period,
                sensitivity=sensitivity, verbose=verbose)
            self.steps = changepoint_pc.format_steps_df(
                transitions, feat_vecs, self.info.sfreq)

        else:
            results = changepoint.step_finder(
                i, sensitivity=sensitivity, min_level_length=min_level_length)
            self.steps = changepoint.format_steps_df(*results, sfreq=self.info.sfreq)

    def get_bv_period(self) -> int:
        return int(self.info.sfreq / self.info.bv.freq)

    def clear_steps(self):
        self.steps = None

    def _get_save_fname(self):
        if self.event_num is not None:
            return self.info.name + f'_eve_{self.event_num:04}'
        else:
            return self.info.name + '_eve'

    def save(self, fname: typing.Optional[os.PathLike] = None, directory=None):
        if fname is None:
            fname = self._get_save_fname()
        fname = utils.check_fname_for_ext(fname, 'h5')
        if directory:
            fname = os.path.join(directory, fname)

        store = pd.HDFStore(fname)

        store.put("nanoporedf", self.data)

        store.get_storer("nanoporedf").attrs.info = self.info
        store.get_storer("nanoporedf").attrs.steps = self.steps

        store.close()

    @classmethod
    def from_h5(cls, fname: typing.Union[os.PathLike, str]):
        fname = utils.check_fname_for_ext(fname, 'h5')

        with (pd.HDFStore(fname) as store):
            data = store['nanoporedf']
            info = store.get_storer('nanoporedf').attrs.info
            steps = store.get_storer('nanoporedf').attrs.steps
            type(info)

        return cls(data, info, steps)

    def plot(self, var="i", start: int = None, stop: int = None,
             lowpass=None,
             savefig=None, fig=None, ax=None,
             line_at_step=False,
             auto_units=True,
             show_open_pore_current: None | bool | tuple = None,
             **kwargs):
        """

        Args:
            var:
            start:
            stop:
            lowpass:
            savefig:
            fig:
            ax:
            line_at_step:
            auto_units:
            show_open_pore_current (:obj:`tuple`, optional): Setting for
                showing open pore current. When set to None, no open pore
                current is plotted. When set to True, a horizontal line is
                plotted at the open pore current. When set to a tuple,
                additional lines are drawn at percentages of the open pore
                current. For example, to show lines at 25% and 75% of the open
                pore current, set `show_open_pore_current=(0.25, 0.75)`.
                Defaults to None.
            **kwargs:

        Returns:

        """
        var = var.lower()
        if var not in ['i', 'v']:
            raise ValueError('Error, please set variable to plot "var" to '
                             'either "i" for current or "v" for voltage.')

        if 'alpha' not in kwargs:
            alpha = 1 if self.steps is None else 0.5
        else:
            alpha = kwargs.pop('alpha')

        x = self.get_time(start=start, stop=stop)
        as_ms = x[-1] - x[0] < 1 if auto_units else False

        fig, ax = self._plot(var, start, stop, fig, ax, lowpass, savefig,
                             as_ms=as_ms, alpha=alpha, **kwargs)

        if not self.is_varv() and self.steps is not None:
            if as_ms:
                x = self.get_time(as_ms=True)  # Need X values for alignment
            fig, ax = changepoint.plot_steps(self.steps,
                                             (x.min(), x.max()),
                                             fig=fig, ax=ax,
                                             line_at_step=line_at_step,
                                             zorder=10)

        if self.info.open_pore_current and show_open_pore_current:
            color = 'grey'
            ax.axhline(self.info.open_pore_current, color=color,
                    label='Open pore current')

            if isinstance(show_open_pore_current, tuple):
                lines = ["--", "-.", ":"]
                linecycler = itertools.cycle(lines)

                for percentage in show_open_pore_current:
                    ax.axhline(self.info.open_pore_current * percentage,
                            color=color,
                            linestyle=next(linecycler), alpha=0.5,
                            label=f'{percentage:.0%}')

                ax.axhspan(
                    self.info.open_pore_current * min(show_open_pore_current),
                    self.info.open_pore_current * max(show_open_pore_current),
                    color=color, alpha=0.05)

            ax.legend(loc='upper right')

        title = self.info.name + "\nEvent"
        if self.event_num is not None:
            title += f" {self.event_num}"

        ax.set_title(title)

        return fig, ax

    def plot_steps(self, fig: plt.Figure = None, ax: plt.Axes = None, plot_errors: bool = True, color='black'):
        if self.is_varv():
            traces, errors = changepoint_pc.get_traces_and_stds_from_steps_df(
                self.steps, plot_errors)

            xs = np.linspace(0, len(self.steps), traces.size).reshape(traces.shape)
            xs += 0.5

            if fig is None and ax is None:
                fig, ax = plt.subplots(figsize=(12, 4))

            if plot_errors:
                for x, trace, error in zip(xs, traces, traces):
                    ax.fill_between(x, trace - error, trace + error,
                                    color=color, alpha=0.1)

            ax.plot(xs.T, traces.T, color=color)

            ax.set_xticks(np.arange(len(self.steps)))
            ax.set_xlabel('Step number')
            ax.set_ylabel('Conductance (nS)')

            title = self.info.name + "\nEvent"
            if self.event_num is not None:
                title += f" {self.event_num}"

            ax.set_title(title)

            return fig, ax


    def _plot(self, var, start=None, stop=None,
              fig: plt.Figure = None, ax: plt.Axes = None,
              lowpass=False, savefig=False, legend=True, as_ms=False,
              **kwargs):

        if fig is None and ax is None:
            fig, ax = plt.subplots(figsize=(12, 4))

        x = self.get_time(as_ms=as_ms)[start:stop]
        y = self.get_data(var)[start:stop]

        if lowpass:
            y = utils.lowpass_filter(y, self.info.sfreq, lowpass)

        ax.plot(x, y, **kwargs)

        ax.set_xlabel(f'Time ({"ms" if as_ms else "s"})', fontsize=14)
        ax.set_ylabel(base.Y_LABELS[var], fontsize=14)

        ax.grid(True)
        if legend:
            ax.legend(loc=3)

        if savefig:
            savefig = utils.check_fname_for_ext(savefig, "png")
            fig.savefig(savefig, dpi=300)

        return fig, ax


class Events:

    def __init__(self, info: base.Info,
                 properties: pd.DataFrame,
                 events: typing.List[Event]):
        self.info = info

        if len(properties) != len(events):
            raise ValueError(f"Error, got data for {len(events)} _events but a "
                             f"properties table with {len(properties)} _events.")

        self.properties = properties
        self._events = events
        self.open_pore_fit = None

    def __add__(self, other):

        if isinstance(self, EmptyEvents):
            return other
        elif isinstance(other, EmptyEvents):
            return self
        elif isinstance(self, Events) and isinstance(other, Events):

            self.properties = pd.concat([self.properties, other.properties],
                                        axis=0)

            other.reassign_event_numbers(offset=len(self))
            self._events += other._events

            return self
        else:
            raise TypeError(f"Error, cannot concatenate object of type "
                            f"{type(self)} with object of type {type(other)}.")


    def __len__(self) -> int:
        return len(self._events)

    def __getitem__(self, item):
        if isinstance(item, (np.ndarray, list, slice)):
            e = copy.deepcopy(self)
            e.properties = self.properties.iloc[item, :]
            if isinstance(item, slice):
                e._events = self._events[item]
            else:
                e._events = list(itemgetter(*item)(self._events))
            e.properties.reset_index(inplace=True, drop=True)
            e.reassign_event_numbers()
            return e
        else:
            return self._events[item]
        # self._check_indexing(item)

    @classmethod
    def from_raw(cls, raw: base.Raw = None,
                 open_pore_current: tuple = (220, 250),
                 n_components_current: int = 3,
                 open_pore_current_extent: float = 0.999,
                 known_good_voltage: tuple = None,
                 n_components_voltage: int = 3,
                 ignore_voltage: bool = False,
                 boundary_trim: int = 5,
                 resample_to_freq: float = 5000,
                 max_samples: int = 1000000,
                 lowpass: float = None,
                 strict: bool = True,
                 verbose=False):
        """Find events in raw data.

        Applies event detection to find events in raw data.

        Args:
            raw (base.Raw): base.Raw object.
            open_pore_current (tuple): A tuple specifying the range in which
                the open state current lies. Units of pA. Defaults to
                (220, 250).
            n_components_current (int): Number of components for the GMM
                used to analyse the current. Defaults to 3.
            open_pore_current_extent (float): Extents of the open state
                current distribution found by the GMM that should be classified
                as indeed being open state current. Defaults to 0.999.
            known_good_voltage (:obj:`tuple`, optional): A tuple specifying the
                range in which the proper bias voltage lies. Defaults to None,
                in which case the bias voltage is found automatically. In this
                case, the bias voltage is assumed to be the distribution found
                by GMM with the largest mean. This method works well for
                constant-voltage data. For-variable voltage, GMM (naturally)
                has a hard time mapping a Gaussian distribution to the
                uniformly-distributed bias voltage sweep created by the
                triangle wave. In this case, specifying a range is necessary.
            n_components_voltage (int): Number of components for the GMM
                used to analyse the voltage. Defaults to 3.
            ignore_voltage (bool): If False, any events with irregular voltages
                are discarded. If True, voltage data is not used in event
                detection.
            boundary_trim (int): Integer specifying the amount of samples to
                trim off the end. Positive values result in trimmed ends.
                Negative values result in data around the edges of the event
                being added into the event data. Defaults to 5.
            resample_to_freq (float): A number specifying which sampling rate in Hz
                to resample the data to before running event detection.
                For measurements with a sampling rate >5 kHz (i.e.
                variable-voltage measurements), the recommended setting is 5
                kHz. Defaults to 5000. When set to None, resampling is disabled.
            max_samples (int): An integer specifying the maximum number of
                samples used for finding the open state current. If set to N,
                N/2 of the samples at the front of the data are used, along
                with N/2 of the samples at the end of the data. The data is
                split in half to account for drift in the open-state current.
            lowpass (float): A floating-point number that when set applies a
                low-pass filter with a cut-off point at that value in Hz.
                Defaults to None, for which the data is not filtered. For
                constant-voltage data, no lowpass filtering is necessary. For
                varviable-voltage measurements, it is recommended to set this
                value at half the bias voltage frequency.
            strict (bool): Boolean specifying whether to require events to be
                found. Defaults to True. When no open current within the
                specified range can be found, an error is thrown. If set to
                False, so error is raised, but an EmptyEvents is returned.
            verbose (bool): Boolean specifying whether to print progress.

        Returns:
            Events: Events object containing the found events.

        """
        GOOD_RANGE_TYPES = (list, tuple, np.ndarray)
        if not isinstance(open_pore_current, GOOD_RANGE_TYPES):
            raise TypeError('Error, parameter open_state_current should be a '
                            'tuple specifying the range in which to search for '
                            'an open state current.')
        if (known_good_voltage
                and not isinstance(known_good_voltage, GOOD_RANGE_TYPES)):
            raise TypeError('Error, parameter known_good_voltage should be a '
                            'tuple specifying the range of the bias votlage.')

        info = raw.info

        if verbose:
            print('Finding open pore current distribution... ', end='')

        try:
            eventdetection.find_open_state(raw,
                                           lower_bound=min(open_pore_current),
                                           upper_bound=max(open_pore_current),
                                           lowpass=lowpass,
                                           n_components=n_components_current,
                                           extent=open_pore_current_extent,
                                           resample_to_freq=resample_to_freq,
                                           max_samples=max_samples,
                                           verbose=verbose)
        except eventdetection.OpenStateNotFoundError as e:
            if strict:
                raise eventdetection.EventDetectionFailure(
                    'Error, cannot find any events. Please check settings. If '
                    'finding no events is acceptable, i.e. in a multi-channel '
                    'or multi-acquisition setting, set strict=False.') from e
            else:
                return EmptyEvents()

        if verbose:
            print('Done!')
            print('Finding erroneous voltages... ', end='')

        if not ignore_voltage:
            eventdetection.find_bad_voltages(
                raw,
                 known_good_voltage=known_good_voltage,
                 n_components=n_components_voltage,
                 resample_to_freq=resample_to_freq,
                 max_samples=max_samples,
                 verbose=verbose)

        if verbose:
            print('Done!')
            print('Creating events... ', end='')

        idxs = eventdetection.get_events_idxs(raw, boundary_trim=boundary_trim)
        events = []

        open_pore_fit = eventdetection.get_open_pore_fit(raw)
        open_pore_current = open_pore_fit(raw.get_t())

        for idx, row in idxs.iterrows():
            start = row['start_idx']
            end = row['end_idx']

            info = copy.copy(raw.info)
            info.start_idx = start
            info.open_pore_current = np.mean(open_pore_current[[start, end]])

            eve = Event(raw.data.truncate(before=start, after=end),
                        info=info, event_num=idx)
            eve.reset_indices()
            events.append(eve)

        if verbose:
            print('Done!')

        c = cls(info, idxs, events)

        c.open_pore_fit = open_pore_fit
        c.add_event_time()
        return c

    def add_event_time(self):
        self.properties['start_s'] = self.properties[
                                         'start_idx'] / self.info.sfreq
        self.properties['end_s'] = self.properties['end_idx'] / self.info.sfreq
        self.properties['dur_s'] = self.properties[
                                       'n_samples'] / self.info.sfreq

    def find_steps(self, sensitivity: float = 1, min_level_length: int = 2):
        for event in tqdm(self._events):
            event.find_steps(sensitivity, min_level_length)

    def reassign_event_numbers(self, offset: int = 0):
        for i, event in enumerate(self._events):
            event.set_event_num(i + offset)

    def get_event_numbers(self) -> np.ndarray:
        return np.array([event.event_num for event in self._events])


    def reset_labels(self, reset_to: int = 0):
        for event in self._events:
            event.info.label = reset_to


    def get_states(self, num) -> np.ndarray:
        return self[num].data['state'].to_numpy()

    def get_v(self, num) -> np.ndarray:
        return self[num].get_v()

    def get_i(self, num) -> np.ndarray:
        return self[num].get_i()

    def get_time(self, num):
        return self[num].get_time()

    def get_labels(self) -> np.ndarray:
        labels = np.zeros(len(self), dtype=int)
        for i, event in enumerate(self._events):
            labels[i] = event.info.label
        return labels

    def set_labels(self, labels) -> None:
        if len(self) != len(labels):
            raise ValueError(f'Error, tried to assign {len(labels)} labels to '
                             f'{len(self)} events.')

        for event, label in zip(self._events, labels):
            event.info.label = label

    def print_label_stats(self, label_df: pd.DataFrame = None):
        labels = self.get_labels()
        if label_df is not None:
            u_labels = label_df.label.to_numpy()
        else:
            u_labels = np.unique(labels).astype(int)

        nums = np.array([np.sum(labels == i)  for i in u_labels])
        perc = nums / len(self) * 100
        df = pd.DataFrame([
            u_labels,
            nums,
            perc,
        ], index=['Labels', 'No.', '%'], columns=label_df.description if label_df is not None else None
        ).astype(int)
        print(df)


    def _check_indexing(self, num):
        if not isinstance(num, int):
            raise TypeError("Error, must request event with integer index.")
        elif num < 0 or num >= len(self):
            raise IndexError(f"Error, expected an event index between 0 and "
                             f"{len(self) - 1}, but got {num}.")

    def save(self, fname: typing.Optional[os.PathLike] = None, directory: str = None, overwrite=True):
        if fname is None:
            if self.info.name is None:
                raise ValueError("Error, no name found in Info for creating "
                                 "file name. Try updating the Info or use the"
                                 "fname parameter.")
            fname = self.info.name + '_eves'
        fname = utils.check_fname_for_ext(fname, 'h5')

        if directory:
            fname = os.path.join(directory, fname)

        if overwrite:
            # Clear the file
            store = pd.HDFStore(fname, mode="w")
            store.close()

        store = pd.HDFStore(fname, mode='a')

        for i, event in enumerate(self._events):
            store.put(f"nanoporedf{i}", event.data)
            if event.steps:
                store.put(f"stepsdf{i}", event.steps)
            if event.info:
                store.get_storer(f"nanoporedf{i}").attrs.info = event.info

        store.put("properties_df", self.properties)

        store.get_storer("properties_df").attrs.info = self.info
        store.get_storer("properties_df").attrs.open_pore_fit = self.open_pore_fit
        store.close()

    @classmethod
    def from_h5(cls, fname: typing.Union[os.PathLike, str]):
        fname = utils.check_fname_for_ext(fname, 'h5')

        with pd.HDFStore(fname) as store:

            info = store.get_storer('properties_df').attrs.info
            open_state_fit = store.get_storer('properties_df').attrs.open_pore_fit
            idxs = store["properties_df"]

            events = []

            for i in range(store.root._v_nchildren - 1):
                event = Event(store[f'nanoporedf{i}'])

                if f'stepsdf{i}' in store:
                    event.steps = store[f'stepsdf{i}']

                handle = store.get_storer(f'nanoporedf{i}')
                if 'info' in handle.attrs:
                    event.info = handle.attrs['info']

                events.append(event)

        eves = cls(info, idxs, events)
        eves.open_pore_fit = open_state_fit
        return eves


    def filter_with_mask(self, good_idxs):
        good_idxs = np.array(good_idxs, dtype=bool)
        self.properties = self.properties.iloc[good_idxs, :]
        self._events = list(itertools.compress(self._events, good_idxs))
        self.properties.reset_index(inplace=True, drop=True)
        self.reassign_event_numbers()

    def filter_by_event_length(self, min_duration: float = 0.1, verbose=False):

        if 'dur_s' not in self.properties.columns:
            raise KeyError("Error, no key 'dur_s' found in event properties "
                           "dataframe. Try running Events.add_event_time "
                           "first.")

        good_idxs = self.properties['dur_s'] >= min_duration
        self.filter_with_mask(good_idxs)

        if verbose:
            print(f"Found {sum(good_idxs)} events from {len(good_idxs)} with "
                  f"a duration of {min_duration} seconds or longer.")

    def filter_by_current_range(self, current_range: tuple = (0.25, 0.75),
                                threshold: float = 0.9, verbose=False,
                                strict: bool = True) -> None:
        """Filters by comparing event current to open pore current.

        Gets the open pore current and determines the number of samples of that
        event that lie within a range determined relative to the open pore
        current. If the fraction of points within the range is above a
        threshold, the event is kept.

        Args:
            current_range (tuple): Tuple containing two values that set the
                range relative to the open pore current. For example, if the
                open pore current is 300 pA, `current_range=(0.333, 0.666)`
                would result in a range from 100 to 200 pA. Defaults to
                (0.25, 0.75).
            threshold (float): A float specifying the minimum fraction of
                samples which have to lie in the correct range for an event to
                be kept. Defaults to 0.9.
            verbose (bool): Whether to print information on the number of
                kept events.
            strict (bool): Whether to raise an exception if any of the events
                have no information on the open pore current. If set to False,
                the method works even for any events do not have open pore
                current. Such events are then kept. Defaults to True.
        """
        good_idxs = np.ones(len(self), dtype=bool)
        for i, event in enumerate(self._events):
            if event.info is None or event.info.open_pore_current <= 0:
                if strict:
                    raise ValueError(f'Error, Event {i} has not been '
                                     f'assigned an open pore current.')
                else:
                    continue

            upper_bound = event.info.open_pore_current * max(current_range)
            lower_bound = event.info.open_pore_current * min(current_range)

            in_range = (event.get_i() > lower_bound) & (event.get_i() < upper_bound)

            if sum(in_range) / len(event) < threshold:
                good_idxs[i] = False

        self.filter_with_mask(good_idxs)

        if verbose:
            print(f"Found {sum(good_idxs)} events from {len(good_idxs)} with "
                  f"at least {threshold:.0%} of samples within a range of "
                  f"{min(current_range):.0%}-{max(current_range):.0%} of the "
                  f"open pore current.")

    def plot(self, num, **kwargs):
        fig, ax = self[num].plot( **kwargs)
        return fig, ax


    def view(self, labels: dict = None):
        """Interactive viewer.

        Creates widget for viewing and labeling events. Requires `ipyml` and
        `ipywidgets`. Can also add colors and labels.

        See Also:
            varv.utils.eventviewer.EventViewer
            varv.utils.eventviewer.Label

        Args:
            labels:

        Returns:

        """
        from varv import widgets
        return widgets.EventViewer(self, labels)()



class EmptyEvents(Events):

    def __init__(self):
        super().__init__(base.EmptyInfo(), [], [])

    def filter_by_event_length(self, min_duration: float = 0.1, verbose=False):
        pass

    def filter_by_current_range(self, current_range: tuple = (0.25, 0.75),
                                threshold: float = 0.9, verbose=False,
                                strict: bool = True):
        pass
