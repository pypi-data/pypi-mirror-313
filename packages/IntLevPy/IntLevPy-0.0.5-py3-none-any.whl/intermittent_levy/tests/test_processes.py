# test_processes.py

import unittest
from intermittent_levy.processes import intermittent3, levy_flight_2D_Simplified
import numpy as np

class TestProcesses(unittest.TestCase):
    def test_intermittent3(self):
        nt = 1000
        dt = 0.1
        mean_bal_sac = 1.0
        diffusion = 0.1
        rate21 = 0.1
        rate12 = 0.1
        x, y = intermittent3(nt, dt, mean_bal_sac, diffusion, rate21, rate12)
        self.assertEqual(len(x), nt)
        self.assertEqual(len(y), nt)
        self.assertFalse(np.isnan(x).any())
        self.assertFalse(np.isnan(y).any())

    def test_levy_flight_2D_Simplified(self):
        n_redirections = 1000
        n_max = 1000
        lalpha = 1.5
        tmin = 1.0
        v_mean = 1.0
        measuring_dt = 0.1
        x, y = levy_flight_2D_Simplified(
            n_redirections, n_max, lalpha, tmin, v_mean, measuring_dt
        )
        self.assertGreater(len(x), 0)
        self.assertGreater(len(y), 0)
        self.assertFalse(np.isnan(x).any())
        self.assertFalse(np.isnan(y).any())

if __name__ == '__main__':
    unittest.main()

