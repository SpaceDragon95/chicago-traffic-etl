"""
Canonical transform functions for Chicago traffic ETL.
"""
import pandas as pd
from pathlib import Path

if __name__ == "__main__":
    data_path = Path("data/raw/chicago_traffic.json")

    df = pd.read_json(data_path)

# ====================
# Schema/ columns groups
# ====================

STRING_COLUMNS =["street",
    "direction",
    "from_street",
    "to_street",
    "starting_heading",
    "comments",
    ]

TITLE_CASE_COLUMNS =["street",
    "from_street",
    "to_street",
    ]

NUMERIC_TEXT_COLUMNS =["length_miles",
    "from_lon",
    "from_lat",
    "to_lon",
    "to_lat",
    "current_speed",
    ]

FLOAT_COLUMNS =["length_miles",
    "from_lon",
    "from_lat",
    "to_lon",
    "to_lat",
    ]

DATETIME_COLUMNS =["last_update",
]

DERIVE_COLUMNS =["length_meters",
]

# ====================
# Schema normalization
# ====================
def normalize_column_names(df):

    # ----- Rename raw source fields to canonical names

    # ----- Enforce canonical column presence
    pass

# ====================
# Canonical metadata
# ====================

def add_snapshot_timestamp(df):

    pass


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

# df = normalize_column_names(df)
# df = add_snapshot_timestamp(df)
# df = standardize_strings(df)
# df = cast_numeric(df)
# df = parse_datetimes(df)
# df = canonicalize_ids(df)
# df = derive_features(df)
