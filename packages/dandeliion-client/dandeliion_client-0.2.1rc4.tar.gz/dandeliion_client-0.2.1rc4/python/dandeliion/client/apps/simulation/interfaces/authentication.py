import threading

from dandeliion.client.tools.authentication import DandeliionAuthenticationException  # noqa: F401
from dandeliion.client.tools.authentication import HTTPTokenAuthenticator

from dandeliion.client.config import (
    DANDELIION_AUTH_ENDPOINT,
    DANDELIION_CLIENT_ID,
)


class HTTPAuthenticator(HTTPTokenAuthenticator):

    urls = {
        'sign_in': 'api-token-auth/',
        'verify': 'account/',
    }

    _client_name = 'http_token_authenticator'
    _local = threading.local()

    @classmethod
    def connect(cls, *args, **kwargs):
        """
        connect(endpoint=None, admin=False)

        Configures the HTTP Request client for use.

        This should be called before using any class relying on this class for
        REST API communication e.g. for setting the endpoint.
        """
        local_client = cls(*args, **kwargs)
        setattr(cls._local, cls._client_name, local_client)
        return local_client

    @classmethod
    def client(cls, *args, **kwargs):
        local_client = getattr(cls._local, cls._client_name, None)
        if not local_client:
            return cls(*args, **kwargs)
        return local_client

    def __init__(self, auth_type, credentials, endpoint=None):
        if not endpoint:
            endpoint = DANDELIION_AUTH_ENDPOINT

        super().__init__(
            endpoint=endpoint,
            urls=self.urls,
            client_id=DANDELIION_CLIENT_ID,
            auth_type=auth_type,
            credentials=credentials
        )
