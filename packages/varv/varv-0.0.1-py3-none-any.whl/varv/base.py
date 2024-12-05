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
#


import os
import copy
import typing

import scipy
import scipy.signal
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from varv import utils
from varv.utils import downsample_by_poly

Y_LABELS = {"v": "Voltage (mV)",
            "i": "Current (pA)"}

UNLABELED_STATE = -1
GOOD_STATE = 0
OPEN_STATE = 1
BAD_VOLTAGE_STATE = 2
STATES = {UNLABELED_STATE: 'Unlabeled',
          GOOD_STATE: 'Good',
          BAD_VOLTAGE_STATE: 'Bad Voltage',
          OPEN_STATE: 'Open'}

class BiasVoltage:

    def __init__(self, dc, amp: float = 0, freq: float = 0):
        self.dc = dc
        self.amp = amp
        self.freq = freq

    def is_varv(self):
        return self.freq > 0 and self.amp > 0


class Info:

    def __init__(self, sfreq: float,
                 name: str = None,
                 bv: BiasVoltage = None,
                 start_idx = 0,
                 chan_num: int = 0,
                 label: int = 0,
                 open_pore_current = 0):
        self.sfreq: float = sfreq
        self.bv = bv if bv else BiasVoltage(0)
        self.name = name
        self.start_idx = start_idx
        self.chan_num = chan_num
        self.label = label
        self.open_pore_current = open_pore_current

    def __str__(self):
        return self.as_dataframe().__str__()

    def as_dataframe(self):
        df = pd.DataFrame({"": [
            self.name,
            self.chan_num,
            self.start_idx,
            self.label,
            f'{self.sfreq:.2f} Hz',
            f'{self.bv.dc:.2f} Hz',
            f'{self.bv.amp:.2f} pA',
            f'{self.bv.freq:.2f} Hz',
            f'{self.open_pore_current:.2f} pA',
        ]})
        df.index = [
            'Name',
            'Channel No.',
            'Start Index',
            'Label',
            'Sampling Rate',
            'Bias Voltage DC',
            'Bias Voltage Amplitude',
            'Bias Voltage Frequency',
            'Open Channel Current',
        ]
        return df

    def shorten(self):
        return self  # Is already short


