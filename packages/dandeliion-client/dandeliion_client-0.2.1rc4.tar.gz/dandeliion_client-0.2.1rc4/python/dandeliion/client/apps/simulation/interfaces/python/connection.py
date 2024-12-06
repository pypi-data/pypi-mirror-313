from ..http_requests import REST_API
from ..authentication import HTTPAuthenticator, DandeliionAuthenticationException
from .. import DandeliionInterfaceException
import json


def connect(username=None, password=None, credentials=None, **kwargs):
    if not credentials and (not username or not password):
        raise ValueError(
            'Either a username and password or a path to a valid credential file have to be provided!'
        )

    if credentials:
        with open(credentials) as cred_file:
            credentials = json.load(cred_file)
            auth_type = 'import'

    else:
        credentials = {
            'username': username,
            'password': password,
        }
        auth_type = 'password'

    try:
        connector = HTTPAuthenticator.connect(
            auth_type=auth_type,
            credentials=credentials,
        )

    except Exception as e:
        raise DandeliionAuthenticationException('Authentication failed') from e

    try:
        REST_API.connect(connector=connector, **kwargs)
    except Exception as e:
        raise DandeliionInterfaceException(
            'Initialisation of connection to Dandeliion REST API failed'
        ) from e
