import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os
import json
import base64
from datetime import datetime
from requests import post
from requests import get
load_dotenv()
#https://www.youtube.com/watch?v=WAmEZBEeNmg&t=352s
client_id=os.getenv("SPOTIFY_CLIENT_ID")
client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), encoding="utf-8")

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        "authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"

    }

    data = {
        "grant_type": "client_credentials"
    }

    result = post(url, data=data, headers=headers)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artists(token, artist_name):
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_header(token)
    query = f'?q={artist_name}&type=artist&limit=1'
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    print(json.dumps(json_result, indent=4))

#token = get_token()
#search_for_artists(token, "ACDC")

def get_track_id(token, track_name, artist_name):
    url = "https://api.spotify.com/v1/search"
    query = f"?q=track:{track_name}+artist:{artist_name}&type=track&limit=1"
    result = get(url + query, headers=get_auth_header(token))

    if result.status_code <200 or result.status_code > 299:
        return None

    try:
        data = result.json()
        items = data["tracks"]["items"]
        if items:
            return items[0]["id"]
        else:
            return None
    except Exception:
        return None



def get_track_details(token, track_id):
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    result = get(url, headers=get_auth_header(token))

    if result.status_code <200 or result.status_code > 299:
        print(result.status_code)
        return None

    return result.json()

def get_artist_details(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    result = get(url, headers=get_auth_header(token))
    return result.json()


