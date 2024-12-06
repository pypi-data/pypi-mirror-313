# utils.py

import numpy as np


def r_square(emp_points, emp_fit):
    l_num = np.mean((np.array(emp_points) - np.array(emp_fit)) ** 2)
    l_den = np.std(np.array(emp_points)) ** 2
    return 1 - l_num / l_den


def adjusted_r_square(emp_points, emp_fit, degrees_freedom):
    n = len(emp_points)
    l_num = np.mean((np.array(emp_points) - np.array(emp_fit)) ** 2)
    l_den = np.std(np.array(emp_points)) ** 2
    rsqu = 1 - l_num / l_den
    return 1 - (1 - rsqu) * ((n - 1) / (n - degrees_freedom))


def adjusted_r_square_array(emp_points, emp_fit, degrees_freedom):
    n = len(emp_points)
    l_num = np.mean((np.array(emp_points) - np.array(emp_fit)) ** 2, axis=1)
    l_den = np.std(np.array(emp_points)) ** 2
    rsqu = 1 - l_num / l_den
    return 1 - (1 - rsqu) * ((n - 1) / (n - degrees_freedom))


def powerl_fit(tau, k, a):
    return k * np.power(2, tau * a)
def funcPairs(larr, n):
    lpairs = []
    for i in range(n):
        for j in range(n):
            lpairs.append([ larr[i],larr[j]])
                         
    return(lpairs)
 

def parse_trials( lparams_list, threshold_ratio):
    log_swaped_lparams_list = np.log(np.swapaxes(lparams_list,0,1))
    max = np.log(threshold_ratio)
    ln = len(log_swaped_lparams_list[0])
    lnn = len(log_swaped_lparams_list)
    indices_del = []
    M_list = []
    for i in range(lnn):
        pairs = funcPairs(log_swaped_lparams_list[i],ln)
        new_M = np.abs(np.diff(pairs,axis=1).reshape(ln,ln)) + (max+1)*np.eye(ln)
        M_list.append(new_M)
