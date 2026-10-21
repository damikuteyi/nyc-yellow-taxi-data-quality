import pandas as pd
file_path = "data/yellow_tripdata_2025-01.parquet"
taxi_data = pd.read_parquet(file_path)

'''
print("First five rows:")
print(taxi_data.head())

print("Dataset shape:")
print(taxi_data.shape)

print("Column names:")
print(taxi_data.columns.tolist())

print("Data types:")
print(taxi_data.dtypes)
'''
'''
print("\nMissing values per column:")
print(taxi_data.isnull().sum())

print("\nNegative trip distances:")
print((taxi_data["trip_distance"] < 0).sum())

print("\nNegative fare amounts:")
print((taxi_data["fare_amount"] < 0).sum())

print("\nZero trip distances:")
print((taxi_data["trip_distance"] == 0).sum())

negative_fares = taxi_data[taxi_data["fare_amount"] < 0]
print("\nFirst 10 records with negative fares:")
print(
    negative_fares[
        ["fare_amount", "total_amount", "payment_type",
         "trip_distance", "passenger_count"]
    ].head(10)
)

print("\nPayment types among negative-fare records:")
print(negative_fares["payment_type"].value_counts().sort_index())

print("\nPayment types across all records:")
print(taxi_data["payment_type"].value_counts().sort_index())


print("\nNegative-fare summary by payment type:")

print(
    negative_fares.groupby("payment_type")[
        ["fare_amount", "total_amount"]].agg(["count", "mean", "min", "max"]).round(2))
'''

# Calculate trip duration in minutes
taxi_data["trip_duration_minutes"] = (
    taxi_data["tpep_dropoff_datetime"]
    - taxi_data["tpep_pickup_datetime"]
).dt.total_seconds() / 60

'''
print("\nTrip duration summary (minutes):")
print(taxi_data["trip_duration_minutes"].describe())

print("\nTrips with negative duration:")
print((taxi_data["trip_duration_minutes"] < 0).sum())

print("\nTrips with zero duration:")
print((taxi_data["trip_duration_minutes"] == 0).sum())

print("\n10 shortest trip durations:")

print(
    taxi_data.nsmallest(10, "trip_duration_minutes")[
        [
            "tpep_pickup_datetime",
            "tpep_dropoff_datetime",
            "trip_duration_minutes",
            "trip_distance",
            "fare_amount",
            "total_amount",
        ]
    ]
)

negative_duration_count = (
    taxi_data["trip_duration_minutes"] < 0
).sum()

zero_duration_count = (
    taxi_data["trip_duration_minutes"] == 0
).sum()

valid_duration_count = (
    taxi_data["trip_duration_minutes"] > 0
).sum()

print("\nTrip duration validation:")
print("Valid positive durations:", valid_duration_count)
print("Zero durations:", zero_duration_count)
print("Negative durations:", negative_duration_count)


taxi_data["valid_timestamp_order"] = (
    taxi_data["tpep_dropoff_datetime"]
    >= taxi_data["tpep_pickup_datetime"]
)

print("\nTimestamp validation results:")
print(taxi_data["valid_timestamp_order"].value_counts())
'''

def check_negative_fares(df):
    negative_fares = df["fare_amount"] < 0
    count = negative_fares.sum()
    print("Negative fare amounts:", count)
    return count



def check_zero_distances(df):
    zero_distance_count = df[df["trip_distance"] == 0].shape[0]
    print("Zero trip distances:", zero_distance_count)
    return zero_distance_count



def check_negative_durations(df):
   # duration = (df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]).dt.total_seconds() / 60
    negative_duration = df["trip_duration_minutes"] < 0
    count = negative_duration.sum()
    print("Negative trip durations:", count)
    return count

check_negative_fares(taxi_data)
check_zero_distances(taxi_data)
check_negative_durations(taxi_data)