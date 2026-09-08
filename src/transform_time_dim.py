"""
Create and transform data for the project's time dimension.

This module creates the hourly records for the time dimension and
derives descriptive attributes such as formatted hour labels,
time-of-day labels, and rush-hour classifications.
"""

import pandas as pd
from datetime import time

def rush_hour_period(hour):
    """
    Determine whether an hour falls within a rush-hour period.

    Morning rush hour is defined as 6:00 AM through 9:59 AM, and
    evening rush hour is defined as 3:00 PM through 7:59 PM.

    Args:
        hour (int):
            Hour of the day using a 24-hour clock (0-23).

    Returns:
        str | None:
            "Morning" or "Evening" if the hour falls within a rush-hour
            period; otherwise None.
    """

    if hour in range (6, 10):
        return 'Morning'
    elif hour in range (15, 20):
        return 'Evening'
    else:
        return None
    
def time_of_day_label(hour):
    """
    Assign a descriptive label to an hour of the day.

    Args:
        hour (int):
            Hour of the day using a 24-hour clock (0-23).

    Returns:
        str:
            One of "Overnight", "Morning", "Afternoon", or "Evening".
    """

    if hour in range (0, 5):
        return 'Overnight'
    elif hour in range (5, 12):
        return 'Morning'
    elif hour in range (12,17):
        return 'Afternoon'
    else:
        return 'Evening'

def derived_time_columns(df):
    """
    Create the derived columns for the time dimension.

    Adds hour-based attributes including a formatted hour label,
    rush-hour classification, rush-hour indicator, and time-of-day
    label.

    Args:
        df (pandas.DataFrame):
            DataFrame containing a time_id column representing each
            hour of the day.

    Returns:
        pandas.DataFrame:
            The DataFrame with all derived time dimension columns
            added.
    """

    df['hour_of_day'] = df['time_id'] 

    df['hour_label'] = df['hour_of_day'].map(
        lambda col: time(hour=col).strftime("%I %p")
    )
    
    df['rush_hour_period'] = df['hour_of_day'].map(
        rush_hour_period
    )

    df['is_rush_hour_window'] = df['rush_hour_period'].notna()

    df['time_of_day_label'] = df['hour_of_day'].map(
        time_of_day_label
    )
    
    return df

def time_dim():
    """
    Creates the time dinension DataFrame.
    
    Generated an hourly time based on the 24 hour clock.
    Adds time of day attributes using derived_time_columns().
    
    Returns:
        pd.DataFrame: Completed time dimension DataFrame.
    """
    
    time_df = pd.DataFrame({'time_id': range(24)})

    time_df = derived_time_columns(time_df)

    return time_df


if __name__ == "__main__":
    time_df = time_dim()