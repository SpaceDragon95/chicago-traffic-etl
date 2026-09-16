
import logging
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
    logging.basicConfig(
        level = logging.INFO,
        filename="logs/chicago_traffic.log",
        format = "%(asctime)s - %(levelname)s - %(message)s"
    )

    logger = logging.getLogger(__name__)

    logger.info("Starting Chicago traffic ETL pipeline.")

    # Call extraction function
    logger.info("Starting traffic extraction")
    raw_df = extract_chicago_traffic()
    logger.info("Traffic extraction complete")

    # Call Segment dim function
    logger.info("Starting segment dimension tranformation")
    seg_df = segment_dim(raw_df.copy())
    logger.info("Segment dimension transformation complete")

    # Call Date dim function
    logger.info("Starting date dimension transformation")
    date_df = date_dim()
    logger.info("Date dimension tranformation complete")

    # Call Time dim function
    logger.info("Starting time dimension transformation")
    time_df = time_dim()
    logger.info("Time dimension transformation complete")

    # Call Speed dim function
    logger.info("Starting speed dimension transformation")
    speed_df = create_speed_band_lookup()
    logger.into("Speed dimension transformation complete")

    # Call Traffic fact function
    traffic_df = traffic_fact(
        raw_df,
        date_df,
        time_df,
        speed_df
)
    
if __name__ == "__main__":
    run_pipeline()

