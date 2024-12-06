from collections.abc import Callable
import json
import threading
import time
from typing import Any

from quantplay.broker.kotak_utils.kotak_ws_lib import HSIWebSocket


ORDER_FEED_URL = "wss://clhsi.kotaksecurities.com/realtime?sId={server_id}"


class NeoWebSocket:
    def __init__(self, sid: str | None, token: str | None, server_id: str | None):
        self.hsiWebsocket = None
        self.is_hsi_open = 0
        self.sid = sid
        self.access_token = token
        self.server_id = server_id
        self.on_message: Callable[[Any], None] | None = None
        self.on_error: Callable[[Any], None] | None = None
        self.on_close: Callable[[], None] | None = None
        self.on_open: Callable[[], None] | None = None
        self.hsi_thread = None

    def on_hsi_open(self):
        server = "WEB"
        json_d = {
            "type": "CONNECTION",
            "Authorization": self.access_token,
            "Sid": self.sid,
            "source": server,
        }
        json_d = json.dumps(json_d)

        if self.hsiWebsocket:
            self.hsiWebsocket.send(json_d)

        if self.on_open:
            self.on_open()

    def on_hsi_close(self):
        if self.is_hsi_open == 1:
            self.is_hsi_open = 0
        if self.on_close:
            self.on_close()

    def on_hsi_error(self, error: Any):
        if self.is_hsi_open == 1:
            self.is_hsi_open = 0

        if self.on_error:
            self.on_error(error)
        else:
            print("Error Occurred in Websocket! Error Message ", error)

    def on_hsi_message(self, message: Any):
        if message:
            if isinstance(message, str):
                req = json.loads(message)
                if req["type"] == "cn":
                    self.is_hsi_open = 1
                    threading.Thread(target=self.start_hsi_ping_thread).start()

        if self.on_message:
            self.on_message({"type": "order_feed", "data": message})

    def start_hsi_ping_thread(self):
        while self.hsiWebsocket and self.is_hsi_open:
            time.sleep(30)
            payload = {"type": "HB"}
            self.hsiWebsocket.send(json.dumps(payload))

    def start_hsi_websocket(self):
        url = ORDER_FEED_URL.format(server_id=self.server_id)
        self.hsiWebsocket = HSIWebSocket()
        self.hsiWebsocket.open_connection(
            url=url,
            onopen=self.on_hsi_open,
            onmessage=self.on_hsi_message,
            onclose=self.on_hsi_close,
            onerror=self.on_hsi_error,
        )

    def start_hsi_websocket_thread(self):
        self.hsi_thread = threading.Thread(target=self.start_hsi_websocket)
        self.hsi_thread.start()

    def get_order_feed(self):
        if self.hsiWebsocket is None or self.is_hsi_open == 0:
            self.start_hsi_websocket_thread()
        else:
            print("you had already subscribed for order feed")
