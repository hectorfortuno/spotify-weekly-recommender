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
        tracks.append(track['uri'])

    return tracks

def get_mean_features(sp, tracks):
    # Get audio features for the given tracks
    audio_features = sp.audio_features(tracks)

    # Extract numeric audio features
    numeric_audio_features = [{k: v for k, v in track.items() if isinstance(v, (int, float))} for track in audio_features]

    # Extract numeric values into an array
    features_array = [[track[param] for param in track if isinstance(track[param], (int, float))] for track in numeric_audio_features]

    # Return mean features
    return [np.mean(param_values) for param_values in np.array(features_array).T]

def main():    
    # Set Spotify credentials
    set_credentials()

    # Define scope for Spotify API access (check https://developer.spotify.com/documentation/web-api/concepts/scopes for reference)
    scope = "user-top-read"

    # Initialize Spotipy client
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    # Define parameters for getting user top tracks
    n_tracks = 10
    time_range = 'short_term' # 'short_term' == 1 month | 'medium_term' == 6 months | 'long_term' == 12 months

    # Get the user top tracks in a given period and compute their mean features
    tracks_uri = get_user_top_tracks(sp, n_tracks, time_range)
    mean_features = get_mean_features(sp, tracks_uri)

    # Print mean features
    print("\nMean Features of Top Tracks:", mean_features)

if __name__ == "__main__":
    main()