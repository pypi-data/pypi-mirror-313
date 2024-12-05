# Created by Ruben Marchau
# Refactored and documented by Thijn Hoekstra

from typing import Optional

import scipy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture

from varv import base, utils

class OpenStateNotFoundError(Exception):
    pass

class EventDetectionFailure(Exception):
    pass


def get_components(a: np.ndarray, n_components: int):
    """Gets Gaussian components describing a dataset

    Fits a Gaussian Mixture Model (GMM) to the dataset and extracts the
    components.

    This function takes a 1D dataset `a` and fits a Gaussian Mixture Model
    (GMM) with a specified number of components (`n_components`). It returns
    the means, standard deviations, and weights of the Gaussian components
    that best describe the dataset.

    Args:
        a (np.ndarray): A 1D array representing the dataset to fit.
        n_components (int): The number of Gaussian components to fit.

    Returns:
        tuple: A tuple containing:
            - means (np.ndarray): The means of the Gaussian components.
            - stds (np.ndarray): The standard deviations of the Gaussian
                components.
            - weights (np.ndarray): The weights (mixing proportions) of the
            Gaussian components.

    Example:
        >>> import numpy as np
        >>> np.random.seed(0)
        >>> a = np.random.randn(1000)
        >>> means, stds, weights = get_components(a, 3)
        >>> print("Means:", means)
        >>> print("Standard Deviations:", stds)
        >>> print("Weights:", weights)
    """
    data = a.reshape(-1, 1)
    gm = GaussianMixture(n_components=n_components, random_state=0).fit(data)
    means = gm.means_.flatten()
    stds = np.sqrt(gm.covariances_.flatten())
    weights = gm.weights_
    return means, stds, weights


def select_component(means: np.ndarray, stds: np.ndarray, weights: np.ndarray,
                     lower_bound: float,
                     upper_bound: float):
    """Selects most abundant Gaussian component

    Selects the most abundant Gaussian component within a specified range of
    means.

    This function takes the means, standard deviations, and weights of
    Gaussian components and selects the component with the highest weight
    (most abundant) whose mean lies between `lower_bound` and `upper_bound`.
    If no components are found in this range, it returns `None`.

    Args:
        means (np.ndarray): An array of the means of the Gaussian components.
        stds (np.ndarray): An array of the standard deviations of the Gaussian
            components.
        weights (np.ndarray): An array of the weights (mixing proportions) of
            the Gaussian components.
        lower_bound (float): The lower bound for the range of acceptable
            component means.
        upper_bound (float): The upper bound for the range of acceptable
            component means.

    Returns:
        tuple: A tuple containing:
            - selected_mean (float or None): The mean of the selected Gaussian
                component, or `None` if no component is found.
            - selected_std (float or None): The standard deviation of the
                selected Gaussian component, or `None` if no component is found.
            - selected_weight (float or None): The weight of the selected
                Gaussian component, or `None` if no component is found.

    Example:
        >>> import numpy as np
        >>> means = np.array([1.0, 2.5, 3.0])
        >>> stds = np.array([0.5, 0.4, 0.6])
        >>> weights = np.array([0.2, 0.5, 0.3])
        >>> lower_bound = 2.0
        >>> upper_bound = 3.0
        >>> select_component(means, stds, weights, lower_bound, upper_bound)
            (2.5, 0.4, 0.5)
    """

    # Filter components within the specified range
    valid_indices = np.where((means > lower_bound) & (means < upper_bound))[0]
    if len(valid_indices) == 0:
        return None, None, None  # No components in the specified range

    # Select the most abundant component within the range
    most_abundant_index = valid_indices[np.argmax(weights[valid_indices])]
    return means[most_abundant_index], stds[most_abundant_index], weights[
        most_abundant_index]


