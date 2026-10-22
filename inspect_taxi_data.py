import pandas as pd

# 1. Load the dataset
file_path = "data/yellow_tripdata_2025-01.parquet"
taxi_data = pd.read_parquet(file_path)

# 2. Calculate trip duration in minutes
print(taxi_data.shape)
missing_values = taxi_data.isnull().sum() 
print(missing_values[missing_values > 0])

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


# 4. Run checks and generate the report
quality_results = [
    check_negative_fares(taxi_data),
    check_zero_distances(taxi_data),
    check_negative_durations(taxi_data),
]

print("DATA QUALITY REPORT")
print("===================")

for result in quality_results:
    print("\nCheck:", result["check_name"])
    print("Description:", result["description"])
    print("Records affected:", result["records_affected"])
    print("Status:", result["status"])
