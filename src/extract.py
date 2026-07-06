"""
Extract traffic congestion data from Chicago Open Data
(Socrata API) and save raw JSON locally
This script performs NO transformations
"""

import json
from pathlib import Path
import requests

RAW_DATA_DIR = Path ("data/raw")
RAW_DATA_DIR.mkdir (parents=True, exist_ok=True)

PAGE_LIMIT = 1000

API_URL = "https://data.cityofchicago.org/resource/n4j6-wkkf.json"
RAW_JSON_OUTPUT = RAW_DATA_DIR/"chicago_traffic_raw.json"

def extract_chicago_traffic():
    """
    Retrieve all traffic records from the Chicago Open Data API
    using pagination and save the raw JSON response locally.
    """

    print("Requesting data from Chicago Open Data API...")

    all_records = []
    offset = 0

    while True:
        params ={
            "$limit":PAGE_LIMIT,
            "$offset":offset
        }

        response=requests.get(API_URL, params=params, timeout=30)
        response.raise_for_status() # fail fast if API breaks

        batch = response.json()

        if not batch:
            break

        all_records.extend(batch)
        offset += PAGE_LIMIT

        print(f"Retrieved {len(all_records)} records so far...")

    
    with open(RAW_JSON_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(all_records, f, indent=2)
    print(f"Extraction complete. Total records: {len(all_records)}")
    print(f"Raw data saved to {RAW_JSON_OUTPUT}")
    return all_records
if __name__ == "__main__":
    extract_chicago_traffic()        