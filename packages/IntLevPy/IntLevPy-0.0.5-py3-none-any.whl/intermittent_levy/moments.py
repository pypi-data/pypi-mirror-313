# moments.py

import numpy as np


def mom4_serg_log(t, v0, D, lambdaB, lambdaD):
    t = np.array(np.hstack([t]), dtype=np.longdouble)
    C1 = (
        3
        * lambdaB ** (-2)
        * (lambdaB + lambdaD) ** (-2)
        * (2 * D * lambdaB ** 2 + v0 ** 2 * lambdaD) ** 2
    )
    C2 = (
        3
        * lambdaB ** (-3)
        * lambdaD
        * (lambdaB + lambdaD) ** (-3)
        * (
            8 * D ** 2 * lambdaB ** 4
            - 8 * D * v0 ** 2 * lambdaB ** 2 * (2 * lambdaB + lambdaD)
            + v0 ** 4 * (3 * lambdaB ** 2 - 2 * lambdaB * lambdaD - 3 * lambdaD ** 2)
        )
    )
    C3 = (
        3
        * lambdaB ** (-4)
        * lambdaD
        * (lambdaB + lambdaD) ** (-4)
        * (
            -8 * D ** 2 * lambdaB ** 5
            + 8 * D * v0 ** 2 * lambdaB ** 2 * (3 * lambdaB ** 2 + 3 * lambdaB * lambdaD + lambdaD ** 2)
            + v0 ** 4 * (-9 * lambdaB ** 3 - 7 * lambdaB ** 2 * lambdaD + 3 * lambdaB * lambdaD ** 2 + 3 * lambdaD ** 3)
        )
    )
    C4 = 3 / 2 * v0 ** 4 * lambdaB ** (-2) * lambdaD * (lambdaB + lambdaD) ** (-1)
    C5 = 6 * v0 ** 4 * lambdaB ** (-2) * (lambdaB + lambdaD) ** (-1)
    C6 = 0.0
    C7 = (
        -3
        * v0 ** 2
        / (lambdaB ** 4 * lambdaD * (lambdaB + lambdaD))
        * (
            8 * D * lambdaB ** 2 * lambdaD
            + v0 ** 2 * (2 * lambdaB ** 2 - 6 * lambdaB * lambdaD + 3 * lambdaD ** 2)
        )
    )
    C8 = (
        6
        * lambdaB
        / (lambdaD * (lambdaB + lambdaD) ** 4)
        * (v0 ** 2 + 2 * D * lambdaD) ** 2
    )
    expr = (
        C1 * t ** 2
        + C2 * t
        + C3
        + C4 * t ** 2 * np.exp(-lambdaB * t)
        + C5 * t * np.exp(-lambdaB * t)
        + C6 * t * np.exp(-(lambdaB + lambdaD) * t)
        + C7 * np.exp(-lambdaB * t)
        + C8 * np.exp(-(lambdaB + lambdaD) * t)
    )
    return np.log(8 * expr / 3)


def mom2_serg_log(tau, v, D, lambdaB, lambdaD):
    beta = lambdaB + lambdaD
    alpha = lambdaB / beta
    DI = (v ** 2) / beta
    C1 = -2 * (1 / (beta * alpha)) * ((1 - alpha) / alpha) * DI
    C2 = 2 * ((1 - alpha) / alpha) * DI + 4 * D * alpha
    expr2 = C1 * (1 - np.exp(-lambdaB * tau)) + C2 * tau
    return np.log(expr2)


def theor_levy_moment(n_mom, alpha, v, t, tmin):
    num = tmin ** alpha * (v ** n_mom) * n_mom * (alpha - 2) * t ** (2 + n_mom - alpha)
    den = (tmin ** 2) * (2 + n_mom - alpha) * (1 + n_mom - alpha)
    return num / den

def levy_moments_log(n_mom, alpha, v_mean, t_list, tmin):
    """
    Calculate the theoretical logarithm of the nth moment for Lévy flights.

    Parameters:
    n_mom (int): The order of the moment (e.g., 2 or 4).
    alpha (float): Lévy distribution exponent (1 < alpha < 3).
    v_mean (float): Mean velocity.
    t_list (array-like): List of time lags.
    tmin (float): Minimum flight time.

    Returns:
    array: Logarithm of the theoretical moments.
    """
    num = (tmin ** alpha) * (v_mean ** n_mom) * n_mom * (alpha - 2) * t_list ** (2 + n_mom - alpha)
    den = (tmin ** 2) * (2 + n_mom - alpha) * (1 + n_mom - alpha)
    moments = num / den
    return np.log(moments)


'''def levy_moments_log(n_mom, alpha, v_mean, t_list, tmin):
    """
    Calculate the theoretical logarithm of the nth moment for Lévy flights.

    Parameters:
    n_mom (int): The order of the moment (e.g., 2 or 4).
    alpha (float): Lévy distribution exponent (1 < alpha < 3).
    v_mean (float): Mean velocity.
    t_list (array-like): List of time lags.
    tmin (float): Minimum flight time.

    Returns:
    array: Logarithm of the theoretical moments.
    """
    num = (tmin ** alpha) * (v_mean ** n_mom) * n_mom * (alpha - 2) * t_list ** (2 + n_mom - alpha)
    den = (tmin ** 2) * (2 + n_mom - alpha) * (1 + n_mom - alpha)
    moments = num / den
    return np.log(moments)'''

def levy_moments_log(n_mom, alpha, v_mean, t_list, tmin):
    """
    Calculate the theoretical logarithm of the nth moment for Lévy flights.

    Parameters:
    n_mom (int): The order of the moment (e.g., 2 or 4).
    alpha (float): Lévy distribution exponent (1 < alpha < 3).
    v_mean (float): Mean velocity.
    t_list (array-like): List of time lags.
    tmin (float): Minimum flight time.

    Returns:
    array: Logarithm of the theoretical moments.
    """
    # Avoid invalid parameter ranges
    if alpha <= 1 or alpha >= 3:
        raise ValueError(f"Invalid alpha value: {alpha}. Must be in the range (1, 3).")
    if v_mean <= 0:
        raise ValueError(f"Invalid v_mean value: {v_mean}. Must be greater than 0.")
    if np.any(t_list <= 0):
        raise ValueError(f"Invalid t_list values: {t_list}. All time lags must be positive.")
    if tmin <= 0:
        raise ValueError(f"Invalid tmin value: {tmin}. Must be greater than 0.")

    # Calculate numerator and denominator
    try:
        num = (tmin ** alpha) * (v_mean ** n_mom) * n_mom * (alpha - 2) * t_list ** (2 + n_mom - alpha)
        den = (tmin ** 2) * (2 + n_mom - alpha) * (1 + n_mom - alpha)
        moments = num / den
    except ZeroDivisionError as e:
        raise ZeroDivisionError(f"Error in moments calculation: {e}")

    # Replace invalid moments with a small positive value
    moments = np.nan_to_num(moments, nan=1e-10, posinf=1e10, neginf=1e-10)
    moments = np.maximum(moments, 1e-10)  # Avoid non-positive values

    # Return logarithm of moments
    return np.log(moments)
