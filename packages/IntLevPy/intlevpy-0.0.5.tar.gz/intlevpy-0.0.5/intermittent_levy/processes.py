# processes.py

import numpy as np
import math
import random


def intermittent3(nt, dt, mean_bal_sac, diffusion, rate21, rate12):
    diffusion = np.sqrt(2 * diffusion)
    P1 = rate21 / (rate12 + rate21)
    if np.random.random() < P1:
        regime = 1
        waitt = -math.log(1.0 - np.random.uniform(0.0, 1.0)) / rate12
    else:
        regime = 2
        angle_fixed = np.random.random() * 2 * math.pi
        waitt = -math.log(1.0 - np.random.uniform(0.0, 1.0)) / rate21

    x = np.zeros(nt)
    y = np.zeros(nt)
    t_array = np.zeros(nt)
    extra_dx = 0
    extra_dy = 0
    rest_dt = dt
    curr_len = 1
    current_time = 0
    total_waiting_times = waitt

    while curr_len < nt:
        current_dt = min(total_waiting_times - current_time, rest_dt)
        continue_regime = total_waiting_times > current_time + rest_dt

        if regime == 1:
            current_dts = np.sqrt(current_dt)
            current_dx = np.random.normal(0, diffusion) * current_dts
            current_dy = np.random.normal(0, diffusion) * current_dts
        elif regime == 2:
            bal = mean_bal_sac * current_dt
            current_dx = bal * math.cos(angle_fixed)
            current_dy = bal * math.sin(angle_fixed)

        if continue_regime:
            x[curr_len] = x[curr_len - 1] + current_dx + extra_dx
            y[curr_len] = y[curr_len - 1] + current_dy + extra_dy
            t_array[curr_len] = current_time
            rest_dt = dt
            extra_dx = 0
            extra_dy = 0
            curr_len += 1
        else:
            extra_dx += current_dx
            extra_dy += current_dy
            rest_dt -= current_dt
            if regime == 1:
                waitt = -math.log(np.random.uniform(0.0, 1.0)) / rate21
                angle_fixed = random.random() * 2 * math.pi
                regime = 2
            elif regime == 2:
                waitt = -math.log(np.random.uniform(0.0, 1.0)) / rate12
                regime = 1
            total_waiting_times += waitt

        current_time += current_dt

    return x, y


def wait_times(taui, lN, lalpha):
    # 1 < alpha < 3
    return taui * (np.random.uniform(0, 1, lN) ** (-1 / (lalpha - 1)) - 1)


def levy_flight_2D_Simplified(n_redirections, n_max, alpha, tmin, v_mean, measuring_dt):
    """
    Simulate a 2D Lévy flight with specified parameters.

    Parameters:
    n_redirections (int): Number of redirections (flight steps).
    n_max (int): Maximum number of measurement points.
    alpha (float): Lévy distribution exponent (1 < alpha < 3).
    tmin (float): Minimum flight time.
    v_mean (float): Mean velocity.
    measuring_dt (float): Time interval for measurements.

    Returns:
    tuple: Arrays of x and y positions at measurement times.
    """
    if alpha <= 1 or alpha >= 3:
        raise ValueError("alpha should be in the range (1, 3)")

    # Generate waiting times from a Lévy distribution
    t_redirection = tmin * (np.random.uniform(0, 1, n_redirections) ** (-1 / (alpha - 1)) - 1)

    # Generate random flight angles
    angles = np.random.uniform(0, 2 * np.pi, n_redirections)

    # Calculate increments
    x_increments = t_redirection * np.cos(angles) * v_mean
    y_increments = t_redirection * np.sin(angles) * v_mean

    # Cumulative sums to get positions
    x_positions = np.cumsum(x_increments)
    y_positions = np.cumsum(y_increments)
    time_points = np.cumsum(t_redirection)

    # Interpolate positions at measurement times
    total_time = time_points[-1]
    measurement_times = np.arange(0, min(n_max * measuring_dt, total_time), measuring_dt)

    x_measured = np.interp(measurement_times, time_points, x_positions)
    y_measured = np.interp(measurement_times, time_points, y_positions)

    return x_measured, y_measured