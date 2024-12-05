# Created by Cees Dekker Lab at the Delft University of Technology
# Refactored by Thijn Hoekstra

import numpy as np

"""the function defining the cpic (bias estimator for introducing transitions)
"""

def cpic_greater_than_1000(x):
    a = 2.456
    b = 1.187
    c = 2.73
    return a * np.log(np.log(x)) + b * np.log(np.log(np.log(x))) + c


def cpic_less_than_1000(x):
    a = 1.239
    b = 0.9872
    c = 1.999
    p3 = 5.913e-10
    p4 = -1.876e-06
    p5 = 0.004354
    ph = -0.1906
    return a * np.log(np.log(x)) + b * np.log(
        x) + p3 * x ** 3 + p4 * x ** 2 + p5 * x + ph * np.abs(x) ** 0.5 + c


def get_cpic_penalty(N_T: int) -> float:
    """

    Calculates the CPIC penalty from the loaded functions. This penalty was
    calculated by Monte Carlo a la LaMont/Wiggins 2016, and serves to prevent
    the overfitting bias in the likelihood maximizing model.

    Args:
        N_T (np.ndarray):

    Returns:

    """

    if N_T >= 1e6:
        p_cpic = cpic_greater_than_1000(1e6)
    elif N_T > 1000:
        p_cpic = cpic_greater_than_1000(N_T)
    else:
        p_cpic = cpic_less_than_1000(N_T)
    return p_cpic
