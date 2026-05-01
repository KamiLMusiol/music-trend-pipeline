
INSERT INTO dim_date (fetch_date, day, month, year, day_of_week)
SELECT DISTINCT
    fetched_date,
    EXTRACT(DAY FROM fetched_date)::INT,
    EXTRACT(MONTH FROM fetched_date)::INT,
    EXTRACT(YEAR FROM fetched_date)::INT,
    EXTRACT(DOW FROM fetched_date)::INT
FROM top_tracks;


INSERT INTO dim_country (country)
SELECT DISTINCT country FROM top_tracks;


INSERT INTO dim_artist (artist)
SELECT DISTINCT artist FROM top_tracks;


INSERT INTO dim_song (song, album, release_date, spotify_url, duration_ms, spotify_id)
SELECT DISTINCT
    name,
    album,
    release_date::DATE,
    spotify_url,
    duration_ms::INT,
    spotify_id
FROM top_tracks;


INSERT INTO fact_fetched_data (date_id, country_id, artist_id, song_id, listeners)
SELECT
    d.date_id,
    c.country_id,
    a.artist_id,
    s.song_id,
    t.listeners
FROM top_tracks t
JOIN dim_date d ON d.fetch_date = t.fetched_date
JOIN dim_country c ON c.country = t.country
JOIN dim_artist a ON a.artist = t.artist
JOIN dim_song s ON s.song = t.name;