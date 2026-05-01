CREATE TABLE dim_date (
    date_id SERIAL PRIMARY KEY,
    fetch_date DATE,
    day INT,
    month INT,
    year INT,
    day_of_week INT
);

CREATE TABLE dim_country (
    country_id SERIAL PRIMARY KEY,
    country VARCHAR
);

CREATE TABLE dim_artist (
    artist_id SERIAL PRIMARY KEY,
    artist VARCHAR
);

CREATE TABLE dim_song (
    song_id SERIAL PRIMARY KEY,
    song VARCHAR,
    album VARCHAR,
    release_date DATE,
    spotify_url VARCHAR,
    duration_ms INT,
    spotify_id VARCHAR
);

CREATE TABLE fact_fetched_data (
    id SERIAL PRIMARY KEY,
    date_id INT REFERENCES dim_date(date_id),
    country_id INT REFERENCES dim_country(country_id),
    artist_id INT REFERENCES dim_artist(artist_id),
    song_id INT REFERENCES dim_song(song_id),
    listeners INT
);