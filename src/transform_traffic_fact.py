"""
Transform raw Chicago traffic observations into traffic fact-table records.

This module standardizes extracted traffic data, creates derived fields,
assigns date, time, and speed-dimension IDs, and prepares the final columns
for loading into the traffic fact table.

When run directly, the module executes the complete transformation for
local testing.
"""

import pandas as pd
from datetime import datetime, timezone
from transform_date_dim import date_dim
from transform_time_dim import time_dim
from speed_band_lookup import create_speed_band_lookup
from extract import extract_chicago_traffic

# ====================
# Schema/ columns groups
# ====================

RAW_COLUMNS = [
    "segment_id",
    "last_update",
    "current_speed_mph",
]

FK_COLUMNS = [
    "segment_id",
    "date_id",
    "speed_band_id",
    "time_id",
]

DERIVED_COLUMNS = [
    "has_traffic_data",
    "snapshot_ts_utc",
    "current_speed_kph"
]

RENAME_MAP = {
    'segmentid': 'segment_id',
    '_last_updt': 'last_update',
    '_traffic': 'current_speed_mph'
}

REQUIRED_COLUMNS = [
    "segment_id",
    "last_update",
    "current_speed_mph"
]

FACT_COLUMNS =[
    "segment_id",
    "date_id",
    "time_id",
    "speed_band_id",
    "current_speed_mph",
    "current_speed_kph",
    "has_traffic_data",
    "last_update",
    "snapshot_ts_utc",
]

# ====================
# Schema normalization
# ====================
def normalize_column_names(df):
    """
    Rename raw source fields to canonical schema names
    and enforce required canonical column presence. 

    Args: 
        df (pd.DataFrame): Raw df from extraction
    
    Returns: 
        pd.DataFrame with standardized columns
    
    Raises:
        ValueError: If required columns are missing   
    """  

    df=df.rename(columns=RENAME_MAP)
    
    # ----- Enforce canonical column presence
    missing = set(REQUIRED_COLUMNS) - set(df.columns)

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    return df

def standardize_raw_columns(df):
    """
    Clean raw traffic columns and convert them to required data types.

    Leanding and trailing whitespace is removed from text values.
    Segment IDs and speeds are converted to numeric values, invalid values are 
    replaced with missing values, and timestamps are converted to datetime values.  
    A speed of -1 is treated as missing traffic data

    Args:
        df (pd.DataFrame): DataFrame returned by 
            normalized_column_names().

    Returns:
        pd.DataFrame: Cleaned traffic data with standardized values 
             and data types.
    """

    df[RAW_COLUMNS] = df[RAW_COLUMNS].apply(
    lambda col: col.str.strip() if col.dtype == "object" else col
)
    
    df["segment_id"] = pd.to_numeric(df["segment_id"], errors="coerce")
    df["current_speed_mph"] = (
        pd.to_numeric(df["current_speed_mph"], errors="coerce")
        .replace(-1, pd.NA)
)
    
    df["last_update"] = pd.to_datetime(df["last_update"], errors="coerce")

    return df

def create_derived_columns(df):
    """
    Creates columns derived from cleaned traffic data
    
    Converts the current speed from miles per hour to kilometers per hour.
    Identifies observations containing valid traffic data.
    Adds a UTC snapshot timestamp for the composited primary key.
    The same snapshot is assigned to every row in the DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame returned by
            standardize_raw_columns

    Returns:
        pd.DataFrame: Traffic data with derived columns added.
    """

    df["current_speed_kph"] = df["current_speed_mph"] * 1.609344
    df["has_traffic_data"] = df["current_speed_mph"].notna()

    snapshot_ts_utc = datetime.now(timezone.utc) 
    df["snapshot_ts_utc"] = snapshot_ts_utc

    return df

def add_date_id(df, date_df):
    """
    Add a date ID to each traffic observation based on its last update.

    Normalizes each last-update timestamp to a date and verifies that
    the date exists in the date dimension before adding its date ID.

    Args:
        df (pd.DataFrame): Traffic data containing the last_update
            column.
        date_df (pd.DataFrame): Date dimension containing the date
            and date_id columns.

    Returns:
        pd.DataFrame: Traffic data with the date_id column added.

    Raises:
        ValueError: If any normalized last-update date is missing from
            the date dimension.
    """

    df["validate_date"] = df["last_update"].dt.normalize()
    invalid_dates = ~df["validate_date"].isin(date_df["date"])

    if invalid_dates.any():
        missing_date = df.loc[invalid_dates, "validate_date"].unique()
        raise ValueError(f"Dates missing from date dimension: {missing_date}")
    
    df = df.merge(
        date_df[["date", "date_id"]],
        how ="left",
        left_on ="validate_date",
        right_on ="date",
        validate ="many_to_one"
    )

    return df

