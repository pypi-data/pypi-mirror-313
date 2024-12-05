# Created by Cees Dekker Lab at the Delft University of Technology
# Refactored by Thijn Hoekstra
import ast
import io
import os
import re
import typing
import warnings

import numpy as np
import pandas as pd

from varv import base, utils


def load(filename: os.PathLike,
         downsample_to_freq: typing.Optional[float] = 5000) -> tuple:
    """Loads _events from nanopore LabView .dat files

    Loads _events from the nanopore setup that were saved as a `.dat` file.
    Expects a file that starts with an utf-8 encoded text header with
    measurements parameters (e.g., sample rate). This _events is then followed by
    binary _events of the samples.

    After reading the _events, it is downsampled by default. This behaviour can
    be turned off.

    Args:
        filename (str): Path to the `.dat` file
        downsample_to_freq (:obj:`float`, optional): Rate to downsample the
            _events to. Defaults to 5000 Hz. Set to None for no downsampling.

    Returns:
        v_data (np.ndarray): An array containing the voltage _events in mV.
        i_data (np.ndarray): An array containing the current _events in pA.
        sfreq (float): (Downsampled) sample rate in Hz
        bdc (str): LongInfo on bias voltage.
    """
    _, ext = os.path.splitext(filename)
    if ext.lower() != '.dat':
        warnings.warn(f"Error, file has extension {ext}, expecting .dat. "
                      f"Are you using the correct file?")

    with open(filename, 'rb') as f:
        header = read_header(f)
        d = dictionary_from_header(header)

        alpha = d.get('ALPHA')
        beta = d.get('BETA')
        station = d.get('STATION')
        v_bias = d.get('voltage')
        coeff_0 = d.get('Coeff0')
        coeff_1 = d.get('Coeff1')
        coeff_2 = d.get('Coeff2')
        coeff_3 = d.get('Coeff3')
        sfreq = d.get('fSamp')
        f_3dB = d.get('f3dB')
        filenum = d.get('filenum')

        # Locate start position
        start_pos = f.tell()
        f.seek(0, 2)
        l = (f.tell() - start_pos) // 2
        num_mb = l * 2 / 1048576

        print(filename)
        print("Reading... ")
        print(f"{num_mb:.3f} MB")
        print(f"Raw at {sfreq:,.0f} Hz")

        f.seek(start_pos)
        total_read = 0
        raw_data = np.zeros(l, dtype=np.int16)
        while total_read < l:
            # printstring = f"{total_read / l * 100:.2f}%"
            # print(printstring, end="")
            read_this_time = min(10000000, l - total_read)
            raw_data[total_read:total_read + read_this_time] = np.fromfile(
                f, dtype=np.int16, count=read_this_time)
            # print("\b" * (len(printstring) - 1))
            total_read += read_this_time

        raw_v_data = raw_data[1::2]
        raw_i_data = raw_data[::2]

    if downsample_to_freq:
        print("Downsampling... ")
        i_data, v_data = utils.downsample_by_poly(downsample_to_freq, sfreq,
                                            (raw_i_data, raw_v_data))
        sfreq = downsample_to_freq
    else:
        i_data = raw_i_data
        v_data = raw_v_data

    print("Calibrating...")
    i_data = (coeff_0 + coeff_1 * i_data + coeff_2 * i_data ** 2) * 1000 / (
            alpha * beta)
    v_data = (coeff_0 + coeff_1 * v_data + coeff_2 * v_data ** 2) * 1000 / (
            alpha * beta)

    print("Done!")
    return v_data, i_data, sfreq, v_bias


def read_measurement_dat(filename: os.PathLike,
                         downsample_to_freq: typing.Optional[float] = 5000,
                         bfreq: float = 0,
                         bamp: float = 0,
                         ) -> base.Raw:
    name = os.path.splitext(os.path.basename(filename))[0]
    v_data, i_data, sfreq, bdc = load(filename, downsample_to_freq)
    return base.Raw.from_arrays(i_data, v_data, sfreq, name=name, bdc=bdc, bamp=bamp, bfreq=bfreq)


def read_header(f: typing.BinaryIO) -> str:
    """Reads header.

    Reads header of the `.dat` file. Expects the last entry in the header to
    be "filenum=0;"

    Args:
        f: A file to read from.

    Returns:
        A string containing the header.

    """
    s = ''
    while True:
        try:
            line = f.readline().decode('utf-8').strip()
            s += line
            if line.startswith('filenum'):
                break
        except UnicodeDecodeError:
            break

    return s


def dictionary_from_header(s: str) -> dict:
    """Converts header to a dictionary.

    Converts a header with _events stored as lines "param_name=param_value;" into
    a dictionary with param_name as keys and param_value as values.

    Args:
        s (str): A string containing the header text.

    Returns:
        A dictionary of the values in the header text.

    """
    s = re.sub(r'([A-z]\w+)', r'"\1"', s)
    s = re.sub('=', ' : ', s)
    s = re.sub(';', ' , ', s)
    s = '{' + s + '}'
    return ast.literal_eval(s)


def dat_to_csv(filepath: os.PathLike,
               export_path: typing.Optional[os.PathLike] = None,
               downsample_to_freq: typing.Optional[float] = 5000) -> None:
    """Convert LabView .dat file to .csv file.

    Converts _events from the nanopore setup that were saved as a `.dat` file into
    `.csv` files. Data is downsampled by default. This behaviour can
    be turned off.

    Args:
        filepath (os.PathLike): Path of the LabView .dat file.
        export_path (:obj:`os.PathLike`, optional): Optional export path.
            defaults to None and places `.csv` in same directory as the `.dat`
            file.
        downsample_to_freq (:obj:`float`, optional): Rate to downsample the
            _events to. Defaults to 5000 Hz. Set to None for no downsampling.
    """
    i_data, v_data, _, _ = load(filepath, downsample_to_freq)
    time_col = np.arange(len(i_data)) / downsample_to_freq

    export_df = pd.DataFrame(
        data={"time(s)": time_col,
              "current(pA)": i_data,
              "voltage(mV)": v_data})
    export_df = export_df.astype("float32")

    path, filename = os.path.split(filepath)
    filename = filename.split(".")[0]

    if isinstance(export_path, io.StringIO):
        path_or_buf = export_path
    elif export_path is not None:
        path_or_buf = export_path + filename + ".csv"
    else:
        path_or_buf = path + filename + ".csv"

    export_df.to_csv(path_or_buf, index=False)
