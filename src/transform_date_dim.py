"""
Create and transform data for the project's date dimension.

This module generates the date dimension, derives calendar
attributes, and identifies federal and non-federal holidays used
for reporting and analysis.
"""

import pandas as pd
from datetime import datetime, timezone
from pandas.tseries.holiday import USFederalHolidayCalendar, Holiday, Easter, AbstractHolidayCalendar, SU, TH
from pandas.tseries.offsets import DateOffset, Day

def get_season(date):
    """
    Determine the meteorological season for a given date.

    Args:
        date (pandas.Timestamp):
            Date used to determine the season.

    Returns:
        str:
            One of "Winter", "Spring", "Summer", or "Fall".
    """

    month = date.month

    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Fall"

def add_holiday_columns(df):
    """
    Add holiday and workday attributes to the date dimension.

    Identifies U.S. federal holidays and selected non-federal
    holidays, combines them into a single holiday column, and
    determines whether each date is a workday.

    Args:
        df (pandas.DataFrame):
            Date dimension DataFrame containing date and
            is_weekend columns.

    Returns:
        pandas.DataFrame:
            The DataFrame with holiday and workday columns added.
    """

    # Create federal holiday calendar
    # Starts in 2010 to cover stale last_update values on records with unavailable traffic data.
    calendar = USFederalHolidayCalendar()
    federal_holidays = calendar.holidays(
        start = df["date"].min(),
        end = df["date"].max(),
        return_name = True
    )

    # Add federal holiday names
    df["federal_holiday"] = df["date"].map(federal_holidays)

    # Add nonfederal holidays
    st_patricks_day = Holiday (
        "St. Patrick's Day",
        month = 3,
        day = 17
    )

    halloween = Holiday (
        "Halloween",
        month = 10,
        day = 31
    )

    new_years_eve = Holiday (
        "New Year's Eve",
        month = 12,
        day = 31
    )

    valentines_day = Holiday (
        "Valentine's Day",
        month = 2,
        day = 14
    )

    christmas_eve = Holiday (
        "Christmas Eve",
        month = 12,
        day = 24
    )

    day_after_christmas = Holiday (
        "Day after Christmas",
        month = 12,
        day = 26
    )

    cinco_de_mayo = Holiday (
        "Cinco de Mayo",
        month = 5,
        day = 5
    )

    easter = Holiday (
        "Easter",
        month = 1,
        day = 1,
        offset = Easter()
    )

    good_friday = Holiday (
        "Good Friday",
        month = 1,
        day = 1,
        offset = [Easter(),
                  Day(-2)]
    )

    wednesday_before_thanksgiving = Holiday (
        "Wednesday before Thanksgiving",
        month = 11,
        day = 1,
        offset = [DateOffset(weekday=TH(4)),
            Day(-1)]
    )

    black_friday = Holiday (
        "Black Friday",
        month = 11,
        day = 1,
        offset = [DateOffset(weekday=TH(4)),
                Day(1)  ]
    )

    sunday_after_thanksgiving = Holiday (
        "Sunday after Thanksgiving",
        month = 11,
        day = 1,
        offset = [DateOffset(weekday=TH(4)),
                  Day (3)]
    )

    mothers_day = Holiday (
        "Mother's Day",
        month = 5,
        day = 1,
        offset = DateOffset(weekday=SU(2))
    )

    fathers_day = Holiday (
        "Father's Day",
        month = 6,
        day = 1,
        offset = DateOffset(weekday=SU(3))
    )

    # Currently Super Bowl Sunday dates have been announced through 2027.  After 2027
    # new dates will need to be verified.
    super_bowl_early = Holiday(
        "Super Bowl Sunday",
        month=2,
        day=1,
        offset=DateOffset(weekday=SU(1)),
        start_date="2020-01-01",
        end_date="2021-12-31"
)

    super_bowl_current = Holiday(
        "Super Bowl Sunday",
        month=2,
        day=1,
        offset=DateOffset(weekday=SU(2)),
        start_date="2022-01-01",
        end_date="2030-12-31"
    )

    nonfederal_calendar = AbstractHolidayCalendar(
    rules=[
        st_patricks_day,
        halloween,
        new_years_eve,
        valentines_day,
        christmas_eve,
        day_after_christmas,
        cinco_de_mayo,
        easter,
        good_friday,
        wednesday_before_thanksgiving,
        black_friday,
        sunday_after_thanksgiving,
        mothers_day,
        fathers_day,
        super_bowl_early,
        super_bowl_current
    ]
)
    
    nonfederal_holidays = nonfederal_calendar.holidays(
    start=df["date"].min(),
    end=df["date"].max(),
    return_name=True
)
    all_holidays = pd.concat([
    federal_holidays,
    nonfederal_holidays
])

    all_holidays = (
        all_holidays
        .groupby(level=0)
        .agg(" / ".join)
    )

    df["holiday"] = df["date"].map(all_holidays)

    # Calculate is_workday using federal holidays only
    df["is_workday"] = (
        ~df["is_weekend"]
        & ~df["date"].isin(federal_holidays.index)
)

    return df

def derived_date_columns(df):
    """
    Create the derived columns for the date dimension.

    Adds calendar attributes such as the date identifier, day,
    month, year, quarter, week of year, weekend indicator,
    holidays, workday indicator, and season.

    Args:
        df (pandas.DataFrame):
            DataFrame containing a date column.

    Returns:
        pandas.DataFrame:
            The completed date dimension DataFrame.
    """
    df["date_id"] = df["date"].dt.strftime("%Y%m%d").astype(int)
    df["day_of_week"] = df["date"].dt.dayofweek + 1
    df["day_name"] = df["date"].dt.day_name()
    df["day_of_month"] = df["date"].dt.day
    df["month"] = df["date"].dt.month
    df["month_name"] = df["date"].dt.month_name()
    df["year"] = df["date"].dt.year
    df["quarter"] = df["date"].dt.quarter
    df["week_of_year"] = df["date"].dt.isocalendar().week.astype(int)
    df["is_weekend"] = df["day_of_week"].isin([6,7])
    df = add_holiday_columns(df)
    df["season"] = df["date"].apply(get_season)

    return df

def date_dim():
    """
    Creates the date dimension DataFrame.

    Generates a daily date range from 2010 through 2030 and adds
    derived date attributes using derived_date_columns().

    Returns:
        pd.DataFrame: Completed date dimension DataFrame.
    """

    date_df = pd.DataFrame({
    "date": pd.date_range(
        start="2010-01-01",
        end="2030-12-31",
        freq="D"
    )    
    })

    date_df = derived_date_columns(date_df)

    return date_df

if __name__ == "__main__":
    date_df = date_dim()
    