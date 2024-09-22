"""

"""
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from spotipy import Spotify


def get_k_similar_tracks(user_id_and_features, spotify_tracks_and_features, k=20):

    user_top_tracks = user_id_and_features[0]
    user_features = user_id_and_features[1]

    # Extract features from spotify tracks features
    spotify_features = [track[1] for track in spotify_tracks_and_features]

    # Compute cosine similarity between mean features of user's top tracks and features of Spotify tracks from different genres
    similarities = []
    for feature in spotify_features:
        similarities.append(cosine_similarity([user_features], [feature])[0])

    # Filter out tracks that are in user's top tracks
    filtered_top_tracks = [track for i, track in enumerate(spotify_tracks_and_features) if track[0] not in user_top_tracks]

    # Sort remaining tracks based on similarity to user's top tracks
    sorted_tracks = sorted(zip(filtered_top_tracks, similarities), key=lambda x: x[1], reverse=True)

    # Get IDs of the most similar tracks
    k_similar_track_ids = [track[0] for track, similarity in sorted_tracks[:k]]  # Adjust the number of tracks as needed

    return k_similar_track_ids


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


def get_tracks_from_playlist(sp, playlist_id, limit=100):
    tracks = sp.playlist_tracks(playlist_id, limit=limit)
    return [item['track']['id'] for item in tracks['items']]


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
    return [tracks, np.mean(normalized_features, axis=0).tolist()]


def create_playlist(sp, userid, tracks):

    # Create a playlist with the desired name and description
    playlist_name = "DRCAV - Fresh Recommendations"
    playlist_description = "Playlist created with the DRCAV's project recommendations."
    playlist = sp.user_playlist_create(user=userid, name=playlist_name, description=playlist_description, public=False)

    # Add tracks to the playlist
    sp.playlist_add_items(playlist_id=playlist['id'], items=tracks)
    
    return playlist['id']


def update_playlist(sp, playlist_id, tracks):

    sp.playlist_replace_items(playlist_id=playlist_id, items=tracks)


def get_userid(access_token):
    sp = Spotify(auth=access_token)
    return sp.me()['id']