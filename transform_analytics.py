"""
Analytical feature derivations for Chicago traffic data.
"""

import pandas as pd
from transform import canonical_transform


SPEED_BANDS =[
    "creeping",
    "slow",
    "normal_or_above",
]

def derive_analytical_features(df):
    """
    Derive analysis-facing features from canonical traffic data.
    """
    # ---- Time-based features
    df["hour_of_day"] = df["last_update"].dt.hour

    df["day_of_week"] = df["last_update"].dt.dayofweek

    # Saturday (5) and Sunday (6)
    df["is_weekend"] = df["day_of_week"] >4 

    # ---- Traffic categorization
    df["speed_band"] = pd.cut(df["current_speed"],
        bins=[0, 10, 20, float("inf")],
        labels = SPEED_BANDS,
        right=False
        )

    # Traffic data is unavailable when current_speed == -1
    df["has_traffic_data"] = df["current_speed"]>-1

    # ---- Aggregation helpers
    df["row_count"] = 1

    return df

if __name__ == "__main__":
    import pandas as pd

    df_raw = pd.read_json("data/raw/chicago_traffic_raw.json")
    df_canonical = canonical_transform(df_raw)
    df_analytical = derive_analytical_features(df_canonical)

print(df_analytical.dtypes)
print(df_analytical.head())
