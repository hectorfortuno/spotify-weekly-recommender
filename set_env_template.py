import os

def set_credentials():
    # Set your Spotify client ID and client secret
    os.environ['SPOTIPY_CLIENT_ID'] = 'your spotify client id'
    os.environ['SPOTIPY_CLIENT_SECRET'] = 'your spotify client secret'
    os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost'