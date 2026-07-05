import pandas as pd
import boto3
from pathlib import Path

from transform import canonical_transform
from transform_analytics import derive_analytical_features

ANALYTICAL_DATA_DIR = Path ("data/analytical")
PARQUET_OUTPUT = ANALYTICAL_DATA_DIR /"chicago_traffic_analytical.parquet"
S3_BUCKET = "dawn-chicago-traffic-etl"
S3_KEY = "chicago-traffic/analytical/chicago_traffic_analytical.parquet"

def run_load():
    # Get configuration values for the run
    data_path = Path("data/raw/chicago_traffic_raw.json")

    # Read raw Chicago traffic JSON file
    df_raw = pd.read_json(data_path)

    print("Raw JSON loaded")

    # Send data through canonical transformation
    df_canonical = canonical_transform(df_raw)

    print("Canonical transformation complete")

    # Send data through analytical transformation
    df_analytical = derive_analytical_features(df_canonical)

    print("Analytical transformation complete")

    # Save transformed data as Parquet
    df_analytical.to_parquet(PARQUET_OUTPUT)

    print(f"Parquet data saved to {PARQUET_OUTPUT}")

    # Upload Parquet file to S3, replacing prior version
    s3 = boto3.client("s3")
    s3.upload_file(str(PARQUET_OUTPUT), S3_BUCKET, S3_KEY)

    print("Upload to S3 complete")

if __name__ == "__main__":
    run_load()

