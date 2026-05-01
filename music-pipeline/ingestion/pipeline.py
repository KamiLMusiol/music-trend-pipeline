import pandas as pd
from ingestion.lastfm_client import fetch_top_tracks
from ingestion.spotify_client import get_token, get_track_id, get_track_details
from datetime import datetime
import time


def fetch_data(country_lastfm: str, country_spotify: str) -> pd.DataFrame:
    lastfm_tracks = fetch_top_tracks(country_lastfm)
    df = pd.DataFrame(lastfm_tracks['tracks'])
    df['listeners'] = df['listeners'].astype(int)
    token = get_token()
    spotify_rows = []

    for _, row in df.iterrows():
        time.sleep(0.5)
        try:
            track_id = get_track_id(token, row['name'], row['artist'])
            if track_id:
                details = get_track_details(token, track_id)
                if details:
                    spotify_rows.append({
                        "name": row["name"],
                        "artist": row["artist"],
                        "spotify_id": track_id,
                        "album": details["album"]["name"],
                        "release_date": details["album"]["release_date"],
                        "duration_ms": details["duration_ms"],
                        "explicit": details["explicit"],
                        "spotify_url": details["external_urls"]["spotify"],
                    })
            else:
                spotify_rows.append({
                    "name": row["name"],
                    "artist": row["artist"],
                    "spotify_id": None,
                    "album": None,
                    "release_date": None,
                    "duration_ms": None,
                    "explicit": None,
                    "spotify_url": None,
                })
        except Exception as e:
            print(f"Błąd dla {row['name']}: {e}")
            spotify_rows.append({
                "name": row["name"],
                "artist": row["artist"],
                "spotify_id": None,
                "album": None,
                "release_date": None,
                "duration_ms": None,
                "explicit": None,
                "spotify_url": None,
            })

    df_spotify = pd.DataFrame(spotify_rows)
    if df_spotify.empty or 'name' not in df_spotify.columns:
        df_merged = df.copy()
        df_merged["spotify_id"] = None
        df_merged["album"] = None
        df_merged["release_date"] = None
        df_merged["duration_ms"] = None
        df_merged["explicit"] = None
        df_merged["spotify_url"] = None
    else:
        df_merged = df.merge(df_spotify, on=["name", "artist"], how="left")
    df_merged["fetched_date"] = datetime.utcnow().date()
    return df_merged


def fetch_all_countries() -> pd.DataFrame:
    countries = [
        ("Poland", "PL"),
        ("United States", "US"),
        ("Germany", "DE"),
    ]
    dfs = []
    for country_lastfm, country_spotify in countries:
        print(f"Pobieranie danych dla {country_lastfm}...")
        df = fetch_data(country_lastfm, country_spotify)
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)