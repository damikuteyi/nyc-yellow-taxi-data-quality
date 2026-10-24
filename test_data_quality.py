
import unittest
import pandas as pd

from inspect_taxi_data import (
    check_negative_fares,
    check_zero_distances,
    check_negative_durations,
    check_missing_values,
)


class TestNegativeFares(unittest.TestCase):

    def test_counts_negative_fares(self):
        df = pd.DataFrame({
            "fare_amount": [10.0, -5.0, 20.0, -2.0, 0.0]
        })

        result = check_negative_fares(df)

        self.assertEqual(result["records_affected"], 2)
        self.assertEqual(result["check_name"], "negative_fares")
        self.assertEqual(result["status"], "requires investigation")


class TestZeroDistances(unittest.TestCase):

    def test_counts_zero_distances(self):
        df = pd.DataFrame({
            "trip_distance": [1.5, 0.0, 3.2, 0.0, 5.0]
        })

        result = check_zero_distances(df)

        self.assertEqual(result["records_affected"], 2)
        self.assertEqual(result["check_name"], "zero_trip_distances")


class TestNegativeDurations(unittest.TestCase):

    def test_counts_negative_durations(self):
        df = pd.DataFrame({
            "trip_duration_minutes": [10.0, -5.0, 20.0, -1.0, 0.0]
        })

        result = check_negative_durations(df)

        self.assertEqual(result["records_affected"], 2)
        self.assertEqual(
            result["check_name"], "negative_trip_durations"
        )


class TestMissingValues(unittest.TestCase):

    def test_counts_missing_cells_and_affected_rows(self):
        df = pd.DataFrame({
            "fare_amount": [10.0, None, 20.0, None],
            "trip_distance": [1.5, 2.0, None, None],
        })

        result = check_missing_values(df)

        self.assertEqual(result["records_affected"], 3)
        self.assertEqual(result["missing_cells"], 4)
        self.assertEqual(result["status"], "WARNING")

    def test_passes_when_no_values_are_missing(self):
        df = pd.DataFrame({
            "fare_amount": [10.0, 20.0],
            "trip_distance": [1.5, 2.0],
        })

        result = check_missing_values(df)

        self.assertEqual(result["records_affected"], 0)
        self.assertEqual(result["missing_cells"], 0)
        self.assertEqual(result["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
