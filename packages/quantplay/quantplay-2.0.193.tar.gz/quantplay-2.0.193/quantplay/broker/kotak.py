import base64
import json
from queue import Queue
from typing import Any, Literal
from urllib.parse import urlencode

import polars as pl
import requests
import urllib
import jwt

from quantplay.broker.generics.broker import Broker
from quantplay.broker.kotak_utils.kotak_ws import NeoWebSocket
from quantplay.model.broker import (
    MarginsResponse,
    ModifyOrderRequest,
    UserBrokerProfileResponse,
)
from quantplay.model.generics import (
    ExchangeType,
    OrderTypeType,
    ProductType,
    TransactionType,
    OrderStatusType,
)
from quantplay.model.order_event import OrderUpdateEvent
from quantplay.exception.exceptions import (
    InvalidArgumentException,
    BrokerException,
    QuantplayOrderPlacementException,
)
from quantplay.utils.constant import Constants
from quantplay.utils.pickle_utils import InstrumentData
from quantplay.wrapper.aws.s3 import S3Utils
import shortuuid  # type:ignore

PROD_BASE_URL = "https://gw-napi.kotaksecurities.com/"
SESSION_PROD_BASE_URL = "https://napi.kotaksecurities.com/"


class Kotak(Broker):
    def __init__(
        self,
        user_id: str,
        order_updates: Queue[OrderUpdateEvent] | None = None,
        consumer_key: str | None = None,
        consumer_secret: str | None = None,
        mobilenumber: str | None = None,
        password: str | None = None,
        otp: str | None = None,
        configuration: dict[str, str] | None = None,
        load_instrument: bool = True,
        verify_config: bool = True,
    ) -> None:
        super().__init__()

        self.configuration: dict[str, str | None] = {
            "fin_key": "X6Nk8cQhUgGmJ2vBdWw4sfzrz4L5En",
        }

        if configuration:
            self.configuration = {
                "fin_key": "X6Nk8cQhUgGmJ2vBdWw4sfzrz4L5En",
                "bearer_token": configuration.get("bearer_token"),
                "view_token": configuration.get("view_token"),
                "sid": configuration.get("sid"),
                "kotakUserId": configuration.get("kotakUserId"),
                "edit_token": configuration.get("edit_token"),
                "edit_sid": configuration.get("edit_sid"),
                "edit_rid": configuration.get("edit_rid"),
                "serverId": configuration.get("serverId"),
            }

            if verify_config:
                self.margins()  # To Verify Configuration

        elif consumer_key and consumer_secret and mobilenumber and password:
            self.login(consumer_key, consumer_secret, mobilenumber, password)

        if otp:
            self.verify_2fa(otp)
            self.margins()  # To Verify Configuration

        if load_instrument:
            self.load_instrument()

        self.order_updates = order_updates
        self.user_id = user_id

    def load_instrument(self, file_name: str | None = None) -> None:
        try:
            self.symbol_data = InstrumentData.get_instance().load_data(  # type: ignore
                "kotak_instruments"
            )
            Constants.logger.info("[LOADING_INSTRUMENTS] loading data from cache")
        except Exception:
            inst_data_df = S3Utils.get_parquet(
                "quantplay-market-data/symbol_data/kotak_instruments.parquet"
            )
            inst_data_df = inst_data_df.with_columns(
                pl.col("tradingsymbol").alias("broker_symbol")
            )
            self.instrument_data = inst_data_df
            self.initialize_symbol_data_v2(save_as="kotak_instruments")

        self.initialize_broker_symbol_map()

    def login(
        self,
        consumer_key: str,
        consumer_secret: str,
        mobilenumber: str,
        password: str,
    ) -> None:
        base64_string = str(consumer_key) + ":" + str(consumer_secret)
        base64_token = base64_string.encode("ascii")

        base64_bytes = base64.b64encode(base64_token)
        final_base64_token = base64_bytes.decode("ascii")

        session_init = requests.post(
            url=f"{SESSION_PROD_BASE_URL}oauth2/token",
            headers={
                "Authorization": "Basic " + final_base64_token,
                "Content-Type": "application/json",
            },
            data=json.dumps({"grant_type": "client_credentials"}),
        )

        if not session_init.ok:
            raise InvalidArgumentException(json.loads(session_init.content))

        json_resp = json.loads(session_init.text)
        self.configuration["bearer_token"] = json_resp.get("access_token")

        view_token_resp = requests.post(
            url=f"{PROD_BASE_URL}login/1.0/login/v2/validate",
            headers={
                "Authorization": "Bearer " + self.configuration["bearer_token"],
                "Content-Type": "application/json",
            },
            data=json.dumps({"mobileNumber": mobilenumber, "password": password}),
        )
        view_token = json.loads(view_token_resp.text)

        self.configuration["view_token"] = view_token.get("data").get("token")
        self.configuration["sid"] = view_token.get("data").get("sid")

        decode_jwt = jwt.decode(  # type: ignore
            self.configuration["view_token"], options={"verify_signature": False}
        )
        userid = decode_jwt.get("sub")
        self.configuration["kotakUserId"] = userid

        generate_otp_resp = requests.post(
            url=f"{PROD_BASE_URL}login/1.0/login/otp/generate",
            headers={"Authorization": "Bearer " + self.configuration["bearer_token"]},
            data=json.dumps({"userId": userid, "sendEmail": True, "isWhitelisted": True}),
        )

        _generate_otp = json.loads(generate_otp_resp.text)

    def verify_2fa(self, otp: str) -> None:
        if (
            self.configuration["bearer_token"] is None
            or self.configuration["sid"] is None
            or self.configuration["view_token"] is None
            or self.configuration["kotakUserId"] is None
        ):
            raise InvalidArgumentException("Missing Params")

        login_resp = requests.post(
            url=f"{PROD_BASE_URL}login/1.0/login/v2/validate",
            headers={
                "Authorization": "Bearer " + self.configuration["bearer_token"],
                "sid": self.configuration["sid"],
                "Auth": self.configuration["view_token"],
                "Content-Type": "application/json",
            },
            data=json.dumps({"userId": self.configuration["kotakUserId"], "otp": otp}),
        )

        edit_token_resp = json.loads(login_resp.text)

        if "error" not in edit_token_resp:
            self.configuration["edit_token"] = edit_token_resp.get("data").get("token")
            self.configuration["edit_sid"] = edit_token_resp.get("data").get("sid")
            self.configuration["edit_rid"] = edit_token_resp.get("data").get("rid")
            self.configuration["serverId"] = edit_token_resp.get("data").get("hsServerId")
            self.user_id = edit_token_resp.get("data").get("ucc")

    def order_history(self, order_id: str) -> pl.DataFrame:
        body = {"nOrdNo": order_id}
        order_history = self.request("order_history", body=body)["data"]  # type:ignore
        order_history_df = pl.DataFrame(order_history)[
            [
                "tok",
                "flDtTm",
                "nOrdNo",
                "exch",
                "prod",
                "trdSym",
                "trnsTp",
                "qty",
                "prcTp",
                "GuiOrdId",
            ]
        ]
        order_history_df = order_history_df.rename(
            {
                "tok": "token",
                "flDtTm": "update_timestamp",
                "nOrdNo": "order_id",
                "exch": "exchange",
                "prod": "product",
                "trdSym": "tradingsymbol",
                "trnsTp": "transaction_type",
                "qty": "quantity",
                "prcTp": "order_type",
                "GuiOrdId": "tag",
            }
        )
        order_history_df = order_history_df.with_columns(
            pl.col("update_timestamp")
            .str.strptime(pl.Datetime(time_unit="ms"), format="%d-%b-%Y %H:%M:%S")
            .alias("update_timestamp")
        ).sort("update_timestamp")

        return order_history_df

    # **
    # ** GET Api's
    # **

    def orders(self, tag: str | None = None, add_ltp: bool = True) -> pl.DataFrame:
        orders_resp = self.request("order_book")

        if orders_resp["stat"] == "Not_Ok" and orders_resp["errMsg"] == "No Data":
            return pl.DataFrame(schema=self.orders_schema)
        orders_df = pl.DataFrame(orders_resp["data"])
        if "rejRsn" not in orders_df.columns:
            orders_df = orders_df.with_columns(pl.lit("").alias("rejRsn"))
        orders_df = orders_df.rename(
            {
                "actId": "user_id",
                "nOrdNo": "order_id",
                "exSeg": "exchange",
                "prod": "product",
                "trdSym": "tradingsymbol",
                "ordSt": "status",
                "prcTp": "order_type",
                "trnsTp": "transaction_type",
                "prc": "price",
                "avgPrc": "average_price",
                "trgPrc": "trigger_price",
                "ordDtTm": "order_timestamp",
                "tok": "token",
                "qty": "quantity",
                "fldQty": "filled_quantity",
                "rejRsn": "status_message",
            }
        )

        orders_df = orders_df.with_columns(
            pl.lit("regular").alias("variety"),
            pl.col("GuiOrdId").str.split(":").list.get(0).alias("tag"),
            pl.lit(None).alias("ltp"),
            pl.col("status_message").alias("status_message_raw"),
            pl.col("order_timestamp")
            .str.strptime(pl.Datetime(time_unit="ms"), format="%d-%b-%Y %H:%M:%S")
            .alias("order_timestamp"),
            pl.col("status").str.to_uppercase().alias("status"),
        )
        orders_df = orders_df.with_columns(
            pl.col("order_timestamp").alias("update_timestamp"),
            (pl.col("quantity") - pl.col("filled_quantity")).alias("pending_quantity"),
        )
        orders_df = orders_df[list(self.orders_schema.keys())].cast(self.orders_schema)

        orders_df = orders_df.with_columns(
            pl.when(pl.col("exchange") == "nse_cm")
            .then(pl.lit("NSE"))
            .when(pl.col("exchange") == "bse_cm")
            .then(pl.lit("BSE"))
            .when(pl.col("exchange") == "nse_fo")
            .then(pl.lit("NFO"))
            .when(pl.col("exchange") == "bse_fo")
            .then(pl.lit("BFO"))
            .when(pl.col("exchange") == "cde_fo")
            .then(pl.lit("CDS"))
            .when(pl.col("exchange") == "bcs-fo")
            .then(pl.lit("BCD"))
            .when(pl.col("exchange") == "mcx")
            .then(pl.lit("MCX"))
            .otherwise(pl.col("exchange"))
            .alias("exchange"),
            pl.when(pl.col("order_type") == "L")
            .then(pl.lit("LIMIT"))
            .when(pl.col("order_type") == "MKT")
            .then(pl.lit("MARKET"))
            .otherwise(pl.col("order_type"))
            .alias("order_type"),
            pl.when(pl.col("transaction_type") == "B")
            .then(pl.lit("BUY"))
            .when(pl.col("transaction_type") == "S")
            .then(pl.lit("SELL"))
            .otherwise(pl.col("transaction_type"))
            .alias("transaction_type"),
        )

        return orders_df

    def add_ltps(self, df: pl.DataFrame) -> pl.DataFrame:
        data = df.to_dicts()
        token_list = [self.token_converter(int(d["token"]), d["exchange"]) for d in data]
        ltps: list[float] = self.ltp_from_tokens(token_list)  # type:ignore

        ltps = [float(a) for a in ltps]
        ltps = pl.Series("ltp", ltps, dtype=pl.Float64)  # type:ignore

        # Assign the Series to a new column in the DataFrame
        df = df.with_columns(ltps)

        df = df.with_columns(
            (
                pl.col("sell_value")
                - pl.col("buy_value")
                + pl.col("quantity") * pl.col("ltp")
            ).alias("pnl")
        )
        return df

    def positions(self, drop_cnc: bool = True) -> pl.DataFrame:
        positions_resp = self.request("positions")

        if positions_resp["stat"] == "Not_Ok" and positions_resp["errMsg"] == "No Data":
            return pl.DataFrame(schema=self.positions_schema)
        positions_df = pl.DataFrame(positions_resp["data"])

        positions_df = positions_df.rename(
            {
                "trdSym": "tradingsymbol",
                "buyAmt": "buy_value",
                "sellAmt": "sell_value",
                "prod": "product",
                "tok": "token",
                "exSeg": "exchange",
                "optTp": "option_type",
            }
        )
        positions_df = positions_df.with_columns(
            (
                pl.col("flBuyQty").fill_null(0).cast(pl.Int64)
                + pl.col("cfBuyQty").fill_null(0).cast(pl.Int64)
            ).alias("buy_quantity"),
            (
                pl.col("flSellQty").fill_null(0).cast(pl.Int64)
                + pl.col("cfSellQty").fill_null(0).cast(pl.Int64)
            ).alias("sell_quantity"),
            pl.lit(0).alias("ltp"),
            pl.lit(0).alias("pnl"),
            pl.when(pl.col("exchange") == "nse_cm")
            .then(pl.lit("NSE"))
            .when(pl.col("exchange") == "bse_cm")
            .then(pl.lit("BSE"))
            .when(pl.col("exchange") == "nse_fo")
            .then(pl.lit("NFO"))
            .when(pl.col("exchange") == "bse_fo")
            .then(pl.lit("BFO"))
            .when(pl.col("exchange") == "cde_fo")
            .then(pl.lit("CDS"))
            .when(pl.col("exchange") == "bcs-fo")
            .then(pl.lit("BCD"))
            .when(pl.col("exchange") == "mcx")
            .then(pl.lit("MCX"))
            .otherwise(pl.col("exchange"))
            .alias("exchange"),
            pl.when(pl.col("option_type") == "XX")
            .then(pl.lit(None))
            .otherwise(pl.col("option_type"))
            .alias("option_type"),
        )
        positions_df = positions_df.with_columns(
            (pl.col("buy_quantity") - pl.col("sell_quantity")).alias("quantity")
        )
        positions_df = positions_df.with_columns(
            (
                (
                    pl.col("buy_value").cast(pl.Float32)
                    - pl.col("sell_value").cast(pl.Float32)
                )
                / pl.col("quantity")
            ).alias("average_price")
        )
        positions_df = positions_df.with_columns(
            pl.when(pl.col("quantity").cast(pl.Int32) == 0)
            .then(pl.lit(0))
            .otherwise(pl.col("average_price"))
            .alias("average_price")
        )
        positions_df = positions_df[list(self.positions_schema.keys())].cast(
            self.positions_schema
        )

        return self.add_ltps(positions_df)

    def trades(self) -> pl.DataFrame:
        self.request("trade_report")

        return pl.DataFrame(schema=self.positions_schema)

    def holdings(self, add_ltp: bool = True) -> pl.DataFrame:
        holdings_resp = self.request("holdings")

        holdings_df = pl.DataFrame(holdings_resp["data"])
        holdings_df = holdings_df.rename(
            {
                "symbol": "tradingsymbol",
                "exchangeSegment": "exchange",
                "exchangeIdentifier": "token",
                "averagePrice": "average_price",
                "closingPrice": "price",
                "holdingCost": "buy_value",
            }
        )
        holdings_df = holdings_df.with_columns(
            pl.when(pl.col("exchange") == "nse_cm")
            .then(pl.lit("NSE"))
            .when(pl.col("exchange") == "bse_cm")
            .then(pl.lit("BSE"))
            .when(pl.col("exchange") == "nse_fo")
            .then(pl.lit("NFO"))
            .when(pl.col("exchange") == "bse_fo")
            .then(pl.lit("BFO"))
            .when(pl.col("exchange") == "cde_fo")
            .then(pl.lit("CDS"))
            .when(pl.col("exchange") == "bcs-fo")
            .then(pl.lit("BCD"))
            .when(pl.col("exchange") == "mcx")
            .then(pl.lit("MCX"))
            .otherwise(pl.col("exchange"))
            .alias("exchange"),
            pl.lit(None).alias("isin"),
        )

        holdings_df = holdings_df.with_columns(
            (pl.col("quantity") * pl.col("price")).alias("value"),
            pl.lit(0).alias("pledged_quantity"),
            (pl.col("quantity") * pl.col("average_price")).alias("buy_value"),
            (pl.col("quantity") * pl.col("price")).alias("current_value"),
            ((pl.col("price") / pl.col("average_price") - 1) * 100).alias("pct_change"),
        )

        holdings_df[list(self.holidings_schema.keys())].cast(self.holidings_schema)

        return holdings_df[list(self.holidings_schema.keys())].cast(self.holidings_schema)

    def ltp(self, exchange: str, tradingsymbol: str) -> float:
        exchange = self.get_quantplay_exchange(exchange)
        tradingsymbol = self.get_quantplay_symbol(tradingsymbol)
        token = self.symbol_data[f"{exchange}:{tradingsymbol}"]["token"]

        instrument_token = self.token_converter(int(token), exchange)
        ltp = self.ltp_from_token(instrument_token)
        if ltp is None:
            raise InvalidArgumentException(
                f"LTP for {exchange} {tradingsymbol} is not available"
            )
        return float(ltp)

    def profile(self) -> UserBrokerProfileResponse:
        return {"user_id": self.user_id or ""}

    def margins(self) -> MarginsResponse:
        limits_resp = self.request(
            "limits", body={"seg": "ALL", "exch": "ALL", "prod": "ALL"}
        )

        return {
            "margin_used": float(limits_resp["MarginUsed"]),
            "margin_available": float(limits_resp["Net"]),
            "total_balance": float(limits_resp["MarginUsed"]) + float(limits_resp["Net"]),
            "cash": 0,
        }

    # **
    # ** POST/PUT Api's
    # **

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
    ) -> str | None:
        if tag:
            tag = tag + ":" + str(shortuuid.uuid())  # type:ignore
        else:
            tag = str(shortuuid.uuid())  # type:ignore
        place_order_body = {
            "am": "NO",
            "dq": "0",
            "es": self.get_exchange(exchange),
            "mp": "0",
            "pc": self.get_product(product),
            "pf": "N",
            "pr": str(price),
            "pt": self.get_order_type(order_type),
            "qt": str(quantity),
            "rt": "DAY",
            "tp": str(trigger_price or "0"),
            "ts": self.get_symbol(tradingsymbol, exchange),
            "tt": self.get_transaction_type(transaction_type),
            "ig": tag,
        }

        place_order_resp = self.request(  # type:ignore
            "place_order", body=place_order_body
        )  # type:ignore
        print(place_order_resp)

        if place_order_resp["stat"] == "Not_Ok":
            raise QuantplayOrderPlacementException(place_order_resp["errMsg"])

        return place_order_resp["nOrdNo"]

    def cancel_order(self, order_id: str, variety: str | None = None) -> None:
        body = {"on": order_id, "am": "No"}

        self.request("cancel_order", body=body)

    def modify_order(self, order: ModifyOrderRequest) -> str:
        order_id = order["order_id"]
        price = order.get("price")
        trigger_price = order.get("trigger_price", 0)
        if trigger_price is None:
            trigger_price = 0

        order_history = self.order_history(order_id).to_dicts()[-1]

        order_type = self.get_order_type(
            order.get("order_type", order_history["order_type"])
        )
        quantity = str(order.get("quantity", order_history["quantity"]))
        modify_order_request = {
            "tk": str(order_history["token"]),
            "mp": "0",
            "pc": order_history["product"],
            "dd": "NA",
            "dq": "0",
            "vd": "DAY",
            "ts": order_history["tradingsymbol"],
            "tt": order_history["transaction_type"],
            "pr": str(price),
            "tp": str(trigger_price),
            "qt": quantity,
            "no": order_id,
            "es": self.get_exchange(order_history["exchange"]),
            "pt": order_type,
            "ig": order_history["tag"],
        }

        try:
            Constants.logger.info(f"Modifying order [{order_id}] new price [{price}]")

            modify_order_response = self.request(  # type:ignore
                "modify_order", body=modify_order_request
            )

            return modify_order_response["nOrdNo"]

        except Exception as e:
            exception_message = (
                f"OrderModificationFailed for {order_id} failed with exception {e}"
            )
            if (
                "Order cannot be modified as it is being processed"
                not in exception_message
            ):
                Constants.logger.error(f"{exception_message}")

        return order_id

    def get_transaction_type(self, transaction_type: TransactionType) -> str:
        transaction_type_map: dict[TransactionType, str] = {
            "BUY": "B",
            "SELL": "S",
        }
        return transaction_type_map.get(transaction_type, transaction_type)

    def get_order_type(self, order_type: OrderTypeType) -> str:
        order_type_map: dict[OrderTypeType, str] = {
            "LIMIT": "L",
            "MARKET": "MKT",
            "SL": "SL",
            "SL-M": "SL-M",
        }

        return order_type_map.get(order_type, order_type)

    def get_quantplay_order_type(self, order_type: str) -> OrderTypeType:
        order_type_map: dict[str, str] = {
            "L": "LIMIT",
            "MKT": "MARKET",
        }

        return order_type_map.get(order_type, order_type)  # type:ignore

    def get_quantplay_order_status(self, status: str) -> OrderStatusType:
        if status in [
            "put order req received",
            "validation pending",
            "open pending",
            "modify pending",
            "modify validation pending",
            "modified",
        ]:
            return "OPEN"
        if status == "cancel pending":
            return "CANCELLED"
        status = status.upper()
        if status not in ["OPEN", "TRIGGER PENDING", "CANCELLED", "REJECTED", "COMPLETE"]:
            Constants.logger.error(f"{status} not supported for Kotak")
            return "INVALID STATUS"  # type:ignore
        return status  # type:ignore

    def get_exchange(self, exchange: ExchangeType) -> str:
        exchange_segment_map: dict[ExchangeType, str] = {
            "NSE": "nse_cm",
            "BSE": "bse_cm",
            "NFO": "nse_fo",
            "BFO": "bse_fo",
            "CDS": "cde_fo",
            "BCD": "bcs-fo",
            "MCX": "mcx",
        }

        return exchange_segment_map.get(exchange, exchange)

    def get_quantplay_exchange(self, exchange: str) -> ExchangeType:
        exchange_segment_map: dict[str, str] = {
            "nse_cm": "NSE",
            "bse_cm": "BSE",
            "nse_fo": "NFO",
            "bse_fo": "BFO",
            "cde_fo": "CDS",
            "mcx": "MCX",
        }

        return exchange_segment_map.get(exchange, exchange)  # type:ignore

    def get_lot_size(self, exchange: str, tradingsymbol: str):
        tradingsymbol = self.get_quantplay_symbol(tradingsymbol)
        exchange = self.get_quantplay_exchange(exchange)

        try:
            return int(
                self.symbol_data["{}:{}".format(exchange, tradingsymbol)]["lot_size"]
            )
        except Exception as e:
            Constants.logger.error(
                "[GET_LOT_SIZE] unable to get lot size for {} {}".format(
                    exchange, tradingsymbol
                )
            )
            raise e

    def get_product(self, product: ProductType) -> str:
        product_map: dict[ProductType, str] = {
            "NRML": "NRML",
            "CNC": "CNC",
            "MIS": "MIS",
        }

        return product_map.get(product, product)

    def get_symbol(self, symbol: str, exchange: ExchangeType | None = None):
        if exchange == "NSE":
            if symbol in ["NIFTY", "BANKNIFTY"]:
                return symbol
            if "-EQ" not in symbol:
                return f"{symbol}-EQ"
            else:
                return symbol
        if exchange == "BSE":
            return symbol

        if symbol not in self.quantplay_symbol_map:
            return symbol
        return self.quantplay_symbol_map[symbol]

    # **
    # ** Kotak Utils
    # **

    def request(
        self,
        item: Literal[
            "place_order",
            "cancel_order",
            "modify_order",
            "order_history",
            "order_book",
            "trade_report",
            "positions",
            "holdings",
            "margin",
            "scrip_master",
            "limits",
            "logout",
        ],
        params: dict[str, str | int | float] | None = None,
        body: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        url_map = {
            "place_order": ("Orders/2.0/quick/order/rule/ms/place", "POST", False),
            "cancel_order": ("Orders/2.0/quick/order/cancel", "POST", False),
            "modify_order": ("Orders/2.0/quick/order/vr/modify", "POST", False),
            "order_history": ("Orders/2.0/quick/order/history", "POST", False),
            "order_book": ("Orders/2.0/quick/user/orders", "GET", True),
            "trade_report": ("Orders/2.0/quick/user/trades", "GET", True),
            "positions": ("Orders/2.0/quick/user/positions", "GET", True),
            "holdings": ("Portfolio/1.0/portfolio/v1/holdings", "GET", True),
            "margin": ("Orders/2.0/quick/user/check-margin", "GET", True),
            "scrip_master": ("Files/1.0/masterscrip/v1/file-paths", "GET", True),
            "limits": ("Orders/2.0/quick/user/limits", "POST", False),
            "logout": ("login/1.0/logout", "GET", True),
        }

        url, method, is_content_type_json = url_map[item]
        content_type = (
            "application/json"
            if is_content_type_json
            else "application/x-www-form-urlencoded"
        )

        url = f"{PROD_BASE_URL}{url}"

        request_headers = {
            "Authorization": f'Bearer {self.configuration["bearer_token"]}',
            "Sid": self.configuration["edit_sid"],
            "Auth": self.configuration["edit_token"],
            "neo-fin-key": self.configuration["fin_key"],
            "Content-Type": content_type,
            "accept": "application/json",
        }

        query_params = {"sId": self.configuration["serverId"]}
        if item == "place_order":
            request_headers.pop("accept", None)

        request_body = None

        if params is not None:
            request_params = urlencode({**params, **query_params})
        else:
            request_params = urlencode(query_params)

        request_body = {}
        if body is not None:
            if content_type == "application/json":
                request_body = json.dumps(body)
            elif item in ["place_order"]:
                request_body["jData"] = json.dumps(body)
            elif content_type == "application/x-www-form-urlencoded":
                request_body = urllib.parse.urlencode(  # type:ignore
                    {"jData": json.dumps(body)},
                    quote_via=urllib.parse.quote,  # type:ignore
                )

        resp = None
        resp_data = None

        if method == "GET":
            resp = requests.get(url=url, params=request_params, headers=request_headers)

        elif method == "POST":
            url += "?" + urlencode(query_params)

            resp = requests.post(
                url,
                headers=request_headers,
                data=request_body,  # type:ignore
            )

        if resp and resp.ok:
            resp_data = resp.json()

        if resp_data is None:
            raise BrokerException("Request Failed: No response from Kotak server")

        return resp_data

    def event_handler_order_update(self, order: dict[str, Any]):
        if "data" not in order:
            return
        data = json.loads(order["data"])
        if data["type"] != "order":
            return
        order = data["data"]
        if order["ordSt"] in [
            "put order req received",
            "validation pending",
            "modify pending",
            "modify validation pending",
            "modified",
            "not cancelled",
        ]:
            return

        quantplay_order: OrderUpdateEvent = {
            "placed_by": self.user_id,  # type:ignore
            "tradingsymbol": order["trdSym"],
            "exchange": self.get_quantplay_exchange(order["exSeg"]),
            "tag": order["GuiOrdId"],
            "order_id": order["nOrdNo"],
            "exchange_order_id": order["exOrdId"],
            "order_type": self.get_quantplay_order_type(order["prcTp"]),
            "price": float(order["prc"]),
            "quantity": int(order["qty"]),
            "product": order["prod"],
            "status": self.get_quantplay_order_status(order["ordSt"]),
        }

        if quantplay_order["exchange"] == "NSE":
            quantplay_order["tradingsymbol"] = quantplay_order["tradingsymbol"].replace(
                "-EQ", ""
            )

        quantplay_order["transaction_type"] = "BUY" if order["trnsTp"] == "B" else "SELL"
        if "trgPrc" in order:
            quantplay_order["trigger_price"] = float(order["trgPrc"])
        else:
            quantplay_order["trigger_price"] = None
        Constants.logger.info(f"Kotak event {quantplay_order}")

        if self.order_updates:
            self.order_updates.put(quantplay_order)

    def stream_order_data(self):
        ws = NeoWebSocket(
            sid=self.configuration.get("sid", ""),
            token=self.configuration.get("edit_token", ""),
            server_id=self.configuration.get("serverId", ""),
        )
        ws.on_message = self.event_handler_order_update
        ws.on_error = lambda x: print(x)

        ws.get_order_feed()
