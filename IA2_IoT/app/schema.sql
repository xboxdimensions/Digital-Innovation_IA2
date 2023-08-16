CREATE TABLE BOMinfo(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    air_temp FLOAT,
    apparent_t FLOAT,
    rel_hum FLOAT,
    local_date_time_full INTEGER
);

CREATE TABLE ARDinfo(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    int_temp FLOAT,
    rel_hum FLOAT,
    timestamp INTEGER
);