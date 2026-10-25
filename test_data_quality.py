
# Import Python's built-in testing framework
import unittest

# Import pandas so we can create small sample datasets
import pandas as pd

# Import the functions we want to test
from inspect_taxi_data import (
    check_negative_fares,
    check_zero_distances,
    check_negative_durations,
    check_missing_values,
)


# Group all negative-fare tests together
class TestNegativeFares(unittest.TestCase):

    def test_counts_negative_fares(self):
        # Create sample data with two negative fares
        df = pd.DataFrame({
            "fare_amount": [10.0, -5.0, 20.0, -2.0, 0.0]
        })

        # Run the function we want to test
        result = check_negative_fares(df)

        # Check whether the function returned the expected results
        self.assertEqual(result["records_affected"], 2)
        self.assertEqual(result["check_name"], "negative_fares")
        self.assertEqual(
            result["status"], "requires investigation"
        )

    def test_returns_zero_when_no_negative_fares(self):
        # All fares are zero or positive
        df = pd.DataFrame({
            "fare_amount": [10.0, 5.0, 0.0]
        })

        result = check_negative_fares(df)

        # No fares should be counted as negative
        self.assertEqual(result["records_affected"], 0)


# Group all zero-distance tests together
class TestZeroDistances(unittest.TestCase):

    def test_counts_zero_distances(self):
        df = pd.DataFrame({
            "trip_distance": [1.5, 0.0, 3.2, 0.0, 5.0]
        })

        result = check_zero_distances(df)

        self.assertEqual(result["records_affected"], 2)
        self.assertEqual(
            result["check_name"], "zero_trip_distances"
        )


# Group all negative-duration tests together
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


# Group all missing-value tests together
class TestMissingValues(unittest.TestCase):

    def test_counts_missing_cells_and_affected_rows(self):
        df = pd.DataFrame({
            "fare_amount": [10.0, None, 20.0, None],
            "trip_distance": [1.5, 2.0, None, None],
        })

        result = check_missing_values(df)

        # Four missing cells occur across three affected rows
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


# Run the tests if this file is executed directly
if __name__ == "__main__":
    unittest.main()
