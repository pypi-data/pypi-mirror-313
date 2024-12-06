import datetime
import hashlib
import json
import logging
import threading
import time
import urllib.parse
from datetime import datetime as dt
from time import sleep
from typing import Any, Callable, Literal, TypedDict

import requests
import websocket

from quantplay.exception import TokenException
from quantplay.model.generics import ExchangeType, NorenTypes

logger = logging.getLogger(__name__)


class position:
    prd: str
    exch: str
    instname: str
    symname: str
    exd: int
    optt: str
    strprc: float
    buyqty: int
    sellqty: int
    netqty: int

    def encode(self):
        return self.__dict__


class ProductType:
    Delivery = "C"
    Intraday = "I"
    Normal = "M"
    CF = "M"


class FeedType:
    TOUCHLINE = 1
    SNAPQUOTE = 2


class PriceType:
    Market = "MKT"
    Limit = "LMT"
    StopLossLimit = "SL-LMT"
    StopLossMarket = "SL-MKT"


class BuyorSell:
    Buy = "B"
    Sell = "S"


def reportmsg(msg: str):
    logger.debug(msg)


def reporterror(msg: str):
    logger.error(msg)


def reportinfo(msg: str):
    logger.info(msg)


class FAServiceConfig(TypedDict):
    host: str
    routes: dict[str, str]
    websocket_endpoint: str


