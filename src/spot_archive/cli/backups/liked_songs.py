import json
import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from spot_archive.constants import BACKUP_FOLDER_PREFIX
from spot_archive.spotify_secrets import CLIENT_ID, CLIENT_SECRET
from spot_archive.spotipy_helpers import unpaginate

scope = ["user-library-read", "playlist-read-private", "playlist-read-collaborative"]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri="http://localhost:8888",
    )
)


def backup_liked_songs(output_folder: str):
    songs = list(unpaginate(sp.current_user_saved_tracks, market="US"))

    favorites_json_file = os.path.join(output_folder, "liked-songs.json")
    os.makedirs(output_folder, exist_ok=True)

    with open(favorites_json_file, "w") as output_file:
        json.dump(songs, output_file)
