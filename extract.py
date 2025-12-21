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

API_URL = "https://data.cityofchicago.org/resource/t2rn-p8d7.json"
OUTPUT_FILE = RAW_DATA_DIR/"chicago_traffic_raw.json"

def extract_chicago_traffic():
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

    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_records, f, indent=2)
    print(f"Extraction complete. Total records: {len(all_records)}")
    print(f"Raw data saved to {OUTPUT_FILE}")
if __name__ == "__main__":
    extract_chicago_traffic()        