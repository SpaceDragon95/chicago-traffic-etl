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

UPPER_CASE_COLUMNS =[
    "direction",
    "starting_heading",
]

LOWER_CASE_COLUMNS =[
    "comments",
]

NUMERIC_TEXT_COLUMNS =[
    "length_miles",
    "from_lon",
    "from_lat",
    "to_lon",
    "to_lat",
    "current_speed",
    ]

INTERGER_COLUMNS =[
    "current_speed"
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
    """
    Canonicalize identifier fields for consistent downstream use.
    """

    if "segment_id" not in df.columns:
        raise ValueError("segment_id column is missing")

    df["segment_id"] = (
        df["segment_id"]
        .astype(str)
        .str.strip()
    )

    return df

def standardize_strings(df):   
    # ----- Universal string cleanup
    df[STRING_COLUMNS] = df[STRING_COLUMNS].apply(
        lambda col: col.str.strip()
    )

    df[STRING_COLUMNS] = df[STRING_COLUMNS].apply(
        lambda col: col.mask(col=="", pd.NA)
    )

    df[STRING_COLUMNS] = df[STRING_COLUMNS].astype("string")

    # ----- Column-specific casing
    df[UPPER_CASE_COLUMNS] = df[UPPER_CASE_COLUMNS].str.upper()
    df[TITLE_CASE_COLUMNS] = df[TITLE_CASE_COLUMNS].str.title()
    df[LOWER_CASE_COLUMNS] = df[LOWER_CASE_COLUMNS].str.lower()

    return df

def cast_numeric(df):
    # ----- Universal numeric cleanup
    df[NUMERIC_TEXT_COLUMNS] = df[NUMERIC_TEXT_COLUMNS].apply(
        lambda col: col.str.strip()
    )

    # ----- Parse numeric text
    df[NUMERIC_TEXT_COLUMNS] = df[NUMERIC_TEXT_COLUMNS].apply (
        lambda col: pd.to_numeric(col, errors="coerce")
    )

    # ----- Cast integer and float columns
    df[INTERGER_COLUMNS] = df[INTERGER_COLUMNS].astype("Int64")
    df[FLOAT_COLUMNS] = df[FLOAT_COLUMNS].astype("float")

    return df

def parse_datetimes(df):
    # ----- Universal datetime cleanup
    df[DATETIME_COLUMNS] = df[DATETIME_COLUMNS].apply(
        lambda col: col.str.strip()
    )

    # ----- Parse datetime text
    df[DATETIME_COLUMNS] = df[DATETIME_COLUMNS].apply (
        lambda col: pd.to_datetime(col, errors="coerce")
    )
    return df

def derive_features(df):
    # ----- Feature derivation from canonical fields
    """
    Derive canonical and analytical features from normalized fields.
    """
    df["length_meters"] = df["length_miles"] * 1609.344

    return df

# ====================
# Pipeline execution
# ====================

if __name__ == "__main__":
    df = pd.read_json(data_path)
    df = normalize_column_names(df)
    df = add_snapshot_timestamp(df)
    df = canonicalize_ids(df)
    df = standardize_strings(df)
    df = cast_numeric(df)
    df = parse_datetimes(df)
    df = derive_features(df)
    print(df[["length_miles", "length_meters"]].head())

