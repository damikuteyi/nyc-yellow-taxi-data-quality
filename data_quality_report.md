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

Three reusable Python functions have been implemented to identify potential data quality issues in the dataset.

Each function returns a structured dictionary containing four fields:

| Field | Purpose |
|---|---|
| `check_name` | Identifies the quality check |
| `description` | Explains what the check measures |
| `records_affected` | Records the number of rows matching the condition |
| `status` | Indicates that the identified records require investigation |

The results from the three checks are collected into a single list called `quality_results`. A Python loop then generates a consistent, human-readable report.

### Check Results

| Quality check | Records identified | Status |
|---|---:|---|
| Negative fare amounts | 144,118 | Requires investigation |
| Zero trip distances | 90,893 | Requires investigation |
| Negative trip durations | 124 | Requires investigation |

### Implementation Notes

- Each check uses a consistent result structure, making the results easier to combine and process.
- Trip duration is calculated in the existing `trip_duration_minutes` column and reused by the negative-duration check.
- Record counts are converted to standard Python integers to improve compatibility with reporting and serialization tools.
- The checks identify potential anomalies but do not automatically delete or modify records.

These functions provide a foundation for extending the quality checks and integrating their results into a more automated data validation pipeline.

## 6. Findings and Next Steps

The initial assessment identified three main areas for further investigation: missing values, unusual fare and distance values, and timestamp anomalies.

Recommended next steps:

1. **Investigate missing values:** Check whether the five affected columns are missing together in the same records and explore possible explanations.
2. **Investigate negative fares:** Examine their distribution by payment type and other relevant fields before deciding how to handle them.
3. **Review zero-distance trips:** Look for patterns in fare amounts, duration, payment type, and pickup/drop-off locations.
4. **Review negative durations:** Inspect the 124 affected records and determine whether the timestamp anomalies can be explained or corrected using reliable evidence.
5. **Preserve the source data:** Keep the original dataset unchanged. Apply any future cleaning rules to a separate, documented transformation.

## 7. Conclusion

This initial assessment establishes a baseline for the quality of the January 2025 NYC Yellow Taxi dataset. The identified anomalies provide a starting point for further investigation, but they do not, on their own, justify deleting or modifying records.

**Scope note:** This report documents initial profiling results. No records have been deleted, corrected, or otherwise removed from the original dataset.
