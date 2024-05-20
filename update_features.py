from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import mariadb

from spotify_utils import get_spotify_tracks, get_spotify_features
from db_utils import get_config, song_processed, delete_features, save_features
from set_env import set_credentials


def update_features():
    """
    
    """

    # Spotify setup
    set_credentials()
    scope = "playlist-read-collaborative"
    sp = Spotify(auth_manager=SpotifyOAuth(scope=scope))

    # connection for MariaDB
    conn = mariadb.connect(**get_config())
    cur = conn.cursor()
    cur.execute("USE recommender;")
    
    print("Getting trendy tracks from Spotify")
    # Get trendy tracks from Spotify
    trendy_tracks = get_spotify_tracks(sp, playlists_per_genre=1, tracks_per_playlist=5)

    print("Checking which songs are already in the db")
    # Check which songs are already in the db
    processed_songs = []
    for songid in trendy_tracks:
        if song_processed(cur, songid):
            trendy_tracks.remove(songid)
            processed_songs.append(songid)

    print("Calculating features for new tracks")
    # Calculate features for non-processed tracks 
    spotify_tracks_and_features = get_spotify_features(trendy_tracks)

    print("Deleting non-trendy tracks from db")
    # Delete non-trendy tracks from db
    delete_features(cur, processed_songs)

    print("Saving new features to db")
    # Add new trendy tracks' features
    for songid, features in spotify_tracks_and_features:
        save_features(cur, songid, features)
   
    conn.close()


update_features()