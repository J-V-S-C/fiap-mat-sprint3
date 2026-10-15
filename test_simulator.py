"""Testes dos modelos e dos cálculos do painel."""
import math
import unittest

from sample_cases import spo2_with_oxygen, spo2_without_oxygen
from simulator import distance_to_limit, numerical_derivative


class ScenarioTests(unittest.TestCase):
    def test_both_scenarios_start_at_92(self):
        self.assertAlmostEqual(spo2_without_oxygen(0), 92.0)
        self.assertAlmostEqual(spo2_with_oxygen(0), 92.0)

    def test_scenarios_approach_their_limits(self):
        self.assertAlmostEqual(spo2_without_oxygen(200), 82.0, places=10)
        self.assertAlmostEqual(spo2_with_oxygen(200), 98.0, places=10)

    def test_derivative_signs_show_trend(self):
        self.assertLess(numerical_derivative(spo2_without_oxygen, 5), 0)
        self.assertGreater(numerical_derivative(spo2_with_oxygen, 5), 0)

    def test_derivative_at_domain_boundary(self):
        derivative = numerical_derivative(spo2_with_oxygen, 0)
        self.assertTrue(math.isclose(derivative, 2.0, rel_tol=1e-6))

    def test_negative_time_is_rejected(self):
        with self.assertRaises(ValueError):
            spo2_with_oxygen(-1)

    def test_distance_to_limit(self):
        self.assertEqual(distance_to_limit(92, 98), 6)


if __name__ == "__main__":
    unittest.main()
