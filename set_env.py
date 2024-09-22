import os

def client_id():
    return 'YOUR CLIENT ID'

def client_secret():
    return 'YOUR CLIENT SECRET'


def set_credentials():
    # Set your Spotify client ID and client secret
    os.environ['SPOTIPY_CLIENT_ID'] = client_id()
    os.environ['SPOTIPY_CLIENT_SECRET'] = client_secret()
    os.environ['SPOTIPY_REDIRECT_URI'] = 'http://127.0.0.1:5000/'