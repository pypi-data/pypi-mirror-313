from dandeliion.client.tools.http_requests import REST_API as Base_REST_API
import logging
import os

from .authentication import HTTPAuthenticator
from dandeliion.client.config import (
    DANDELIION_SIMULATION_ENDPOINT,
)
from . import DandeliionInterfaceException

if os.environ.get('DANDELIION_DEBUG'):
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig()


class REST_API(Base_REST_API):

    _connector = None

    @classmethod
    def connect(cls, *args, **kwargs):
        """
        connect(username=None, password=None, endpoint=None, admin=False)

        Configures the HTTP Request client for use.

        Note that there is no need to call this unless you need to pass one or
        more of the below arguments.  By default, the client will connect to
        the REST API as an anonymous user (i.e. no authentication is performed)
        """
        try:
            local_client = super().connect(*args, **kwargs)
            local_client.login()
            return local_client
        except Exception as e:
            raise DandeliionInterfaceException('Initialisation of connection to Dandeliion REST API failed') from e

    def __init__(
        self,
        admin=None,
        connector=None,
        **auth_args
    ):

        # self._http_headers['default']['User-Agent'] = \
        # 'dandeliion-python-client/version=' \
        # + version('dandeliion_python_client')  # TODO fix

        self._connector = connector if connector else HTTPAuthenticator(
            credentials=auth_args.get('credentials', None),
            auth_type=auth_args.get('auth_type', None)
        )

        Base_REST_API.__init__(
            self,
            endpoint=DANDELIION_SIMULATION_ENDPOINT,
            admin=admin,
            session=self._connector.get_session(),
        )

        self.logger = logging.getLogger('simulation_rest_api_client')

    def login(self):
        self._connector.login()

    def http_request(
        self,
        method,
        path,
        params={},
        headers={},
        json=None,
        etag=None,
        endpoint=None,
        retry=False
    ):

        headers.update(self._connector.get_auth_headers())

        return super().http_request(
            method=method,
            path=path,
            params=params,
            headers=headers,
            json=json,
            etag=etag,
            endpoint=endpoint,
            retry=retry
        )
