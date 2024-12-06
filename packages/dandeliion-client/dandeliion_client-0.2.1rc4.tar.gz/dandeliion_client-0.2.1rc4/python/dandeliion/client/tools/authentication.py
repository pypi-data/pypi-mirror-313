import getpass
import logging
import os
import requests
from abc import abstractmethod
from datetime import datetime, timedelta

if os.environ.get('DANDELIION_DEBUG'):
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig()


class DandeliionAuthenticationException(Exception):
    """
    Raised whenever the authentication returns an error.
    """
    pass


class HTTPAuthenticator:

    @abstractmethod
    def logged_in(self):
        pass

    @abstractmethod
    def login(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_auth_headers(self):
        pass

    @abstractmethod
    def get_session(self):
        pass


class HTTPOathAuthenticator(HTTPAuthenticator):

    # additional headers meant to be added for any http request using the login
    extra_headers = {}

    def __init__(
        self,
        endpoint,
        urls,
        request_session=None,
        redirect_url=None,
        client_id=None,
        client_secret=None,
        username=None,
        password=None,
        login=None,
    ):

        self.logger = logging.getLogger('http_authenticator')

        # use provided session, otherwise create new one
        self._session = request_session if request_session else requests.session()
        self._auth_endpoint = endpoint
        self._urls = urls
        self._redirect_url = redirect_url
        self._client_id = client_id

        self._client_secret = client_secret

        self._logged_in = False
        self._bearer_token = None
        self._refresh_token = None

        self._username = None
        self._password = None

        self._auth(login, username, password)
        self.login()

    def logged_in(self):
        return self._logged_in

    def _auth(self, auth_type, username, password):
        if username is None or password is None:
            if auth_type == 'interactive':
                username, password = self._interactive_login()

            elif auth_type == 'keyring':
                # Get credentials from python keyring
                pass

        self._username = username
        self._password = password

    def _interactive_login(self):
        print('Enter your credentials...')
        username = input('Username: ')
        password = getpass.getpass()

        return username, password

    def login(self, username=None, password=None):

        if self._logged_in:
            return

        if not username:
            username = self._username
        else:
            self._username = username

        if not password:
            password = self._password
        else:
            self._password = password

        if not username or not password:
            return

        login_data = {
            'authenticity_token': self._get_csrf_token(),
            'user': {
                'login': username,
                'password': password,
                'remember_me': True,
            },
        }
        response = self._session.post(
            self._auth_endpoint + self._urls['sign_in'],
            json=login_data,
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            }
        )
        if response.status_code != 200:
            raise HTTPAuthenticationException(
                response.json().get('error', 'Login failed')
            )
        self._logged_in = True

        return response

    def _get_csrf_token(self):
        url = self._auth_endpoint + self._urls['sign_in']
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        return self._session.get(url, headers=headers).headers['x-csrf-token']

    def _get_bearer_token(self):
        if not self._valid_bearer_token():
            grant_type = 'password'

            if self._client_secret:
                grant_type = 'client_credentials'

            if not self.logged_in:
                if grant_type == 'password':
                    if not self.login():
                        return

            if (self._bearer_token and self._refresh_token):
                bearer_data = {
                    'grant_type': 'refresh_token',
                    'refresh_token': self._refresh_token,
                    'client_id': self._client_id,
                }
            else:
                bearer_data = {
                    'grant_type': grant_type,
                    'client_id': self._client_id,
                }

            if grant_type == 'client_credentials':
                bearer_data['client_secret'] = self._client_secret
                bearer_data['url'] = self._redirect_url

            token_response = self._session.post(
                str(self._auth_endpoint) + self._urls['token'],
                bearer_data
            ).json()

            if 'errors' in token_response:
                raise HTTPAuthenticationException(token_response['errors'])

            self._bearer_token = token_response['access_token']
            if (self._bearer_token and grant_type == 'client_credentials'):
                self.logged_in = True
            if 'refresh_token' in token_response:
                self._refresh_token = token_response['refresh_token']
            else:
                self._refresh_token = None
            self._bearer_expires = (
                datetime.now()
                + timedelta(seconds=token_response['expires_in'])
            )
        return self.bearer_token

    def _valid_bearer_token(self):
        # Return invalid if there is no token
        if not self._has_bearer_token():
            return False

        now = datetime.now()
        expires = self._bearer_expires
        # Buffer to allow time for requests
        # to fire without expiring in transit
        buffer_ = timedelta(minutes=2)

        # Add time to now --> pretend time is later
        # Effect of making token expire earlier
        return now + buffer_ <= expires

    def _has_bearer_token(self):
        return self._bearer_token is not None

    def get_auth_headers(self):
        token = self._get_bearer_token()

        headers = {
            'Authorization': 'Bearer %s' % token,
        }
        return headers

    def get_session(self):
        return self._session


class HTTPTokenAuthenticator(HTTPAuthenticator):

    # additional headers meant to be added for any http request using the login
    extra_headers = {}

    def __init__(
        self,
        endpoint,
        urls,
        request_session=None,
        client_id=None,
        credentials=None,
        auth_type=None,
    ):

        self.logger = logging.getLogger('http_authenticator')

        self._session = request_session if request_session else requests.session()
        self._auth_endpoint = endpoint
        self._urls = urls
        self._client_id = client_id

        self._logged_in = False
        self._token = None

        self._credentials = credentials
        self._auth_type = auth_type

        self.login()

    def logged_in(self):
        return self._logged_in  # check if token is still valid?

    def _auth(self, auth_type, login_data):

        if auth_type == 'password':
            response = self._session.post(
                self._auth_endpoint + self._urls['sign_in'],
                json=login_data,
                headers={
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                }
            )
            if response.status_code != 200:
                raise HTTPAuthenticationException(
                    response.json().get('non_field_errors', 'Login failed')
                )
            self._token = response.json()['token']

        elif auth_type == 'import':
            self._token = login_data['token']

        self._credentials = login_data
        self._auth_type = auth_type

    def _interactive_login(self):
        print('Enter your credentials...')
        username = input('Username: ')
        password = getpass.getpass()

        return username, password

    def login(self, username=None, password=None, auth_type=None):

        if self._logged_in:
            return

        if not username and not password and not auth_type:
            login_data = self._credentials
            auth_type = self._auth_type

        if not auth_type or auth_type == 'interactive':
            username, password = self._interactive_login()
            auth_type = 'password'

        if auth_type == 'password' and not login_data:
            login_data = {
                'username': username,
                'password': password,
            }

        self._auth(auth_type, login_data)
        self._logged_in = True
        return self._logged_in

    def _get_token(self):
        if not self._valid_token():
            if not self.login():
                return

        return self._token

    def _valid_token(self):
        # Return invalid if there is no token
        if not self._has_token():
            return False
        return True

    def _has_token(self):
        return self._token is not None

    def get_auth_headers(self):
        token = self._get_token()

        headers = {
            'Authorization': 'Token %s' % token,
        }
        return headers

    def get_session(self):
        return self._session


class HTTPAuthenticationException(Exception):
    """
    Raised whenever the authentication returns an error.
    """

    pass
