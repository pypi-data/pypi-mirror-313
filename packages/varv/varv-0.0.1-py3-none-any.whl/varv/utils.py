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
import typing

from cycler import cycler

import scipy
import numpy as np
import matplotlib.pyplot as plt

def lowpass_filter(i, sfreq, cutoff_freq):
    b, a = scipy.signal.butter(3, cutoff_freq / sfreq)
    zi = scipy.signal.lfilter_zi(b, a)
    i, _ = scipy.signal.lfilter(b, a, i, zi=zi * i[0])
    return i


def check_if_array_is_half_cycle(a: np.ndarray, period: int) -> None:
    """Checks if array contains data on half a cycle

    Checks if array contains data on half a bias votlage cycle. Such an array
    is referred to a 'long' matrix by Noakes et. al. (2019). In such an array,
    each row now corresponds to a single voltage, as opposed to a single phase
    point (each voltage point corresponds to two phase points, one for the up
    swing of the voltage cycle and one for the down swing.

    Args:
        a (np.ndarray): An array to check.
        period (int): The period of the bias votlage cycle in samples.
    """
    if a.ndim != 2:
        raise ValueError('Error, expected array to be 2-dimensional.')
    elif a.shape[0] == period:
        raise ValueError(f'Error, expected half-cycle array to have '
                         f'{period // 2} rows, but instead got {a.shape[0]}. '
                         f'You might have accidentally used a full-cycle array '
                         f'instead.')
    elif a.shape[0] != period // 2:
        raise ValueError(f'Error, expected half-cycle array to have '
                         f'{period // 2} rows, but instead got {a.shape[0]}.')


def check_if_array_is_full_cycle(a: np.ndarray, period: int) -> None:
    """Checks if array contains data on half a cycle

    Checks if array contains data on the full bias votlage cycle. In such an
    array each column contains the voltage/current data of a full bias votlage
    cycle. Each voltage has two columns, one for the up swing of the voltage
    cycle and one for the down swing.

    Args:
        a (np.ndarray): An array to check.
        period (int): The period of the bias votlage cycle in samples.
    """
    if a.ndim != 2:
        raise ValueError('Error, expected array to be 2-dimensional.')
    elif a.shape[0] == period // 2:
        raise ValueError(f'Error, expected half-cycle array to have '
                         f'{period} rows, but instead got {a.shape[0]}. '
                         f'You might have accidentally used a half-cycle array '
                         f'instead.')
    elif a.shape[0] != period:
        raise ValueError(f'Error, expected half-cycle array to have '
                         f'{period} rows, but instead got {a.shape[0]}.')


def set_tu_delft_plotting_style():
    default_cycler = (cycler(color=[
        '#0076C2',
        '#EC6842',
        '#009B77',
        '#A50034',
        '#6F1D77',
        '#0C2340',
        '#EF60A3',
        '#6CC24A',
        '#FFB81C',
        '#00B8C8',
    ]))

    plt.rc('axes', prop_cycle=default_cycler)
    plt.rcParams["font.sans-serif"] = ["Arial"]

def get_phase_of_period(v_data: np.ndarray, period: int,
                        max_length_to_check: int = 10000,
                        min_amplitude: float = 1) -> int:
    """Finds the phase of a frequency of a known period.

    Args:
        v_data (np.ndarray): A numpy array containing the time series of bias
            voltage.
        period (int): The period in samples of the known bias frequency.
        max_length_to_check (int): Maximum number of samples in which to find a
            period and phase. Defaults to 10,000 samples. Speeds up Fourier
            transform.
        min_amplitude (float): The minimum amplitude in mV the bias frequency
            component should have. If this is not the case, the bias frequency
            is assumed to not be present and an error is raised.

    Returns:
        An integer specifying the phase (offset) in samples of the bias
        frequency signal.


    Raises:
        ValueError: This error is raised when no Fourier component of
            significant amplitude is found in the arrays. This might mean that
            no AC bias votlage was applied during the measurement.
    """
    N = min(max_length_to_check, len(v_data))
    x = v_data[:N]
    k = N / period  # Frequency to look for
    fourier_component = 1 / N * np.sum(
        x * np.exp(-1j * k * 2 * np.pi / N * np.arange(N))
    )

    if np.abs(fourier_component) < min_amplitude:
        raise ValueError(
            f'No AC voltage applied in first {N} points of file - could not '
            f'determine phase of component with period {period}. Found '
            f'component with magnitude {np.abs(fourier_component)}.')

    return get_phase_from_fourier_component(fourier_component, period)


def get_phase_from_fourier_component(fourier_component: np.complex128,
                                     period: int) -> int:
    """Finds the phase in samples for a known complex fourier component.

    The complex fourier component is assumed to be the component associated to
    the frequency equivalent to `period`.

    Args:
        fourier_component (np.complex128): A complex fourier component of
            frequency related to the period.
        period (int): The period in samples.

    Returns:
        The phase in samples of that complex component.
    """
    phase = round((np.angle(fourier_component) + np.pi) / (2 * np.pi) * period)
    return phase % period


def check_fname_for_ext(fname, ext):
    if os.path.splitext(fname)[1].lower() != f'.{ext}':
        fname = f'{fname}.{ext}'
    return fname


def downsample_by_poly(downsample_to_rate: float, f_samp: float,
                       arrays: typing.Union[np.ndarray, tuple, list]) -> tuple:
    """Downsample raw _events using SciPy.

    Better alternative to `downsample_by_mean`.

    Args:
        downsample_to_rate (float): Rate to downsample to in Hz.
        f_samp (float): Sample rate in Hz.
        arrays (np.ndarray): Array containing current/votlage events in pA.

    Returns:
        i_data: Array containing downsampled current events in pA.
        v_data: Array containing downsampled voltage events in mV.
    """
    # Weird problem where input has to be a float rather than int.
    # Otherwise, resampled to zeros.
    up = int(downsample_to_rate)
    down = int(f_samp)

    if up == down:
        return arrays

    if isinstance(arrays, np.ndarray) and arrays.ndim == 1:
        return scipy.signal.resample_poly(arrays.astype(np.float64),
                                          up, down)
    elif ((isinstance(arrays, np.ndarray) and arrays.ndim == 2)
          or isinstance(arrays, (tuple, list))):
        if isinstance(arrays, tuple):
            arrays = list(arrays)
        for i, array in enumerate(arrays):
            arrays[i] = scipy.signal.resample_poly(array.astype(np.float64),
                                                   up, down)
        return arrays

    else:
        raise ValueError(f'Unexpected array(s) to downsample. Expected single '
                         f'array or 2D/list of arrays but got: {type(arrays)}')


def downsample_by_mean(data, factor):
    """Downsample by taking averages.

    This might not be a smart way of downsampling:

    https://dsp.stackexchange.com/questions/58632/decimation-vs-mean-in-downsampling-operation

    Args:
        data: Array to downsample
        factor: Downsampling factor

    Returns:
        Downsampled array.

    """
    if factor == 1:
        return data
    num_dspts = len(data) // factor
    data = data[0:num_dspts * factor]
    newdata = np.mean(data.reshape(num_dspts, factor), axis=1)
    return newdata
