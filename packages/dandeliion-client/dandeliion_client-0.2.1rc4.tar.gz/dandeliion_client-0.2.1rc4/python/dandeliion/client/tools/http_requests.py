import logging
import requests
import threading
from redo import retrier

HTTP_RETRY_LIMIT = 5
RETRY_BACKOFF_INTERVAL = 5

logging.basicConfig()


class REST_API:
    """
    The low-level abstract REST_API client class. Use this class to log into the
    API. In most cases you can just call :py:meth:`.REST_API.connect` once and
    all subsequent API requests will be authenticated.

    If you want to configure multiple clients, e.g. to perform operations as
    multiple users, you should initialise the client as a context manager,
    using the `with` statement instead of using :py:meth:`.REST_API.connect`.
    Using the `with` statement in this way ensures it is clear which user will
    be used for each action.
    """

    _client_name = 'rest_api_client'

    _http_headers = {
        'default': {
            'Accept': 'application/vnd.api.v1+json',
            'User-Agent': '',
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        },
        'GET': {},
        'PUT': {
            'Content-Type': 'application/json',
        },
        'POST': {
            'Content-Type': 'application/json',
        },
        'DELETE': {
            'Content-Type': 'application/json',
        },
    }

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

    def __init__(
        self,
        endpoint=None,
        admin=None,
        session=None,
    ):
        if session:
            self._session = session
        else:
            self._session = requests.session()
        self.endpoint = endpoint
        self.admin = admin

        self.logger = logging.getLogger('rest_api_client')

    def __enter__(self):
        current_client = getattr(
            self._local,
            'rest_api_client',
            None,
        )

        if current_client:
            if hasattr(self._local, 'previous_' + self._client_name):
                getattr(self._local, 'previous_' + self._client_name).append(current_client)
            else:
                setattr(self._local, 'previous_' + self._client_name, [current_client])

        setattr(self._local, self._client_name, self)
        return self

    def __exit__(self, *exc):
        previous_client = getattr(self._local, 'previous_' + self._client_name).pop()
        setattr(self._local, self._client_name, previous_client)

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
        _headers = self._http_headers['default'].copy()
        _headers.update(self._http_headers[method])
        _headers.update(headers)
        headers = _headers

        if etag:
            headers.update({
                'If-Match': etag,
            })

        url = (endpoint if endpoint else self.endpoint) + path

        # Setting the parameter at all turns on admin mode
        if self.admin:
            params.update({'admin': self.admin})

        if params:
            self.logger.debug(
                "params={}".format(params)
            )

        if json:
            self.logger.debug(
                "json={}".format(json)
            )

        if retry:
            retry_attempts = HTTP_RETRY_LIMIT
        else:
            retry_attempts = 1

        for _ in retrier(
            attempts=retry_attempts,
            sleeptime=RETRY_BACKOFF_INTERVAL,
        ):
            response = self._session.request(
                method,
                url,
                params=params,
                headers=headers,
                json=json,
            )
            if response.status_code < 500:
                break
        else:
            raise APIException(
                'Received HTTP status code {} from API'.format(
                    response.status_code
                )
            )
        # print('====RESPONSE====', response.json(), '====END RESPONSE')
        return response

    def json_request(
        self,
        method,
        path,
        params={},
        headers={},
        json=None,
        etag=None,
        endpoint=None,
        retry=False,
    ):
        response = self.http_request(
            method=method,
            path=path,
            params=params,
            headers=headers,
            json=json,
            etag=etag,
            endpoint=endpoint,
            retry=retry,
        )

        if (
            response.status_code == 204
            or int(response.headers.get('Content-Length', -1)) == 0
            or len(response.text) == 0
        ):
            json_response = None
        else:
            json_response = response.json()
            if 'errors' in json_response:
                raise APIException(', '.join(
                    map(lambda e: e.get('message', ''),
                        json_response['errors'])
                ))
            elif 'error' in json_response:
                raise APIException(json_response['error'])

        return (json_response, response.headers.get('ETag'))

    def get(
        self,
        path,
        params={},
        headers={},
        endpoint=None,
        retry=False,
    ):
        return self.json_request(
            'GET',
            path,
            params=params,
            headers=headers,
            endpoint=endpoint,
            retry=retry,
        )

    def put(
        self,
        path,
        params={},
        headers={},
        json=None,
        etag=None,
        endpoint=None,
        retry=False,
    ):
        return self.json_request(
            'PUT',
            path,
            params=params,
            headers=headers,
            json=json,
            etag=etag,
            endpoint=endpoint,
            retry=retry,
        )

    def post(
        self,
        path,
        params={},
        headers={},
        json=None,
        etag=None,
        endpoint=None,
        retry=False,
    ):
        return self.json_request(
            'POST',
            path,
            params=params,
            headers=headers,
            json=json,
            etag=etag,
            endpoint=endpoint,
            retry=retry,
        )

    def delete(
        self,
        path,
        params={},
        headers={},
        json=None,
        etag=None,
        endpoint=None,
        retry=False,
    ):
        return self.json_request(
            'DELETE',
            path,
            params=params,
            headers=headers,
            json=json,
            etag=etag,
            endpoint=endpoint,
            retry=retry,
        )


class APIException(Exception):
    """
    Raised whenever the API returns an error. The exception will contain the
    raw error message from the API.
    """

    pass


class ResultPaginator(object):
    def __init__(self, object_class, response, etag):
        if response is None:
            response = {}

        self.object_class = object_class
        self.set_page(response)
        self.etag = etag

    def __iter__(self):
        return self

    def __next__(self):
        if self.object_index >= self.object_count:
            if self.object_count and self.next_href:
                response, _ = self.object_class._rest_api_cls.client().get(self.next_href)
                self.set_page(response)
                return next(self)
            else:
                raise StopIteration

        i = self.object_index
        self.object_index += 1
        return self.object_class(self.object_list[i], etag=self.etag)
    next = __next__

    def set_page(self, response):
        self.meta = response.get('meta', {})
        # self.meta = self.meta.get(self.object_class.Meta.api_slug, {})
        self.page = self.meta.get('page', 1)
        self.page_count = self.meta.get('page_count', 1)
        self.next_href = self.meta.get('next_href')
        self.object_list = response.get(self.object_class.Meta.api_slug, [])
        self.object_count = len(self.object_list)
        self.object_index = 0
