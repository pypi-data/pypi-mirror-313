from collections.abc import Callable
import json
import ssl
from typing import Any

import websocket


class StartHSIServer:
    def __init__(
        self,
        url: str,
        onopen: Callable[[], None],
        onmessage: Callable[[Any], None],
        onerror: Callable[[Any], None],
        onclose: Callable[[], None],
    ):
        self.openState = None
        self.readyState = None
        self.url = url
        self.onopen = onopen
        self.onmessage = onmessage
        self.onerror = onerror
        self.onclose = onclose
        # self.token, self.sid = token, sid
        global hsiWs
        try:
            # websocket.enableTrace(True)
            hsiWs = websocket.WebSocketApp(
                self.url,
                on_open=self.on_open,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close,
            )
            hsiWs.run_forever(  # type: ignore
                ping_interval=5, reconnect=5, sslopt={"cert_reqs": ssl.CERT_NONE}
            )
        except Exception:
            print("WebSocket not supported!")

    def on_message(self, ws: websocket.WebSocket, message: Any):
        # print("Received message:", message)
        self.onmessage(message)

    def on_error(self, ws: websocket.WebSocket, error: Any):
        print("Error:", error)
        self.onerror(error)

    def on_close(self, ws: websocket.WebSocket, close_status_code: Any, close_msg: Any):
        # print("Connection closed")
        self.openState = 0
        self.readyState = 0
        if hsiWs:
            hsiWs.close()  # type: ignore
        self.onclose()

    def on_open(self, ws: websocket.WebSocket):
        # print("Connection established HSWebSocket")
        self.openState = 1
        self.readyState = 1
        self.onopen()


class HSIWebSocket:
    def __init__(self):
        # self.hsiWs = None
        self.hsiSocket = None
        self.reqData = None
        self.openState = 0
        self.readyState = 0
        self.url = None
        self.onopen = None
        self.onmessage = None
        self.onclose = None
        self.onerror = None
        # self.token, self.sid = token, sid

    def open_connection(
        self,
        url: str,
        onopen: Callable[[], None],
        onmessage: Callable[[Any], None],
        onerror: Callable[[Any], None],
        onclose: Callable[[], None],
    ):
        self.url = url
        self.onopen = onopen
        self.onmessage = onmessage
        self.onclose = onclose
        self.onerror = onerror
        StartHSIServer(self.url, self.onopen, self.onmessage, self.onerror, self.onclose)

    def send(self, d: Any):
        reqJson = json.loads(d)
        req = None
        if reqJson["type"] == "CONNECTION":
            if "Authorization" in reqJson and "Sid" in reqJson and "source" in reqJson:
                req = {
                    "type": "cn",
                    "Authorization": reqJson["Authorization"],
                    "Sid": reqJson["Sid"],
                    "src": reqJson["source"],
                }
                self.reqData = req
            else:
                if "x-access-token" in reqJson and "src" in reqJson:
                    req = {
                        "type": "cn",
                        "x-access-token": reqJson["x-access-token"],
                        "source": reqJson["source"],
                    }
                    self.reqData = req
                else:
                    print("Invalid connection mode !")

        elif reqJson["type"] == "HB":
            # self.reqData=reqJson
            req = {"type": "hb"}
            self.reqData = req

        else:
            if reqJson["type"] == "FORCE_CONNECTION":
                self.reqData = self.reqData["type"] = "fcn"  # type: ignore
                req = self.reqData
            else:
                print("Invalid Request !")

        if hsiWs and req:
            js_obj = json.dumps(req)
            hsiWs.send(js_obj)
        else:
            print(
                "Unable to send request! Reason: Connection faulty or request not valid!"
            )

    def close(self):
        self.openState = 0
        self.readyState = 0

        if hsiWs:
            hsiWs.close()  # type: ignore
