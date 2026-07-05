-- traffic_analytical
-- Grain: (segment_id, snapshot_ts_utc)
-- Layer: Analytical
-- Loaded via Python ETL into AWS RDS

CREATE TABLE traffic_analytical (
	segment_id text, 
    snapshot_ts_utc timestamptz,
	street text,
	direction text, 
	from_street text, 
	to_street text,
	length_miles double precision,
	starting_heading text,
	from_lon double precision,
	from_lat double precision,
	to_lon double precision,
	to_lat double precision,
	current_speed integer,
	last_update timestamp,
	comments text,
    length_meters double precision,
    hour_of_day integer,
    day_of_week integer,
    is_weekend boolean,
    speed_band text, 
    has_traffic_data boolean, 
    row_count bigint,
    PRIMARY KEY (segment_id, snapshot_ts_utc)
);

CREATE INDEX idx_traffic_snapshot
ON traffic_analytical (snapshot_ts_utc);

