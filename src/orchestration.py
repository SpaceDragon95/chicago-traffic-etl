
from extract import extract_chicago_traffic
from transform_segment_dim import segment_dim
from transform_date_dim import date_dim
from transform_time_dim import time_dim
from speed_band_lookup import create_speed_band_lookup
from transform_traffic_fact import traffic_fact

def run_pipeline():
    """
    Orchestrates the Chicago traffic ETL pipeline.

    Extracts traffic data and creates the DataFrames required for
    the segment, date, time, speed band, and traffic fact data.
    """

    # Call extraction function
    raw_df = extract_chicago_traffic()

    # Call Segment dim function
    seg_df = segment_dim(raw_df.copy())

    # Call Date dim function
    date_df = date_dim()

    # Call Time dim function
    time_df = time_dim()

    # Call Speed dim function
    speed_df = create_speed_band_lookup()

    # Call Traffic fact function
    traffic_df = traffic_fact(
        raw_df,
        date_df,
        time_df,
        speed_df
)
    
if __name__ == "__main__":
    run_pipeline()

