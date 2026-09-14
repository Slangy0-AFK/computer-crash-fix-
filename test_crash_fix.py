import unittest

from crash_fix import (
    get_buffer_window,
    get_capacity_limit,
    get_recommendation,
    get_task_granularity,
)


class CrashFixTests(unittest.TestCase):
    def test_small_workload_uses_safe_defaults(self):
        self.assertEqual(get_buffer_window(1), 1)
        self.assertEqual(get_capacity_limit(1), 64)
        self.assertEqual(get_task_granularity(1), 2048)

    def test_large_workload_returns_valid_limits(self):
        recommendation = get_recommendation(1_000_000)
        self.assertGreaterEqual(recommendation["buffer_window"], 1)
        self.assertGreaterEqual(recommendation["parallel_tasks"], 1)
        self.assertGreaterEqual(recommendation["task_size"], 1)

    def test_invalid_workload_is_rejected(self):
        with self.assertRaises(ValueError):
            get_recommendation(0)
        with self.assertRaises(ValueError):
            get_recommendation(1.5)
        with self.assertRaises(ValueError):
            get_recommendation(True)

    def test_recommendations_stay_within_built_in_limits(self):
        for workload in (1, 2, 2048, 1_000_000, 10**1000):
            recommendation = get_recommendation(workload)
            self.assertLessEqual(recommendation["buffer_window"], 4096)
            self.assertLessEqual(recommendation["parallel_tasks"], 64)
            self.assertLessEqual(recommendation["task_size"], 2048)
            self.assertTrue(all(value >= 1 for value in recommendation.values()))


if __name__ == "__main__":
    unittest.main()