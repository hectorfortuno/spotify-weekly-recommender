import json
import spotipy
import numpy as np
from set_env import set_credentials
from spotipy.oauth2 import SpotifyOAuth

def get_user_top_tracks(sp, n_tracks=10, time_range='short_term'):
    # Define variables
    tracks = []
    if time_range == 'short_term':
        period = 'month'
    elif time_range == 'medium_term':
        period = '6 months'
    elif time_range == 'long_term':
        period = 'year'

    # Get top tracks for the last month
    results = sp.current_user_top_tracks(limit=n_tracks, time_range=time_range)

    # Print top tracks
    print(f"User Top Tracks in the last {period}:")
    for i, track in enumerate(results['items'], start=1):
        # Print track name and artists
        print(f"{i}. {track['name']} by {', '.join(artist['name'] for artist in track['artists'])}")
        # Append track URI to the list
        tracks.append(track['id'])

    return tracks

def get_mean_features(sp, tracks):
    # Get audio features for the given tracks
    audio_features = sp.audio_features(tracks)

    # Extract numeric audio features
    numeric_audio_features = [{k: v for k, v in track.items() if isinstance(v, (int, float)) and k not in ['tempo', 'duration_ms', 'mode', 'key']} for track in audio_features]

    # Extract numeric values into an array
    features_array = np.array([[track[param] for param in track if isinstance(track[param], (int, float))] for track in numeric_audio_features])

    # Normalize the features
    normalized_features = np.apply_along_axis(lambda x: x / np.linalg.norm(x), 1, features_array)

    # Return mean features
    return np.mean(normalized_features, axis=0).tolist()

def main():    
    # Set Spotify credentials
    set_credentials()

    # Define scope for Spotify API access
    scope = "user-top-read"

    # Initialize Spotipy client
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    # Define parameters for getting user top tracks
    n_tracks = 10
    time_range = 'short_term'

    # Get the user's top tracks in a given period and compute their mean features
    user_tracks_id = get_user_top_tracks(sp, n_tracks, time_range)
    user_mean_features = get_mean_features(sp, user_tracks_id)

    # Get user ID and make an array [UserID, Features]
    user_id = sp.me()['id']
    user_data = [user_id, user_mean_features]

    # Write user data to a JSON file
    with open('user_id_and_features.json', 'w') as json_file:
        json.dump(user_data, json_file)

if __name__ == "__main__":
    main()
