import os
import uuid
from flask import Flask, redirect, request, session, url_for
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import set_env

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configuration
SPOTIPY_CLIENT_ID = set_env.client_id()
SPOTIPY_CLIENT_SECRET = set_env.client_secret()
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:5000/callback/'

app.config['SPOTIPY_CLIENT_ID'] = SPOTIPY_CLIENT_ID
app.config['SPOTIPY_CLIENT_SECRET'] = SPOTIPY_CLIENT_SECRET
app.config['SPOTIPY_REDIRECT_URI'] = SPOTIPY_REDIRECT_URI

# Create the SpotifyOAuth object
sp_oauth = SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope='user-library-read'  # Add other scopes as needed
)

@app.route('/')
def home():
    return '<a href="/login">Login with Spotify</a>'

@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback/')
def callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    
    if token_info:
        session['token_info'] = token_info
        return redirect(url_for('profile'))
    else:
        return 'Authorization failed.'

@app.route('/profile')
def profile():
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect(url_for('login'))

    sp = Spotify(auth=token_info['access_token'])
    user_data = sp.current_user()
    return f'Hello, {user_data["display_name"]}'

if __name__ == '__main__':
    app.run(debug=True)
