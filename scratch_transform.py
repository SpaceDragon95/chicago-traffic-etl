"""
Canonical transform functions for Chicago traffic ETL.
"""
.gitignore

import pandas as pd

data = {
    "_segID_": ["101", " 102", "103 ", "104"],
    "direction": [" n ", "S", "", None],
    "street": ["  main st ", "ELM STREET", "oak avenue", ""],
    "traffic_condition": ["Heavy ", " LIGHT", None, ""],
    "traffic_count": ["42 ", " 19", None, ""],
    "average_speed": [None, "", "  35.5 ", "22.0  "],
    "travel_time_seconds": ["  120", None, " 300 ", ""],
    "snapshot_ts_utc": [
    "",
    "2024-01-15T18:00:00Z",
    None,
    "2024-01-15T17:00:00Z"
    ],
    "measurement_ts_utc": [
    "2024-01-15T16:58:30Z",
    None,
    "2024-01-15T17:59:10Z",
    ""
    ],
    "event_date": [
    None,
    "2024-01-16",
    "2024-01-15",
    ""
    ],
}

df = pd.DataFrame(data)

# ====================
# Schema/ columns groups
# ====================

STRING_COLUMNS = ["direction",
    "street",
    "traffic_condition",
    ]
NUMERIC_TEXT_COLUMNS = ["traffic_count",
    "travel_time_seconds",
    "average_speed",
    ]
INT_COLUMNS = ["traffic_count",
    "travel_time_seconds",
    ]
DATETIME_COLUMNS = ["snapshot_ts_utc",
    "measurement_ts_utc",
    "event_date",
    ]

CONVERT_DT_COLUMNS = ["snapshot_ts_utc",
    "measurement_ts_utc",
    ]

# ====================
# Transform functions
# ====================

def canonicalize_ids(df):
    # ---- Gardrails

    required_columns = {"_segID_", "snapshot_ts_utc"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
        f"canonicalize_ids: missing required columns: {missing_columns}"
    )

    df.rename(columns={'_segID_': 'segment_id'}, inplace=True)

    # ----- Universal ID cleanup
    df["segment_id"] = df["segment_id"].str.strip()
    
    # ----- Parse ID text
    df["segment_id"] = pd.to_numeric(df["segment_id"], errors="coerce")

    # ----- Cast ID column
    df["segment_id"] = df["segment_id"].astype("Int64")

    null_count = df["segment_id"].isna().sum()
    if null_count > 0:
        print(f"Canonicalize IDs: Found {null_count} null segment_id values.")

    duplicate_count = df[["segment_id", "snapshot_ts_utc"]].duplicated().sum()
    if duplicate_count > 0:
        print(f"Canonicalize IDs: Found {duplicate_count} duplicate values.")
   
    return df


def standardize_strings(df):
    # ---- Gardrails
    
    required_columns = {"direction",
    "street",
    "traffic_condition",
    }
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
        f"standardize_strings: missing required columns: {missing_columns}"
    )


    # ----- Universal string cleanup
    df[STRING_COLUMNS] = df[STRING_COLUMNS].apply(
        lambda col: col.str.strip()
    )

    df[STRING_COLUMNS] = df[STRING_COLUMNS].apply(
        lambda col: col.mask(col=="", pd.NA)
    )

    df[STRING_COLUMNS] = df[STRING_COLUMNS].astype("string")

    # ----- Column-specific casing
    df["direction"] = df["direction"].str.upper()
    df["street"] = df["street"].str.title()
    df["traffic_condition"] = df["traffic_condition"].str.lower()

    return df


def cast_numeric(df):
    # ---- Gardrails

    required_columns = {"traffic_count",
    "travel_time_seconds",
    "average_speed",
    }
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
        f"cast_numeric: missing required columns: {missing_columns}"
    )

    # ----- Universal numeric cleanup
    df[NUMERIC_TEXT_COLUMNS] = df[NUMERIC_TEXT_COLUMNS].apply(
        lambda col: col.str.strip()
    )

    # ----- Parse numeric text
    df[NUMERIC_TEXT_COLUMNS] = df[NUMERIC_TEXT_COLUMNS].apply (
        lambda col: pd.to_numeric(col, errors="coerce")
    )

    # ----- Cast integer columns
    df[INT_COLUMNS] = df[INT_COLUMNS].astype("Int64")

    return df

def parse_datetimes(df):
    # ---- Gardrails

    required_columns = {"snapshot_ts_utc",
    "measurement_ts_utc",
    "event_date",
    }
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
        f"parse_datetime: missing required columns: {missing_columns}"
    )

    # ----- Universal datetime cleanup
    df[DATETIME_COLUMNS] = df[DATETIME_COLUMNS].apply(
        lambda col: col.str.strip()
    )

    # ----- Parse datetime text
    df[DATETIME_COLUMNS] = df[DATETIME_COLUMNS].apply (
        lambda col: pd.to_datetime(col, errors="coerce")
    )

    df["snapshot_ts_ct"] = df["snapshot_ts_utc"].dt.tz_convert("America/Chicago")

    df["measurement_ts_ct"] = df["measurement_ts_utc"].dt.tz_convert("America/Chicago")

    return df



# ====================
# Pipeline execution
# ====================

df = standardize_strings(df)
df = cast_numeric(df)
df = parse_datetimes(df)
df = canonicalize_ids(df)

print("\n=== FINAL DATAFRAME ===")
print(df)

print("\n=== DTYPES ===")
print(df.dtypes)