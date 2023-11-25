import json
import os
import base64
from dotenv import load_dotenv
from requests import post, get

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
user_id = os.getenv("USER_ID")


def get_token():
    auth_string = f"{client_id}:{client_secret}"
    auth_string_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_string_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


def get_auth_header(token):
    return {
        "Authorization": f"Bearer {token}"
    }


def get_playlist(playlist_id):
    token = get_token()
    headers = get_auth_header(token)
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    response = get(url, headers=headers)
    json_response = json.loads(response.content)
    return json_response


def get_user_playlists(user_id):
    token = get_token()
    headers = get_auth_header(token)
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    response = get(url, headers=headers)
    json_response = json.loads(response.content)
    playlists = json_response["items"]
    return playlists


def get_tracks_from_playlist(playlist_id):
    token = get_token()
    headers = get_auth_header(token)
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    response = get(url, headers=headers)
    json_response = json.loads(response.content)
    tracks = json_response["items"]
    return [track["track"] for track in tracks]


def get_spotify_playlists():
    return get_user_playlists(user_id)


