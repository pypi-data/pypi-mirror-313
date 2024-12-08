from typing import Any, Literal

import socketio  # type: ignore


class OrderSocket_io(socketio.Client):
    """A Socket.IO client.
    This class implements a fully compliant Socket.IO web client with support
    for websocket and long-polling transports.
    :param reconnection: 'True'. if the client should automatically attempt to
                         reconnect to the server after an interruption, or
                         'False' to not reconnect. The default is 'True'.
    :param reconnection_attempts: How many reconnection attempts to issue
                                  before giving up, or 0 for infinity attempts.
                                  The default is 0.
    :param reconnection_delay: How long to wait in seconds before the first
                               reconnection attempt. Each successive attempt
                               doubles this delay.
    :param reconnection_delay_max: The maximum delay between reconnection
                                   attempts.
    :param randomization_factor: Randomization amount for each delay between
                                 reconnection attempts. The default is 0.5,
                                 which means that each delay is randomly
                                 adjusted by +/- 50%.
    :param logger: To enable logging set to 'True' or pass a logger object to
                   use. To disable logging set to 'False'. The default is
                   'False'.
    :param binary: 'True' to support binary payloads, 'False' to treat all
                   payloads as text. On Python 2, if this is set to 'True',
                   'unicode' values are treated as text, and 'str' and
                   'bytes' values are treated as binary.  This option has no
                   effect on Python 3, where text and binary payloads are
                   always automatically discovered.
    :param json: An alternative json module to use for encoding and decoding
                 packets. Custom json modules must have 'dumps' and 'loads'
                 functions that are compatible with the standard library
                 versions.
    """

    def __init__(
        self,
        token: str,
        userID: str,
        root_url: str,
        reconnection: bool = True,
        reconnection_attempts: int = 0,
        reconnection_delay: float = 1,
        reconnection_delay_max: float = 50000,
        randomization_factor: float = 0.5,
        logger: bool = False,
        binary: bool = False,
        json: Any | None = None,
        **kwargs: Any,
    ):
        self.sid = socketio.Client(logger=False, engineio_logger=False)
        self.eventlistener = self.sid

        self.userID = userID
        self.token = token

        self.port = root_url

        port = f"{self.port}/?token="

        self.connection_url = (
            port + self.token + "&userID=" + self.userID + "&apiType=INTERACTIVE"
        )

    def setup_event_listners(self, on_order: Any):
        self.sid.on("order", on_order)  # type: ignore

        # self.sid.on("connect", self.on_connect)
        self.sid.on("message", self.on_message)  # type: ignore
        # self.sid.on("joined", self.on_joined)
        self.sid.on("error", self.on_error)  # type: ignore
        self.sid.on("trade", self.on_trade)  # type: ignore
        self.sid.on("position", self.on_position)  # type: ignore
        self.sid.on("tradeConversion", self.on_tradeconversion)  # type: ignore
        self.sid.on("logout", self.on_messagelogout)  # type: ignore
        # self.sid.on("disconnect", self.on_disconnect)

    def connect(  # type: ignore
        self,
        headers: dict[str, str] = {},
        transports: Literal["polling", "websocket"] = "websocket",
        namespaces: list[str] | None = None,
        socketio_path: str = "/interactive/socket.io",
        verify: bool = False,
    ):
        """Connect to a Socket.IO server.
        :param url: The URL of the Socket.IO server. It can include custom
                    query string parameters if required by the server.
        :param headers: A dictionary with custom headers to send with the
                        connection request.
        :param transports: The list of allowed transports. Valid transports
                           are 'polling' and 'websocket'. If not
                           given, the polling transport is connected first,
                           then an upgrade to websocket is attempted.
        :param namespaces: The list of custom namespaces to connect, in
                           addition to the default namespace. If not given,
                           the namespace list is obtained from the registered
                           event handlers.
        :param socketio_path: The endpoint where the Socket.IO server is
                              installed. The default value is appropriate for
                              most cases.

        """
        """Connect to the socket."""
        url = self.connection_url

        """Connected to the socket."""
        self.sid.connect(url, headers, transports, namespaces, socketio_path)  # type: ignore
        self.sid.wait()
        """Disconnect from the socket."""
        # self.sid.disconnect()

    def on_connect(self):
        """Connect from the socket"""
        print("Interactive socket connected successfully!")

    def on_message(self):
        """On message from socket"""
        print("I received a message!")

    def on_joined(self, data: Any):
        """On socket joined"""
        print(f"Interactive socket joined successfully!{data}")

    def on_error(self, data: Any):
        """On receiving error from socket"""
        print(f"Interactive socket error!{data}")

    def on_order(self, data: Any):
        """On receiving order placed data from socket"""
        print(f"Order placed!{data}")

    def on_trade(self, data: Any):
        """On receiving trade data from socket"""
        print(f"Trade Received!{data}")

    def on_position(self, data: Any):
        """On receiving position data from socket"""
        print(f"Position Retrieved!{data}")

    def on_tradeconversion(self, data: Any):
        """On receiving trade conversion data from socket"""
        print(f"Trade Conversion Received!{data}")

    def on_messagelogout(self, data: Any):
        """On receiving user logout message"""
        print(f"User logged out!{data}")

    def on_disconnect(self):
        """On receiving disconnection from socket"""
        print("Interactive Socket disconnected!")

    def get_emitter(self):
        """For getting event listener"""
        return self.eventlistener
