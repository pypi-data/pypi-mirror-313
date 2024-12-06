# test_optimization.py

import unittest
import numpy as np
from intermittent_levy.optimization import to_optimize_mom4_and_2_serg_log, to_optimize_levy
from intermittent_levy.moments import mom2_serg_log, mom4_serg_log, levy_moments_log

class TestOptimization(unittest.TestCase):

    def test_to_optimize_mom4_and_2_serg_log(self):
        # Test the to_optimize_mom4_and_2_serg_log function
        variables = [10.0, 0.1, 0.1, 0.05]  # v0, D, lambdaB, lambdaD
        tau_list = np.arange(1, 10)
        # Generate synthetic data
        logdx2 = mom2_serg_log(tau_list, *variables)
        logdx4 = mom4_serg_log(tau_list, *variables)
        # Add noise to simulate empirical data
        np.random.seed(0)  # For reproducibility
        noise_level = 0.05
        logdx2_noisy = logdx2 + np.random.normal(0, noise_level, size=logdx2.shape)
        logdx4_noisy = logdx4 + np.random.normal(0, noise_level, size=logdx4.shape)
        # Evaluate the objective function
        result = to_optimize_mom4_and_2_serg_log(variables, tau_list, logdx2_noisy, logdx4_noisy)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0)

    def test_to_optimize_levy(self):
        # Test the to_optimize_levy function
        params = [1.8, 1.0]  # alpha, v_mean
        tau_list = np.arange(1, 10)
        tmin = 1.0
        # Generate synthetic data
        dx2_log = levy_moments_log(2, params[0], params[1], tau_list, tmin)
        dx4_log = levy_moments_log(4, params[0], params[1], tau_list, tmin)
        # Add noise to simulate empirical data
        np.random.seed(0)  # For reproducibility
        noise_level = 0.05
        dx2_log_noisy = dx2_log + np.random.normal(0, noise_level, size=dx2_log.shape)
        dx4_log_noisy = dx4_log + np.random.normal(0, noise_level, size=dx4_log.shape)
        # Evaluate the objective function
        result = to_optimize_levy(params, tau_list, dx2_log_noisy, dx4_log_noisy, tmin)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0)

        # Test with invalid alpha
        with self.assertRaises(ValueError):
            to_optimize_levy([0.5, 1.0], tau_list, dx2_log_noisy, dx4_log_noisy, tmin)
        with self.assertRaises(ValueError):
            to_optimize_levy([3.5, 1.0], tau_list, dx2_log_noisy, dx4_log_noisy, tmin)

if __name__ == '__main__':
    unittest.main()