def sort_components(means: np.ndarray, stds: np.ndarray, weights: np.ndarray):
    """Sorts Gaussian components by their means in descending order.

    This function takes the means, standard deviations, and weights of Gaussian
    components and sorts them in descending order based on the means. The
    standard deviations and weights are reordered accordingly to match the
    sorted means.

    Args:
        means (np.ndarray): An array of the means of the Gaussian components.
        stds (np.ndarray): An array of the standard deviations of the Gaussian
            components.
        weights (np.ndarray): An array of the weights of the Gaussian
            components.

    Returns:
        tuple: A tuple containing:
            - sorted_means (np.ndarray): The means of the Gaussian components
                sorted in descending order.
            - sorted_stds (np.ndarray): The standard deviations sorted to match
                the sorted means.
            - sorted_weights (np.ndarray): The weights sorted to match the
                sorted means.

    Example:
        >>> import numpy as np
        >>> means = np.array([1.5, 2.0, 1.0])
        >>> stds = np.array([0.3, 0.2, 0.4])
        >>> weights = np.array([0.4, 0.3, 0.3])
        >>> sorted_means, sorted_stds, sorted_weights = sort_components(means, stds, weights)
        >>> sorted_means
            np.array([2.0, 1,5, 1.0])
        >>> sorted_stds
            np.array([0.2, 0.3, 0.4])
        >>> sorted_weights
            np.array([0.3, 0.4, 0.3]))
    """
    indices = np.argsort(means)[::-1]
    means = means[indices]
    stds = stds[indices]
    weights = weights[indices]
    return means, stds, weights


def get_open_state_current_distr(i: np.ndarray, lower_bound: float,
                                 upper_bound: float, n_components: int = 3):
    """Gets open state current distribution

    Computes the Gaussian component describing the distribution of the
    open-state current.

    This function takes numpy array with the current trace and fits a
    Gaussian Mixture Model (GMM) with the specified number of components
    (`n_components`) to the current. It then selects the most abundant Gaussian
    component within the given range.

    Args:
        i (np.ndarray): A numpy array with the current assets
        lower_bound (float): The lower bound of the current range in which to
            find a component
        upper_bound (float): The upper bound of the current range in which to
            find a component
        n_components (int, optional): The number of Gaussian components to fit.
            Default is 3.

    Returns:
        list or None: A list containing the mean, standard deviation, and
            weight of the selected Gaussian component, or `None` if no
            component is found within the range.

    # TODO update doctstring
    Example:
        >>> i = np.random.randn(1000)
        >>> lower_bound = 220
        >>> upper_bound = 250
        >>> open_state, _, _ = get_open_state_current_distr(i, lower_bound, upper_bound)
    """
    components = get_components(i, n_components)

    means, stds, _, = sort_components(*components)

    mean, std, weight = select_component(*components, lower_bound, upper_bound)

    if mean is None:
        raise OpenStateNotFoundError(
            f"Error, could not find a current distribution within the bounds "
            f"({lower_bound}, {upper_bound}) pA. Found components have means "
            f"at {', '.join(np.round(components[0], 1).astype(str))}. "
            f"Try checking the data or changing the ranges."
        )


    return mean, std, weight


def get_open_state_mask(i: np.ndarray, open_state_component: list,
                        extent: float = 0.9999) -> np.ndarray:
    """Generates a boolean mask identifying the open pore state

    This function computes a boolean array that marks the current _events points
    belonging to the open pore state. It uses the mean and standard deviation
    from the provided `open_state_component` (Gaussian component) to calculate
    current values that fall inside a confidence interval defined by
    `extent` (default 99.99%) and creates a mask based on the _events within that
    interval.

    Args:
        i (np.ndarray): The current trace
        open_state_component (list): A list containing the mean, standard
            deviation, and weight of the Gaussian component representing the
            open pore state.
        extent (float, optional): The confidence interval for defining the
            open pore state. Default is 0.9999 (99.99%).


    Returns:
        np.ndarray: A boolean array where `True` indicates the _events points
        within the open pore state.

    Example:
        >>> i = np.random.randn(1000)
        >>> open_state_component = [0.0, 0., 0.5]
        >>> mask = get_open_state_mask(i, open_state_component)
        >>> print(mask)  # A boolean array marking the open pore state
    """
    mean, sigma = open_state_component[0], open_state_component[1]

    q_low = scipy.stats.norm.ppf(0.5 - extent / 2, loc=mean, scale=sigma)
    q_high = scipy.stats.norm.ppf(0.5 + extent / 2, loc=mean, scale=sigma)

    open_state_bool = (i >= q_low) & (i <= q_high)

    return open_state_bool


