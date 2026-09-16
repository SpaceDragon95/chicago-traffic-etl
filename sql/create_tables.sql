
CREATE TABLE IF NOT EXISTS speed_dim (
    speed_band_id INTEGER PRIMARY KEY,
    speed_band VARCHAR NOT NULL,
    min_speed INTEGER,
    max_speed INTEGER
);

INSERT INTO speed_dim
(speed_band_id, speed_band, min_speed, max_speed)
VALUES
    (1, 'No Data', NULL, NULL),
    (2, 'Very Slow', 0, 10),
    (3, 'Slow', 11, 25),
    (4, 'Moderate', 26, 40),
    (5, 'Fast', 41, 70);
    
CREATE TABLE IF NOT EXISTS date_dim (
    date_id INTEGER PRIMARY KEY,
    day_of_week TEXT,
    day_of_month INTEGER,
    date DATE,
    month TEXT,
    year INTEGER,
    week_of_year INTEGER,
    quarter INTEGER,
    season TEXT,
    holiday TEXT,
    is_weekend BOOLEAN,
    is_workday BOOLEAN
);

CREATE TABLE IF NOT EXISTS time_dim (
    time_id INTEGER PRIMARY KEY,
    hour_of_day INTEGER,
    time_of_day_label TEXT,
    is_rush_hour_window BOOLEAN,
    rush_hour_period VARCHAR
);

CREATE TABLE IF NOT EXISTS segment_dim (
    segment_id INTEGER PRIMARY KEY,
    street TEXT,
    direction CHAR(2),
    from_street TEXT,
    to_street TEXT,
    length_miles NUMERIC(6,3),
    length_meters NUMERIC(8,2),
    from_lon NUMERIC(9,6),
    from_lat NUMERIC(9,6),
    to_lon NUMERIC(9,6),
    to_lat NUMERIC(9,6),
    starting_heading CHAR(1),
    comments TEXT
);

CREATE TABLE IF NOT EXISTS traffic_fact(
    snapshot_ts_utc TIMESTAMPTZ NOT NULL,
    segment_id INTEGER NOT NULL,
    date_id INTEGER NOT NULL,
    time_id INTEGER NOT NULL,
    speed_band_id INTEGER NOT NULL,
    last_update TIMESTAMPTZ NOT NULL,
    current_speed INTEGER,
    has_traffic_data BOOLEAN,

    PRIMARY KEY (segment_id, snapshot_ts_utc),

    FOREIGN KEY (segment_id)
        REFERENCES segment_dim(segment_id),

    FOREIGN KEY (date_id)
        REFERENCES date_dim(date_id),

    FOREIGN KEY (time_id)
        REFERENCES time_dim(time_id),

    FOREIGN KEY (speed_band_id)
        REFERENCES speed_dim(speed_band_id)
);

