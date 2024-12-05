import logging, filelock, time, urllib3, webbrowser, requests, socket, socketserver, http.server, urllib.parse, os, ssl

from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import TokenExpiredError, LegacyApplicationClient
from typing import Dict, List, Callable, Optional

from etiket_client.exceptions import (
    NoLoginInfoFoundException,
    RequestFailedException,
    LoginFailedException,
    TokenRefreshException,
)
from etiket_client.settings.user_settings import user_settings, get_user_data_dir

PREFIX = "/api/v2"
logger = logging.getLogger(__name__)

os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

class classproperty:
    def __init__(self, func):
        self.fget = func
    def __get__(self, instance, owner) -> OAuth2Session:
        return self.fget(owner)

class client:
    session : requests.Session = requests.Session()
    __session : OAuth2Session = None
    __user_sub : str = None
    __SERVER_URL : str = None
    __open_id_config : Dict = None
    
    @classmethod
    def __initialize(cls):
        '''
        Initialize the client with user settings.

        This method loads user settings and initializes the OAuth2 session,
        user subject, OpenID configuration, and server URL. If any required
        information is missing, it raises a NoLoginInfoFoundException.

        Raises:
            NoLoginInfoFoundException: If user_sub, token, open_id_config, or SERVER_URL is missing.
        '''
        user_settings.load()

        if user_settings.user_sub is None:
            raise NoLoginInfoFoundException("No user name found, please log in first.")
        cls.__user_sub = user_settings.user_sub

        if user_settings.token is None or user_settings.open_id_config is None:
            raise NoLoginInfoFoundException("No access token or OpenID configuration found, please log in first.")
        cls.__session = OAuth2Session(client_id=user_settings.client_id, token=user_settings.token)
        cls.__open_id_config = user_settings.open_id_config

        if user_settings.SERVER_URL is None:
            raise NoLoginInfoFoundException("No Server URL found, please log in first.")
        cls.__SERVER_URL = user_settings.SERVER_URL
    
    @staticmethod
    def url():
        """
        Get the full URL for the API endpoint.

        This method constructs the full URL for the API endpoint by combining
        the server URL and the prefix. If the server URL is not initialized,
        it calls the __initialize method.

        Returns:
            str: The full URL for the API endpoint.
        """
        if client.__SERVER_URL is None:
            client.__initialize()
            
        return f"{client.__SERVER_URL}{PREFIX}"

    @classproperty
    def oath_session(cls) -> OAuth2Session:
        if cls.__session is None:
            cls.__initialize()
        return cls.__session

    @staticmethod
    def _login_legacy(username : str, password : str, SERVER_URL : str):
        logger.info("Attempt to log-in user %s", username)
        try :
            session = OAuth2Session(client=LegacyApplicationClient(client_id=""),)
            token = session.fetch_token(token_url = f"{SERVER_URL}{PREFIX}/token", 
                                        username=username,
                                        password=password,
                                        timeout=10)
        except Exception as e:
            logger.exception("Log in failed for %s", username)
            raise LoginFailedException("Log in failed, please try again.") from e
        
        logger.info("Legacy log-in successful for %s", username)
        
        client.__SERVER_URL = SERVER_URL
        client.__session = session
        client.__user_sub = username
        
        user_settings.load()
        user_settings.token = token
        user_settings.open_id_config = {
            'revocation_endpoint' : f"{SERVER_URL}{PREFIX}/revoke",
            'token_endpoint' : f"{SERVER_URL}{PREFIX}/token",
            'userinfo_endpoint' : f"{SERVER_URL}{PREFIX}/userinfo"
        }
        user_settings.client_id = None
        user_settings.SERVER_URL = SERVER_URL
        try:
            response = client.__session.get(user_settings.open_id_config['userinfo_endpoint'])
            response.raise_for_status()
            user_settings.user_sub = response.json()['sub']
        except Exception as e:
            logger.exception("Failed to fetch user info for %s", username)
            raise LoginFailedException("Failed to fetch user info") from e
        user_settings.write()
    
    @staticmethod
    def _login_via_sso(client_id : str, open_id_config : Dict, SERVER_URL : str,
                       scope : Optional[List[str]] = None, tcp_server_listener : Optional[Callable[[int], str]] = None):
        '''
        login users via single sign-on using the OAuth2.0 protocol (authorization code flow)
        
        Parameters:
        client_id (str) : the client id of the application
        open_id_config (dict) : the OpenID configuration of the identity provider (.well-known/openid-configuration)
        SERVER_URL (str) : the server URL of the application
        scope (Optional[List[str]]) : the scopes that need to be requested from the identity provider
        tcp_server_listener (Optional[Callable[[int], str]]) : a function that listens to the authorization code sent by the identity provider,
            the function should return the authorization code and accept the port number as an argument.
        '''
        if scope == None:
            scope = ["openid", "email", "profile"]
        if tcp_server_listener == None:
            tcp_server_listener = handle_auth_code_request_with_python_TCP_server
        try:
            open_id_config = requests.get(open_id_config, timeout=10).json()
            port = get_port()
            
            session = OAuth2Session(client_id, redirect_uri=f'http://localhost:{port}',
                                        scope=scope, pkce="S256")
            
            authorization_url, _ = session.authorization_url(open_id_config['authorization_endpoint'])
            webbrowser.open(authorization_url)
            
            auth_response = tcp_server_listener(port)
        
        except Exception as e:
            logger.exception("Failed to log in via SSO")
            raise LoginFailedException("Failed to log in via SSO") from e
        
        logger.info("SSO log-in successful for %s", client_id)
        
        client.__open_id_config = open_id_config
        client.__SERVER_URL = SERVER_URL
        client.__session = session
        
        user_settings.load()
        user_settings.client_id = client_id
        user_settings.open_id_config = client.__open_id_config
        user_settings.SERVER_URL = SERVER_URL
        try:
            token = client.__session.fetch_token(open_id_config['token_endpoint'],
                                                            code=auth_response,
                                                            include_client_id=True,
                                                            timeout=10)
        except Exception as e:
            logger.exception("Failed to fetch token for %s", client_id)
            raise LoginFailedException("Failed to fetch token") from e
        
        logger.info("Token exchange for auth code successful for client %s", client_id)
        
        user_settings.token = token
        try:
            user_settings.user_sub = client.__session.get(f"{SERVER_URL}{PREFIX}/userinfo").json()['sub']
            client.__user_sub = user_settings.user_sub
        except Exception as e:
            logger.exception("Managed to fetch token but failed to fetch user info, for %s", client_id)
            raise LoginFailedException("Managed to fetch token but failed to fetch user info") from e
        user_settings.write()
        
        return authorization_url
    
    @staticmethod
    def _logout():
        try:
            user_settings.load()
            if user_settings.token is not None and user_settings.open_id_config is not None and user_settings.client_id is not None:
                if "revocation_endpoint" in user_settings.open_id_config:
                    revoke_data = {"token": user_settings.token['refresh_token'], "client_id": user_settings.client_id}
                    response = client.oath_session.post(user_settings.open_id_config['revocation_endpoint'], data=revoke_data)
                    if response.status_code == 200:
                        print("Log out successful.")
                        logger.info("Log out successful of user %s", user_settings.user_sub)
                elif "end_session_endpoint" in user_settings.open_id_config:
                    # TODO : revise/investigate, the refresh token is not invalidated after this?
                    response = client.oath_session.get(user_settings.open_id_config['end_session_endpoint'])
                    webbrowser.open(response.url)
                    if response.status_code == 200:
                        print("Log out successful.")
                        logger.info("Log out successful of user %s", user_settings.user_sub)
                else:
                    # try refreshing twice with the same refresh token, to invalidate it.
                    data = {"grant_type": "refresh_token", "refresh_token": user_settings.token['refresh_token']}
                    client.session.post(user_settings.open_id_config['token_endpoint'], data=data)
                    response = client.session.post(user_settings.open_id_config['token_endpoint'], data=data)
                    if response.status_code != 200:
                        raise Exception("Failed to log out, clearing tokens locally.")
        except Exception as e:
            logger.exception("Failed to log out.")
            raise e
        finally:
            client.reset()
            user_settings.token = None
            user_settings.user_sub = None
            user_settings.write()

    @staticmethod
    def _refresh_token(retries = 0, max_retries = 10):
        try:
            user_settings.load()
        except Exception:
            # in some rare cases, just after a write, the file is not yet readable (race condition between different processes)
            time.sleep(0.05)
            user_settings.load()
        
        if user_settings.user_sub is None:
            raise NoLoginInfoFoundException("No user name found, please log in first.")

        logger.info("Refreshing token for %s", user_settings.user_sub)
                
        try:
            with filelock.FileLock(f"{get_user_data_dir()}/lock"):
                try:
                    token_endpoint = user_settings.open_id_config["token_endpoint"]
                    refresh_token = user_settings.token['refresh_token']
                    token = client.oath_session.refresh_token(token_url=token_endpoint,
                                                        refresh_token=refresh_token,
                                                        client_id = user_settings.client_id,
                                                        timeout=10)
                    user_settings.token = token
                    user_settings.write()
                    
                    # release the lock 100ms later, to ensure that all the changes are written to the file.
                    logger.warning("Token refresh successful for %s", user_settings.user_sub)
                    time.sleep(0.1)
                except (requests.exceptions.RequestException, urllib3.exceptions.HTTPError,
                        socket.error, ssl.SSLError, TimeoutError) as e:
                    raise e
                except Exception as e:
                    logger.exception("Failed to refresh token.")
                    raise TokenRefreshException("Failed to refresh token.") from e
        except filelock.Timeout:
            logger.warning("Token refresh delayed due to a lock timeout (user_id : %s).", user_settings.user_sub)
            # In case another process is refreshing the token, wait for it to finish
            time.sleep(1)
            user_settings.load()
            if client.oath_session.token["access_token"] == user_settings.token["access_token"]:
                if retries < max_retries: # timeout is 10 seconds.
                    client._refresh_token(retries + 1)
                else:
                    raise TokenRefreshException("Failed to refresh token after multiple attempts, due to lock timeout.") from e
            else:
                client.oath_session.token = user_settings.token
        except (requests.exceptions.RequestException, urllib3.exceptions.HTTPError,
                        socket.error, ssl.SSLError, TimeoutError) as e:
            logger.warning("Token refresh failed due to connection/timeout error.")
            raise e
        except Exception as e:
            logger.exception("Failed to refresh token.")
            user_settings.load()
            user_settings.user_sub = None            
            user_settings.token = None
            user_settings.write()
            client.reset()
            print("Error:", e)
            print("Token refresh failed, please log in again.")
    
    @staticmethod 
    def post(url, data = None, json_data=None, params=None, headers = None):
        return client.__handle_request(url, client.oath_session.post, data, json_data, params, headers)
    
    @staticmethod
    def get(url, params=None, data=None, json_data=None, headers=None):
        return client.__handle_request(url, client.oath_session.get, data, json_data, params, headers)
    
    @staticmethod
    def put(url, data = None, params=None, headers = None):
        return client.__handle_request(url, client.oath_session.put, data, params, headers)
    
    @staticmethod
    def patch(url, data = None, json_data=None, params=None, headers = None):
        return client.__handle_request(url, client.oath_session.patch, data, json_data, params, headers)
    
    @staticmethod
    def delete(url, data = None, json_data=None, params=None, headers = None):
        return client.__handle_request(url, client.oath_session.delete, data, json_data, params, headers)
    
    @staticmethod
    def __handle_request(url, method, data = None, json_data=None, params=None, headers = None):
        try:
            response = method(f'{client.url()}{url}', data=data, json=json_data, params=params, headers=headers, timeout=10)
            process_error_in_response(response)
        except TokenExpiredError:
            client._refresh_token()
            response = method(f'{client.url()}{url}', data=data, json=json_data, params=params, headers=headers, timeout=10)

        return response.json()
    
    @staticmethod
    def reset() -> None:
        '''
        Resets the client to its initial state. It will force the session to be re-initialized and use whatever is stored in the user_settings.
        '''
        client.__session = None
        client.__SERVER_URL = None
        client.__open_id_config = None
        
    @staticmethod
    def check_user_session() -> None:
        '''
        Checks if the same user is still logged in, if not, resets the client.
        '''
        user_settings.load()
        if client.__user_sub != user_settings.user_sub:
            logger.warning("User has changed, resetting the client.")
            client.reset()
    
def process_error_in_response(response):
    if response.status_code >=400:
        try:
            detail = response.json().get("detail", "Request failed, no details provided.")
        except requests.JSONDecodeError:
            detail = response.text
        raise RequestFailedException(response.status_code, detail)

def get_port():
    # assign a random port to the client
    with socket.socket() as s: 
        s.bind(('',0))
        port = s.getsockname()[1]
    return port

def handle_auth_code_request_with_python_TCP_server(port) -> str:
    with socketserver.TCPServer(("", port), RedirectHandler) as httpd:
        httpd.timeout = 120
        httpd.handle_request()
        auth_response = httpd.auth_code
    return auth_response

class RedirectHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        query_components = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)

        if 'code' in query_components:
            auth_code = query_components['code'][0]
            self.server.auth_code = auth_code
            response = "Authorization successful! You can close this window."

        elif 'error' in query_components:
            error = query_components['error'][0]
            self.server.auth_code = None
            response = f"Authorization failed: {error}. You can close this window."
        else:
            self.server.auth_code = None
            response = "No authorization code received. You can close this window."

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(response.encode())

        self.server.server_close()