def find_open_state(raw: base.Raw, lower_bound: float = 220,
                    upper_bound: float = 250,
                    lowpass: float = None,
                    n_components: int = 3, extent=0.9999,
                    resample_to_freq: float = None,
                    max_samples: int = None,
                    verbose: bool = False) -> None:
    """Mark the open state of a measurement

    This function identifies the open pore state of a Raw by applying
    a Gaussian mixture model to the current _events and determining the Gaussian
    component representing the open state current distribution. This component
    must lie within the specified bounds (`lower_bound` to `upper_bound`). It
    then generates a boolean mask for the open state within a confidence
    interval (`extent`), and marks the relevant _events points in the Raw.

    Args:
        lowpass: # TODO update docstring with reasample and lowpass filter
        resample_to_freq:
        raw (Raw): A Raw object.
        lower_bound (float, optional): The lower bound of the current range in
            which the open state curent must lie. Default is 220 pA.
        upper_bound (float, optional): The upper bound of the current range in
            which the open state curent must lie. Default is 220 pA.
        n_components (int, optional): The number of Gaussian components to fit.
            Default is 3.
        extent (float, optional): The confidence interval for defining the open
            pore state. Default is 0.9999 (99.99%). A higher number means a
            larger number of points will be assigned as being the open state
            current.

    Returns:
        None: The function modifies the Raw in place by assigning the
        open state to relevant _events points.

    Example:
        >>> raw = Raw()  # Assume this is a valid Raw object
        >>> find_open_state(raw,lower_bound=220,upper_bound=250,n_components=3,extent=0.9999)
        >>> print(raw.get_states())  # Raw will have the open states marked
    """
    raw.reset_states()

    i_original = raw.get_i()
    i = raw.get_i(resample_to_freq=resample_to_freq)
    i = shorten_data_to_ends(i, max_samples)

    if verbose:
        print_resampling_and_shortening(len(i), len(raw), resample_to_freq)

    if lowpass is not None:
        i = utils.lowpass_filter(i, raw.info.sfreq, lowpass)
        i_original = utils.lowpass_filter(i_original, raw.info.sfreq, lowpass)

    comp = get_open_state_current_distr(i, lower_bound, upper_bound,
                                        n_components=n_components)

    mask = get_open_state_mask(i_original, comp, extent=extent)

    raw.data.loc[mask, 'state'] = base.OPEN_STATE


def print_resampling_and_shortening(new_length, old_length, resample_to_freq):
    shortened = new_length > old_length
    print(f'Original data has {old_length} samples. ', end='')
    if shortened and resample_to_freq:
        print(f'Resampled data to {resample_to_freq:.0f} Hz and shortened '
              f'to {new_length} samples. ', end='')
    elif not shortened and resample_to_freq:
        print(f'Resampled data to {resample_to_freq:.0f} Hz. ', end='')
    elif shortened:
        print(f'Shortened data to {new_length} samples. ', end='')
    else:
        print('Using all data. ', end='')
    print(f'Continuing with {new_length}/{old_length} '
          f'({new_length / old_length:.0%}) samples. ', end='')


