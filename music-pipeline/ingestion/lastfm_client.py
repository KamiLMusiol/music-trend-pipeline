import requests
from dotenv import load_dotenv
import os
import json
from datetime import datetime

load_dotenv()

#https://www.last.fm/api/show/geo.getTopTracks
#JSON: http://ws.audioscrobbler.com/2.0/?method=geo.gettoptracks&country=spain&api_key=YOUR_API_KEY&format=json
API_KEY = os.getenv("LASTFM_API_KEY")
BASE_URL = "http://ws.audioscrobbler.com/2.0/"

def fetch_top_tracks(country:str = 'Poland') -> dict:
    params={
        'method': 'geo.gettoptracks',
        'country': country,
        'api_key': API_KEY,
        'format': 'json',
        'limit': 50,
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    tracks = []
    for track in data['tracks']['track']:
        tracks.append({
            'name': track['name'],
            'artist': track['artist']['name'],
            'listeners': track['listeners'],
            'fetched_at': datetime.utcnow().isoformat(),
            'country': country,
        })
    return {"country": country, "tracks": tracks}


