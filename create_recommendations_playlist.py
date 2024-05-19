import json
import spotipy
import numpy as np
from set_env import set_credentials
from spotipy.oauth2 import SpotifyOAuth
from sklearn.metrics.pairwise import cosine_similarity


def get_k_similar_tracks(user_id_and_features, spotify_tracks_and_features, k=20):
    # Extract user features and reshape to be 2D
    user_features = [user_id_and_features[1]]

    # Extract features from spotify tracks features
    spotify_features = [track[1] for track in spotify_tracks_and_features]

    # Compute cosine similarity between mean features of user's top tracks and features of Spotify tracks from different genres
    similarities = cosine_similarity(user_features, spotify_features)[0]

    # Filter out tracks that are in user's top tracks
    filtered_top_tracks = [track for i, track in enumerate(spotify_tracks_and_features) if track[0] not in user_id_and_features[0]]

    # Sort remaining tracks based on similarity to user's top tracks
    sorted_tracks = sorted(zip(filtered_top_tracks, similarities), key=lambda x: x[1], reverse=True)

    # Get IDs of the most similar tracks
    k_similar_track_ids = [track[0] for track, similarity in sorted_tracks[:k]]  # Adjust the number of tracks as needed

    return k_similar_track_ids


def create_playlist(tracks):
    # Set Spotify credentials
    set_credentials()

    # Define scope for Spotify API access
    scope = "playlist-modify-private"

    # Initialize Spotipy client
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    # Create a playlist with the desired name and description
    playlist_name = "DRCAV - Recommendations 19/05/2024"
    playlist_description = "Playlist created with the DRCAV's project recommendations."
    playlist = sp.user_playlist_create(user=sp.me()['id'], name=playlist_name, description=playlist_description, public=False)

    # Add tracks to the playlist
    sp.playlist_add_items(playlist_id=playlist['id'], items=tracks)
    print(f"Playlist '{playlist_name}' created successfully!")



def main():    
    with open('spotify_tracks_and_features.json', 'r') as json_file:
        spotify_tracks_and_features = json.load(json_file)

    with open('user_id_and_features.json', 'r') as json_file:
        user_id_and_features = json.load(json_file)

    recommended_tracks = get_k_similar_tracks(user_id_and_features, spotify_tracks_and_features, k=20)
    create_playlist(recommended_tracks)


if __name__ == "__main__":
    main()