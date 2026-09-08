

import pandas as pd

def create_speed_band_lookup():
    """
    Creates a reference DataFrame containing traffic speed bands.

    Returns:
        pd.DataFrame: Speed band IDs, labels, and speed ranges.
    """

    data = {
        'speed_band_id': (1, 2, 3, 4, 5),
        'speed_band': ('No Data', 'Very Slow', 'Slow', 'Moderate', 'Fast'),
        'min_speed': (pd.NA, 0, 11, 26, 41),
        'max_speed': (pd.NA, 10, 25, 40, 70)
    }

    speed_df = pd.DataFrame(data)
    speed_df[["min_speed", "max_speed"]] = (
        speed_df[["min_speed", "max_speed"]].astype("Int64")
    )

    return speed_df