class FA_NorenApi:
    __service_config: FAServiceConfig = {
        "host": "http://wsapihost/",
        "routes": {
            "authorize": "/QuickAuth",
            "logout": "/Logout",
            "forgot_password": "/ForgotPassword",
            "change_password": "/Changepwd",
            "watchlist_names": "/MWList",
            "watchlist": "/MarketWatch",
            "watchlist_add": "/AddMultiScripsToMW",
            "watchlist_delete": "/DeleteMultiMWScrips",
            "placeorder": "/PlaceOrder",
            "modifyorder": "/ModifyOrder",
            "cancelorder": "/CancelOrder",
            "exitorder": "/ExitSNOOrder",
            "product_conversion": "/ProductConversion",
            "orderbook": "/OrderBook",
            "tradebook": "/TradeBook",
            "singleorderhistory": "/SingleOrdHist",
            "searchscrip": "/SearchScrip",
            "TPSeries": "/TPSeries",
            "optionchain": "/GetOptionChain",
            "holdings": "/Holdings",
            "limits": "/Limits",
            "positions": "/PositionBook",
            "scripinfo": "/GetSecurityInfo",
            "getquotes": "/GetQuotes",
            "span_calculator": "/SpanCalc",
            "option_greek": "/GetOptionGreek",
            "get_daily_price_series": "/EODChartData",
        },
        "websocket_endpoint": "wss://wsendpoint/",
    }

    def __init__(self, host: str, websocket_endpoint: str) -> None:
        self.__service_config["host"] = host
        self.__service_config["websocket_endpoint"] = websocket_endpoint

        self.__websocket: websocket.WebSocketApp | None = None
        self.__websocket_connected = False
        self.__ws_mutex = threading.Lock()
        self.__on_error = None
        self.__on_disconnect = None
        self.__on_open = None
        self.__subscribe_callback = None
        self.__order_update_callback = None

        self.__username: str | None = None

    def __ws_run_forever(self):
        while self.__websocket is None:
            sleep(0.05)

        while not self.__stop_event.is_set():
            try:
                self.__websocket.run_forever(ping_interval=3, ping_payload='{"t":"h"}')  # type: ignore
            except Exception:
                pass

            sleep(0.1)

    def __ws_send(self, data: str | bytes):
        while not self.__websocket_connected or self.__websocket is None:
            sleep(0.05)

        with self.__ws_mutex:
            ret = self.__websocket.send(data)

        return ret

    def __on_close_callback(
        self, wsapp: websocket.WebSocket, close_status_code: str, close_msg: str
    ):
        reportmsg(close_status_code)
        reportmsg(str(wsapp))

        self.__websocket_connected = False
        if self.__on_disconnect:
            self.__on_disconnect()

    def __on_open_callback(self, ws: websocket.WebSocket | None = None):
        self.__websocket_connected = True

        values = {
            "t": "c",
            "uid": self.__username,
            "actid": self.__username,
            "susertoken": self.__susertoken,
            "source": "API",
        }

        payload = json.dumps(values)

        reportmsg(payload)
        self.__ws_send(payload)

    def __on_error_callback(
        self, ws: websocket.WebSocket | None = None, error: Any | None = None
    ):
        if type(ws) is not websocket.WebSocketApp:
            error = ws

        if self.__on_error:
            self.__on_error(error)

    def __on_data_callback(
        self,
        ws: websocket.WebSocket | None = None,
        message: str | None = None,
        data_type: Any | None = None,
        continue_flag: Any | None = None,
    ):
        res = json.loads(message)  # type: ignore

        if self.__subscribe_callback is not None:
            if res["t"] == "tk" or res["t"] == "tf":
                self.__subscribe_callback(res)
                return
            if res["t"] == "dk" or res["t"] == "df":
                self.__subscribe_callback(res)
                return

        if self.__on_error is not None:
            if res["t"] == "ck" and res["s"] != "OK":
                self.__on_error(res)
                return

        if self.__order_update_callback is not None:
            if res["t"] == "om":
                self.__order_update_callback(res)
                return

        if self.__on_open:
            if res["t"] == "ck" and res["s"] == "OK":
                self.__on_open()
                return

    def start_websocket(
        self,
        subscribe_callback: Callable[[Any], None] | None = None,
        order_update_callback: Callable[[Any], None] | None = None,
        socket_open_callback: Callable[[], None] | None = None,
        socket_close_callback: Callable[[], None] | None = None,
        socket_error_callback: Callable[[Any], None] | None = None,
    ):
        """Start a websocket connection for getting live data"""
        self.__on_open = socket_open_callback
        self.__on_disconnect = socket_close_callback
        self.__on_error = socket_error_callback
        self.__subscribe_callback = subscribe_callback
        self.__order_update_callback = order_update_callback
        self.__stop_event = threading.Event()
        url = self.__service_config["websocket_endpoint"].format(
            access_token=self.__susertoken
        )
        reportmsg("connecting to {}".format(url))

        self.__websocket = websocket.WebSocketApp(
            url,
            on_data=self.__on_data_callback,
            on_error=self.__on_error_callback,
            on_close=self.__on_close_callback,
            on_open=self.__on_open_callback,
        )

        self.__ws_thread = threading.Thread(target=self.__ws_run_forever)
        self.__ws_thread.daemon = True
        self.__ws_thread.start()

    def close_websocket(self):
        if not self.__websocket_connected or self.__websocket is None:
            return

        self.__stop_event.set()
        self.__websocket_connected = False
        self.__websocket.close()  # type: ignore
        self.__ws_thread.join()

    def login(
        self,
        userid: str,
        password: str,
        twoFA: str,
        vendor_code: str,
        api_secret: str,
        imei: str,
    ):
        config = FA_NorenApi.__service_config

        url = f"{config['host']}{config['routes']['authorize']}"
        reportmsg(url)

        # Convert to SHA 256 for password and app key
        pwd = hashlib.sha256(password.encode("utf-8")).hexdigest()
        u_app_key = "{0}|{1}".format(userid, api_secret)
        app_key = hashlib.sha256(u_app_key.encode("utf-8")).hexdigest()

        values = {
            "source": "API",
            "apkversion": "1.0.0",
            "uid": userid,
            "pwd": pwd,
            "factor2": twoFA,
            "vc": vendor_code,
            "appkey": app_key,
            "imei": imei,
        }

        payload = "jData=" + json.dumps(values)
        reportmsg("Req:" + payload)

        res = requests.post(url, data=payload)
        reportmsg("Reply:" + res.text)

        resdict: dict[str, Any] = json.loads(res.text)

        self.__username = userid
        self.__accountid = userid

        if "stat" in resdict and resdict["stat"].lower() == "not_ok":
            raise TokenException(resdict["emsg"])
        self.__susertoken = resdict["susertoken"]

        return resdict

    def set_session(self, userid: str, usertoken: str) -> Literal[True]:
        self.__username = userid
        self.__accountid = userid
        self.__susertoken = usertoken

        reportmsg(f"{userid} session set to : {self.__susertoken}")

        return True

    def forgot_password(self, userid: str, pan: str, dob: str):
        config = FA_NorenApi.__service_config

        url = f"{config['host']}{config['routes']['forgot_password']}"
        reportmsg(url)

        values = {
            "source": "API",
            "uid": userid,
            "pan": pan,
            "dob": dob,
        }

        payload = "jData=" + json.dumps(values)
        reportmsg("Req:" + payload)

        res = requests.post(url, data=payload)
        reportmsg("Reply:" + res.text)

        resDict = json.loads(res.text)

        return resDict

    def logout(self):
        config = FA_NorenApi.__service_config

        url = f"{config['host']}{config['routes']['logout']}"
        reportmsg(url)

        values = {
            "ordersource": "API",
            "uid": self.__username,
        }

        payload = "jData=" + json.dumps(values) + f"&jKey={self.__susertoken}"

        reportmsg(payload)

        res = requests.post(url, data=payload)
        reportmsg(res.text)

        resDict = json.loads(res.text)

        self.__username = None
        self.__accountid = None
        self.__susertoken = None

        return resDict

    def subscribe(self, instrument: str, feed_type: Literal[1, 2] = FeedType.TOUCHLINE):
        values = {}

        if feed_type == FeedType.TOUCHLINE:
            values["t"] = "t"
        elif feed_type == FeedType.SNAPQUOTE:
            values["t"] = "d"
        else:
            values["t"] = str(feed_type)

        if isinstance(instrument, list):
            values["k"] = "#".join(instrument)
        else:
            values["k"] = instrument

        data = json.dumps(values)

        self.__ws_send(data)

    def unsubscribe(self, instrument: str, feed_type: Literal[1, 2] = FeedType.TOUCHLINE):
        values = {}

        if feed_type == FeedType.TOUCHLINE:
            values["t"] = "u"
        elif feed_type == FeedType.SNAPQUOTE:
            values["t"] = "ud"

        if isinstance(instrument, list):
            values["k"] = "#".join(instrument)
        else:
            values["k"] = instrument

        data = json.dumps(values)

        self.__ws_send(data)

    def subscribe_orders(self):
        values = {
            "t": "o",
            "actid": self.__accountid,
        }

        data = json.dumps(values)

        reportmsg(data)
        self.__ws_send(data)

    def get_watch_list_names(self):
        config = FA_NorenApi.__service_config

        url = f"{config['host']}{config['routes']['watchlist_names']}"
        reportmsg(url)

        values = {
            "ordersource": "API",
            "uid": self.__username,
        }

        payload = "jData=" + json.dumps(values) + f"&jKey={self.__susertoken}"

        reportmsg(payload)

        res = requests.post(url, data=payload)
        reportmsg(res.text)

        resDict = json.loads(res.text)

        return resDict

    def get_watch_list(self, wlname: str):
        config = FA_NorenApi.__service_config

        url = f"{config['host']}{config['routes']['watchlist']}"
        reportmsg(url)

        values = {
            "ordersource": "API",
            "uid": self.__username,
            "wlname": wlname,
        }

        payload = "jData=" + json.dumps(values) + f"&jKey={self.__susertoken}"

        reportmsg(payload)

        res = requests.post(url, data=payload)
        reportmsg(res.text)

        resDict = json.loads(res.text)

        return resDict

    def add_watch_list_scrip(self, wlname: str, instrument: str):
        config = FA_NorenApi.__service_config

        url = f"{config['host']}{config['routes']['watchlist_add']}"
        reportmsg(url)

        values = {
            "ordersource": "API",
            "uid": self.__username,
            "wlname": wlname,
        }

        if isinstance(instrument, list):
            values["scrips"] = "#".join(instrument)
        else:
            values["scrips"] = instrument
        payload = "jData=" + json.dumps(values) + f"&jKey={self.__susertoken}"

        reportmsg(payload)

        res = requests.post(url, data=payload)
        reportmsg(res.text)

        resDict = json.loads(res.text)

        return resDict

    def delete_watch_list_scrip(self, wlname: str, instrument: str):
        config = FA_NorenApi.__service_config

        url = f"{config['host']}{config['routes']['watchlist_delete']}"
        reportmsg(url)

        values = {
            "ordersource": "API",
            "uid": self.__username,
            "wlname": wlname,
        }

        if isinstance(instrument, list):
            values["scrips"] = "#".join(instrument)
        else:
            values["scrips"] = instrument
        payload = "jData=" + json.dumps(values) + f"&jKey={self.__susertoken}"

        reportmsg(payload)

        res = requests.post(url, data=payload)
        reportmsg(res.text)

        resDict = json.loads(res.text)

        return resDict

    def place_order(
        self,
        buy_or_sell: NorenTypes.TransactionTypeType,
        product_type: NorenTypes.ProductType,
        exchange: ExchangeType,
        tradingsymbol: str,
        quantity: int,
        discloseqty: int,
        price_type: NorenTypes.OrderTypeType,
        price: float = 0.0,
        trigger_price: float | None = None,
        retention: str = "DAY",
        amo: str = "NO",
        remarks: str | None = None,
        bookloss_price: float = 0.0,
        bookprofit_price: float = 0.0,
        trail_price: float = 0.0,
    ):
        config = FA_NorenApi.__service_config

        url = f"{config['host']}{config['routes']['placeorder']}"
        reportmsg(url)

        values = {
            "ordersource": "API",
            "uid": self.__username,
            "actid": self.__accountid,
            "trantype": buy_or_sell,
            "prd": product_type,
            "exch": exchange,
            "tsym": urllib.parse.quote_plus(tradingsymbol),
            "qty": str(quantity),
            "dscqty": str(discloseqty),
            "prctyp": price_type,
            "prc": str(price),
            "trgprc": str(trigger_price),
            "ret": retention,
            "remarks": remarks,
            "amo": amo,
        }

        # if cover order or high leverage order
        if product_type == "H":
            values["blprc"] = str(bookloss_price)
            # trailing price
            if trail_price != 0.0:
                values["trailprc"] = str(trail_price)

        # bracket order
        if product_type == "B":
            values["blprc"] = str(bookloss_price)
            values["bpprc"] = str(bookprofit_price)
            # trailing price
            if trail_price != 0.0:
                values["trailprc"] = str(trail_price)

        payload = "jData=" + json.dumps(values) + f"&jKey={self.__susertoken}"

        reportmsg(payload)

        res = requests.post(url, data=payload)
        reportmsg(res.text)

        resDict = json.loads(res.text)

        return resDict

    def modify_order(
        self,
        orderno: str,
        exchange: ExchangeType,
        tradingsymbol: str,
        newquantity: int,
        newprice_type: NorenTypes.OrderTypeType,
        newprice: float = 0.0,
        newtrigger_price: float | None = None,
        bookloss_price: float = 0.0,
        bookprofit_price: float = 0.0,
        trail_price: float = 0.0,
    ):
        config = FA_NorenApi.__service_config

        url = f"{config['host']}{config['routes']['modifyorder']}"

        values = {
            "ordersource": "API",
            "uid": self.__username,
            "actid": self.__accountid,
            "norenordno": str(orderno),
            "exch": exchange,
            "tsym": urllib.parse.quote_plus(tradingsymbol),
            "qty": str(newquantity),
            "prctyp": newprice_type,
            "prc": str(newprice),
        }

        if (newprice_type == "SL-LMT") or (newprice_type == "SL-MKT"):
            if newtrigger_price is not None:
                values["trgprc"] = str(newtrigger_price)
            else:
                reporterror("trigger price is missing")
                return None

        # if cover order or high leverage order
        if bookloss_price != 0.0:
            values["blprc"] = str(bookloss_price)

        # trailing price
        if trail_price != 0.0:
            values["trailprc"] = str(trail_price)

        # book profit of bracket order
        if bookprofit_price != 0.0:
            values["bpprc"] = str(bookprofit_price)

        payload = "jData=" + json.dumps(values) + f"&jKey={self.__susertoken}"

        reportmsg(payload)

        res = requests.post(url, data=payload)
        reportmsg(res.text)

        resDict = json.loads(res.text)

        return resDict

    def cancel_order(self, orderno: str):
        config = FA_NorenApi.__service_config

        url = f"{config['host']}{config['routes']['cancelorder']}"

        values = {
            "ordersource": "API",
            "uid": self.__username,
            "norenordno": str(orderno),
        }

        payload = "jData=" + json.dumps(values) + f"&jKey={self.__susertoken}"

        reportmsg(payload)

        res = requests.post(url, data=payload)

        resDict = json.loads(res.text)

        return resDict

    def exit_order(self, orderno: str, product_type: NorenTypes.ProductType):
        config = FA_NorenApi.__service_config

        url = f"{config['host']}{config['routes']['exitorder']}"

        values = {
            "ordersource": "API",
            "uid": self.__username,
            "norenordno": orderno,
            "prd": product_type,
        }

        payload = "jData=" + json.dumps(values) + f"&jKey={self.__susertoken}"

        reportmsg(payload)

        res = requests.post(url, data=payload)
        reportmsg(res.text)

        resDict = json.loads(res.text)

        return resDict

    def position_product_conversion(
        self,
        exchange: ExchangeType,
        tradingsymbol: str,
        quantity: int,
        new_product_type: NorenTypes.ProductType,
        previous_product_type: NorenTypes.ProductType,
        buy_or_sell: NorenTypes.TransactionTypeType,
        day_or_cf: str,
    ):
        """
        Coverts a day or carryforward position from one product to another.
        """
        config = FA_NorenApi.__service_config

        url = f"{config['host']}{config['routes']['product_conversion']}"

        values = {
            "ordersource": "API",
            "uid": self.__username,
            "actid": self.__accountid,
            "exch": exchange,
            "tsym": urllib.parse.quote_plus(tradingsymbol),
            "qty": str(quantity),
            "prd": new_product_type,
            "prevprd": previous_product_type,
            "trantype": buy_or_sell,
            "postype": day_or_cf,
        }

        payload = "jData=" + json.dumps(values) + f"&jKey={self.__susertoken}"

        reportmsg(payload)

        res = requests.post(url, data=payload)
        reportmsg(res.text)

        resDict = json.loads(res.text)

        return resDict

    def single_order_history(self, orderno: str) -> list[Any] | None:
        config = FA_NorenApi.__service_config

        url = f"{config['host']}{config['routes']['singleorderhistory']}"

        values = {
            "ordersource": "API",
            "uid": self.__username,
            "norenordno": orderno,
        }

        payload = "jData=" + json.dumps(values) + f"&jKey={self.__susertoken}"

        reportmsg(payload)

        res = requests.post(url, data=payload)
        reportmsg(res.text)

        resDict: Any | list[Any] = json.loads(res.text)
        if not isinstance(resDict, list):
            return None

        return resDict

    def get_order_book(self):
        config = FA_NorenApi.__service_config

        url = f"{config['host']}{config['routes']['orderbook']}"
        reportmsg(url)

        values = {
            "ordersource": "API",
            "uid": self.__username,
        }

        payload = "jData=" + json.dumps(values) + f"&jKey={self.__susertoken}"

        reportmsg(payload)

        res = requests.post(url, data=payload)
        reportmsg(res.text)

        resDict: Any | list[Any] = json.loads(res.text)

        if not isinstance(resDict, list):
            return None

        return resDict

    def get_trade_book(self):
        config = FA_NorenApi.__service_config

        url = f"{config['host']}{config['routes']['tradebook']}"
        reportmsg(url)

        values = {
            "ordersource": "API",
            "uid": self.__username,
            "actid": self.__accountid,
        }

        payload = "jData=" + json.dumps(values) + f"&jKey={self.__susertoken}"

        reportmsg(payload)

        res = requests.post(url, data=payload)
        reportmsg(res.text)

        resDict: Any | list[Any] = json.loads(res.text)

        if not isinstance(resDict, list):
            return None

        return resDict

    def searchscrip(self, exchange: ExchangeType, searchtext: str | None):
        config = FA_NorenApi.__service_config

        url = f"{config['host']}{config['routes']['searchscrip']}"
        reportmsg(url)

        if searchtext is None:
            reporterror("search text cannot be null")
            return None

        values = {
            "uid": self.__username,
            "exch": exchange,
            "stext": urllib.parse.quote_plus(searchtext),
        }

        payload = "jData=" + json.dumps(values) + f"&jKey={self.__susertoken}"

        reportmsg(payload)

        res = requests.post(url, data=payload)
        reportmsg(res.text)

        resDict = json.loads(res.text)

        return resDict

    def get_option_chain(
        self,
        exchange: ExchangeType,
        tradingsymbol: str,
        strikeprice: float,
        count: int = 2,
    ):
        config = FA_NorenApi.__service_config

        url = f"{config['host']}{config['routes']['optionchain']}"
        reportmsg(url)

        values = {
            "uid": self.__username,
            "exch": exchange,
            "tsym": urllib.parse.quote_plus(tradingsymbol),
            "strprc": str(strikeprice),
            "cnt": str(count),
        }

        payload = "jData=" + json.dumps(values) + f"&jKey={self.__susertoken}"

        reportmsg(payload)

        res = requests.post(url, data=payload)
        reportmsg(res.text)

        resDict = json.loads(res.text)

        return resDict

    def get_security_info(self, exchange: ExchangeType, token: int):
        config = FA_NorenApi.__service_config

        url = f"{config['host']}{config['routes']['scripinfo']}"
        reportmsg(url)

        values = {
            "uid": self.__username,
            "exch": exchange,
            "token": token,
        }

        payload = "jData=" + json.dumps(values) + f"&jKey={self.__susertoken}"

        reportmsg(payload)

        res = requests.post(url, data=payload)
        reportmsg(res.text)

        resDict = json.loads(res.text)

        return resDict

    def get_quotes(self, exchange: ExchangeType, token: str):
        config = FA_NorenApi.__service_config

        url = f"{config['host']}{config['routes']['getquotes']}"
        reportmsg(url)

        values = {
            "uid": self.__username,
            "exch": exchange,
            "token": token,
        }

        payload = "jData=" + json.dumps(values) + f"&jKey={self.__susertoken}"

        reportmsg(payload)

        res = requests.post(url, data=payload)
        reportmsg(res.text)

        resDict = json.loads(res.text)

        return resDict

    def get_time_price_series(
        self,
        exchange: ExchangeType,
        token: int,
        starttime: float | None = None,
        endtime: float | None = None,
        interval: str | None = None,
    ):
        """
        gets the chart data
        interval possible values 1, 3, 5 , 10, 15, 30, 60, 120, 240
        """
        config = FA_NorenApi.__service_config

        url = f"{config['host']}{config['routes']['TPSeries']}"
        reportmsg(url)

        if starttime is None:
            timestring = time.strftime("%d-%m-%Y") + " 00:00:00"
            timeobj = time.strptime(timestring, "%d-%m-%Y %H:%M:%S")
            starttime = time.mktime(timeobj)

        values = {
            "ordersource": "API",
            "uid": self.__username,
            "exch": exchange,
            "token": token,
            "st": str(starttime),
        }

        if endtime is not None:
            values["et"] = str(endtime)
        if interval is not None:
            values["intrv"] = str(interval)

        payload = "jData=" + json.dumps(values) + f"&jKey={self.__susertoken}"

        reportmsg(payload)

        res = requests.post(url, data=payload)
        reportmsg(res.text)

        resDict: Any | list[Any] = json.loads(res.text)

        if not isinstance(resDict, list):
            return None

        return resDict

    def get_daily_price_series(
        self,
        exchange: ExchangeType,
        tradingsymbol: str,
        startdate: float | None = None,
        enddate: float | None = None,
    ):
        config = FA_NorenApi.__service_config

        url = f"{config['host']}{config['routes']['get_daily_price_series']}"
        reportmsg(url)

        if startdate is None:
            week_ago = datetime.date.today() - datetime.timedelta(days=7)
            startdate = dt.combine(week_ago, dt.min.time()).timestamp()

        if enddate is None:
            enddate = dt.now().timestamp()

        values = {
            "uid": self.__username,
            "sym": "{0}:{1}".format(exchange, tradingsymbol),
            "from": str(startdate),
            "to": str(enddate),
        }

        payload = "jData=" + json.dumps(values) + f"&jKey={self.__susertoken}"
        reportmsg(payload)

        headers = {"Content-Type": "application/json; charset=utf-8"}
        res = requests.post(url, data=payload, headers=headers)
        reportmsg(str(res))

        if res.status_code != 200:
            return None

        if len(res.text) == 0:
            return None

        resDict: Any | list[Any] = json.loads(res.text)

        # error is a json with stat and msg wchih we printed earlier.
        if not isinstance(resDict, list):
            return None

        return resDict

    def get_holdings(self, product_type: str | None = None):
        config = FA_NorenApi.__service_config

        url = f"{config['host']}{config['routes']['holdings']}"
        reportmsg(url)

        if product_type is None:
            product_type = ProductType.Delivery

        values = {
            "uid": self.__username,
            "actid": self.__accountid,
            "prd": product_type,
        }

        payload = "jData=" + json.dumps(values) + f"&jKey={self.__susertoken}"

        reportmsg(payload)

        res = requests.post(url, data=payload)
        reportmsg(res.text)

        resDict: Any | list[Any] = json.loads(res.text)

        if not isinstance(resDict, list):
            return None

        return resDict

    def get_limits(
        self,
        product_type: str | None = None,
        segment: str | None = None,
        exchange: str | None = None,
    ):
        config = FA_NorenApi.__service_config

        url = f"{config['host']}{config['routes']['limits']}"
        reportmsg(url)

        values = {
            "uid": self.__username,
            "actid": self.__accountid,
        }

        if product_type is not None:
            values["prd"] = product_type

        if product_type is not None:
            values["seg"] = segment

        if exchange is not None:
            values["exch"] = exchange

        payload = "jData=" + json.dumps(values) + f"&jKey={self.__susertoken}"

        reportmsg(payload)

        res = requests.post(url, data=payload)
        reportmsg(res.text)

        resDict = json.loads(res.text)

        return resDict

    def get_positions(self):
        config = FA_NorenApi.__service_config

        url = f"{config['host']}{config['routes']['positions']}"
        reportmsg(url)

        values = {
            "uid": self.__username,
            "actid": self.__accountid,
        }

        payload = "jData=" + json.dumps(values) + f"&jKey={self.__susertoken}"

        reportmsg(payload)

        res = requests.post(url, data=payload)
        reportmsg(res.text)

        resDict: Any | list[Any] = json.loads(res.text)

        if not isinstance(resDict, list):
            return None

        return resDict

    def span_calculator(self, actid: str, positions: list[Any]):
        config = FA_NorenApi.__service_config
        url = f"{config['host']}{config['routes']['span_calculator']}"
        reportmsg(url)

        senddata = {
            "actid": self.__accountid,
            "pos": positions,
        }

        payload = (
            "jData="
            + json.dumps(senddata, default=lambda o: o.encode())
            + f"&jKey={self.__susertoken}"
        )
        reportmsg(payload)

        res = requests.post(url, data=payload)
        reportmsg(res.text)

        resDict = json.loads(res.text)

        return resDict

    def option_greek(
        self,
        expiredate: float,
        StrikePrice: float,
        SpotPrice: float,
        InterestRate: float,
        Volatility: float,
        OptionType: str,
    ):
        config = FA_NorenApi.__service_config

        url = f"{config['host']}{config['routes']['option_greek']}"
        reportmsg(url)

        values = {
            "source": "API",
            "actid": self.__accountid,
            "exd": expiredate,
            "strprc": StrikePrice,
            "sptprc": SpotPrice,
            "int_rate": InterestRate,
            "volatility": Volatility,
            "optt": OptionType,
        }

        payload = "jData=" + json.dumps(values) + f"&jKey={self.__susertoken}"

        reportmsg(payload)

        res = requests.post(url, data=payload)
        reportmsg(res.text)

        resDict = json.loads(res.text)

        return resDict
