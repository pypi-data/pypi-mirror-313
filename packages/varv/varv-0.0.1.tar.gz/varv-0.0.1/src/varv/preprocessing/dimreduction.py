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

from importlib import resources as impresources

import numpy as np
import scipy.linalg

from varv.preprocessing import assets

inp_file_dim_red = impresources.files(assets) / 'principal_components.npy'

BASIS_FNS_DIM_RED = np.load(inp_file_dim_red)


def get_comp_amps_and_cov(g_mat_long: np.ndarray,
                          bfs: np.ndarray = BASIS_FNS_DIM_RED):
    """

    Args:
        g_mat_long:
        bfs:

    Returns:

    Todo:
        For the < 10% of states for which the covariance is not well estimated,
        fill in the covariance with the 90th percentile largest (by value of
        the determinant) well-estimated covariance.

    """
    num_bfs = bfs.shape[1]
    num_half_cycle_samples = g_mat_long.shape[1]

    p = np.full((num_bfs, num_half_cycle_samples), np.nan)

    good_columns = ~np.any(np.isnan(g_mat_long), axis=0)

    p[:, good_columns], res, rnk, s = scipy.linalg.lstsq(bfs, g_mat_long[:,
                                                              good_columns])


    cov = np.cov(p[:, good_columns])
    return p, cov


def get_mean_comp_amp(p: np.ndarray) -> np.ndarray:
    return np.nanmean(p, axis=1)


def reconstitute_signal(x: np.ndarray,
                        bfs: np.ndarray = BASIS_FNS_DIM_RED) -> np.ndarray:
    return bfs @ x


def get_var_from_cov(mean: np.ndarray, cov: np.ndarray,
                     num_draws: int = 100) -> np.ndarray:
    """

    TODO: Rewrite docstring
    We converted the associated covariance of each mean conductance curve to a
    standard deviation around the mean by taking 100 random draws from a multivariate
    normal distribution with matching mean and covariance, then taking the standard
    deviation of these 100 random curves at each DNA position.

    Only used for display. HMM uses covariance matrix

    """
    if mean.ndim == 1 and cov.ndim == 2:
        p = np.random.multivariate_normal(mean, cov, size=num_draws).T

        curves = reconstitute_signal(p)

        return np.var(curves, axis=1)

    elif mean.ndim == 2 and cov.ndim == 3:
        var_array = []
        for i in range(len(mean)):
            var_array.append(get_var_from_cov(mean[i], cov[i], num_draws))

        return np.array(var_array)



def get_std_from_cov(mean: np.ndarray, cov: np.ndarray,
                     num_draws: int = 100) -> float:
    return np.sqrt(get_var_from_cov(mean, cov, num_draws))


def get_vector_from_cov(cov: np.ndarray) -> np.ndarray:
    """

    If covariance matrix has dimensionality N then number of triangonal matrix
    elements including the diagonal is N * (N + 1) / 2

    Args:
        cov:

    Returns:

    """
    idxs = np.triu_indices(len(cov))
    return cov[idxs]

def get_cov_from_vector(cov_vec: np.ndarray) -> np.ndarray:
    if cov_vec.ndim == 1:
        n = get_cov_dim_from_cov_vec_length(len(cov_vec))

        cov = np.zeros((n, n))
        cov[np.triu_indices(n)] = cov_vec
        cov += cov.T
        cov /= (np.eye(n) + np.full_like(cov, 1))  # Middle values filled in twice.
        return cov
    elif cov_vec.ndim == 2:
        n = get_cov_dim_from_cov_vec_length(cov_vec.shape[1])
        cov = np.zeros((len(cov_vec), n, n))
        for i in range(cov_vec.shape[0]):
            cov[i, :, :] = get_cov_from_vector(cov_vec[i, :])

        return cov

    else:
        raise ValueError(f'Error, expected either a single vector or a 2-d '
                         f'array of vectors, but got an array of dimension '
                         f'{cov_vec.ndim}')


def get_cov_vec_size(cov_dim: int):
    """Gets size of the covariance matrix expressed as a vector.

    Args:
        cov_dim: Dimensionality of the covariance matrix.

    Returns:
        int: Size of the vector created from the covariance matrix.

    See Also:
        get_cov_dim_from_cov_vec_length: The inverse function.
    """
    return int(cov_dim * (cov_dim + 1) / 2)

def get_cov_dim_from_cov_vec_length(l: int):
    """Gets the size of the covariance matrix from its vector expression.

    Args:
        l (int): Length of the vector expressing the values of the covariance
            matrix.

    Returns:
        int: An integer specifying the dimensionality of the covariance matrix.


    See Also:
        get_cov_vec_size: The inverse function.

    """
    n = -0.5 + 0.5 * np.sqrt(1 + 4 * 2 * l)
    if n % 1:
        raise ValueError(f"Error, got the covariance as a {l}-"
                         f"dimensional vector which cannot be the values "
                         f"of the upper triangle of an NxN covariance matrix.")
    return int(n)


def get_feature_vector(x: np.ndarray, cov_vec: np.ndarray) -> np.ndarray:
    return np.hstack((x, cov_vec))


def get_average_from_half_cycle(data_mat_long: np.ndarray) -> np.ndarray:
    return np.nanmean(data_mat_long, axis=1)

def dimreduction(g_step_long: np.ndarray, num_bf_dr: int = 3) -> np.ndarray:
    """Master function for dimension reduction

    Args:
        g_step_long:
        num_bf_dr: Integer specifying number of basis functions used. Unused.

    Todo:
        - Add option for using varying number of basis functions.
    """
    p, cov = get_comp_amps_and_cov(g_step_long)
    x = get_mean_comp_amp(p)

    cov_vec = get_vector_from_cov(cov)
    return get_feature_vector(x, cov_vec)



