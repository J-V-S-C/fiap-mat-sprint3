"""Testes dos modelos e dos cálculos do painel."""
import math
import unittest

from sample_cases import (
    CRITICAL_SPO2,
    deficit_with_oxygen,
    deficit_without_oxygen,
    spo2_with_oxygen,
    spo2_without_oxygen,
)
from simulator import decision, distance_to_limit, numerical_derivative


class ScenarioTests(unittest.TestCase):
    def test_both_scenarios_start_at_case_value(self):
        self.assertAlmostEqual(spo2_without_oxygen(0), 90.0)
        self.assertAlmostEqual(spo2_with_oxygen(0), 90.0)

    def test_scenarios_approach_their_limits(self):
        self.assertAlmostEqual(spo2_without_oxygen(200), 85.0, places=10)
        self.assertAlmostEqual(spo2_with_oxygen(200), 97.0, places=10)

    def test_derivative_signs_show_trend(self):
        self.assertLess(numerical_derivative(spo2_without_oxygen, 5), 0)
        self.assertGreater(numerical_derivative(spo2_with_oxygen, 5), 0)

    def test_derivative_at_domain_boundary(self):
        derivative = numerical_derivative(spo2_with_oxygen, 0)
        self.assertTrue(math.isclose(derivative, 7 / 3, rel_tol=1e-6))

    def test_negative_time_is_rejected(self):
        with self.assertRaises(ValueError):
            spo2_with_oxygen(-1)

    def test_distance_to_limit(self):
        self.assertEqual(distance_to_limit(90, 97), 7)

    def test_integral_matches_area_under_deficit_curve(self):
        # Independently approximate the area by trapezoids on [0, 10].
        steps = 10000
        width = 10 / steps
        for curve, integral in (
            (spo2_without_oxygen, deficit_without_oxygen),
            (spo2_with_oxygen, deficit_with_oxygen),
        ):
            area = sum(
                width * ((100 - curve(i * width)) + (100 - curve((i + 1) * width))) / 2
                for i in range(steps)
            )
            self.assertAlmostEqual(integral(10), area, places=5)
            self.assertEqual(integral(0), 0)

    def test_integral_and_decision_compare_same_period(self):
        t = 10
        no_action = deficit_without_oxygen(t)
        intervention = deficit_with_oxygen(t)
        self.assertLess(intervention, no_action)
        self.assertEqual(
            decision(spo2_without_oxygen(t), numerical_derivative(spo2_without_oxygen, t),
                     85, no_action, no_action, CRITICAL_SPO2),
            "Em atenção",
        )
        self.assertEqual(
            decision(spo2_with_oxygen(t), numerical_derivative(spo2_with_oxygen, t),
                     97, intervention, no_action, CRITICAL_SPO2),
            "Em evolução",
        )

    def test_invalid_time_and_indicators_are_rejected(self):
        for invalid in (-1, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                deficit_with_oxygen(invalid)
        with self.assertRaises(ValueError):
            decision(90, float("nan"), 97, 10, 20)
        with self.assertRaises(ValueError):
            decision(90, 1, 97, -1, 20)


if __name__ == "__main__":
    unittest.main()
