import json
import spotipy
from set_env import set_credentials
from spotipy.oauth2 import SpotifyOAuth
import numpy as np

def get_features_for_tracks(sp, track_ids):
    # Fetch audio features for each track
    audio_features = sp.audio_features(track_ids)
        
    # Create a list of [track_id, normalized_features]
    track_features = []
    for track in audio_features:
        # Extract numeric audio features
        numeric_audio_features = [value for key, value in track.items() if isinstance(value, (int, float)) and key not in ['tempo', 'duration_ms', 'mode', 'key']]
        
        # Normalize the features
        normalized_features = np.array(numeric_audio_features) / np.linalg.norm(numeric_audio_features)
        
        track_features.append([track['id'], normalized_features.tolist()])
        
    return track_features

def get_spotify_tracks(sp, playlists_per_genre=1, tracks_per_playlist=5):
    # Function to fetch playlists for a genre
    def get_playlists_for_genre(genre, limit=playlists_per_genre):
        results = sp.search(q=f'genre:{genre}', type='playlist', limit=limit)
        return results['playlists']['items']

    # Function to fetch tracks from a playlist
    def get_tracks_from_playlist(playlist_id, limit=tracks_per_playlist):
        tracks = sp.playlist_tracks(playlist_id, limit=limit)
        return [item['track']['id'] for item in tracks['items']]

    # Get available genres
    genres = sp.recommendation_genre_seeds()['genres']

    # List to hold track IDs
    all_track_ids = []

    # Fetch playlists and tracks for each genre
    for genre in genres:
        playlists = get_playlists_for_genre(genre)
        for playlist in playlists:
            track_ids = get_tracks_from_playlist(playlist['id'])
            all_track_ids.extend(track_ids)

    return all_track_ids


def get_spotify_features(sp, track_ids):
    # Remove duplicates by converting the list to a set and back to a list
    unique_track_ids = list(set(track_ids))

    # Function to call get_features_for_tracks in batches, as there is a limit of calls to the API
    def get_features_in_batches(sp, track_ids, batch_size=20):
        features = []
        for i in range(0, len(track_ids), batch_size):
            batch_ids = track_ids[i:i+batch_size]
            batch_features = get_features_for_tracks(sp, batch_ids)
            features.extend(batch_features)
        return features

    # Call the function in batches of 20
    trendy_tracks_features = get_features_in_batches(sp, unique_track_ids)

    return trendy_tracks_features


def main():    
    # Set Spotify credentials
    set_credentials()

    # Define scope for Spotify API access (check https://developer.spotify.com/documentation/web-api/concepts/scopes for reference)
    scope = "playlist-read-collaborative"

    # Initialize Spotipy client
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    # Define parameters for getting spotify tracks
    playlists_per_genre = 1
    tracks_per_playlist = 5

    # Get the Spotify top tracks from different genres and compute their features
    spotify_tracks_id = get_spotify_tracks(sp, playlists_per_genre, tracks_per_playlist)
    spotify_tracks_and_features = get_spotify_features(sp, spotify_tracks_id)

    # Writing to JSON file
    with open('spotify_tracks_and_features.json', 'w') as json_file:
        json.dump(spotify_tracks_and_features, json_file)

if __name__ == "__main__":
    main()
