import hmac
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import os
import threading
import time
from urllib.parse import urlparse, parse_qs, quote
import socket

import arrow
from furl import furl
import requests
import webbrowser

from .constants import (
    AUTH0_AUTHORIZE_URL, CLIENT_ID,
    AUTH0_AUDIENCE, AUTH0_TOKEN_URL, MAX_WAIT_TIME_LOGIN, VINZ_URL, SCOPES
)
from .utils import generate_code_verifier, generate_code_challenge


SERVER_PORT = None
TARGET_PORTS = [50000, 50005]

logger = logging.getLogger(__name__)


class AuthCallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query_components = parse_qs(urlparse(self.path).query)
        if "code" in query_components:
            self.server.auth_code = query_components["code"][0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Authentication successful! You can close this window.")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Authentication failed!")


def include_authorization(url, headers, access_key=None, secret_key=None):
    product, version = 'vinz', '1'
    headers.update({
        'Host': urlparse(url).netloc,
        'X-AtlasAI-Date': arrow.utcnow().isoformat(),
        'X-AtlasAI-Credential': '/'.join([product, version, access_key]),
        'X-AtlasAI-SignedHeaders': 'x-atlasai-date;x-atlasai-credential;host',
    })

    sign_request(headers, secret_key)


def sign_request(headers, secret_key):
    product, version, access_key = headers['X-AtlasAI-Credential'].split('/')
    key = f'{product}{version}{secret_key}'.encode('utf-8')
    for msg in (
        headers['X-AtlasAI-Date'],
        f'{product}_{version}_request',
    ):
        obj = hmac.new(key, msg.encode('utf-8'), 'sha256')
        key = obj.digest()

    msg = '\n'.join([
        headers['X-AtlasAI-Date'],
        headers['X-AtlasAI-Credential'],
        headers['Host']
    ])
    headers['X-AtlasAI-Signature'] = hmac.new(key, msg.encode('utf-8'), 'sha256').hexdigest()


def login():
    access_key = os.getenv('ATLASAI_ACCESS_KEY')
    secret_key = os.getenv('ATLASAI_SECRET_KEY')
    if access_key and secret_key:
        access_token = _login_flow_api(access_key, secret_key)
    else:
        access_token = _login_flow_ui()

    print("Finished authentication...")
    return access_token


def _login_flow_api(access_key, secret_key):
    f = furl(VINZ_URL)
    f.path = 'api/token'
    url = f.url
    headers = {}
    include_authorization(url, headers, access_key, secret_key)
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    token = data['access_token']
    return token


def _login_flow_ui():
    return authenticate_user()

def redirect_uri(port):
    return f"http://127.0.0.1:{port}/callback"


def start_auth_flow(code_challenge):
    auth_url = (
        f"{AUTH0_AUTHORIZE_URL}?"
        f"response_type=code&"
        f"client_id={CLIENT_ID}&"
        f"redirect_uri={quote(redirect_uri(SERVER_PORT))}&"
        f"audience={quote(AUTH0_AUDIENCE)}&"
        f"scope={quote(SCOPES)}&"
        f"code_challenge={code_challenge}&"
        f"code_challenge_method=S256"
    )
    webbrowser.open(auth_url)


def run_local_server():
    global SERVER_PORT
    for port in TARGET_PORTS:
        try:
            server = HTTPServer(("127.0.0.1", port), AuthCallbackHandler)
        except socket.error:
            pass
        else:
            SERVER_PORT = port
            break
    if not SERVER_PORT:
        raise Exception(f'Could not start localhost server on any ports: {TARGET_PORTS}')
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    return server


def exchange_code_for_tokens(auth_code, code_verifier):
    payload = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "code": auth_code,
        "redirect_uri": redirect_uri(SERVER_PORT),
        "code_verifier": code_verifier
    }
    response = requests.post(AUTH0_TOKEN_URL, json=payload)
    if response.status_code == 200:
        tokens = response.json()
        return tokens
    else:
        raise Exception(f"Token exchange failed: {response.text}")


def authenticate_user():
    tokens = {}
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)

    server = run_local_server()

    print("Opening browser for authentication...")
    start_auth_flow(code_challenge)

    counter = 0
    while not hasattr(server, "auth_code"):
        time.sleep(1)
        counter += 1
        if counter > MAX_WAIT_TIME_LOGIN:
            print(f"Waited for {MAX_WAIT_TIME_LOGIN} seconds. Stopping server..")
            break
    else:
        tokens = exchange_code_for_tokens(server.auth_code, code_verifier)

    server.shutdown()
    return tokens['access_token'] if 'access_token' in tokens else None
