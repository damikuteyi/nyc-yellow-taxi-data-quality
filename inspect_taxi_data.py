from pathlib import Path
import pandas as pd

#Locate the project directory and dataset
PROJECT_DIR = Path(__file__).resolve().parent
DATA_PATH = PROJECT_DIR / "data" / "yellow_tripdata_2025-01.parquet"

# 3. Reusable data quality checks

def check_negative_fares(df):
    negative_fares = df["fare_amount"] < 0
    count = int(negative_fares.sum())

    return {
        "check_name": "negative_fares",
        "description": "Count trips with negative fare amounts",
        "records_affected": count,
        "status": "WARNING" if count > 0 else "PASS",
    }


def check_zero_distances(df):
    zero_distance_count = int((df["trip_distance"] == 0).sum())

    return {
        "check_name": "zero_trip_distances",
        "description": "Count trips with zero distances",
        "records_affected": zero_distance_count,
        "status": "WARNING" if zero_distance_count > 0 else "PASS",
    }


def check_negative_durations(df):
    negative_duration = df["trip_duration_minutes"] < 0
    count = int(negative_duration.sum())

    return {
        "check_name": "negative_trip_durations",
        "description": "Count trips with negative durations",
        "records_affected": count,
        "status": "WARNING" if count > 0 else "PASS",
    }


def check_missing_values(df):
    missing_cells = int(df.isnull().sum().sum())
    affected_rows = int(df.isnull().any(axis=1).sum())

    return {
        "check_name": "missing_values",
        "description": "Count missing cells and affected rows",
        "records_affected": affected_rows,
        "missing_cells": missing_cells,
        "status": "WARNING" if affected_rows > 0 else "PASS",
    }


def main():
    # 1. Load the dataset
    print("Loading taxi dataset...")

    taxi_data = pd.read_parquet(DATA_PATH)

    print(f"Dataset loaded: {taxi_data.shape[0]:,} rows, "
          f"{taxi_data.shape[1]} columns")
    
    # 2. Calculate trip duration in minutes
    taxi_data["trip_duration_minutes"] = (
        taxi_data["tpep_dropoff_datetime"]
        - taxi_data["tpep_pickup_datetime"]
    ).dt.total_seconds() / 60

    # 3. Run the data quality checks
    quality_results = [
        check_negative_fares(taxi_data),
        check_zero_distances(taxi_data),
        check_negative_durations(taxi_data),
        check_missing_values(taxi_data),
    ]

    # 4. Print the data quality report
    print("\nDATA QUALITY REPORT")
    print("===================")

    for result in quality_results:
        print(f"\nCheck: {result['check_name']}")
        print(f"Description: {result['description']}")
        print(f"Records affected: {result['records_affected']}")

        if "missing_cells" in result:
            print(f"Missing cells: {result['missing_cells']}")

        print(f"Status: {result['status']}")

if __name__ == "__main__":
    main()