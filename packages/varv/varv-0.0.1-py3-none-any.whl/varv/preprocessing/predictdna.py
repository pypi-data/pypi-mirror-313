# Created by Cees Dekker Lab at the Delft University of Technology
# Refactored by Thijn Hoekstra

from importlib import resources as impresources
from varv.preprocessing import assets

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

inp_file = impresources.files(assets) / 'temp_file'
MODEL_CSV = 'DNA_6mer_prediction_model.csv'


def moving_6mer_substrings(string):
    window_size = 6
    str_length = len(string)
    return [string[i:i + window_size] for i in
            range(str_length - window_size + 1)]


def get_model_path(csv_filename):
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the CSV file
    csv_path = os.path.join(current_dir, csv_filename)
    return csv_path


def predict_dna_6mer_5_3(template, LUT_6mer=None):

    if LUT_6mer is None:
        f = impresources.files(assets) / MODEL_CSV
        LUT_6mer = pd.read_csv(f)

    template = template[::-1]  # Reverse the string (3'->5')
    constriction_kmer_offset = -4

    sub_6mer = moving_6mer_substrings(template)
    DNA_prediction_mean = np.zeros(len(sub_6mer) * 2)
    DNA_prediction_std = np.zeros(len(sub_6mer) * 2)

    for str_i, kmer in enumerate(sub_6mer):
        kmer_index = LUT_6mer.index[LUT_6mer['kmer_pull_3_5'] == kmer].tolist()
        if kmer_index:
            kmer_index = kmer_index[0]
            DNA_prediction_mean[str_i * 2] = LUT_6mer.loc[
                kmer_index, 'pre_mean']
            DNA_prediction_mean[str_i * 2 + 1] = LUT_6mer.loc[
                kmer_index, 'post_mean']
            DNA_prediction_std[str_i * 2] = LUT_6mer.loc[kmer_index, 'pre_std']
            DNA_prediction_std[str_i * 2 + 1] = LUT_6mer.loc[
                kmer_index, 'post_std']

    # Organize results into DataFrame
    result_length = 2 * len(template)
    mean = np.full(result_length, np.nan)
    std = np.full(result_length, np.nan)
    base = [''] * result_length
    mode = [''] * result_length
    step = np.arange(0, result_length) + constriction_kmer_offset

    start_index = -constriction_kmer_offset
    end_index = len(DNA_prediction_mean) - constriction_kmer_offset
    mean[start_index:end_index] = DNA_prediction_mean
    std[start_index:end_index] = DNA_prediction_std

    for str_i in range(len(template)):
        base[2 * str_i] = template[str_i]
        base[2 * str_i + 1] = template[str_i]
        mode[2 * str_i] = 'pre'
        mode[2 * str_i + 1] = 'post'

    table_result = pd.DataFrame({
        'step': step,
        'base': base,
        'mode': mode,
        'mean': mean,
        'std': std
    })

    return table_result


def visualize_template_dna(DNA_prediction_results):
    nan_filter = DNA_prediction_results['mean'].notna()

    # Create plot
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.grid(True)

    # Plot assets
    ax.step(DNA_prediction_results[nan_filter]['step'],
            DNA_prediction_results[nan_filter]['mean'], where='mid',
            linewidth=1.3)
    ax.errorbar(DNA_prediction_results[nan_filter]['step'],
                DNA_prediction_results[nan_filter]['mean'],
                yerr=DNA_prediction_results[nan_filter]['std'], fmt='none',
                elinewidth=1)

    # Add base labels
    base_y_coor = 0.13
    for i in range(0, len(DNA_prediction_results), 2):
        base_char = DNA_prediction_results['base'].iloc[i]
        base_coor = DNA_prediction_results['step'].iloc[i] + 0.5
        ax.text(base_coor, base_y_coor, base_char, fontsize=12)

    # Set axis limits and labels
    ax.set_ylim(0.1, 0.5)
    ax.set_xlim(-4, len(DNA_prediction_results) - 2)
    ax.set_xlabel('Step number', fontsize=15)
    ax.set_ylabel('Relative levels', fontsize=15)
    ax.tick_params(axis='both', which='major', labelsize=12)

    # Show plot
    # plt.show()
    # plt.savefig(f'{plots_path}template_DNA_prediction.svg')
    # plt.savefig(f'{plots_path}template_DNA_prediction.png', dpi=300)
    return None
