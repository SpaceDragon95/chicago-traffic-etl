"""
Extract traffic congestion data from Chicago Open Data
(Socrata API) and save raw JSON locally
This script performs NO transformations
"""

import json
import logging
from pathlib import Path
import requests
import pandas as pd

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
    
    logger = logging.getLogger(__name__)

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

        logger.info("Retrieved %d records so far", len(all_records))

    with open(RAW_JSON_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(all_records, f, indent=2)
    logger.info("Total records extracted %d", len(all_records))
    logger.info("Raw data saved to %s", RAW_JSON_OUTPUT)
    raw_df = pd.DataFrame(all_records)
    return raw_df
if __name__ == "__main__":
    extract_chicago_traffic()        