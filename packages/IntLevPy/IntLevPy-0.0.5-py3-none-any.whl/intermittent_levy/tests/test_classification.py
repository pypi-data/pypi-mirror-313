# test_classification.py

import unittest
import numpy as np
from intermittent_levy.classification import form_groups, real_k_and_fisher

class TestClassification(unittest.TestCase):

    def test_form_groups(self):
        # Test the form_groups function
        data = np.concatenate([
            np.random.normal(0, 1, size=500),
            np.random.normal(5, 1, size=500)
        ])
        threshold_array = np.linspace(np.min(data), np.max(data), 20)
        detection, detectionfisher, lkmin, lfishermin = form_groups(
            data, threshold_array, graph=False, x_label='v', title='title', x_axis_format='%.2f'
        )
        self.assertIsInstance(detection, np.ndarray)
        self.assertIsInstance(detectionfisher, np.ndarray)
        self.assertIsInstance(lkmin, np.ndarray)
        self.assertIsInstance(lfishermin, np.ndarray)
        self.assertEqual(len(detection), len(threshold_array))
        self.assertEqual(len(detectionfisher), len(threshold_array))

    def test_real_k_and_fisher(self):
        # Test the real_k_and_fisher function
        data = np.random.randint(0, 2, size=1000)  # Binary data
        k_values = np.random.randint(1, 10, size=1000)
        thresholds = np.linspace(0, 1, 20)
        lindex, lkmin = real_k_and_fisher(data, k_values, thresholds)
        self.assertIsInstance(lindex, np.ndarray)
        self.assertIsInstance(lkmin, np.ndarray)
        self.assertEqual(len(lindex), len(thresholds))
        self.assertEqual(len(lkmin), len(thresholds))

if __name__ == '__main__':
    unittest.main()
