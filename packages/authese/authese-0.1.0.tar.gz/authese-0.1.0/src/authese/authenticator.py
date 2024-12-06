import base64
import json
import time
import uuid
import webbrowser
from functools import partial
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from queue import Queue, Empty
from socketserver import BaseServer
from threading import Thread
from urllib.parse import urlparse, parse_qs, urlencode

import jwt
import requests

from .environment import EnvConfig, Environment


def cached(file_name):
    """Decorator used to cache the return value.
    Cache key is a str representation of the decorated function's param

    Parameters
    ----------

    file_name (str): Filename of the cache"""

    def cached_wrapper(original_func):
        try:
            with open(file_name, 'r') as file:
                cache = json.load(file)
        except (IOError, ValueError):
            cache = {}

        def before_cached_return(param):
            key = repr(param)
            if key not in cache or not is_valid(cache[key]):
                cache[key] = original_func(param)
                with open(file_name, 'w') as cache_file:
                    json.dump(cache, cache_file)
            return cache[key]

        return before_cached_return

    return cached_wrapper


cache_location = '/tmp/authese-cache.dat'


def clear_cache():
    Path(cache_location).unlink(missing_ok=True)


@cached(cache_location)
def get_token(env_config: EnvConfig):
    """Gets a token from an Openid server and caches it.
    Cache key is based on __repr__ implementation of EnvConfig
    If EnvConfig is LOCAL:
        - returns an unsigned JWT token that has { roles: [ADMIN, local_test] }
        - add 'exp' to config.yaml to set JWT expiry.  Default now + 6 minutes

    Parameters
    ----------
    env_config (EnvConfig): Environment config for openid server

    Returns
    -------
    str: JWT token
    """
    if env_config.environment is Environment.LOCAL:
        expiry = env_config.raw.get('exp') or int(time.time()) + 6 * 60
        desired_jwt_token_content = {
            "sub": "1234567890",
            "exp": expiry,
            "name": "John Doe",
            "iat": 1516239022,
            "realm_access": {
                "roles": [
                    "ADMIN",
                    "local_test"
                ]
            }
        }
        return generate_local_token(desired_jwt_token_content)
    else:
        if env_config.raw["grant_type"] == "client_credentials":
            return get_client_credentials_token(env_config)
        elif env_config.raw["grant_type"] == "authorization_code":
            return login_and_return_token(env_config)
        else:
            raise Exception("Invalid grant_type. Must be one of: client_credentials, authorization_code")


def generate_local_token(json_string: dict):
    payload = json.loads(json.dumps(json_string))
    token = jwt.encode(payload, 'secret', algorithm='HS256')
    return token


def is_valid(token: str | None) -> bool:
    """Validate that token is present and that the expiry is at least 3 seconds out.

    Parameters
    ----------

    token (str): Token to validate"""
    if token is None:
        return False
    else:
        info = json.loads(base64.urlsafe_b64decode(token.split(".")[1] + "==="))
        if info["exp"] < time.time() + 3:
            print("token expired or will expire in 3 seconds!")
            return False
        return True


def get_client_credentials_token(env_config: EnvConfig):
    """Authenticate using openID client credentials flow.

    Parameters
    ----------

    env_config (EnvConfig): Environment config for openid server

    Returns
    -------
    str: JWT token
    """
    token_response = requests.post(env_config.keycloak_url + "/token", data={
        'client_id': env_config.client_id,
        'client_secret': env_config.client_secret,
        'grant_type': 'client_credentials'
    })
    return token_response.json()['access_token']


def login_and_return_token(env_config: EnvConfig) -> str:
    """Start user authorization_code login flow and wait for a token to be extracted.

    Parameters
    ----------

    env_config (EnvConfig): Environment config for openid server

    Returns
    -------
    str: JWT token
    """
    queue = Queue()
    thread, server = start_server_and_login(env_config, queue)
    wait_for = 60
    # You have x seconds to enter your credentials
    try:
        new_token = queue.get(timeout=wait_for)
    except Empty:
        shutdown(thread, server)
        raise Exception("Failed to login. (timed out)")
    if new_token is not None:
        shutdown(thread, server)
        return new_token
    shutdown(thread, server)
    raise Exception("Failed to login. (bad response)")


def shutdown(thread, server):
    server.shutdown()
    thread.join()


def start_server_and_login(env_config: EnvConfig, queue: Queue) -> tuple[Thread, BaseServer]:
    """Start a simple response server that will handle the Openid redirect
    and extract the JWT token from the response.

    Parameters
    ----------

    env_config (EnvConfig): Environment config for openid server
    queue (Queue)
    
    Returns tuple[Thread, BaseServer]
    """
    nonce = str(uuid.uuid4())
    query = {
        "response_type": "code",
        "client_id": env_config.client_id,
        "redirect_uri": f"{env_config.redirect_host}:{env_config.redirect_port}",
        "scope": " ".join(env_config.scopes),
        "state": nonce,
        "access_type": "offline",
        "prompt": "select_account",
    }
    thread, server = serve_response_server(env_config, nonce, queue)
    webbrowser.get().open(env_config.keycloak_url + "/auth?" + urlencode(query))
    return thread, server


def serve_response_server(env_config: EnvConfig, nonce: str, queue: Queue) -> tuple[Thread, BaseServer]:
    httpd = SmartHTTPServer(env_config, nonce, queue)
    httpd.server_bind()
    httpd.server_activate()

    def serve_forever(server):
        with server:  # to make sure httpd.server_close is called
            server.serve_forever()

    thread = Thread(target=serve_forever, args=(httpd,))
    thread.start()
    return thread, httpd


class SmartHTTPServer(HTTPServer):

    def __init__(self, config, nonce, queue):
        self.config = config
        self.nonce = nonce
        self.queue = queue
        handler = partial(TokenHTTPHandler)

        super().__init__((config.redirect_host.replace('http://', ''), config.redirect_port), handler, False)


class TokenHTTPHandler(BaseHTTPRequestHandler):
    """Openid redirect handler will request a new JWT token with context 
    provided by the redirect url of the Openid server.
    Puts the token on the queue to be read asynchronously.

    Parameters
    ----------

    env_config (EnvConfig): Environment config for openid server
    queue (Queue)
    """

    def do_GET(self):
        env_config = self.server.config
        nonce = self.server.nonce
        queue = self.server.queue
        code_response = parse_qs(urlparse(self.path).query)
        if "code" in code_response:
            token_response = requests.post(env_config.keycloak_url + "/token", data={
                "client_id": env_config.client_id,
                "client_secret": env_config.client_secret,
                "code": code_response["code"][0],
                "code_verifier": nonce,
                "grant_type": "authorization_code",
                "redirect_uri": f"{env_config.redirect_host}:{env_config.redirect_port}",
            })
            if not token_response.ok:
                raise Exception(f"Failed to get authentication token.\n{token_response.text}")
            try:
                access_token = token_response.json()["access_token"]
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("""
                    <html>
                        <head>
                            <script>window.close();</script>
                            <title>Spark login</title>
                        </head>
                        <body>
                            <p>Login success. And for some reason the tab didn't close. You'll have to do that yourself I guess.</p>                
                        </body>
                    </html>
                """, "utf-8"))
                queue.put(access_token)
            except KeyError:
                queue.put(None)
                raise Exception("No key access_token in response.")
