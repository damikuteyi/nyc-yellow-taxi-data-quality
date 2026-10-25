# NYC Yellow Taxi Data Quality Report

## 1. Dataset Overview

- **Dataset:** NYC Yellow Taxi Trip Records — January 2025
- **Total records:** 3,475,226
- **Total columns:** 20
- **Source format:** Parquet

This report assesses missing values, fare amounts, trip distances, and trip durations to identify potential data quality issues before cleaning or transformation.

## 2. Missing Values

Five columns contain missing values.

| Column | Missing values |
|---|---:|
| `passenger_count` | 540,149 |
| `RatecodeID` | 540,149 |
| `store_and_fwd_flag` | 540,149 |
| `congestion_surcharge` | 540,149 |
| `Airport_fee` | 540,149 |

Each of these columns has missing values in approximately **15.54% of records**.

**Finding:** The matching missing-value counts may indicate a shared pattern in the affected records. Further investigation is needed to determine whether these missing values have a common cause and whether they should be retained, imputed, or handled differently.

### Missing-Value Pattern Investigation

The five columns with missing values—`passenger_count`, `RatecodeID`, `store_and_fwd_flag`, `congestion_surcharge`, and `Airport_fee`—each contain 540,149 missing values.

Further investigation established that all 540,149 rows with missing values across these five columns have `payment_type = 0`, which the TLC data dictionary identifies as Flex Fare. Conversely, all rows with `payment_type = 0` in this dataset have missing values in all five columns.

This represents 100% of Flex Fare rows and approximately 15.54% of the complete dataset.

The pattern suggests that the missing values are associated with the Flex Fare category. However, the observed association does not establish why the fields are missing or whether their absence is expected. Further validation against authoritative documentation is required before deciding how to handle these values.

No records have been deleted or modified as a result of this investigation.

## 3. Fare and Distance Checks

| Quality check | Records identified |
|---|---:|
| Negative fare amounts | 144,118 |
| Negative trip distances | 0 |
| Zero trip distances | 90,893 |

**Findings:**

- Negative fare amounts require investigation. They may be associated with adjustments, reversals, or other transaction circumstances and should not automatically be classified as invalid.
- No negative trip distances were identified.
- Zero trip distances require further analysis to determine whether they represent legitimate records, data-entry issues, or other unusual trip circumstances.

## Negative Fare Investigation

### Findings

The January 2025 NYC Yellow Taxi dataset contains **144,118 records with negative `fare_amount` values**.

The investigation identified the following:

- Negative fares occur across multiple payment types, including Flex Fare (`payment_type = 0`), cash, no charge and disputes.
- Of the records with negative fares, 81,402 have a non-negative `total_amount`. Of these, 81,401 are associated with payment type 0.
- The Flex Fare records examined show varied differences between `total_amount` and the sum of available fare components. The reconciliation differences are not consistently zero.
- Some fare components are missing in these records, so the calculated component sum may not include every amount relevant to the recorded total.

### Data Quality Assessment

Negative fare values warrant investigation, but their presence alone does not establish that a record is invalid. The available analysis has not established the reason for every negative fare or the expected reconciliation rules for Flex Fare transactions.

**Decision:** Retain negative fares as a validation finding for investigation rather than automatically deleting or correcting these records. Further interpretation would require authoritative documentation of the applicable fare and adjustment rules.

### Limitation

This investigation identifies patterns in the dataset but does not establish the cause of negative fares or prove that the associated total amounts are incorrect.

## 4. Trip Duration Checks

Trip duration was calculated as the difference between the drop-off and pickup timestamps.

| Duration category | Records identified |
|---|---:|
| Positive duration | 3,473,175 |
| Zero duration | 1,927 |
| Negative duration | 124 |
| **Total** | **3,475,226** |

**Findings:**

- Most records have positive trip durations.
- The 124 negative-duration records have drop-off timestamps earlier than their pickup timestamps. These records should be flagged for investigation because their timestamp sequence is inconsistent.
- The 1,927 zero-duration records should also be investigated. They may reflect timestamp precision, recording issues, or other circumstances; the duration alone does not establish that a record is invalid.

## 5. Automated Data Quality Checks

Four reusable Python functions have been implemented to identify potential data quality issues in the dataset.

Each function returns a structured dictionary containing four fields:

| Field | Purpose |
|---|---|
| `check_name` | Identifies the quality check |
| `description` | Explains what the check measures |
| `records_affected` | Records the number of rows matching the condition |
| `status` | Returns PASS when no records match the validation rule and WARNING when one or more records match it.|

The results from the four checks are collected into a single list called `quality_results`. A Python loop then generates a consistent, human-readable report.

### Check Results

| Quality check | Records identified | Status |
|---|---:|---|
| Negative fare amounts | 144,118 | WARNING |
| Zero trip distances | 90,893 | WARNING |
| Negative trip durations | 124 | WARNING |
| Missing values | 540,149 affected rows; 2,700,745 missing cells | WARNING |

A `WARNING` status means that one or more records matched the defined validation rule. It does not automatically mean that every flagged record is invalid.

The missing-values check reports both affected rows and missing cells because a single row can contain missing values in multiple columns. The other checks report the number of records matching their respective conditions.

### Implementation Notes

- Each check uses a consistent result structure, making the results easier to combine and process.
- Trip duration is calculated in the existing `trip_duration_minutes` column and reused by the negative-duration check.
- Record counts are converted to standard Python integers to improve compatibility with reporting and serialization tools.
- The checks identify potential anomalies but do not automatically delete or modify records.
- The missing cells are not the same as distinct affected records, as a single trip can have missing values in multiple columns.
- The missing-values check returns `Pass` when no missing cells are found and `Warning` when at least one missing cell is found

These functions provide a foundation for extending the quality checks and integrating their results into a more automated data validation pipeline.

## 6. Findings and Next Steps

The initial investigations have established several patterns, but some causes and implications remain unresolved.

Recommended next steps:

1. **Validate missing-value interpretation:** Compare the observed Flex Fare pattern with authoritative documentation before deciding how to handle missing values.
2. **Clarify negative-fare rules:** Establish the applicable fare and adjustment rules before classifying negative fares or reconciling their totals.
3. **Investigate zero-distance trips:** Examine fare amounts, duration, payment type, and pickup/drop-off locations to understand the flagged records.
4. **Review negative durations:** Inspect the 124 affected records and determine whether the timestamp anomalies can be explained using reliable evidence.
5. **Preserve source data:** Keep the original dataset unchanged and apply any future cleaning rules to a separate, documented transformation.

## 7. Conclusion

This initial assessment establishes a baseline for the quality of the January 2025 NYC Yellow Taxi dataset. The identified anomalies provide a starting point for further investigation, but they do not, on their own, justify deleting or modifying records.

**Scope note:** This report documents initial profiling results. No records have been deleted, corrected, or otherwise removed from the original dataset.
