import pandas as pd

# 1. Load the dataset
file_path = "data/yellow_tripdata_2025-01.parquet"
taxi_data = pd.read_parquet(file_path)

# 2. Select records with negative fare amounts
negative_fares = taxi_data[taxi_data["fare_amount"] < 0]

print("NEGATIVE FARE INVESTIGATION")
print("===========================")

print("Total negative-fare records:", len(negative_fares))

# 3. Compare negative fares by payment type
print("\nNegative fares by payment type:")
print(
    negative_fares["payment_type"]
    .value_counts(dropna=False)
    .sort_index()
)

# 4. Summarise fare amounts by payment type
print("\nFare summary by payment type:")
print(
    negative_fares.groupby("payment_type", dropna=False)["fare_amount"]
    .agg(["count", "mean", "min", "max"])
    .round(2)
)

# 5. Inspect the 10 most negative fare amounts
print("\n10 MOST NEGATIVE FARES")

columns_to_inspect = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "payment_type",
    "trip_distance",
    "fare_amount",
    "tip_amount",
    "tolls_amount",
    "total_amount",
]

print(
    negative_fares.nsmallest(10, "fare_amount")[columns_to_inspect]
    .to_string(index=False)
)

# 6. Inspect fare components for the 10 most negative fares
print("\nFARE COMPONENTS FOR THE 10 MOST NEGATIVE FARES")

fare_components = [
    "fare_amount",
    "extra",
    "mta_tax",
    "tip_amount",
    "tolls_amount",
    "improvement_surcharge",
    "congestion_surcharge",
    "Airport_fee",
    "cbd_congestion_fee",
    "total_amount",
]

print(
    negative_fares.nsmallest(10, "fare_amount")[
        ["payment_type", "trip_distance"] + fare_components
    ].to_string(index=False)
)

# 7. Compare negative fares with negative total amounts
negative_total_count = (negative_fares["total_amount"] < 0).sum()
nonnegative_total_count = (negative_fares["total_amount"] >= 0).sum()

print("\nTOTAL AMOUNT ANALYSIS")
print("Negative fares with negative total amounts:", int(negative_total_count))
print("Negative fares with zero or positive total amounts:", int(nonnegative_total_count))

# 8. Investigate negative fares with nonnegative totals
negative_fare_nonnegative_total = negative_fares[
    negative_fares["total_amount"] >= 0
]

print("\nNEGATIVE FARE WITH NONNEGATIVE TOTAL")
print("Records:", len(negative_fare_nonnegative_total))

print("\nPayment types:")
print(
    negative_fare_nonnegative_total["payment_type"]
    .value_counts(dropna=False)
    .sort_index()
)

# 9. Examine fare components for Flex Fare records
flex_fare_adjustments = negative_fare_nonnegative_total[
    negative_fare_nonnegative_total["payment_type"] == 0
]

print("\nFLEX FARE COMPONENT ANALYSIS")
print("Records:", len(flex_fare_adjustments))

fare_components = [
    "fare_amount",
    "extra",
    "mta_tax",
    "tip_amount",
    "tolls_amount",
    "improvement_surcharge",
    "congestion_surcharge",
    "Airport_fee",
    "cbd_congestion_fee",
    "total_amount",
]

print(
    flex_fare_adjustments[fare_components]
    .describe()
    .round(2)
)

# 10. Check whether fare components reconcile with total_amount
component_columns = [
    "fare_amount",
    "extra",
    "mta_tax",
    "tip_amount",
    "tolls_amount",
    "improvement_surcharge",
    "congestion_surcharge",
    "Airport_fee",
    "cbd_congestion_fee",
]

# Sum available components while ignoring missing values
flex_fare_adjustments = flex_fare_adjustments.copy()

flex_fare_adjustments["component_sum"] = (
    flex_fare_adjustments[component_columns].sum(axis=1, min_count=1)
)

flex_fare_adjustments["difference"] = (
    flex_fare_adjustments["total_amount"]
    - flex_fare_adjustments["component_sum"]
)

print("\nFARE RECONCILIATION CHECK")
print(
    flex_fare_adjustments[
        ["fare_amount", "component_sum", "total_amount", "difference"]
    ].head(10).to_string(index=False)
)

# 11. Inspect components for records with a difference of 2.50
difference_250 = flex_fare_adjustments[
    flex_fare_adjustments["difference"].round(2) == 2.50
]

print("\nRECORDS WITH A DIFFERENCE OF 2.50")
print(
    difference_250[
        [
            "fare_amount",
            "extra",
            "mta_tax",
            "tip_amount",
            "tolls_amount",
            "improvement_surcharge",
            "congestion_surcharge",
            "Airport_fee",
            "cbd_congestion_fee",
            "component_sum",
            "total_amount",
            "difference",
        ]
    ].head(10).to_string(index=False)
)

print("\nCOUNT OF RECORDS WITH A DIFFERENCE OF 2.50:")
print(len(difference_250))

# 12. Summarise fare reconciliation differences
print("\nFARE RECONCILIATION DIFFERENCE SUMMARY")

print(
    flex_fare_adjustments["difference"]
    .round(2)
    .value_counts()
    .head(10)
    .to_string()
)

# 13. Check missing fare components against reconciliation differences
print("\nMISSING FARE COMPONENTS AND DIFFERENCES")

missing_component_counts = (
    flex_fare_adjustments[component_columns]
    .isna()
    .sum(axis=1)
)

print("\nNumber of missing components:")
print(missing_component_counts.value_counts().sort_index())

print("\nAverage difference by number of missing components:")
print(
    flex_fare_adjustments.assign(
        missing_components=missing_component_counts
    )
    .groupby("missing_components")["difference"]
    .agg(["count", "mean", "median"])
    .round(2)
)