class BaseData:

    def __init__(self, info: Info, data: pd.DataFrame):
        self.info = info
        self.data = data

    def __len__(self):
        return len(self.data.index)

    def __str__(self):
        df = self.info.as_dataframe()
        df_dur = pd.DataFrame([
            [f'{self.get_dur():.2f} s'],
            [f'{len(self)}']
        ],
                              columns=[''])
        df_dur.index = ['Duration', 'No. Samples']
        df = pd.concat([df_dur, df])
        return df.__str__()

    def is_varv(self):
        return bool(self.info.bv.is_varv())

    def _get_save_fname(self):
        return self.info.name

    def save(self, fname: typing.Optional[os.PathLike] = None, directory=None):
        if fname is None:
            fname = self._get_save_fname()
        fname = utils.check_fname_for_ext(fname, 'h5')
        if directory:
            fname = os.path.join(directory, fname)

        store = pd.HDFStore(fname)

        store.put("nanoporedf", self.data)

        store.get_storer("nanoporedf").attrs.info = self.info

        store.close()

    @classmethod
    def from_h5(cls, fname: typing.Union[os.PathLike, str]):
        fname = utils.check_fname_for_ext(fname, 'h5')

        with (pd.HDFStore(fname) as store):
            data = store['nanoporedf']
            info = store.get_storer('nanoporedf').attrs.info
            type(info)

        return cls(data, info)

    def get_data(self, var: typing.Optional[str] = None, start=None, stop=None,
                 resample_to_freq: float = None):
        if var:
            data = self.data[var].iloc[start:stop].to_numpy()
        else:
            data = self.data.iloc[start:stop]

        if resample_to_freq:
            if isinstance(data, pd.DataFrame):
                data = data.to_numpy()
            data = downsample_by_poly(resample_to_freq, self.info.sfreq, data)

        return data

    def set_data(self, var, data):
        self.data[var] = data

    def get_time(self, start=None, stop=None, as_ms=False):
        t = np.arange(len(self.data))[start:stop] / self.info.sfreq
        if as_ms:
            t *= 1e3
        return t

    def get_t(self, **kwargs):
        return self.get_time(**kwargs)

    def get_dur(self):
        return len(self) / self.info.sfreq

    def get_v(self, start=None, stop=None, **kwargs) -> np.ndarray:
        return self.get_data('v', start, stop, **kwargs)

    def get_i(self, start=None, stop=None, **kwargs) -> np.ndarray:
        return self.get_data('i', start, stop, **kwargs)

    def get_g(self, start=None, stop=None, **kwargs) -> np.ndarray:
        return self.get_data('g', start, stop, **kwargs)

    def has_g(self):
        return 'g' in self.data

    def get_states(self) -> np.ndarray:
        return self.data['state'].to_numpy()

    def notch_filter(self, f0, Q, var='i'):
        """

        Args:
            f0: Frequency to be removed from signal (Hz)
            Q: Quality factor
        """

        freqs = np.arange(f0, self.get_nyquist(), f0)
        filters = [scipy.signal.iirnotch(f, Q, self.info.sfreq) for f in freqs]

        sos = np.block([[b, a] for b, a in filters])
        filtered = copy.deepcopy(self)

        x = self.get_data(var)
        x = scipy.signal.sosfilt(sos, x)

        filtered.data[var] = x

        return filtered

    def get_nyquist(self):
        return self.info.sfreq / 2

    def _plot(self, var, start=None, stop=None,
              fig: plt.Figure = None, ax: plt.Axes = None,
              lowpass=False, savefig=False, legend=True, scatter=None,
              **kwargs):

        if fig is None and ax is None:
            fig, ax = plt.subplots(figsize=(12, 4))

        x = self.get_time()[start:stop]
        y = self.get_data(var)[start:stop]
        s = self.get_states()[start:stop]

        if scatter is None:
            scatter = len(x) > 200

        if lowpass:
            y = utils.lowpass_filter(y, self.info.sfreq, lowpass)

        for state in np.unique(s):
            mask = s == state
            if scatter:
                ax.scatter(x[mask],
                           y[mask],
                           s=1, label=f"{STATES[state]}", **kwargs)
            else:
                ax.plot(x[mask], y[mask],
                        label=f"{STATES[state]}", **kwargs)

        ax.set_xlabel('Time (s)', fontsize=14)
        ax.set_ylabel(Y_LABELS[var], fontsize=14)

        ax.grid(True)
        if legend:
            ax.legend(loc=3)

        if savefig:
            savefig = utils.check_fname_for_ext(savefig, "png")
            fig.savefig(savefig, dpi=300)

        return fig, ax

    def truncate(self, before=None, after=None, inplace=True):
        if inplace:
            self.data = self.data.truncate(before=before, after=after)
        else:
            new_obj = copy.deepcopy(self)
            new_obj.truncate(before=before, after=after)
            return new_obj

    def reset_indices(self):
        """Resets indices of data

        """
        self.info.start_idx = self.data.index[0]
        self.data.reset_index(inplace=True, drop=True)



class Raw(BaseData):

    def __init__(self, data: pd.DataFrame, info: Info):
        super().__init__(info, data)

        if 'state' not in self.data.columns:
            self.set_states()

    def _get_save_fname(self):
        return self.info.name + '_raw'

    def set_states(self, states: np.ndarray = None):

        if states is None:
            states = 0
        else:
            assert len(states) == len(self.data), ("States not same "
                                                   "length as _events")
        # TODO also make so it can change existing state column
        self.data.insert(len(self.data.columns), "state", states)

    def reset_states(self):
        self.data['state'] = GOOD_STATE

    def get_states(self) -> np.ndarray:
        return self.data['state'].to_numpy()

    @classmethod
    def from_arrays(cls, i_data: np.ndarray, v_data: np.ndarray, sfreq: float, name: str = '', bdc: float = 180,
                    bamp: float = 0, bfreq: float = None):
        return cls(pd.DataFrame(data=np.vstack([v_data, i_data]).T,
                                columns=['v', 'i']),
                   Info(sfreq, name, bv=BiasVoltage(bdc, bamp, bfreq)))

    def plot(self, var="i", start: int = None, stop: int = None,
             lowpass=None,
             savefig=None, fig=None, ax=None, **kwargs):

        var = var.lower()
        if var not in ['i', 'v']:
            raise ValueError('Error, please set variable to plot "var" to '
                             'either "i" for current or "v" for voltage.')

        fig, ax = self._plot(var, start, stop, fig, ax, lowpass, savefig,
                             **kwargs)

        if var == "i" and not self.is_varv():
            ax.set_ylim([0, 250])

        ax.set_title(self.info.name + f"\nRaw")

        return fig, ax


def read_measurement_h5(fname: typing.Optional[os.PathLike]):
    """Wrapper for reading measurement from HDF5

    Wrapper for varv.base.Measurement.from_h5

    Args:
        fname:

    Returns:

    """
    return Raw.from_h5(fname)


class EmptyInfo(Info):

    def __init__(self):
        super().__init__(0)
