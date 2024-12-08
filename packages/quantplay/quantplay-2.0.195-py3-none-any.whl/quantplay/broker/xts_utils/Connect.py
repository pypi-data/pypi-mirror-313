"""
Connect.py

API wrapper for XTS Connect REST APIs.

"""

import json
import logging
import os
from typing import Any, Literal

import requests
import requests.adapters
import urllib3  # type:ignore
from six.moves.urllib.parse import urljoin  # type:ignore

from quantplay.broker.xts_utils import Exception as ex
from quantplay.model.generics import (
    XTSTypes,
)

log = logging.getLogger(__name__)

# Disable requests SSL warning
urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)


class XTSCommon:
    """
    Base variables class
    """

    def __init__(
        self,
        token: str | None = None,
        userID: str | None = None,
        isInvestorClient: bool | None = None,
    ):
        """Initialize the common variables."""
        self.token = token
        self.userID = userID
        self.isInvestorClient = isInvestorClient


class XTSConnect(XTSCommon):
    """
    The XTS Connect API wrapper class.
    In production, you may initialise a single instance of this class per `api_key`.
    """

    """Get the configurations from config.ini"""

    root_folder = os.path.dirname(os.path.abspath(__file__))
    ini_file = os.path.join(root_folder, "config.ini")

    # Default root API endpoint. It's possible to
    # override this by passing the `root` parameter during initialisation.
    _default_root_uri = "https://developers.symphonyfintech.in"
    _default_login_uri = _default_root_uri + "/user/session"
    _default_timeout = 7  # In seconds

    # SSL Flag
    _ssl_flag = True

    # Constants
    # Products
    PRODUCT_MIS = "MIS"
    PRODUCT_NRML = "NRML"

    # Order types
    ORDER_TYPE_MARKET = "MARKET"
    ORDER_TYPE_LIMIT = "LIMIT"
    ORDER_TYPE_STOPMARKET = "STOPMARKET"
    ORDER_TYPE_STOPLIMIT = "STOPLIMIT"

    # Transaction type
    TRANSACTION_TYPE_BUY = "BUY"
    TRANSACTION_TYPE_SELL = "SELL"

    # Squareoff mode
    SQUAREOFF_DAYWISE = "DayWise"
    SQUAREOFF_NETWISE = "Netwise"

    # Squareoff position quantity types
    SQUAREOFFQUANTITY_EXACTQUANTITY = "ExactQty"
    SQUAREOFFQUANTITY_PERCENTAGE = "Percentage"

    # Validity
    VALIDITY_DAY = "DAY"

    # Exchange Segments
    EXCHANGE_NSECM = "NSECM"
    EXCHANGE_NSEFO = "NSEFO"
    EXCHANGE_NSECD = "NSECD"
    EXCHANGE_MCXFO = "MCXFO"
    EXCHANGE_BSECM = "BSECM"

    # URIs to various calls
    _routes: dict[str, str] = {
        # Interactive API endpoints
        "interactive.prefix": "interactive",
        "user.login": "/interactive/user/session",
        "user.logout": "/interactive/user/session",
        "user.profile": "/interactive/user/profile",
        "user.balance": "/interactive/user/balance",
        "orders": "/interactive/orders",
        "trades": "/interactive/orders/trades",
        "order.status": "/interactive/orders",
        "order.place": "/interactive/orders",
        "bracketorder.place": "/interactive/orders/bracket",
        "bracketorder.modify": "/interactive/orders/bracket",
        "bracketorder.cancel": "/interactive/orders/bracket",
        "order.place.cover": "/interactive/orders/cover",
        "order.exit.cover": "/interactive/orders/cover",
        "order.modify": "/interactive/orders",
        "order.cancel": "/interactive/orders",
        "order.cancelall": "/interactive/orders/cancelall",
        "order.history": "/interactive/orders",
        "portfolio.positions": "/interactive/portfolio/positions",
        "portfolio.holdings": "/interactive/portfolio/holdings",
        "portfolio.positions.convert": "/interactive/portfolio/positions/convert",
        "portfolio.squareoff": "/interactive/portfolio/squareoff",
        "portfolio.dealerpositions": "interactive/portfolio/dealerpositions",
        "order.dealer.status": "/interactive/orders/dealerorderbook",
        "dealer.trades": "/interactive/orders/dealertradebook",
        # Market API endpoints
        "marketdata.prefix": "apimarketdata",
        "market.login": "/apimarketdata/auth/login",
        "market.logout": "/apimarketdata/auth/logout",
        "market.config": "/apimarketdata/config/clientConfig",
        "market.instruments.master": "/apimarketdata/instruments/master",
        "market.instruments.subscription": "/apimarketdata/instruments/subscription",
        "market.instruments.unsubscription": "/apimarketdata/instruments/subscription",
        "market.instruments.ohlc": "/apimarketdata/instruments/ohlc",
        "market.instruments.indexlist": "/apimarketdata/instruments/indexlist",
        "market.instruments.quotes": "/apimarketdata/instruments/quotes",
        "market.search.instrumentsbyid": "/apimarketdata/search/instrumentsbyid",
        "market.search.instrumentsbystring": "/apimarketdata/search/instruments",
        "market.instruments.instrument.series": "/apimarketdata/instruments/instrument/series",
        "market.instruments.instrument.equitysymbol": "/apimarketdata/instruments/instrument/symbol",
        "market.instruments.instrument.futuresymbol": "/apimarketdata/instruments/instrument/futureSymbol",
        "market.instruments.instrument.optionsymbol": "/apimarketdata/instruments/instrument/optionsymbol",
        "market.instruments.instrument.optiontype": "/apimarketdata/instruments/instrument/optionType",
        "market.instruments.instrument.expirydate": "/apimarketdata/instruments/instrument/expiryDate",
    }

    def __init__(
        self,
        apiKey: str,
        secretKey: str,
        root: str,
        source: str = "WEBAPI",
        debug: bool = False,
        timeout: float | None = None,
        pool: dict[str, Any] | None = None,
        disable_ssl: bool = _ssl_flag,
    ):
        """
        Initialise a new XTS Connect client instance.

        - `api_key` is the key issued to you
        - `token` is the token obtained after the login flow. Pre-login, this will default to None,
        but once you have obtained it, you should persist it in a database or session to pass
        to the XTS Connect class initialisation for subsequent requests.
        - `root` is the API end point root. Unless you explicitly
        want to send API requests to a non-default endpoint, this
        can be ignored.
        - `debug`, if set to True, will serialise and print requests
        and responses to stdout.
        - `timeout` is the time (seconds) for which the API client will wait for
        a request to complete before it fails. Defaults to 7 seconds
        - `pool` is manages request pools. It takes a dict of params accepted by HTTPAdapter
        - `disable_ssl` disables the SSL verification while making a request.
        If set requests won't throw SSLError if its set to custom `root` url without SSL.
        """
        self.debug = debug
        self.apiKey = apiKey
        self.secretKey = secretKey
        self.source = source
        self.disable_ssl = disable_ssl
        self.root = root
        self.timeout = timeout or self._default_timeout

        super().__init__()

        # Create requests session only if pool exists. Reuse session
        # for every request. Otherwise create session for each request
        if pool:
            self.reqsession = requests.Session()
            reqadapter = requests.adapters.HTTPAdapter(**pool)
            self.reqsession.mount("https://", reqadapter)
        else:
            self.reqsession = requests

    def _set_common_variables(
        self, access_token: str, userID: str, isInvestorClient: bool
    ):
        """Set the `access_token` received after a successful authentication."""
        super().__init__(access_token, userID, isInvestorClient)

    def _login_url(self):
        """Get the remote login url to which a user should be redirected to initiate the login flow."""
        return self._default_login_uri

    def interactive_login(self):
        """Send the login url to which a user should receive the token."""
        params = {
            "appKey": self.apiKey,
            "secretKey": self.secretKey,
            "source": self.source,
        }
        response = self._post("user.login", params)

        if "token" in response["result"]:
            self._set_common_variables(
                response["result"]["token"],
                response["result"]["userID"],
                response["result"]["isInvestorClient"],
            )
        return response

    def get_order_book(self, clientID: str | None = None):
        """Request Order book gives states of all the orders placed by an user"""
        params: dict[str, Any] = {}

        if not self.isInvestorClient:
            params["clientID"] = clientID

        response = self._get("order.status", params)
        return response

    def place_order(
        self,
        exchangeSegment: XTSTypes.ExchangeType,
        exchangeInstrumentID: int | str,
        productType: XTSTypes.ProductType,
        orderType: XTSTypes.OrderType,
        orderSide: XTSTypes.OrderSide,
        timeInForce: XTSTypes.DayOrNetType,
        disclosedQuantity: int,
        orderQuantity: int,
        limitPrice: float,
        stopPrice: float,
        orderUniqueIdentifier: str,
        clientID: str | None = None,
    ):
        """To place an order"""
        params: dict[str, Any] = {
            "exchangeSegment": exchangeSegment,
            "exchangeInstrumentID": exchangeInstrumentID,
            "productType": productType,
            "orderType": orderType,
            "orderSide": orderSide,
            "timeInForce": timeInForce,
            "disclosedQuantity": disclosedQuantity,
            "orderQuantity": orderQuantity,
            "limitPrice": limitPrice,
            "stopPrice": stopPrice,
            "orderUniqueIdentifier": orderUniqueIdentifier,
        }

        if not self.isInvestorClient:
            params["clientID"] = clientID

        response = self._post("order.place", json.dumps(params))
        return response

    def get_dealer_orderbook(self, clientID: str | None = None):
        """Request Order book gives states of all the orders placed by an user"""
        params: dict[str, Any] = {}
        if not self.isInvestorClient:
            params["clientID"] = clientID

        response = self._get("order.dealer.status", params)
        return response

    def get_dealer_tradebook(self, clientID: str | None = None):
        """Trade book returns a list of all trades executed on a particular day , that were placed by the user . The
        trade book will display all filled and partially filled orders."""
        params: dict[str, Any] = {}
        if not self.isInvestorClient:
            params["clientID"] = clientID
        response = self._get("dealer.trades", params)
        return response

    def get_dealerposition_netwise(self, clientID: str | None = None):
        """The positions API positions by net. Net is the actual, current net position portfolio."""
        params: dict[str, Any] = {"dayOrNet": "NetWise"}
        if not self.isInvestorClient:
            params["clientID"] = clientID
        response = self._get("portfolio.dealerpositions", params)
        return response

    def get_dealerposition_daywise(self, clientID: str | None = None):
        """The positions API returns positions by day, which is a snapshot of the buying and selling activity for
        that particular day."""
        params: dict[str, Any] = {"dayOrNet": "DayWise"}
        if not self.isInvestorClient:
            params["clientID"] = clientID

        response = self._get("portfolio.dealerpositions", params)

        return response

    def place_bracketorder(
        self,
        exchangeSegment: XTSTypes.ExchangeType,
        exchangeInstrumentID: int,
        orderType: XTSTypes.OrderType,
        orderSide: XTSTypes.OrderSide,
        disclosedQuantity: int,
        orderQuantity: int,
        limitPrice: float,
        squarOff: int,
        stopLossPrice: float,
        trailingStoploss: float,
        isProOrder: bool,
        orderUniqueIdentifier: str,
    ):
        """To place a bracketorder"""
        params: dict[str, Any] = {
            "exchangeSegment": exchangeSegment,
            "exchangeInstrumentID": exchangeInstrumentID,
            "orderType": orderType,
            "orderSide": orderSide,
            "disclosedQuantity": disclosedQuantity,
            "orderQuantity": orderQuantity,
            "limitPrice": limitPrice,
            "squarOff": squarOff,
            "stopLossPrice": stopLossPrice,
            "trailingStoploss": trailingStoploss,
            "isProOrder": isProOrder,
            "orderUniqueIdentifier": orderUniqueIdentifier,
        }
        response = self._post("bracketorder.place", json.dumps(params))
        return response

    def get_profile(self, clientID: str | None = None):
        """Using session token user can access his profile stored with the broker, it's possible to retrieve it any
        point of time with the http: //ip:port/interactive/user/profile API."""
        params: dict[str, Any] = {}
        if not self.isInvestorClient:
            params["clientID"] = clientID

        response = self._get("user.profile", params)
        return response

    def get_balance(self, clientID: str | None = None):
        """Get Balance API call grouped under this category information related to limits on equities, derivative,
        upfront margin, available exposure and other RMS related balances available to the user.
        """
        params: dict[str, Any] = {}
        params["clientID"] = clientID
        response = self._get("user.balance", params)
        return response

    def modify_order(
        self,
        appOrderID: int,
        modifiedProductType: XTSTypes.ProductType,
        modifiedOrderType: XTSTypes.OrderType,
        modifiedOrderQuantity: int,
        modifiedDisclosedQuantity: int,
        modifiedLimitPrice: float,
        modifiedStopPrice: float,
        modifiedTimeInForce: XTSTypes.DayOrNetType,
        orderUniqueIdentifier: str,
        clientID: str | None = None,
    ):
        """The facility to modify your open orders by allowing you to change limit order to market or vice versa,
        change Price or Quantity of the limit open order, change disclosed quantity or stop-loss of any
        open stop loss order."""
        appOrderID = int(appOrderID)
        params: dict[str, Any] = {
            "appOrderID": appOrderID,
            "modifiedProductType": modifiedProductType,
            "modifiedOrderType": modifiedOrderType,
            "modifiedOrderQuantity": modifiedOrderQuantity,
            "modifiedDisclosedQuantity": modifiedDisclosedQuantity,
            "modifiedLimitPrice": modifiedLimitPrice,
            "modifiedStopPrice": modifiedStopPrice,
            "modifiedTimeInForce": modifiedTimeInForce,
            "orderUniqueIdentifier": orderUniqueIdentifier,
        }

        if not self.isInvestorClient:
            params["clientID"] = clientID

        response = self._put("order.modify", json.dumps(params))
        return response

    def get_trade(self, clientID: str | None = None):
        """Trade book returns a list of all trades executed on a particular day , that were placed by the user . The
        trade book will display all filled and partially filled orders."""
        params: dict[str, Any] = {}

        if not self.isInvestorClient:
            params["clientID"] = clientID
        response = self._get("trades", params)
        return response

    def get_holding(self, clientID: str | None = None):
        """Holdings API call enable users to check their long term holdings with the broker."""
        params: dict[str, Any] = {}
        if not self.isInvestorClient:
            params["clientID"] = clientID

        response = self._get("portfolio.holdings", params)
        return response

    def get_position_daywise(self, clientID: str | None = None):
        """The positions API returns positions by day, which is a snapshot of the buying and selling activity for
        that particular day."""
        params: dict[str, Any] = {"dayOrNet": "DayWise"}

        if not self.isInvestorClient:
            params["clientID"] = clientID

        response = self._get("portfolio.positions", params)
        return response

    def get_position_netwise(self, clientID: str | None = None):
        """The positions API positions by net. Net is the actual, current net position portfolio."""
        params: dict[str, Any] = {"dayOrNet": "NetWise"}

        if not self.isInvestorClient:
            params["clientID"] = clientID

        response = self._get("portfolio.positions", params)
        return response

    def convert_position(
        self,
        exchangeSegment: XTSTypes.ExchangeType,
        exchangeInstrumentID: int,
        targetQty: int,
        isDayWise: bool,
        oldProductType: XTSTypes.ProductType,
        newProductType: XTSTypes.ProductType,
        clientID: str | None = None,
    ):
        """Convert position API, enable users to convert their open positions from NRML intra-day to Short term MIS or
        vice versa, provided that there is sufficient margin or funds in the account to effect such conversion
        """
        params: dict[str, Any] = {
            "exchangeSegment": exchangeSegment,
            "exchangeInstrumentID": exchangeInstrumentID,
            "targetQty": targetQty,
            "isDayWise": isDayWise,
            "oldProductType": oldProductType,
            "newProductType": newProductType,
        }
        if not self.isInvestorClient:
            params["clientID"] = clientID
        response = self._put("portfolio.positions.convert", json.dumps(params))
        return response

    def cancel_order(
        self, appOrderID: int, orderUniqueIdentifier: str, clientID: str | None = None
    ):
        """This API can be called to cancel any open order of the user by providing correct appOrderID matching with
        the chosen open order to cancel."""
        params: dict[str, Any] = {
            "appOrderID": int(appOrderID),
            "orderUniqueIdentifier": orderUniqueIdentifier,
        }
        if not self.isInvestorClient:
            params["clientID"] = clientID
        response = self._delete("order.cancel", params)
        return response

    def cancelall_order(
        self, exchangeSegment: XTSTypes.ExchangeSegmentType, exchangeInstrumentID: int
    ):
        """This API can be called to cancel all open order of the user by providing exchange segment and exchange instrument ID"""
        params: dict[str, Any] = {
            "exchangeSegment": exchangeSegment,
            "exchangeInstrumentID": exchangeInstrumentID,
        }
        if not self.isInvestorClient:
            params["clientID"] = self.userID
        response = self._post("order.cancelall", json.dumps(params))
        return response

    def place_cover_order(
        self,
        exchangeSegment: XTSTypes.ExchangeType,
        exchangeInstrumentID: int,
        orderSide: XTSTypes.OrderSide,
        orderType: XTSTypes.OrderType,
        orderQuantity: int,
        disclosedQuantity: int,
        limitPrice: float,
        stopPrice: float,
        orderUniqueIdentifier: str,
        clientID: str | None = None,
    ):
        """A Cover Order is an advance intraday order that is accompanied by a compulsory Stop Loss Order. This helps
        users to minimize their losses by safeguarding themselves from unexpected market movements. A Cover Order
        offers high leverage and is available in Equity Cash, Equity F&O, Commodity F&O and Currency F&O segments. It
        has 2 orders embedded in itself, they are Limit/Market Order Stop Loss Order"""
        params: dict[str, Any] = {
            "exchangeSegment": exchangeSegment,
            "exchangeInstrumentID": exchangeInstrumentID,
            "orderSide": orderSide,
            "orderType": orderType,
            "orderQuantity": orderQuantity,
            "disclosedQuantity": disclosedQuantity,
            "limitPrice": limitPrice,
            "stopPrice": stopPrice,
            "orderUniqueIdentifier": orderUniqueIdentifier,
        }
        if not self.isInvestorClient:
            params["clientID"] = clientID
        response = self._post("order.place.cover", json.dumps(params))
        return response

    def exit_cover_order(self, appOrderID: int, clientID: str | None = None):
        """Exit Cover API is a functionality to enable user to easily exit an open stoploss order by converting it
        into Exit order."""
        params: dict[str, Any] = {"appOrderID": appOrderID}
        if not self.isInvestorClient:
            params["clientID"] = clientID
        response = self._put("order.exit.cover", json.dumps(params))
        return response

    def get_order_history(self, appOrderID: int, clientID: str | None = None):
        """Order history will provide particular order trail chain. This indicate the particular order & its state
        changes. i.e.Pending New to New, New to PartiallyFilled, PartiallyFilled, PartiallyFilled & PartiallyFilled
        to Filled etc"""
        params: dict[str, Any] = {"appOrderID": appOrderID}
        if not self.isInvestorClient:
            params["clientID"] = clientID
        response = self._get("order.history", params)
        return response

    def interactive_logout(self, clientID: str | None = None):
        """This call invalidates the session token and destroys the API session. After this, the user should go
        through login flow again and extract session token from login response before further activities.
        """
        params: dict[str, Any] = {}
        if not self.isInvestorClient:
            params["clientID"] = clientID
        response = self._delete("user.logout", params)
        return response

    ########################################################################################################
    # Market data API
    ########################################################################################################

    def marketdata_login(self):
        params = {
            "appKey": self.apiKey,
            "secretKey": self.secretKey,
            "source": self.source,
        }
        response = self._post("market.login", params)
        if "token" in response["result"]:
            self._set_common_variables(
                response["result"]["token"], response["result"]["userID"], False
            )
        return response

    def get_config(self):
        params: dict[str, Any] = {}
        response = self._get("market.config", params)
        return response

    def get_quote(
        self,
        Instruments: list[XTSTypes.InstrumentType],
        xtsMessageCode: XTSTypes.XTSMessageCodeType,
        publishFormat: XTSTypes.PublishFormatType,
    ):
        params: dict[str, Any] = {
            "instruments": Instruments,
            "xtsMessageCode": xtsMessageCode,
            "publishFormat": publishFormat,
        }
        response = self._post("market.instruments.quotes", json.dumps(params))
        return response

    def send_subscription(
        self,
        Instruments: list[XTSTypes.InstrumentType],
        xtsMessageCode: XTSTypes.XTSMessageCodeType,
    ):
        params: dict[str, Any] = {
            "instruments": Instruments,
            "xtsMessageCode": xtsMessageCode,
        }
        response = self._post("market.instruments.subscription", json.dumps(params))
        return response

    def send_unsubscription(
        self,
        Instruments: list[XTSTypes.InstrumentType],
        xtsMessageCode: XTSTypes.XTSMessageCodeType,
    ):
        params: dict[str, Any] = {
            "instruments": Instruments,
            "xtsMessageCode": xtsMessageCode,
        }
        response = self._put("market.instruments.unsubscription", json.dumps(params))
        return response

    def get_master(self, exchangeSegmentList: list[XTSTypes.ExchangeType]):
        params: dict[str, Any] = {"exchangeSegmentList": exchangeSegmentList}
        response = self._post("market.instruments.master", json.dumps(params))
        return response

    def get_ohlc(
        self,
        exchangeSegment: XTSTypes.ExchangeSegmentType,
        exchangeInstrumentID: str | int,
        startTime: str,
        endTime: str,
        compressionValue: Literal[1, 60, 120, 180, 300, 600, 900, 1800, 3600],
    ):
        params: dict[str, Any] = {
            "exchangeSegment": exchangeSegment,
            "exchangeInstrumentID": exchangeInstrumentID,
            "startTime": startTime,
            "endTime": endTime,
            "compressionValue": compressionValue,
        }
        response = self._get("market.instruments.ohlc", params)
        return response

    def get_series(self, exchangeSegment: XTSTypes.ExchangeSegmentType):
        params: dict[str, Any] = {"exchangeSegment": exchangeSegment}
        response = self._get("market.instruments.instrument.series", params)
        return response

    def get_equity_symbol(
        self,
        exchangeSegment: XTSTypes.ExchangeSegmentType,
        series: XTSTypes.SeriesType,
        symbol: str,
    ):
        params: dict[str, Any] = {
            "exchangeSegment": exchangeSegment,
            "series": series,
            "symbol": symbol,
        }
        response = self._get("market.instruments.instrument.equitysymbol", params)
        return response

    def get_expiry_date(
        self,
        exchangeSegment: XTSTypes.ExchangeSegmentType,
        series: XTSTypes.SeriesType,
        symbol: str,
    ):
        params: dict[str, Any] = {
            "exchangeSegment": exchangeSegment,
            "series": series,
            "symbol": symbol,
        }
        response = self._get("market.instruments.instrument.expirydate", params)
        return response

    def get_future_symbol(
        self,
        exchangeSegment: XTSTypes.ExchangeSegmentType,
        series: XTSTypes.SeriesType,
        symbol: str,
        expiryDate: str,
    ):
        params: dict[str, Any] = {
            "exchangeSegment": exchangeSegment,
            "series": series,
            "symbol": symbol,
            "expiryDate": expiryDate,
        }
        response = self._get("market.instruments.instrument.futuresymbol", params)
        return response

    def get_option_symbol(
        self,
        exchangeSegment: XTSTypes.ExchangeSegmentType,
        series: XTSTypes.SeriesType,
        symbol: str,
        expiryDate: str,
        optionType: Literal["CE", "PE"],
        strikePrice: int,
    ):
        params: dict[str, Any] = {
            "exchangeSegment": exchangeSegment,
            "series": series,
            "symbol": symbol,
            "expiryDate": expiryDate,
            "optionType": optionType,
            "strikePrice": strikePrice,
        }
        response = self._get("market.instruments.instrument.optionsymbol", params)
        return response

    def get_option_type(
        self,
        exchangeSegment: XTSTypes.ExchangeSegmentType,
        series: XTSTypes.SeriesType,
        symbol: str,
        expiryDate: str,
    ):
        params: dict[str, Any] = {
            "exchangeSegment": exchangeSegment,
            "series": series,
            "symbol": symbol,
            "expiryDate": expiryDate,
        }
        response = self._get("market.instruments.instrument.optiontype", params)
        return response

    def get_index_list(self, exchangeSegment: XTSTypes.ExchangeSegmentType):
        params: dict[str, Any] = {"exchangeSegment": exchangeSegment}
        response = self._get("market.instruments.indexlist", params)
        return response

    def search_by_instrumentid(self, Instruments: list[XTSTypes.InstrumentType]):
        params: dict[str, Any] = {"source": self.source, "instruments": Instruments}
        response = self._post("market.search.instrumentsbyid", json.dumps(params))
        return response

    def search_by_scriptname(self, searchString: str):
        params = {"searchString": searchString}
        response = self._get("market.search.instrumentsbystring", params)
        return response

    def marketdata_logout(self):
        params: dict[str, Any] = {}
        response = self._delete("market.logout", params)
        return response

    ########################################################################################################
    # Common Methods
    ########################################################################################################

    def _get(self, route: str, params: dict[str, Any] | None = None):
        """Alias for sending a GET request."""
        return self._request(route, "GET", params)

    def _post(self, route: str, params: dict[str, Any] | str | None = None):
        """Alias for sending a POST request."""
        return self._request(route, "POST", params)

    def _put(self, route: str, params: dict[str, Any] | str | None = None):
        """Alias for sending a PUT request."""
        return self._request(route, "PUT", params)

    def _delete(self, route: str, params: dict[str, Any] | None = None):
        """Alias for sending a DELETE request."""
        return self._request(route, "DELETE", params)

    def _request(
        self,
        route: str,
        method: Literal["GET", "POST", "PUT", "DELETE"],
        parameters: dict[str, Any] | str | None = None,
    ):
        """Make an HTTP request."""
        params = parameters if parameters else {}

        # Form a restful URL
        uri = self._routes[route].format(params)
        url = urljoin(self.root, uri)
        headers: dict[str, str] = {}

        if self.token:
            # set authorization header
            headers.update(
                {"Content-Type": "application/json", "Authorization": self.token}
            )

        try:
            r = self.reqsession.request(
                method,
                url,
                data=params if method in ["POST", "PUT"] else None,
                params=params if method in ["GET", "DELETE"] else None,
                headers=headers,
                verify=not self.disable_ssl,
            )

        except Exception as e:
            raise e

        if self.debug:
            log.debug(
                "Response: {code} {content}".format(code=r.status_code, content=r.content)
            )

        # Validate the content type.
        if "json" in r.headers["content-type"]:
            try:
                data = json.loads(r.content.decode("utf8"))
            except ValueError:
                raise ex.XTSDataException(
                    "Couldn't parse the JSON response received from the server: {content}".format(
                        content=r.content
                    )
                )

            # api error
            if data.get("type"):
                if (
                    r.status_code == 400
                    and data["type"] == "error"
                    and data["description"] == "Invalid Token"
                ):
                    raise ex.XTSTokenException(data["description"])

                if (
                    r.status_code == 400
                    and data["type"] == "error"
                    and data["description"] == "Bad Request"
                ):
                    message = (
                        "Description: "
                        + data["description"]
                        + " errors: "
                        + str(data["result"]["errors"])
                    )
                    raise ex.XTSInputException(str(message))

            return data
        else:
            raise ex.XTSDataException(
                "Unknown Content-Type ({content_type}) with response: ({content})".format(
                    content_type=r.headers["content-type"], content=r.content
                )
            )
