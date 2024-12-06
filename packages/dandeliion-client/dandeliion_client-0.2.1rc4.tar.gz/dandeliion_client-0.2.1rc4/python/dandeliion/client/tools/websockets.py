import threading
import websocket


class WebSocketClient:

    def __init__(self, url, on_open=None, on_message=None, on_error=None, on_close=None, extra_headers=None):
        self._app = websocket.WebSocketApp(url,
                                           on_open=on_open,
                                           on_message=on_message,
                                           on_error=on_error,
                                           on_close=on_close,
                                           header=extra_headers,
                                           )

        # Initialise the run_forever inside a thread and make this thread as a daemon thread
        wst = threading.Thread(target=self._app.run_forever)
        wst.daemon = True
        wst.start()

    def send_message(self, message):
        self._app.send(message)
