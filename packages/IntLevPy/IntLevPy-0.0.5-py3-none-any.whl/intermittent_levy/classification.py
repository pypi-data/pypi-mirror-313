# classification.py

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

import numpy as np
from scipy.stats import fisher_exact

def real_k_and_fisher(binary_vector):
    """
    Calculate the frequency matrix and detection metrics for a binary vector.
    
    Parameters:
    binary_vector (array-like): A sequence of binary values (0s and 1s).
    
    Returns:
    tuple: A tuple containing the frequency matrix, detection value, and Fisher exact test value.
    """
    matrix = np.zeros((2, 2))
    for i in range(len(binary_vector) - 1):
        matrix[int(binary_vector[i])][int(binary_vector[i + 1])] += 1

    detectionfisher = []
    detection = []

    fisher_p_value = fisher_exact(matrix)[1]
    p_value = np.clip(p_value, a_min=1e-10, a_max=None)
    detectionfisher.append(np.log(fisher_p_value))

    p = matrix.sum(axis=1)[0] / matrix.sum()
    detection_value = (matrix[1][0]) / (matrix.sum() * (p * (1 - p)))
    detection.append(detection_value)

    return matrix, detection, detectionfisher

def frequency_matrix_2D(d__ss, threshold, normalized):
    d__ss = np.array(d__ss)
    d__ss = (d__ss - np.min(d__ss)) / ((np.max(d__ss) - np.min(d__ss)) * 1.000001)
    binary_vector = (d__ss > threshold).astype(int)
    matrix = np.histogram2d(binary_vector[1:], binary_vector[:-1], bins=[0, 1, 2])[0]
    if normalized:
        for j in range(2):
            matrix[j, :] = matrix[j, :] / matrix.sum(axis=1)[j]
    return matrix


def form_groups(vector, threshold_array, graph=False, x_label='', title='', x_axis_format=''):
    detectionfisher = []
    detection = []
    for i in threshold_array:
        matrix = frequency_matrix_2D(vector, i, False)
        odds_ratio, p_value = stats.fisher_exact(matrix)
        detectionfisher.append(np.log(p_value))
        p = matrix.sum(axis=1)[0] / matrix.sum()
        if p == 1 or p == 0:
            detection.append(1)
        else:
            detection.append((matrix[1][0]) / (matrix.sum() * (p * (1 - p))))

    minim = min(vector)
    diff = max(vector) - minim
    min_k = np.argmin(detection) * diff + minim
    min_fisher = np.argmin(detectionfisher) * diff + minim

    if graph:
        xticks_labels = [x_axis_format % (minim + diff * pipi) for pipi in threshold_array]
        plt.plot(detection)
        plt.xlabel(x_label)
        plt.title(title)
        if len(threshold_array) > 40:
            plt.xticks(
                np.arange(len(threshold_array))[:: int(len(threshold_array) / 10)],
                xticks_labels[:: int(len(threshold_array) / 10)],
            )
        else:
            plt.xticks(np.arange(len(threshold_array))[::4], xticks_labels[::4])
        plt.ylabel("k")
        plt.show()

        plt.plot(detectionfisher)
        plt.xlabel(x_label)
        plt.title(title)
        if len(threshold_array) > 40:
            plt.xticks(
                np.arange(len(threshold_array))[:: int(len(threshold_array) / 10)],
                xticks_labels[:: int(len(threshold_array) / 10)],
            )
        else:
            plt.xticks(np.arange(len(threshold_array))[::4], xticks_labels[::4])
        plt.ylabel("log-fisher exact test")
        plt.show()

    return detection, detectionfisher, min_k, min_fisher


def parse_trials(lparams_list, threshold_ratio):
    log_swaped_lparams_list = np.log(np.swapaxes(lparams_list, 0, 1))
    max_log_ratio = np.log(threshold_ratio)
    ln = len(log_swaped_lparams_list[0])
    lnn = len(log_swaped_lparams_list)
    M_list = []
    for i in range(lnn):
        pairs = []
        for j in range(ln):
            for k in range(ln):
                pairs.append([log_swaped_lparams_list[i][j], log_swaped_lparams_list[i][k]])
        pairs = np.array(pairs)
        new_M = np.abs(np.diff(pairs, axis=1).reshape(ln, ln)) + (max_log_ratio + 1) * np.eye(ln)
        M_list.append(new_M)

    list_dists = np.zeros(ln)
    for i in range(ln):
        list_dists += np.sum(M_list[i], axis=0)

    opt_index = np.argmin(list_dists)
    return lparams_list[opt_index]

