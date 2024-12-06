import threading
import json
from threading import Condition

from dandeliion.client.config import (
    DANDELIION_WEBSOCKET_ENDPOINT,
    DANDELIION_AUTH_ENDPOINT,
    DANDELIION_CLIENT_ID,
)
from dandeliion.client.tools.websockets import WebSocketClient
from .authentication import HTTPAuthenticator
from . import DandeliionInterfaceException


class SimulationUpdateWebSocketClient(WebSocketClient):

    _client_name = 'simulation_update_websocket_client'
    _local = threading.local()

    @classmethod
    def connect(cls, *args, **kwargs):
        """
        connect(endpoint=None, admin=False)

        Configures the HTTP Request client for use.

        This should be called before using any class relying on this class for
        REST API communication e.g. for setting the endpoint.
        """
        try:
            local_client = cls(*args, **kwargs)
            setattr(cls._local, cls._client_name, local_client)
            return local_client
        except Exception as e:
            raise DandeliionInterfaceException(
                'Initialisation of connection to Dandeliion Update WebSocket failed'
            ) from e

    @classmethod
    def client(cls, *args, **kwargs):
        local_client = getattr(cls._local, cls._client_name, None)
        if not local_client:
            return cls(*args, **kwargs)
        return local_client

    def __init__(self,
                 *args,
                 on_update=None,
                 connector=None,
                 credentials=None,
                 auth_type=None,
                 **kwargs):
        if not connector:
            connector = HTTPAuthenticator(
                self,
                endpoint=DANDELIION_AUTH_ENDPOINT,
                urls=self._urls,
                client_id=DANDELIION_CLIENT_ID,
                credentials=credentials,
                auth_type=auth_type
            )
        super().__init__(
            *args,
            url=f'{DANDELIION_WEBSOCKET_ENDPOINT}/updates/',
            on_message=self.on_update,
            on_open=self.on_open,
            on_close=self.on_close,
            on_error=self.on_error,
            extra_headers=connector.get_auth_headers(),
            **kwargs
        )
        self._on_update = on_update
        self._is_opened = False
        self._is_ready = Condition()

    def subscribe(self, message):
        with self._is_ready:
            self._is_ready.wait_for(lambda: self._is_opened)
        self.send_message(message)

    def on_open(self, app):
        with self._is_ready:
            self._is_opened = True
            self._is_ready.notify_all()

    def on_update(self, app, message):
        self._on_update(json.loads(message)['updates'])

    def on_close(self, wsapp, close_status_code, close_msg):
        # Because on_close was triggered, we know the opcode = 8
        print("on_close args:")
        print("close status code: " + str(close_status_code))
        print("close message: " + str(close_msg))

    def on_error(self, app, err):
        print("ERROR", app, err)
