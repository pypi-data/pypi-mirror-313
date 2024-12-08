import codecs
import json
import pickle
import traceback
from datetime import datetime
from queue import Queue
from typing import Any

import pandas as pd
import polars as pl
from retrying import retry  # type: ignore

from quantplay.broker.generics.broker import Broker
from quantplay.broker.xts_utils_v2.ConnectV2 import XTSConnectV2
from quantplay.broker.xts_utils.Connect import XTSConnect
from quantplay.broker.xts_utils.Exception import (
    XTSDataException,
    XTSGeneralException,
    XTSNetworkException,
    XTSTokenException,
)
from quantplay.broker.xts_utils.InteractiveSocketClient import OrderSocket_io
from quantplay.exception.exceptions import (
    BrokerException,
    InvalidArgumentException,
    RetryableException,
    TokenException,
    retry_exception,
)
from quantplay.model.broker import (
    ExchangeType,
    MarginsResponse,
    ModifyOrderRequest,
    UserBrokerProfileResponse,
)
from quantplay.model.generics import OrderTypeType, ProductType, TransactionType, XTSTypes
from quantplay.model.order_event import OrderUpdateEvent
from quantplay.utils.constant import Constants, OrderType
from quantplay.utils.pickle_utils import InstrumentData, PickleUtils


