"""
Common transformation functions shared across the Chicago Traffic ETL pipeline.

This module contains reusable helper functions that standardize raw data
before it is transformed into dimension and fact tables. These functions
perform tasks that may be needed by multiple pipeline stages, such as
normalizing timestamps and adding metadata columns.
"""


import pandas as pd
from datetime import datetime, timezone

RENAME_MAP = {'_last_updt' : 'last_update' }

DATE_TIME_COLUMNS = ["last_update"]


def normalize_last_update(df):
    """
    Standardize the last_update column from the raw traffic data.

    Renames the raw timestamp column, removes leading and trailing
    whitespace, and converts the values to pandas datetime objects.
    Invalid or missing timestamps are converted to NaT.

    Args:
        df (pandas.DataFrame):
            DataFrame containing the raw traffic data.

    Returns:
        pandas.DataFrame:
            The DataFrame with a standardized last_update column.
    """

    df=df.rename(columns=RENAME_MAP)

    df[DATE_TIME_COLUMNS]=df[DATE_TIME_COLUMNS].apply(
        lambda col: col.astype("string").str.strip()
    )

    df[DATE_TIME_COLUMNS]=df[DATE_TIME_COLUMNS].apply(
        lambda col: pd.to_datetime(col, errors="coerce")
    )

    return df

def add_snapshot_timestamp(df):
    """
    Standardize the last_update column from the raw traffic data.

    Renames the raw timestamp column, removes leading and trailing
    whitespace, and converts the values to pandas datetime objects.
    Invalid or missing timestamps are converted to NaT.

    Args:
        df (pandas.DataFrame):
            DataFrame containing the raw traffic data.

    Returns:
        pandas.DataFrame:
            The DataFrame with a standardized last_update column.
    """

    snapshot_ts = datetime.now(timezone.utc)
    df["snapshot_ts_utc"] = snapshot_ts

    return df


