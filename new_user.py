from spotipy import Spotify
import mariadb

from spotify_utils import get_user_top_tracks, get_mean_features, get_k_similar_tracks, create_playlist
from db_utils import get_features, add_user, user_exists, get_config


def main_with_args(access_token):
    """
    
    """

    sp = Spotify(auth=access_token)
    userid = sp.me()['id']

    # connection for MariaDB
    conn = mariadb.connect(**get_config())
    cur = conn.cursor()
    cur.execute("USE recommender;")

    if user_exists(cur, userid):

        username = sp.me()['username']

        # Get user music tastes
        n_tracks = 10
        time_range = 'short_term'
        user_track_ids = get_user_top_tracks(sp, n_tracks, time_range)

        # Calculate user feature vector
        user_id_and_features = get_mean_features(sp, user_track_ids)

        # Obtain trendy tracks and features
        spotify_tracks_and_features = get_features(cur)

        # Obtain recommendations
        recommendations = get_k_similar_tracks(user_id_and_features, spotify_tracks_and_features, k=20)

        # Create playlist
        playlist_id = create_playlist(sp, recommendations)

        # Insert user in db
        add_user(cur, userid, username, access_token, playlist_id)

        conn.close()
        return None
    else:
        conn.close()
        return -1


