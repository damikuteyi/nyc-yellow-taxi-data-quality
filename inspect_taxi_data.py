import pandas as pd

# 1. Load the dataset, show overview
file_path = "data/yellow_tripdata_2025-01.parquet"
taxi_data = pd.read_parquet(file_path)
print(taxi_data.shape)

# 2. Show missing values, and calculate trip duration in minutes

missing_summary = taxi_data.isnull().sum().to_frame(name="missing_count")
missing_summary["missing_percentage"] = (
    missing_summary["missing_count"] / len(taxi_data) * 100
    )
missing_summary = missing_summary[missing_summary["missing_count"]> 0]
if len(missing_summary) == 0:
    print("PASS: No missing values found")
else:
    print("WARNING: Missing values detected")
print("\nMISSING VALUES REPORT")
print("==========================")
print(missing_summary)

taxi_data["trip_duration_minutes"] = (
    taxi_data["tpep_dropoff_datetime"]
    - taxi_data["tpep_pickup_datetime"]
).dt.total_seconds() / 60

# 3. Reusable data quality checks
def check_negative_fares(df):
    negative_fares = df["fare_amount"] < 0
    count = negative_fares.sum()

    return {
        "check_name": "negative_fares",
        "description": "Count trips with negative fare amounts",
        "records_affected": int(count),
        "status": "requires investigation",
    }


def check_zero_distances(df):
    zero_distance_count = (df["trip_distance"] == 0).sum()

    return {
        "check_name": "zero_trip_distances",
        "description": "Count trips with zero distances",
        "records_affected": int(zero_distance_count),
        "status": "requires investigation",
    }


def check_negative_durations(df):
    negative_duration = df["trip_duration_minutes"] < 0
    count = negative_duration.sum()

    return {
        "check_name": "negative_trip_durations",
        "description": "Count trips with negative durations",
        "records_affected": int(count),
        "status": "requires investigation",
    }

def check_missing_values(df):
    missing_cells = int(df.isnull().sum().sum())
    affected_rows = int(df.isnull().any(axis=1).sum())

    if missing_cells == 0:
        status = "PASS"
    else:
        status = "WARNING"

    return {
        "check_name": "missing_values",
        "description": "Count missing cells and affected rows",
        "records_affected": affected_rows,
        "missing_cells": missing_cells,
        "status": status,
    }


# 4. Run checks and generate the report
quality_results = [
    check_negative_fares(taxi_data),
    check_zero_distances(taxi_data),
    check_negative_durations(taxi_data),
    check_missing_values(taxi_data)
]

print("DATA QUALITY REPORT")
print("===================")

for result in quality_results:
    print(f"\nCheck: {result['check_name']}")
    print(f"Description: {result['description']}")
    print(f"Records affected: {result['records_affected']}")

    if "missing_cells" in result:
        print(f"Missing cells: {result['missing_cells']}")

    print(f"Status: {result['status']}")