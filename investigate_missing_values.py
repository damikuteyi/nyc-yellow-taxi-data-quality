
import pandas as pd

# 1. Load the dataset
file_path = "data/yellow_tripdata_2025-01.parquet"
taxi_data = pd.read_parquet(file_path)

# 2. Identify rows where all five columns are missing
missing_columns = [
    "passenger_count",
    "RatecodeID",
    "store_and_fwd_flag",
    "congestion_surcharge",
    "Airport_fee",
]

all_five_missing = taxi_data[missing_columns].isnull().all(axis=1)

print("Rows missing values in all five columns:", int(all_five_missing.sum()))

# 3. Compare payment types between the two groups
print("\nPAYMENT TYPE COMPARISON")

print("\nRows missing all five values:")
print(
    taxi_data.loc[all_five_missing, "payment_type"]
    .value_counts(dropna=False)
    .sort_index()
)

print("\nRows with at least one of the five values present:")
print(
    taxi_data.loc[~all_five_missing, "payment_type"]
    .value_counts(dropna=False)
    .sort_index()
)

# 4. Investigate Flex Fare rows
flex_fare_rows = taxi_data.loc[all_five_missing]
flex_fare_count = (taxi_data["payment_type"] == 0).sum()

print("\nFLEX FARE SUMMARY")
print("Total Flex Fare rows:", int(flex_fare_count))
print("Rows missing all five values:", len(flex_fare_rows))

if flex_fare_count > 0:
    percentage = len(flex_fare_rows) / flex_fare_count * 100
    print("Percentage of Flex Fare rows missing all five values:",
          round(percentage, 2), "%")
else:
    print("No Flex Fare rows found; percentage cannot be calculated.")

print("\nVENDOR DISTRIBUTION")
print(flex_fare_rows["VendorID"].value_counts(dropna=False))

print("\nSAMPLE OF FIVE AFFECTED TRIPS")
print(
    flex_fare_rows[
        [
            "VendorID",
            "tpep_pickup_datetime",
            "tpep_dropoff_datetime",
            "trip_distance",
            "fare_amount",
            "total_amount",
            "payment_type",
        ]
    ].head()
)
