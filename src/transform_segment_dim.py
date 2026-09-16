"""
Create and transform data for the project's segment dimension.

This module standardizes the raw roadway segment data, converts values
to the appropriate data types, derives additional attributes, and
prepares the data for loading into the segment dimension table.
"""

import pandas as pd
import logging

# ====================
# Schema/ columns groups
# ====================

RAW_STRING_COLUMNS = [ 
    "street",
    "direction",
    "from_street",
    "to_street",
    "starting_heading",
    "comments",
]

RAW_NUMERIC_COLUMNS = [
    "segment_id",
    "length_miles",
    "from_lon",
    "from_lat",
    "to_lon",
    "to_lat",
]

TITLE_CASE_COLUMNS = [
    "street",
    "from_street",
    "to_street",
    "comments",
]

UPPER_CASE_COLUMNS = [
    "direction",
    "starting_heading",
]

INTEGER_COLUMNS = [
    "segment_id"
]

FLOAT_COLUMNS = [
    "length_miles",
    "from_lon",
    "from_lat",
    "to_lon",
    "to_lat",
]

DERIVED_COLUMNS = [
    "length_meters"
]

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
        '_comments': 'comments',
        }

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
        ]

# ====================
# Schema normalization
# ====================
def normalize_column_names(df):
    """
    Normalize source column names to the project schema.

    Renames raw Chicago traffic columns using the defined rename map
    and validates that all required columns are present.

    Args:
        df (pandas.DataFrame):
            DataFrame containing raw Chicago traffic data.

    Returns:
        pandas.DataFrame:
            DataFrame with normalized column names.

    Raises:
        ValueError:
            If any required columns are missing.
    """
    df=df.rename(columns=RENAME_MAP)
    
    # ----- Enforce canonical column presence
    missing = set(REQUIRED_COLUMNS) - set(df.columns)

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    return df

def standardize_string_columns(df):   
    # ----- Universal string cleanup
    df[RAW_STRING_COLUMNS] = df[RAW_STRING_COLUMNS].apply(
        lambda col: col.str.strip())
    
    df[RAW_STRING_COLUMNS] = df[RAW_STRING_COLUMNS].apply(
        lambda col: col.mask(col =="", pd.NA)
    )

    df[RAW_STRING_COLUMNS] = df[RAW_STRING_COLUMNS].astype("string")

    # ----- Title Case Columns
    df[TITLE_CASE_COLUMNS] = df[TITLE_CASE_COLUMNS].apply(
        lambda col: col.str.title()
    )

    # ----- Upper Case Columns
    df[UPPER_CASE_COLUMNS] = df[UPPER_CASE_COLUMNS].apply(
        lambda col: col.str.upper()
    )

    return df

def cast_numeric_columns(df):
    """
    Clean and convert numeric columns.

    Removes leading and trailing whitespace from numeric values,
    converts invalid values to NaN, and casts columns to their
    appropriate integer or floating-point data types.

    Args:
        df (pandas.DataFrame):
            DataFrame containing the normalized segment data.

    Returns:
        pandas.DataFrame:
            The DataFrame with standardized numeric columns.
    """

    # ----- Universal numeric clean-up
    df[RAW_NUMERIC_COLUMNS] = df[RAW_NUMERIC_COLUMNS].apply(
        lambda col: col.astype("string").str.strip()
    )

    df[RAW_NUMERIC_COLUMNS] = df[RAW_NUMERIC_COLUMNS].apply(
        lambda col: pd.to_numeric(col, errors="coerce")
    )

    # ----- Cast integer and float columns
    df[INTEGER_COLUMNS] = df[INTEGER_COLUMNS].astype("Int64")

    df[FLOAT_COLUMNS] = df[FLOAT_COLUMNS].astype("float")

    return df

def derive_features(df):
    """
    Derive additional attributes from the standardized segment data.

    Calculates the roadway segment length in meters from the length in
    miles.

    Args:
        df (pandas.DataFrame):
            DataFrame containing standardized segment data.

    Returns:
        pandas.DataFrame:
            The DataFrame with derived feature columns added.
    """

    # ----- Feature derivation from canonical fields

    df["length_meters"] = df["length_miles"] * 1609.344

    return df

# ====================
# Segment Pipeline execution
# ====================

def segment_dim(df):
    """
    Execute the segment dimension transformation pipeline.

    Applies schema normalization, standardizes string and numeric
    columns, derives additional features, and returns the completed
    segment dimension DataFrame.

    Args:
        df (pandas.DataFrame):
            Raw segment data.

    Returns:
        pandas.DataFrame:
            The fully transformed segment dimension DataFrame.
    """

    logger = logging.getLogger(__name__)
    logger.info("Segment dimension received %d rows", len(df))

    df = normalize_column_names(df)
    df = standardize_string_columns(df)
    df = cast_numeric_columns(df)
    df = derive_features(df)

    logger.info("Segment dimension produced %d rows", len(df))
    return df


