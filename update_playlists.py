from spotipy import Spotify
import mariadb

from spotify_utils import get_user_top_tracks, get_mean_features, get_k_similar_tracks, update_playlist
from db_utils import get_features, get_config, get_users


def update_playlists():
    """
    
    """

    # Parameters
    n_tracks = 10
    time_range = 'short_term'

    # connection for MariaDB
    conn = mariadb.connect(**get_config())
    cur = conn.cursor()
    cur.execute("USE recommender;")
    
    print(f'Getting users from db')
    # Get users from the db
    users = get_users(cur)

    for (userid, username, access_token, playlist_id) in users:
        print(f'Updating {username} playlist')
        
        sp = Spotify(auth=access_token)

        # Get user music tastes
        user_track_ids = get_user_top_tracks(sp, n_tracks, time_range)

        # Calculate user feature vector
        user_id_and_features = get_mean_features(sp, user_track_ids)

        # Obtain trendy tracks and features
        spotify_tracks_and_features = get_features(cur)

        # Obtain recommendations
        recommendations = get_k_similar_tracks(user_id_and_features, spotify_tracks_and_features, k=30)

        # Create playlist
        update_playlist(sp, playlist_id, recommendations)

        print(f'{username} playlist updated correctly!')

    conn.close()


update_playlists()