def shorten_data_to_ends(a, max_samples):
    if max_samples and max_samples < len(a):

        a = np.concatenate([a[:max_samples // 2],
                            a[-max_samples // 2:]])
    return a


def get_voltage_distrs(v: np.ndarray,
                       n_components: int = 3,
                       known_good_voltage: Optional[tuple] = None):
    """Get Gaussian distributions in voltage _events

    Retrieves a number of Gaussian distributions in the voltage _events that
    describe the dataset.

    This function applies a Gaussian Mixture Model to the voltage _events in the
    Raw to identify the `n_components` Gaussian components that best
    describe the voltage distribution. The components are then sorted by their
    means in descending order.

    TODO update docstring

    Args:
        v (np.ndarray): Array with voltage values object.
        n_components (int, optional): The number of Gaussian components to fit.
            Default is 3.

    Returns:
        tuple: A tuple containing:
            - means (np.ndarray): The sorted means of the Gaussian components.
            - stds (np.ndarray): The sorted standard deviations of the Gaussian
                components.
            - weights (np.ndarray): The sorted weights of the Gaussian
                components.

    Example:
        >>> raw = Raw()  # Assume this is a valid Raw object
        >>> means, stds, weights = get_voltage_distrs(raw, n_components=3)
        >>> print("Means:", means)
        >>> print("Standard Deviations:", stds)
        >>> print("Weights:", weights)
    """
    if known_good_voltage:
        v = v[(v < min(known_good_voltage)) | (v > max(known_good_voltage))]

        mean = sum(known_good_voltage) / 2
        scale = max(known_good_voltage) - mean
        good_distr = scipy.stats.uniform(loc=mean - scale, scale=scale * 2)

        n_components -= 1  # Need to look for 1 fewer component
    else:
        good_distr = None

    components = get_components(v, n_components)

    means, stds, _, = sort_components(*components)

    distrs = [scipy.stats.norm(mean, std) for mean, std in zip(means, stds)]

    if good_distr:
        distrs.insert(0, good_distr)

    return distrs


def get_bad_voltage_mask(v: np.ndarray, distr_good_voltage, distr_rest):
    """
    TODO: Update
    Assumes components sorted by mean with largest mean first

    Args:
        raw:
        means:
        stds:
        weights:

    Returns:

    """


    p_normal = distr_good_voltage.pdf(v)
    p_rest = np.max(np.vstack([g.pdf(v) for g in distr_rest]), axis=0)

    return p_rest > p_normal


def find_bad_voltages(raw: base.Raw, n_components: int = 3,
                      known_good_voltage: Optional[tuple] = None,
                      resample_to_freq: float = 5000,
                      max_samples: int = None,
                      verbose: bool = False) -> None:

    v = raw.get_v(resample_to_freq=resample_to_freq)
    v = shorten_data_to_ends(v, max_samples)

    if verbose:
        print_resampling_and_shortening(len(v), len(raw), resample_to_freq)

    distrs = get_voltage_distrs(v,
                                n_components=n_components,
                                known_good_voltage=known_good_voltage)

    v_original = raw.get_v()
    mask = get_bad_voltage_mask(v_original, distrs[0], distrs[1:])

    raw.data.loc[mask, 'state'] = base.BAD_VOLTAGE_STATE


def plot_voltage_state(raw: base.Raw, normalise_distr_curves=True, n_components=3,
                       known_good_voltage: Optional[tuple] = None):
    distrs = get_voltage_distrs(raw.get_v(),
                                n_components=n_components,
                                known_good_voltage=known_good_voltage)

    fig, axs = plt.subplots(1, 2,
                            figsize=(12, 4),
                            sharey=True,
                            gridspec_kw={'width_ratios': [8, 1]})

    raw.plot('v', ax=axs[0])

    ys = []
    xs = []
    for i, distr in enumerate(distrs):
        y = np.linspace(*distr.ppf([0.001, 0.999]), num=200)
        x = distr.pdf(y)
        ys.append(y)
        xs.append(x)

    if normalise_distr_curves:
        scale = None
    else:
        scale = 1 / max([np.max(x) for x in xs])

    for i, (x, y) in enumerate(zip(xs, ys)):
        if normalise_distr_curves:
            scale = 1 / np.max(x)
        axs[1].fill_betweenx(y, x1=x * scale, x2=0, label=f'p{i}')
        axs[1].plot(x * scale, y)

    axs[1].set_xlim(left=0)
    axs[1].legend(loc=3)

    axs[0].set_title(None)
    fig.suptitle(raw.info.name + "\nVoltage States")
    fig.subplots_adjust(wspace=0)

    return fig, axs
def plot_GMM_current(raw: base.Raw, normalise_distr_curves=True, n_components=3):
    comps = get_components(raw.get_i(), n_components)

    distrs = get_distrs_from_comps(comps)

    fig, axs = plt.subplots(1, 2,
                            figsize=(12, 4),
                            sharey=True,
                            gridspec_kw={'width_ratios': [8, 1]})

    raw.plot('i', ax=axs[0])

    ys = []
    xs = []
    for i, distr in enumerate(distrs):
        y = np.linspace(*distr.ppf([0.001, 0.999]), num=200)
        x = distr.pdf(y)
        ys.append(y)
        xs.append(x)

    if normalise_distr_curves:
        scale = None
    else:
        scale = 1 / max([np.max(x) for x in xs])

    for i, (x, y) in enumerate(zip(xs, ys)):
        if normalise_distr_curves:
            scale = 1 / np.max(x)
        axs[1].fill_betweenx(y, x1=x * scale, x2=0, label=f'p{i}')
        axs[1].plot(x * scale, y)

    axs[1].set_xlim(left=0)
    axs[1].legend(loc=3)

    axs[0].set_title(None)
    fig.suptitle(raw.info.name + "\nCurrent GMM")
    fig.subplots_adjust(wspace=0)

    return fig, axs


def get_distrs_from_comps(components: tuple):
    means, stds, _ = components
    distrs = [scipy.stats.norm(mean, std) for mean, std in zip(means, stds)]
    return distrs


def get_open_state_segments(raw: base.Raw):
    open_clean_state = raw.get_states() == base.OPEN_STATE

    state_changes = np.diff(np.concatenate(([0], open_clean_state, [0])))

    if not np.any(state_changes):
        raise RuntimeError("Error, did not find any states. Please run "
                           "find_open_state() and find_bad_voltages() first.")

    # Find start and end indices
    starts = np.where(state_changes == 1)[0]
    ends = np.where(state_changes == -1)[0] - 1
    # Create DataFrame with segments

    segments = pd.DataFrame({
        'start_idx': raw.data['i'].index[starts],
        'end_idx': raw.data['i'].index[ends]
    })

    return segments


def get_open_pore_fit(raw: base.Raw, degree: int = 1):
    open_clean_state = raw.get_states() == base.OPEN_STATE

    y = raw.get_i()[open_clean_state]
    x = raw.get_time()[open_clean_state]

    return np.polynomial.Polynomial.fit(x, y, deg=degree)


def get_unique_states(raw: base.Raw):
    return np.unique(raw.get_states())


def get_events_idxs(raw: base.Raw, boundary_trim: int = 5):
    """

    Assumes the Raw state has been annotated with bad voltages and open
    pore voltages

    Args:
        boundary_trim (int):
        raw:

    Returns:

    """
    open_clean_state = raw.get_states() == base.GOOD_STATE

    d = np.diff(open_clean_state.astype(int))

    start_indices = np.where(d == 1)[0] + 1
    end_indices = np.where(d == -1)[0]

    if open_clean_state[0]:
        start_indices = np.insert(start_indices, 0, 0)
    if open_clean_state[-1]:
        end_indices = np.append(end_indices, len(open_clean_state) - 1)

    start_indices += boundary_trim
    end_indices -= boundary_trim
    start_indices = np.clip(start_indices, 0, len(open_clean_state) - 1)
    end_indices = np.clip(end_indices, 0, len(open_clean_state) - 1)

    # Create a DataFrame from the start and end indices
    events_df = pd.DataFrame({
        'start_idx': start_indices,
        'end_idx': end_indices
    })

    # Add a duration column
    events_df['n_samples'] = events_df['end_idx'] - events_df['start_idx'] + 1

    # Remove negative length (due to trim) _events
    events_df = events_df[events_df['n_samples'] > 0]
    # Reset index
    events_df.reset_index(drop=True, inplace=True)

    return events_df


def plot_open_state_fit(raw, degree=3, fig=None, ax=None, savefig=False,
                        ignore_voltage=False, recalculate=True):
    if fig is None and ax is None:
        fig, ax = plt.subplots(figsize=(12, 4))

    if recalculate:
        find_open_state(raw)
        if not ignore_voltage:
            find_bad_voltages(raw)

    poly = get_open_pore_fit(raw, degree=degree)

    fig, ax = raw.plot(fig=fig, ax=ax)
    t = raw.get_time()[::100]
    ax.plot(t, poly(t), "r", label="Fit")

    ax.legend(loc=3)
    # ax.set_ylim([0, 250])
    # ax.set_xlim([3.5, 10])
    ax.grid(True)
    ax.legend(loc=3)

    if savefig:
        savefig = utils.check_fname_for_ext(savefig, "png")
        fig.savefig(savefig, dpi=300)

    return fig, ax
