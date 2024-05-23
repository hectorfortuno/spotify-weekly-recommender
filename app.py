import os
import uuid
from flask import Flask, redirect, request, session, url_for, render_template
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from set_env import client_id, client_secret
from new_user import main_with_args
from db_utils import delete_user
from spotify_utils import get_userid

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configuration
SPOTIPY_CLIENT_ID = client_id()
SPOTIPY_CLIENT_SECRET = client_secret()
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:5000/callback/'
SPOTIPY_REDIRECT_URI_UNS = 'http://127.0.0.1:5000/unsubscribed'

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

sp_oauth_unsubscribe = SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI_UNS,
    scope='user-library-read'  # Add other scopes as needed
)

@app.route('/')
def home():
    return render_template('home.html')

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
        return render_template('error.html')

@app.route('/profile')
def profile():
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect(url_for('login'))

    username, returned = main_with_args(token_info['access_token'])
    if returned == 0: # New user
        return render_template('new_profile.html', name=username)
    else:
        return render_template('existing_profile.html', name=username)

@app.route('/unsubscribe')
def unsubscribe():
    auth_url = sp_oauth_unsubscribe.get_authorize_url()
    return redirect(auth_url)

@app.route('/unsubscribed')
def unsubscribed():
    code = request.args.get('code')
    token_info = sp_oauth_unsubscribe.get_access_token(code)
    
    if token_info:
        session['token_info'] = token_info
        userid = get_userid(token_info['access_token'])
        delete_user(userid)
        return render_template('unsubscribe.html')
    else:
        return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)
