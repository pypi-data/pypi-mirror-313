# optimization.py

import numpy as np
from .moments import mom2_serg_log, mom4_serg_log, levy_moments_log


def to_optimize_mom4_serg_log(variables, tau_list, logdx4):
    v0, D, lambdaB, lambdaD = variables
    expr = mom4_serg_log(tau_list, v0, D, lambdaB, lambdaD)
    l_num = np.mean((logdx4 - expr) ** 2)
    return l_num


def to_optimize_mom2_serg_log(variables, tau_list, logdx2):
    v0, D, lambdaB, lambdaD = variables
    expr = mom2_serg_log(tau_list, v0, D, lambdaB, lambdaD)
    l_num = np.mean((logdx2 - expr) ** 2)
    return l_num


def to_optimize_mom4_and_2_serg_log(variables, tau_list, logdx2, logdx4):
    v0, D, lambdaB, lambdaD = variables
    expr4 = mom4_serg_log(tau_list, v0, D, lambdaB, lambdaD)
    expr2 = mom2_serg_log(tau_list, v0, D, lambdaB, lambdaD)
    l_num4 = np.mean((logdx4 - expr4) ** 2)
    l_num2 = np.mean((logdx2 - expr2) ** 2)
    l_num = l_num4 + 2 * l_num2
    return l_num


def to_optimize_mom4_serg_log_vl(variables, tau_list, logdx4, tos_D, tos_lambdaD):
    v0, lambdaB = variables
    D = tos_D
    lambdaD = tos_lambdaD
    expr = mom4_serg_log(tau_list, v0, D, lambdaB, lambdaD)
    l_num = np.mean(np.abs(logdx4 - expr) / logdx4)
    return l_num


def to_optimize_second_ll(variables, tau_list, logdx2, tos_v, tos_D):
    lambdaB, lambdaD = variables
    expr2 = mom2_serg_log(tau_list, tos_v, tos_D, lambdaB, lambdaD)
    l_num = np.mean(np.abs(logdx2 - expr2) / logdx2)
    return l_num

def to_optimize_levy(params, t_list, dx2_log, dx4_log, tmin):
    """
    Objective function to optimize 'alpha' and 'v_mean' for Lévy flights.

    Parameters:
    params (list): [alpha, v_mean]
    t_list (array-like): List of time lags.
    dx2_log (array-like): Empirical log second moments.
    dx4_log (array-like): Empirical log fourth moments.
    tmin (float): Minimum flight time.

    Returns:
    float: The objective function value to minimize.
    """
    alpha, v_mean = params
    if alpha <= 1 or alpha >= 3:
        return np.inf  # Penalize invalid alpha

    theoretical_dx2_log = levy_moments_log(2, alpha, v_mean, t_list, tmin)
    theoretical_dx4_log = levy_moments_log(4, alpha, v_mean, t_list, tmin)
    error = np.mean((dx2_log - theoretical_dx2_log) ** 2) + \
            np.mean((dx4_log - theoretical_dx4_log) ** 2)
    return error