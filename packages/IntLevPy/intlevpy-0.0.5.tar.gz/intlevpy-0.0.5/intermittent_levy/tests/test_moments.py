# test_moments.py

import unittest
import numpy as np
from intermittent_levy.moments import mom2_serg_log, mom4_serg_log, levy_moments_log

class TestMoments(unittest.TestCase):

    def test_mom2_serg_log(self):
        # Test the mom2_serg_log function
        tau_list = np.arange(1, 10)
        v0 = 10.0
        D = 0.1
        lambdaB = 0.1
        lambdaD = 0.05

        result = mom2_serg_log(tau_list, v0, D, lambdaB, lambdaD)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(len(result), len(tau_list))
        # Additional checks
        self.assertFalse(np.any(np.isnan(result)))
        self.assertTrue(np.all(np.isfinite(result)))

    def test_mom4_serg_log(self):
        # Test the mom4_serg_log function
        tau_list = np.arange(1, 10)
        v0 = 10.0
        D = 0.1
        lambdaB = 0.1
        lambdaD = 0.05

        result = mom4_serg_log(tau_list, v0, D, lambdaB, lambdaD)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(len(result), len(tau_list))
        # Additional checks
        self.assertFalse(np.any(np.isnan(result)))
        self.assertTrue(np.all(np.isfinite(result)))

    def test_levy_moments_log(self):
        # Test the levy_moments_log function
        n_mom = 2
        alpha = 1.8
        v_mean = 1.0
        t_list = np.arange(1, 10)
        tmin = 1.0

        result = levy_moments_log(n_mom, alpha, v_mean, t_list, tmin)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(len(result), len(t_list))
        # Additional checks
        self.assertFalse(np.any(np.isnan(result)))
        self.assertTrue(np.all(np.isfinite(result)))

        # Test with invalid alpha (should raise ValueError if implemented)
        with self.assertRaises(ValueError):
            levy_moments_log(n_mom, 0.5, v_mean, t_list, tmin)  # alpha < 1
        with self.assertRaises(ValueError):
            levy_moments_log(n_mom, 3.5, v_mean, t_list, tmin)  # alpha > 3

if __name__ == '__main__':
    unittest.main()
