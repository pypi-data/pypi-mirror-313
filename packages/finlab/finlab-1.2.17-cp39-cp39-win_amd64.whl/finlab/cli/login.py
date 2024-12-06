from flask import Flask, request, jsonify, render_template_string
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from threading import Thread
from .utils import read_resource_file
from .data_encryptor import DataEncryptor
from pathlib import Path
import subprocess
import datetime
import logging
import signal
import base64
import time
import json
import sys
import os

os.environ['FLASK_DEBUG'] = '0'

app = Flask(__name__)

_USER = None
_flask_user_request_filled = False
_webview_process = None
google_token = None

# Firebase configuration
firebase_config = {
    'apiKey': "AIzaSyB9Ogv6Vbwfy6_I0aLEfcpsPhqhlc4FSTw",
    'authDomain': "fdata-299302.firebaseapp.com",
    'projectId': "fdata-299302",
    'storageBucket': "fdata-299302.appspot.com",
    'messagingSenderId': "748308483506",
    'appId': "1:748308483506:web:7c78dd82b422cd4ea5a8ab"
}


def google_login():

    assert isinstance(_USER, DataEncryptor)

    creds = None
    if 'google_login_data' in _USER.data:
        creds = Credentials.from_authorized_user_info(json.loads(_USER.data['google_login_data']))

    is_refreshed = False
    if creds is not None and not creds.valid:
        creds.refresh(Request())
        is_refreshed = True

    if not creds or not creds.valid:
        is_refreshed = True 
        flow = InstalledAppFlow.from_client_config(
            json.loads(read_resource_file('finlab.cli', 'oauth_google.json')),
            scopes=[
                'https://www.googleapis.com/auth/userinfo.profile',
                'openid',
                'https://www.googleapis.com/auth/userinfo.email',
            ],
        )
        creds = flow.run_local_server()

    _USER.data['google_login_data'] = creds.to_json()
    _USER.to_file()

    return creds, is_refreshed


@app.route('/')
def index():
    global google_token
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://www.gstatic.com/firebasejs/9.6.1/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.6.1/firebase-auth-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.6.1/firebase-firestore-compat.js"></script>
    <script>
        // Firebase configuration
        const firebaseConfig = {{ firebase_config | safe }};
        const googleToken = "{{ google_token }}";

        // Initialize Firebase
        firebase.initializeApp(firebaseConfig);

        async function googleSignIn() {
            try {
                const credential = firebase.auth.GoogleAuthProvider.credential(googleToken);
                const result = await firebase.auth().signInWithCredential(credential);

                const user = result.user;
                const token = await user.getIdToken();
                
                // get user custom claims
                const idToken = await user.getIdTokenResult();
                // alert('customClaims:', idToken.claims['role']);

                const response = await fetch('/fetch-data', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ token, claims: idToken.claims })
                });

                if (response.ok) {
                    console.log("Data fetched successfully");
                } else {
                    console.error("Error fetching data");
                }
            } catch (error) {
                // alert("Error during sign-in: " + error.message);
                console.error("Error during sign-in:", error);
            }
        }

        window.onload = googleSignIn;
    </script>
</head>
<body>
    <h1>Firestore Data Fetch</h1>
</body>
</html>
"""
    return render_template_string(html_content, firebase_config=json.dumps(firebase_config), google_token=google_token)

def get_user_data_path(user_folder):
    return os.path.join(user_folder, 'finlab.userdata.txt')

def write_user_data(claims):

    _USER.data['firebase_login_data'] = claims
    _USER.to_file()

def read_user_data():

    if 'firebase_login_data' in _USER.data:
        return _USER.data['firebase_login_data']
    return None


@app.route('/fetch-data', methods=['POST'])
def fetch_data():

    firebase_token = request.json.get('token')
    claims = request.json.get('claims')

    # encrypt claims into
    claims['google_token'] = google_token
    claims['firebase_token'] = firebase_token
    write_user_data(claims)

    global _webview_process
    _webview_process.terminate()
    _webview_process.wait()
    _webview_process = None

    print('User login firebase successfully')

    return jsonify({'message': 'Data fetched successfully'})


def with_firebase_token():

    # Start the Flask server in a separate thread
    global google_token

    global _flask_user_request_filled
    _flask_user_request_filled = False

    import logging
    log = logging.getLogger('werkzeug')
    log.disabled = True
    cli = sys.modules['flask.cli']
    cli.show_server_banner = lambda *x: None

    server = Thread(target=app.run, kwargs={'port': 5000, 'debug': False}, daemon=True)
    server.start()

    global _webview_process
    python_executable = sys.executable

    _webview_process = subprocess.Popen([python_executable, "-c", """
import webview
window = webview.create_window('Authenticate Firebase', 'http://127.0.0.1:5000', hidden=True)
webview.start()
    """], env=os.environ.copy())
    
    cnt = 0
    while _webview_process:
        time.sleep(1)
        cnt += 1
        
        if cnt > 10:
            print('login not working please report the FinLab')

def _login(workspace, update_firebase_token=False):

    global _USER

    _USER = DataEncryptor.from_file(os.path.join(workspace, 'user.txt'))
    if 'firebase_login_data' not in _USER.data:
        if 'google_login_data' in _USER.data:
            del _USER.data['google_login_data']
            _USER.to_file()

    google_credential, is_refreshed = google_login()

    global google_token
    google_token = None
    if is_refreshed:
        google_token = google_credential.id_token
    elif update_firebase_token:
        google_token = google_credential.id_token

    if google_token:
        old_stdout = sys.stdout # backup current stdout
        sys.stdout = open(os.devnull, "w")
        with_firebase_token()
        sys.stdout = old_stdout # reset old stdout

    return _USER

def _logout(workspace):

    _USER = DataEncryptor.from_file(os.path.join(workspace, 'user.txt'))

    if 'firebase_login_data' in _USER.data:
        del _USER.data['firebase_login_data']

    if 'google_login_data' in _USER.data:
        del _USER.data['google_login_data']

    _USER.to_file()
    return True

def set_token(workspace):
    _USER = DataEncryptor.from_file(os.path.join(workspace, 'user.txt'))
    if 'firebase_login_data' in _USER.data:
        os.environ['FINLAB_API_TOKEN'] = _USER.data['firebase_login_data']['api_token']


def register_auth_commands(click, auth, WORKSPACE_PATH):

    @auth.command()
    def login():
        """Login to FinLab."""
        if not os.path.exists(WORKSPACE_PATH):
            click.echo('Creating workspace...')
            # create folder
            Path(WORKSPACE_PATH).mkdir(parents=True, exist_ok=True)

        _login(WORKSPACE_PATH)
        click.echo('Login successful')

    @auth.command()
    def logout():
        """Logout from FinLab."""
        _logout(WORKSPACE_PATH)
        click.echo('Logout successful')