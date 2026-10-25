# NYC Yellow Taxi Data Quality Analysis

## Overview

This project performs a data quality assessment of the January 2025 NYC Yellow Taxi trip dataset using Python and pandas.

The goal is to identify missing values, unusual fare and distance values, and timestamp anomalies before making data-cleaning decisions.

The project demonstrates practical data engineering skills in data ingestion, exploratory data analysis, data validation, and technical documentation.

## Dataset

- **Source:** [NYC Taxi and Limousine Commission Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- **Dataset:** Yellow Taxi Trip Records, January 2025
- **Format:** Parquet
- **Records:** 3,475,226
- **Columns:** 20

The dataset is not included in this repository. Download the January 2025 Yellow Taxi Parquet file from the official source and place it at `data/yellow_tripdata_2025-01.parquet`.

## Tools and Technologies

- Python
- pandas
- PyArrow
- Parquet
- Git and GitHub

## Project Structure

```text
nyc-yellow-taxi-data-quality/
├── data/
│   └── yellow_tripdata_2025-01.parquet
├── .gitignore
├── requirements.txt
├── inspect_taxi_data.py
├── investigate_missing_values.py
├── investigate_negative_fares.py
├── test_data_quality.py
├── data_quality_report.md
└── README.md
```

The Parquet dataset and virtual environment are excluded from version control. The dataset must be downloaded separately before running the analysis.

## Data Quality Findings

The initial assessment identified the following:

| Check | Result |
|---|---:|
| Missing values in each of five columns | 540,149 |
| Negative fare amounts | 144,118 |
| Negative trip distances | 0 |
| Zero trip distances | 90,893 |
| Negative trip durations | 124 |
| Zero trip durations | 1,927 |

The five columns containing missing values are `passenger_count`, `RatecodeID`, `store_and_fwd_flag`, `congestion_surcharge`, and `Airport_fee`.

The missing-values investigation found that all 540,149 rows with these missing values have `payment_type = 0`. This association is documented for further interpretation; the cause and implications have not been established.

The negative-fare investigation identified patterns across payment types and differences between recorded totals and calculated fare components. These findings require careful interpretation because negative fares and reconciliation differences do not, by themselves, prove that records are invalid.

All findings are documented in `data_quality_report.md`.

## How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/damikuteyi/nyc-yellow-taxi-data-quality.git
cd nyc-yellow-taxi-data-quality
```

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Download the dataset

Download the January 2025 Yellow Taxi Parquet file from the [official NYC TLC source](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page).

Place it at:

```text
data/yellow_tripdata_2025-01.parquet
```

Create the `data` directory if it does not exist.

### 5. Run the data quality checks

```bash
python inspect_taxi_data.py
```

The script loads the dataset, calculates trip durations, and reports findings from four reusable checks:

- Negative fare amounts
- Zero trip distances
- Negative trip durations
- Missing values

Additional investigation scripts examine missing-value patterns and negative fare records.

## Automated Tests

The project includes automated tests for the reusable data quality validation functions. The tests use Python's built-in `unittest` framework and small sample DataFrames, so they do not require loading the full taxi dataset.

The test suite covers:

- Counting negative fare amounts and handling cases with no negative fares.
- Counting zero trip distances and handling cases with no zero distances.
- Counting negative trip durations and handling cases with no negative durations.
- Counting missing cells and affected rows, including datasets with no missing values.

Run the tests from the project root:

```bash
python -m unittest discover -v
```

**Current test result:** 8 tests passed.

The tests verify the expected behaviour of the validation functions for the scenarios covered. They do not guarantee that every possible data quality issue has been detected.

## Data Quality Approach

The project follows a cautious data quality workflow:

1. Inspect the dataset structure and data types.
2. Measure missing values.
3. Identify unusual fare and trip-distance values.
4. Calculate trip durations from pickup and drop-off timestamps.
5. Investigate patterns in missing values and negative fares.
6. Implement reusable validation checks.
7. Document findings and limitations before applying cleaning rules.

The original source data is preserved. No records are automatically deleted or corrected as part of this assessment.

## Project Status

**Completed**

- Initial dataset profiling and data quality investigation.
- Reusable validation functions for negative fares, zero distances, negative trip durations, and missing values.
- Investigation of missing-value patterns and negative fare records.
- Standardised `PASS` and `WARNING` statuses across the validation checks.
- Automated test suite with eight passing tests.
- Technical documentation and dependency declaration.

**Finalisation tasks**

- Verify that a fresh environment can reproduce the documented setup and test results.
- Review the data quality report and README for consistency.
- Confirm the final changes are committed and pushed to GitHub.
- Prepare the final portfolio demonstration and YouTube video.

The project flags records for investigation rather than automatically deleting or correcting them.