def add_time_id(df, time_df):
    """
    Add a time ID to each traffic observation based on its last update.
    
    Extracts the hour from each last-update timestamp and verifies that
    the hour exists in the time dimension before adding its time ID.

    Args:
        df (pd.DataFrame): Traffic data containing the last_update
            column.
        time_df (pd.DataFrame): Time dimension containing the hour_of_day
            and time_id columns.

    Returns:
        pd.DataFrame: Traffic data with tsdxhe time_id column added.

    Raises:
        ValueError: If any normalized last-update time is missing from
            the time dimension.
    """

    df["validate_time"] = df["last_update"].dt.hour
    invalid_times = ~df["validate_time"].isin(time_df["hour_of_day"])

    if invalid_times.any():
        missing_time = df.loc[invalid_times, "validate_time"].unique()
        raise ValueError(f"Times missing from time dimension: {missing_time}")

    df = df.merge(
        time_df[["hour_of_day", "time_id"]],
        how = "left",
        left_on = "validate_time",
        right_on = "hour_of_day",
        validate = "many_to_one"
    )

    return df

def add_speed_band_id(df, speed_df):
    """
    Add a speed band ID to each traffic observation based on its current speed mph.

    Observations with a missing current speed are assigned to the "No Data"
    speed band. This includes raw speeds of -1 that were converted to missing
    values during standardization. Valid speeds are matched to the appropriate
    minimum and maximum speed range in the speed dimension.

    Args:
        df (pd.DataFrame): Traffic data containing current_speed_mph
            column.
        speed_df (pd.DataFrame): Speed dimension containing speed_band_id, 
            speed_band, min_speed, and max_speed columns
        

    Returns:
        pd.DataFrame: Traffic data with the speed_band_id column added.

    Raises:
        ValueError: If current speed is not included in speed bands.
    """

    df["speed_band_id"] = pd.NA
    df["speed_band_id"] = df["speed_band_id"].astype("Int64")
    no_data_mask = df["current_speed_mph"].isna()
    no_data_id = speed_df.loc[
        speed_df["speed_band"] == "No Data",
        "speed_band_id"
    ].iloc[0]
    df.loc[no_data_mask, "speed_band_id"] = no_data_id

    numeric_bands = speed_df.dropna(
        subset = ["min_speed", "max_speed"]
    )

    for _, band in numeric_bands.iterrows():
        band_mask = df["current_speed_mph"].between(
            band["min_speed"],
            band["max_speed"],
            inclusive = "both"
            )

        df.loc[band_mask, "speed_band_id"] = band["speed_band_id"]

    missing_speed_bands = df["speed_band_id"].isna()

    if missing_speed_bands.any():
            unmatched_speeds = df.loc[
                missing_speed_bands,
                "current_speed_mph"
                ].unique()
            
            raise ValueError(
                f"Speed missing a speed band: {unmatched_speeds}"
            )

    invalid_speed_ids = ~df["speed_band_id"].isin(
        speed_df["speed_band_id"]
    )

    if invalid_speed_ids.any():
        invalid_speed_ids = df.loc[
            invalid_speed_ids,
            "speed_band_id"
        ].unique()

        raise ValueError(
            f"Invalid speed band IDs: {invalid_speed_ids}"
        )

    return df

def select_fact_columns(df):
    """
    Select and order the columns required for the traffic fact table.

    Verifies that all required fact columns are present, removes columns
    used only during transformation, and orders the remaining columns
    according to FACT_COLUMNS.

    Args:
        df (pd.DataFrame): Transformed traffic data containing the
            required fact-table columns.

    Returns:
        pd.DataFrame: A copy of the traffic data containing only the
            ordered fact-table columns.

    Raises:
        ValueError: If any required fact-table columns are missing.
    """

    missing_fact_columns = set(FACT_COLUMNS) - set(df.columns)

    if missing_fact_columns:
        raise ValueError (f"Missing required columns: {missing_fact_columns}")

    df = df[FACT_COLUMNS].copy()

    return df

def traffic_fact(df, date_df, time_df, speed_df):
    """
    Transform raw traffic data into the traffic fact-table structure.

    Standardizes the raw data, creates derived columns, assigns date,
    time, and speed-band IDs, and selects the final fact-table columns.

    Args:
        df (pd.DataFrame): Raw traffic data from the extraction process.
        date_df (pd.DataFrame): Date dimension used to assign date IDs.
        time_df (pd.DataFrame): Time dimension used to assign time IDs.
        speed_df (pd.DataFrame): Speed dimension used to assign
            speed-band IDs.

    Returns:
        pd.DataFrame: Transformed traffic data ready to load into the
            traffic fact table.

    Raises:
        ValueError: If required columns or dimension values are missing.
    """

    df = normalize_column_names(df)
    df = standardize_raw_columns(df)
    df = create_derived_columns(df)
    df = add_date_id(df, date_df)
    df = add_time_id(df, time_df)
    df = add_speed_band_id(df, speed_df)
    df = select_fact_columns(df)

    return df

if __name__ == "__main__":
    # Run the complete traffic fact transformation for local testing.
    raw_df = extract_chicago_traffic()

    date_df = date_dim()
    time_df = time_dim()
    speed_df = create_speed_band_lookup()

    traffic_fact_df = traffic_fact(raw_df, date_df, time_df, speed_df)
