import os

def client_id():
    return '01492ff702be425ab91cda6b61078317'

def client_secret():
    return '9bc0959478bd474199929967ab13ee4f'


def set_credentials():
    # Set your Spotify client ID and client secret
    os.environ['SPOTIPY_CLIENT_ID'] = client_id()
    os.environ['SPOTIPY_CLIENT_SECRET'] = client_secret()
    os.environ['SPOTIPY_REDIRECT_URI'] = 'http://127.0.0.1:5000/'