# NYC Yellow Taxi Data Quality Analysis

## Overview

This project performs an initial data quality assessment of the January 2025 NYC Yellow Taxi trip dataset using Python and pandas.

The goal is to identify missing values, unusual fare and distance values, and timestamp anomalies before making any data-cleaning decisions.

This project demonstrates practical data engineering skills in data ingestion, exploratory data analysis, data validation, and technical documentation.

## Dataset

- **Source:** [NYC Taxi and Limousine Commission Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- **Dataset:** Yellow Taxi Trip Records, January 2025
- **Format:** Parquet
- **Records:** 3,475,226
- **Columns:** 20

The dataset is not included in this repository. Download the January 2025 Yellow Taxi Parquet file from the official source and place it in the `data/` directory.

## Tools and Technologies

- Python
- pandas
- PyArrow
- Parquet
- Git and GitHub

## Project Structure

```text
ai-data-engineering-portfolio-dk/
├── data/
│   └── yellow_tripdata_2025-01.parquet
├── .gitignore
├── inspect_taxi_data.py
├── data_quality_report.md
└── README.md
```

The `data/` directory and virtual environment are excluded from version control.

## Data Quality Findings

The initial assessment identified the following:

| Check | Result |
|---|---:|
| Missing values in five columns | 540,149 per column |
| Negative fare amounts | 144,118 |
| Negative trip distances | 0 |
| Zero trip distances | 90,893 |
| Negative trip durations | 124 |
| Zero trip durations | 1,927 |

The five columns containing missing values are `passenger_count`, `RatecodeID`, `store_and_fwd_flag`, `congestion_surcharge`, and `Airport_fee`.

These findings identify records that require further investigation. They do not automatically establish that those records are invalid.

## How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/damikuteyi/nyc-yellow-taxi-data-quality.git
cd nyc-yellow-taxi-data-quality
```

### 2. Create and activate a virtual environment

On Windows Command Prompt:

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

### 3. Install dependencies

```bash
python -m pip install pandas pyarrow
```

### 4. Download the dataset

Download the January 2025 Yellow Taxi Parquet file from the official NYC TLC website and place it at:

```text
data/yellow_tripdata_2025-01.parquet
```

Create the `data` directory if it does not already exist.

### 5. Run the analysis

```bash
python inspect_taxi_data.py
```

## Data Quality Approach

The project follows a cautious data quality workflow:

1. Inspect the dataset structure and data types.
2. Measure missing values.
3. Identify unusual fare and trip-distance values.
4. Calculate trip durations from pickup and drop-off timestamps.
5. Flag timestamp anomalies for investigation.
6. Document findings before implementing any cleaning rules.

The original source data is preserved. No records are deleted or modified as part of this initial assessment.
## Automated Data Quality Checks
The python script includes reusable functions to identify:
- Negative fare amounts
- Zero trip distances
- Negative trip durations

Run the checks with:
```bash
python inspect_taxi_data.py

## Next Steps

- Investigate patterns in missing values.
- Analyse negative fares by payment type.
- Examine zero-distance trips.
- Investigate negative-duration records.
- Implement reusable data quality checks. (done)
- Extend the project into a reproducible data ingestion and transformation pipeline.

## Project Status

**Milestone 1:** Initial data profiling and data quality documentation. (done)