class XTS(Broker):
    source = "WebAPI"

    def __init__(
        self,
        root_url: str,
        api_key: str | None = None,
        api_secret: str | None = None,
        md_api_key: str | None = None,
        md_api_secret: str | None = None,
        order_updates: Queue[OrderUpdateEvent] | None = None,
        wrapper: str | None = None,
        md_wrapper: str | None = None,
        ClientID: str | None = None,
        is_dealer: bool = False,
        load_instrument: bool = True,
    ) -> None:
        super().__init__()
        self.order_updates: Queue[OrderUpdateEvent] | None = order_updates
        self.root_url = root_url
        self.is_dealer = is_dealer

        try:
            if wrapper and md_wrapper and ClientID:
                self.set_wrapper(wrapper, md_wrapper)
                self.ClientID = ClientID

            elif (
                api_key is not None
                and api_secret is not None
                and md_api_key is not None
                and md_api_secret
            ):
                self.login(api_key, api_secret, md_api_key, md_api_secret)

            else:
                raise InvalidArgumentException("Missing Arguments")

        except Exception as e:
            traceback.print_exc()
            raise e

        if load_instrument:
            self.load_instrument()

    def set_wrapper(self, serialized_wrapper: str, serialized_md_wrapper: str):
        self.wrapper: XTSConnect | XTSConnectV2 = pickle.loads(
            codecs.decode(serialized_wrapper.encode(), "base64")
        )

        self.root_url = self.wrapper.root

        self.md_wrapper: XTSConnect | XTSConnectV2 = pickle.loads(
            codecs.decode(serialized_md_wrapper.encode(), "base64")
        )

    def load_instrument(self, file_name: str | None = None) -> None:
        try:
            self.symbol_data = InstrumentData.get_instance().load_data("xts_instruments")  # type: ignore
            Constants.logger.info("[LOADING_INSTRUMENTS] loading data from cache")

        except Exception:
            instruments = pd.read_csv(  # type: ignore
                "https://quantplay-public-data.s3.ap-south-1.amazonaws.com/symbol_data/instruments.csv"
            )
            instruments = instruments.to_dict("records")  # type: ignore
            self.symbol_data = {}

            for instrument in instruments:
                exchange = instrument["exchange"]
                tradingsymbol = instrument["tradingsymbol"]
                # NIFTY 08JUN2023 PE 17850 <- NIFTY2360817850PE
                # 2023-06-27 -> 08JUN2023
                # For FUTURES : EURINR23AUGFUT -> EURINR 23AUG2023 FUT

                ins_type = instrument["instrument_type"]
                name = instrument["name"]

                if ins_type in ["CE", "PE"]:
                    expiry = datetime.strftime(
                        datetime.strptime(str(instrument["expiry"]), "%Y-%m-%d"),
                        "%d%b%Y",
                    ).upper()
                    strike = str(instrument["strike"]).rstrip("0")

                    if strike[-1] == ".":
                        strike = strike[:-1]

                    instrument["broker_symbol"] = f"{name} {expiry} {ins_type} {strike}"

                elif ins_type == "FUT":
                    expiry = datetime.strftime(
                        datetime.strptime(str(instrument["expiry"]), "%Y-%m-%d"),
                        "%d%b%Y",
                    ).upper()
                    instrument["broker_symbol"] = f"{name} {expiry}"

                else:
                    instrument["broker_symbol"] = tradingsymbol

                self.symbol_data[f"{exchange}:{tradingsymbol}"] = instrument  # type: ignore

            PickleUtils.save_data(self.symbol_data, "xts_instruments")
            Constants.logger.info("[LOADING_INSTRUMENTS] loading data from server")

        self.initialize_broker_symbol_map()

    def login(self, api_key: str, api_secret: str, md_api_key: str, md_api_secret: str):
        try:
            self.wrapper = XTSConnect(
                apiKey=api_key,
                secretKey=api_secret,
                root=self.root_url,
            )
            xt_core_response = self.invoke_xts_api(self.wrapper.interactive_login)

            self.md_wrapper = XTSConnect(
                apiKey=md_api_key,
                secretKey=md_api_secret,
                root=self.root_url,
            )
            md_response = self.invoke_xts_api(self.md_wrapper.marketdata_login)

            if "type" not in xt_core_response or xt_core_response["type"] != "success":
                print(f"api login response {xt_core_response}")
                raise TokenException("Api key credentials are incorrect")

            if "type" not in md_response or md_response["type"] != "success":
                print(f"market data login response {md_response}")
                raise TokenException("Market data api credentials are invalid")

            self.ClientID = xt_core_response["result"]["userID"]

        except TokenException:
            raise

        except Exception:
            raise InvalidArgumentException("Invalid api key/secret")

    def margins(self) -> MarginsResponse:
        api_response = self.invoke_xts_api(
            self.wrapper.get_balance, clientID=self.ClientID
        )

        if (
            api_response["code"] == "e-user-0001"
            and api_response["description"] == "No RMS Limit assign to user"
        ):
            raise BrokerException("Fetch Margins Failed: No RMS Limit assign to user")

        if not api_response:
            return {
                "margin_used": 0,
                "margin_available": 0,
                "total_balance": 0,
                "cash": 0,
            }

        api_response = api_response["result"]["BalanceList"][0]["limitObject"]
        margin_used = api_response["RMSSubLimits"]["marginUtilized"]
        margin_available = api_response["RMSSubLimits"]["netMarginAvailable"]

        return {
            "margin_used": float(margin_used),
            "margin_available": float(margin_available),
            "total_balance": float(margin_used) + float(margin_available),
            "cash": 0,
        }

    def profile(self) -> UserBrokerProfileResponse:
        if self.broker_name == "Jainam":
            if self.user_id is None:
                raise InvalidArgumentException(
                    "UserId is not set, please contact support team"
                )
            response: UserBrokerProfileResponse = {"user_id": self.user_id}
            return response
        api_response = self.invoke_xts_api(
            self.wrapper.get_profile, clientID=self.ClientID
        )
        api_response = api_response["result"]

        response: UserBrokerProfileResponse = {
            "user_id": api_response["ClientId"],
            "full_name": api_response["ClientName"],
            "segments": api_response["ClientExchangeDetailsList"],
        }

        return response

    def orders(self, tag: str | None = None, add_ltp: bool = True) -> pl.DataFrame:
        api_response = self.invoke_xts_api(
            (
                self.wrapper.get_dealer_orderbook
                if self.is_dealer
                else self.wrapper.get_order_book
            ),
            clientID=None if self.is_dealer else self.ClientID,
        )

        api_response = api_response["result"]

        if api_response is None or len(api_response) == 0:
            return pl.DataFrame(schema=self.orders_schema)

        orders_df = pl.from_dicts(api_response)

        orders_df = orders_df.rename(
            {
                "TradingSymbol": "tradingsymbol",
                "ClientID": "user_id",
                "AppOrderID": "order_id",
                "OrderStatus": "status",
                "ExchangeSegment": "exchange",
                "OrderPrice": "price",
                "OrderType": "order_type",
                "OrderSide": "transaction_type",
                "OrderAverageTradedPrice": "average_price",
                "OrderGeneratedDateTime": "order_timestamp",
                "OrderQuantity": "quantity",
                "CumulativeQuantity": "filled_quantity",
                "LeavesQuantity": "pending_quantity",
                "ProductType": "product",
                "OrderStopPrice": "trigger_price",
                "OrderUniqueIdentifier": "tag",
                "ExchangeInstrumentID": "token",
                "OrderCategoryType": "variety",
            }
        )
        orders_df = orders_df.with_columns(
            pl.struct(["tradingsymbol"])
            .map_elements(
                lambda x: self.get_quantplay_symbol(x["tradingsymbol"]),
                return_dtype=pl.String,
            )
            .alias("tradingsymbol")
        )

        if add_ltp:
            positions = self.positions()
            positions = positions.sort("product").group_by("tradingsymbol").head(1)

            orders_df = orders_df.join(
                positions.select(["tradingsymbol", "ltp"]), on="tradingsymbol", how="left"
            )
        else:
            orders_df = orders_df.with_columns(pl.lit(None).cast(pl.Float64).alias("ltp"))

        orders_df = orders_df.with_columns(
            pl.col("filled_quantity").cast(pl.Int64).alias("filled_quantity"),
            pl.col("order_id").cast(pl.String).alias("order_id"),
        )

        orders_df = orders_df.with_columns(
            pl.when(pl.col("average_price") == "")
            .then(0)
            .otherwise(pl.col("average_price"))
            .cast(pl.Float64)
            .alias("average_price"),
            pl.col("order_timestamp")
            .str.strptime(pl.Datetime, "%d-%m-%Y %H:%M:%S")
            .alias("order_timestamp"),
            pl.col("LastUpdateDateTime")
            .str.strptime(pl.Datetime, "%d-%m-%Y %H:%M:%S")
            .alias("update_timestamp"),
            pl.when(pl.col("exchange") == "NSECM")
            .then(pl.lit("NSE"))
            .when(pl.col("exchange") == "NSEFO")
            .then(pl.lit("NFO"))
            .when(pl.col("exchange") == "BSECM")
            .then(pl.lit("BSE"))
            .when(pl.col("exchange") == "BSEFO")
            .then(pl.lit("BFO"))
            .otherwise(pl.col("exchange"))
            .alias("exchange"),
            pl.when(pl.col("status") == "Rejected")
            .then(pl.lit("REJECTED"))
            .when(pl.col("status") == "Cancelled")
            .then(pl.lit("CANCELLED"))
            .when(pl.col("status") == "Filled")
            .then(pl.lit("COMPLETE"))
            .when(pl.col("status") == "New")
            .then(pl.lit("OPEN"))
            .otherwise(pl.col("status"))
            .alias("status"),
            pl.when(pl.col("order_type") == pl.lit("Limit"))
            .then(pl.lit("LIMIT"))
            .when(pl.col("order_type") == pl.lit("StopLimit"))
            .then(pl.lit("SL"))
            .when(pl.col("order_type") == pl.lit("Market"))
            .then(pl.lit("MARKET"))
            .otherwise(pl.col("order_type"))
            .alias("order_type"),
        )

        orders_df = orders_df.with_columns(
            (
                pl.col("ltp") * pl.col("filled_quantity")
                - pl.col("average_price") * pl.col("filled_quantity")
            ).alias("pnl")
        )

        orders_df = orders_df.with_columns(
            pl.when(pl.col("transaction_type") == "SELL")
            .then(-pl.col("pnl"))
            .otherwise(pl.col("pnl"))
            .alias("pnl")
        )

        orders_df = orders_df.with_columns(
            pl.col("CancelRejectReason").alias("status_message"),
            pl.col("CancelRejectReason").alias("status_message_raw"),
        )

        if tag:
            orders_df = orders_df.filter(pl.col("tag") == tag)

        return orders_df.select(list(self.orders_schema.keys())).cast(self.orders_schema)

    def holdings(self, add_ltp: bool = True) -> pl.DataFrame:
        return pl.DataFrame(schema=self.holidings_schema)

    def positions(self, drop_cnc: bool = True) -> pl.DataFrame:
        api_response = self.invoke_xts_api(
            (
                self.wrapper.get_dealerposition_netwise
                if self.is_dealer
                else self.wrapper.get_position_netwise
            ),
            clientID=None if self.is_dealer else self.ClientID,
        )

        api_response = api_response["result"]["positionList"]
        positions_df = pl.DataFrame(api_response)

        if len(positions_df) == 0:
            return pl.DataFrame(schema=self.positions_schema)

        positions_df = positions_df.rename(
            {
                "TradingSymbol": "tradingsymbol",
                "ExchangeSegment": "exchange",
                "OpenBuyQuantity": "buy_quantity",
                "OpenSellQuantity": "sell_quantity",
                "Quantity": "quantity",
                "SumOfTradedQuantityAndPriceBuy": "buy_value",
                "SumOfTradedQuantityAndPriceSell": "sell_value",
                "ProductType": "product",
                "ExchangeInstrumentId": "token",
            }
        )

        positions_df = positions_df.with_columns(
            pl.when(pl.col("exchange") == "NSECM")
            .then(pl.lit("NSE"))
            .when(pl.col("exchange") == "NSEFO")
            .then(pl.lit("NFO"))
            .when(pl.col("exchange") == "BSECM")
            .then(pl.lit("BSE"))
            .when(pl.col("exchange") == "BSEFO")
            .then(pl.lit("BFO"))
            .otherwise(pl.col("exchange"))
            .alias("exchange")
        )

        positions_df = positions_df.with_columns(
            (pl.col("exchange") + ":" + pl.col("token")).alias("exchange_symbol")
        )

        symbols = (
            positions_df.select(pl.col("exchange_symbol").unique()).to_series().to_list()
        )
        symbol_ltps = self.get_ltps(symbols)

        positions_df = positions_df.with_columns(
            pl.col("token")
            .cast(pl.Int64)
            .replace_strict(symbol_ltps, default=0)
            .cast(pl.Float64)
            .alias("ltp")
        )

        positions_df = positions_df.with_columns(
            (
                pl.col("sell_value").cast(pl.Float64)
                - pl.col("buy_value").cast(pl.Float64)
            ).alias("pnl")
        )
        positions_df = positions_df.with_columns(
            (pl.col("pnl") + (pl.col("quantity").cast(pl.Float64) * pl.col("ltp"))).alias(
                "pnl"
            )
        )

        positions_df = positions_df.with_columns(
            pl.struct(["tradingsymbol"])
            .map_elements(
                lambda x: self.get_quantplay_symbol(x["tradingsymbol"]),
                return_dtype=pl.String,
            )
            .alias("tradingsymbol")
        )
        positions_df = positions_df.with_columns(
            pl.when(pl.col("tradingsymbol").str.slice(-2) == "PE")
            .then(pl.lit("PE"))
            .otherwise(pl.lit("CE"))
            .alias("option_type")
        )
        positions_df = positions_df.with_columns(
            pl.when(pl.col("exchange").is_in(["NFO", "BFO"]))
            .then(pl.col("option_type"))
            .otherwise(None)
            .alias("option_type")
        )
        positions_df = positions_df.with_columns(pl.lit(0).alias("average_price"))

        positions_df = positions_df[list(self.positions_schema.keys())].cast(
            self.positions_schema
        )

        positions_df = positions_df.with_columns(
            ((pl.col("buy_value") - pl.col("sell_value")) / pl.col("quantity")).alias(
                "average_price"
            )
        )
        positions_df = positions_df.with_columns(
            pl.when(pl.col("quantity") == 0)
            .then(pl.lit(0))
            .otherwise(pl.col("average_price"))
            .alias("average_price")
        )

        return positions_df

    def get_quantplay_symbol(self, symbol: str):
        if symbol in self.broker_symbol_map:
            return self.broker_symbol_map[symbol]
        return symbol

    def get_ltps(self, symbols: list[str]):
        instruments: list[XTSTypes.InstrumentType] = [
            {
                "exchangeSegment": self.get_exchange_code(x.split(":")[0]),
                "exchangeInstrumentID": int(x.split(":")[1]),
            }
            for x in symbols
        ]

        api_response = self.invoke_xts_api(
            self.md_wrapper.get_quote,
            Instruments=instruments,
            xtsMessageCode=1512,
            publishFormat="JSON",
        )

        if "type" in api_response and api_response["type"] == "error":
            raise TokenException(api_response["description"])

        api_response = api_response["result"]

        ltp_json = api_response["listQuotes"]

        ltp = [json.loads(x) for x in ltp_json]

        ltp = {x["ExchangeInstrumentID"]: float(x["LastTradedPrice"]) for x in ltp}
        return ltp

    def get_exchange_code(
        self, exchange: ExchangeType | str
    ) -> XTSTypes.ExchangeSegmentType:
        exchange_code_map: dict[str, XTSTypes.ExchangeSegmentType] = {
            "NSE": 1,
            "NFO": 2,
            "BFO": 12,
            "BSE": 11,
            "NSECM": 1,
            "NSEFO": 2,
            "NSECD": 3,
            "BSECM": 11,
            "BSEFO": 12,
        }

        if exchange not in exchange_code_map:
            raise KeyError(
                f"INVALID_EXCHANGE: Exchange {exchange} not in ['NSE', 'NFO', 'NSECD', 'BSECM', 'BSEFO']"
            )

        return exchange_code_map[exchange]

    def get_exchange_name(self, exchange: ExchangeType) -> XTSTypes.ExchangeType:
        exchange_code_map: dict[str, XTSTypes.ExchangeType] = {
            "NSE": "NSECM",
            "NFO": "NSEFO",
            "BFO": "BSEFO",
            "NSECD": "NSECD",
            "BSECM": "BSECM",
            "BSEFO": "BSEFO",
        }

        if exchange not in exchange_code_map:
            raise KeyError(
                f"INVALID_EXCHANGE: Exchange {exchange} not in ['NSE', 'NFO', 'NSECD', 'BSECM', 'BSEFO']"
            )

        return exchange_code_map[exchange]

    def ltp(self, exchange: ExchangeType, tradingsymbol: str) -> float:
        exchange_code = self.get_exchange_code(exchange)
        exchange_token = self.symbol_data[f"{exchange}:{tradingsymbol}"].get(
            "exchange_token", ""
        )

        api_response = self.invoke_xts_api(
            self.md_wrapper.get_quote,
            Instruments=[
                {
                    "exchangeSegment": exchange_code,
                    "exchangeInstrumentID": exchange_token,
                }
            ],
            xtsMessageCode=1512,
            publishFormat="JSON",
        )

        if api_response["type"] == "error":
            raise BrokerException(
                api_response.get("description", "Broker Failed to Provide LTP")
            )

        api_response = api_response["result"]

        try:
            ltp_json = api_response["listQuotes"][0]

        except IndexError:
            traceback.print_exc()
            raise BrokerException("Broker Provided Invalid Response")

        ltp = json.loads(ltp_json)["LastTradedPrice"]

        return ltp

    def place_order(
        self,
        tradingsymbol: str,
        exchange: ExchangeType,
        quantity: int,
        order_type: OrderTypeType,
        transaction_type: TransactionType,
        tag: str | None,
        product: ProductType,
        price: float,
        trigger_price: float | None = None,
    ) -> str:
        exchange_name = self.get_exchange_name(exchange)
        xts_order_type = self.get_order_type(order_type)

        exchange_token = self.symbol_data[f"{exchange}:{tradingsymbol}"].get(
            "exchange_token", ""
        )
        if trigger_price is None:
            trigger_price = 0

        if tag is None:
            tag = ""

        api_response = self.wrapper.place_order(
            exchangeSegment=exchange_name,
            exchangeInstrumentID=exchange_token,
            orderType=xts_order_type,
            disclosedQuantity=0,
            orderQuantity=quantity,
            limitPrice=price,
            timeInForce="DAY",
            stopPrice=trigger_price,
            orderSide=transaction_type,
            productType=product,
            orderUniqueIdentifier=tag,
            clientID=self.ClientID,
        )
        Constants.logger.info(f"[XTS_PLACE_ORDER_RESPONSE] {api_response}")

        if api_response["type"] == "error":
            Constants.logger.info(f"[XTS_PLACE_ORDER_ERROR] {api_response}")

            raise Exception("[XTS_ERROR]: " + api_response["description"])

        return api_response["result"]["AppOrderID"]

    def cancel_order(self, order_id: str, variety: str | None = None):
        orders = self.orders()

        order_data = orders.filter(pl.col("order_id").eq(str(order_id)))
        if len(order_data) == 0:
            raise InvalidArgumentException(f"Order [{order_id}] not found")
        order_data = order_data.to_dicts()[0]

        tag = order_data["tag"]

        api_response = self.invoke_xts_api(
            self.wrapper.cancel_order,
            appOrderID=int(order_id),
            clientID=order_data["user_id"],
            orderUniqueIdentifier=tag,
        )

        if api_response["type"] == "error":
            Constants.logger.info(f"[XTS_CANCEL_ORDER_ERROR] {api_response}")

            raise Exception("[XTS_ERROR]: " + api_response["description"])

        return api_response["result"]["AppOrderID"]

    def get_order_type(self, order_type: OrderTypeType):
        if order_type == OrderType.market:
            return "Market"
        elif order_type == OrderType.sl:
            return "StopLimit"
        elif order_type == OrderType.slm:
            return "StopMarket"
        elif order_type == OrderType.limit:
            return "Limit"

        return order_type

    def modify_order(self, order: ModifyOrderRequest) -> str:
        order_id = order["order_id"]

        price = order.get("price", None)
        trigger_price = order.get("trigger_price", None)
        order_type = order.get("order_type", None)
        product = order.get("product", None)
        tag = order.get("tag", None)

        orders = self.orders()
        order_data = orders.filter(pl.col("order_id").eq(order_id))

        if len(order_data) == 0:
            raise InvalidArgumentException(f"Order [{order_id}] not found")

        order_data = order_data.to_dicts()[0]

        price = price or order_data["price"]
        trigger_price = trigger_price or order_data["trigger_price"]
        order_type = order_type or order_data["order_type"]
        tag = tag or order_data["tag"]
        product = product or order_data["product"]

        quantity = order_data["quantity"]
        time_in_force = "DAY"
        disclosed_quantity = 0

        api_response = self.invoke_xts_api(
            self.wrapper.modify_order,
            appOrderID=int(order_id),
            modifiedTimeInForce=time_in_force,
            modifiedDisclosedQuantity=disclosed_quantity,
            modifiedLimitPrice=price,
            modifiedOrderQuantity=quantity,
            modifiedOrderType=self.get_order_type(order_type),
            modifiedProductType=product,
            modifiedStopPrice=trigger_price,
            orderUniqueIdentifier=tag,
            clientID=self.ClientID,
        )

        if api_response["type"] == "error":
            Constants.logger.info(f"[XTS_MODIFY_ORDER_ERROR] {api_response}")

            raise Exception("[XTS_ERROR]: " + api_response["description"])

        return api_response["result"]["AppOrderID"]

    def modify_price(
        self,
        order_id: str,
        price: float,
        trigger_price: float | None = None,
        order_type: OrderTypeType | None = None,
    ):
        data: ModifyOrderRequest = {
            "order_id": str(order_id),
            "price": price,
            "trigger_price": trigger_price,
        }

        if order_type is not None:
            data["order_type"] = order_type

        self.modify_order(data)

    def get_exchange(self, exchange: ExchangeType) -> Any:
        return exchange

    def get_product(self, product: ProductType) -> Any:
        return product

    def stream_order_updates(self):
        if self.wrapper.token is None:
            raise InvalidArgumentException("XTS Token Missing")

        socket = OrderSocket_io(
            userID=self.ClientID,
            token=self.wrapper.token,
            root_url=self.root_url,
        )
        socket.setup_event_listners(on_order=self.order_event_handler)
        socket.connect()

    def order_event_handler(self, order: str):
        if self.order_updates is None:
            raise Exception("Event Queue Not Initalised")

        order_data = json.loads(order)
        new_ord: OrderUpdateEvent = {}  # type: ignore

        try:
            new_ord["placed_by"] = order_data["ClientID"]
            new_ord["tag"] = order_data["ClientID"]
            new_ord["order_id"] = order_data["AppOrderID"]
            new_ord["exchange_order_id"] = order_data["ExchangeOrderID"]
            new_ord["exchange"] = order_data["ExchangeSegment"]
            new_ord["tradingsymbol"] = order_data["TradingSymbol"]

            if new_ord["exchange"] == "NSEFO":
                new_ord["exchange"] = "NFO"
            elif new_ord["exchange"] == "NSECM":
                new_ord["exchange"] = "NSE"

            if new_ord["exchange"] in ["NFO", "MCX"]:
                new_ord["tradingsymbol"] = self.broker_symbol_map[
                    new_ord["tradingsymbol"]
                ]

            new_ord["order_type"] = order_data["OrderType"].upper()
            new_ord["product"] = order_data["ProductType"].upper()
            new_ord["transaction_type"] = order_data["OrderSide"].upper()
            new_ord["quantity"] = int(order_data["OrderQuantity"])

            if "OrderStopPrice" in order_data:
                new_ord["trigger_price"] = float(order_data["OrderStopPrice"])
            else:
                new_ord["trigger_price"] = None

            new_ord["price"] = float(order_data["OrderPrice"])
            new_ord["status"] = order_data["OrderStatus"].upper()

            if new_ord["status"] == "PENDINGNEW":
                new_ord["status"] = "TRIGGER PENDING"
            elif new_ord["status"] == "PENDINGCANCEL":
                new_ord["status"] = "PENDING"
            elif new_ord["status"] == "PENDINGREPLACE":
                new_ord["status"] = "TRIGGER PENDING"
            elif new_ord["status"] == "REPLACED":
                new_ord["status"] = "UPDATE"
            elif new_ord["status"] == "NEW":
                new_ord["status"] = "OPEN"
            elif new_ord["status"] == "FILLED":
                new_ord["status"] = "COMPLETE"

            if new_ord["order_type"].upper() == "MARKET":
                new_ord["order_type"] = OrderType.market
            elif new_ord["order_type"].upper() == "STOPLIMIT":
                new_ord["order_type"] = OrderType.sl
            elif new_ord["order_type"].upper() == "STOPMARKET":
                new_ord["order_type"] = OrderType.slm
            elif new_ord["order_type"].upper() == "LIMIT":
                new_ord["order_type"] = OrderType.limit

            if new_ord["order_type"] == "LIMIT" and new_ord["status"] == "UPDATE":
                new_ord["status"] = "OPEN"

            if new_ord["status"] == "TRIGGER PENDING" and new_ord["trigger_price"] == 0:
                return

            if self.order_updates:
                self.order_updates.put(new_ord)

        except Exception as e:
            traceback.print_exc()
            Constants.logger.error("[ORDER_UPDATE_PROCESSING_FAILED] {}".format(e))

    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
        retry_on_exception=retry_exception,
    )
    def invoke_xts_api(self, fn: Any, *args: Any, **kwargs: Any) -> dict[str, Any]:
        try:
            response = fn(*args, **kwargs)

            if "data" in response and "description" in response["data"]:
                data = response["data"]

                if "max limit" in data["description"].lower():
                    user_id = self.profile()["user_id"]
                    raise RetryableException(f"{user_id}: Request limit exceeded")

            if (
                "description" in response
                and "Authorization not found" in response["description"]
            ):
                raise TokenException(response["description"])

            if (
                "type" in response and response["type"] == "error"
            ) or "result" not in response:
                raise BrokerException(f"[XTS_Error]: {response['description']}")

            return response

        except XTSTokenException as e:
            raise TokenException(str(e))

        except (TokenException, RetryableException, BrokerException):
            raise

        except (
            XTSGeneralException,
            XTSDataException,
            XTSNetworkException,
        ) as e:
            raise BrokerException(str(e))

        except Exception:
            traceback.print_exc()
            raise
