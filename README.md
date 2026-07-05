# Chicago Traffic ETL Pipeline

A production-style ETL pipeline that ingests Chicago traffic congestion data, transforms it using Python and pandas, stores analytical Parquet files in AWS S3, and loads structured data into PostgreSQL on AWS RDS.

## API (Chicago Open Data)
        ↓
extract.py
        ↓
Raw JSON
        ↓
transform.py
        ↓
transform_analytics.py
        ↓
Parquet
        ↓
AWS S3
        ↓
PostgreSQL (AWS RDS)

## Project Goals
- Practice production-style ETL architecture
- Learn AWS cloud storage and databases
- Implement layered transformations
- Work with structured analytical datasets
- Prepare for future orchestration with Airflow

## Technologies Used

- Python
- pandas
- pyarrow
- boto3
- PostgreSQL
- pgAdmin
- AWS S3
- AWS RDS
- Git / GitHub

## Data Source

Chicago Open Data Portal:
https://data.cityofchicago.org/
Dataset: Traffic Tracker - Congestion Estimates by Road Segment

## Project Structure

chicago-traffic-etl/
│
├── extract.py
├── transform.py
├── transform_analytics.py
├── load.py
│
├── data/
│   ├── raw/
│   └── analytical/
│
├── requirements.txt
└── README.md

## Canonical Transformations

- Normalize column names
- Standardize string formatting
- Cast numeric and datetime types
- Add snapshot timestamps
- Derive distance metrics

## Analytical Transformations

- hour_of_day
- day_of_week
- is_weekend
- speed_band
- has_traffic_data

## AWS Components

- S3 bucket used for analytical Parquet storage
- PostgreSQL hosted on AWS RDS
- IAM user configured for CLI and boto3 access

## Running the Pipeline

1. Extract raw traffic data
python extract.py

2. Run transformations and load pipeline
python transform.py
       transform_analytics.py 
python load.py

## Future Improvements
- Airflow orchestration
- Partitioned Parquet datasets
- Athena integration
- Incremental loading
- Docker containerization
- Star schema warehouse design
- dashboard layer

## Key Learning Outcomes

- Built a layered ETL architecture
- Worked with AWS S3 and RDS
- Implemented analytical feature engineering
- Managed cloud IAM permissions securely
- Connected Python pipelines to PostgreSQL

# Restructuring Plan

## Outstanding Questions
- Verify starting_heading data type.
- Confirm whether comments vary by traffic reading.
- Verify segment_id is always numeric.

  
