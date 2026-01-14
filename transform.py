"""
Canonical transform functions for Chicago traffic ETL.
"""
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone

if __name__ == "__main__":
    data_path = Path("data/raw/chicago_traffic_raw.json")

    df = pd.read_json(data_path)

# ====================
# Schema/ columns groups
# ====================

STRING_COLUMNS =[
    "street",
    "direction",
    "from_street",
    "to_street",
    "starting_heading",
    "comments",
    ]

TITLE_CASE_COLUMNS =[
    "street",
    "from_street",
    "to_street",
    ]

NUMERIC_TEXT_COLUMNS =[
    "length_miles",
    "from_lon",
    "from_lat",
    "to_lon",
    "to_lat",
    "current_speed",
    ]

FLOAT_COLUMNS =[
    "length_miles",
    "from_lon",
    "from_lat",
    "to_lon",
    "to_lat",
    ]

DATETIME_COLUMNS =[
    "last_update",
]

DERIVE_COLUMNS =[
    "length_meters",
]

# ====================
# Schema normalization
# ====================
def normalize_column_names(df):
    """
    Rename raw source fields to canonical schema names
    and enforce required canonical column presence.    
    """
         
    RENAME_MAP={
        'segmentid': 'segment_id',
        '_direction': 'direction',
        '_fromst': 'from_street',
        '_tost': 'to_street',
        '_length': 'length_miles',
        '_strheading': 'starting_heading',
        'start_lon': 'from_lon',
        '_lif_lat': 'from_lat',
        '_lit_lon': 'to_lon',
        '_lit_lat': 'to_lat',
        '_traffic': 'current_speed',
        '_last_updt': 'last_update',
        }

    df=df.rename(columns=RENAME_MAP)

    # ----- Enforce canonical column presence

    REQUIRED_COLUMNS =[
        "segment_id",
        "direction",
        "from_street",
        "to_street",
        "length_miles",
        "starting_heading",
        "from_lon",
        "from_lat",
        "to_lon",
        "to_lat",
        "current_speed",
        "last_update",
        ]
    
    missing = set(REQUIRED_COLUMNS) - set(df.columns)

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    return df

# ====================
# Canonical metadata
# ====================

def add_snapshot_timestamp(df):
    """
    Add a UTC snapshot timestamp representing when the pipeline ran.
    """

    snapshot_ts = datetime.now(timezone.utc)
    df["snapshot_ts_utc"] = snapshot_ts

    return df
    
# ====================
# Transform functions
# ====================

def canonicalize_ids(df):
    # ---- Guardrails

    # ----- Universal ID cleanup
 
    # ----- Parse ID text

    # ----- Cast ID column
    pass

def standardize_strings(df):
    # ---- Guardrails
   
    # ----- Universal string cleanup
    
    # ----- Column-specific casing
    pass

def cast_numeric(df):
    # ---- Guardrails

    # ----- Universal numeric cleanup

    # ----- Parse numeric text

    # ----- Cast integer columns
    pass

def parse_datetimes(df):
    # ---- Guardrails

    # ----- Universal datetime cleanup
    
    # ----- Parse datetime text
    pass

def derive_features(df):
    # ---- Guardrails

    # ----- Feature derivation from canonical fields

    # ----- Time-based features (hour, day, weekend, etc.)
    pass

# ====================
# Pipeline execution
# ====================

if __name__ == "__main__":
    df = pd.read_json(data_path)
    df = normalize_column_names(df)
    df = add_snapshot_timestamp(df)
    # df = standardize_strings(df)
    # df = cast_numeric(df)
    # df = parse_datetimes(df)
    # df = canonicalize_ids(df)
    # df = derive_features(df)

