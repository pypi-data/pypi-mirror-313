import binascii
import copy
import hashlib
import json
from queue import Queue
from typing import Any

import polars as pl
import pyotp
import requests
from retrying import retry  # type: ignore

from quantplay.broker.generics.broker import Broker
from quantplay.exception.exceptions import (
    InvalidArgumentException,
    QuantplayOrderPlacementException,
    RetryableException,
    TokenException,
    retry_exception,
)
from quantplay.model.broker import MarginsResponse, UserBrokerProfileResponse
from quantplay.model.generics import (
    ExchangeType,
    OrderTypeType,
    ProductType,
    TransactionType,
)
from quantplay.model.order_event import OrderUpdateEvent
from quantplay.utils.constant import Constants, OrderType
from quantplay.utils.pickle_utils import InstrumentData
from quantplay.wrapper.aws.s3 import S3Utils


class Motilal(Broker):
    user_id = "motilal_user_id"
    api_key = "motilal_api_key"
    password = "motilal_password"
    auth_token = "motilal_auth_token"
    two_factor_authentication = "motilal_2FA"
    secret_key = "motilal_secret_key"

    headers: dict[str, str] = {
        "Accept": "application/json",
        "User-Agent": "MOSL/V.1.1.0",
        "SourceId": "WEB",
        "MacAddress": "00:50:56:BD:F4:0B",
        "ClientLocalIp": "192.168.165.165",
        "ClientPublicIp": "106.193.137.95",
        "osname": "Ubuntu",
        "osversion": "10.0.19041",
        "devicemodel": "AHV",
        "manufacturer": "DELL",
        "productname": "Your Product Name",
        "productversion": "Your Product Version",
        "installedappid": "AppID",
        "browsername": "Chrome",
        "browserversion": "105.0",
    }

    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=2,
        retry_on_exception=retry_exception,
    )
    def __init__(
        self,
        is_uat: bool = False,
        headers: dict[str, str] | None = None,
        load_instrument: bool = True,
        user_id: str | None = None,
        password: str | None = None,
        api_key: str | None = None,
        two_fa: str | None = None,
        totp: str | None = None,
        order_updates: Queue[OrderUpdateEvent] | None = None,
    ) -> None:
        super().__init__()
        self.order_updates = order_updates

        self.instrument_data_by_exchange = {}

        uat = ""
        if is_uat:
            uat = "uat"

        self.url = (
            "https://{}openapi.motilaloswal.com/rest/login/v3/authdirectapi".format(uat)
        )
        self.otp_url = (
            "https://{}openapi.motilaloswal.com/rest/login/v3/resendotp".format(uat)
        )
        self.verify_otp_url = (
            "https://{}openapi.motilaloswal.com/rest/login/v3/verifyotp".format(uat)
        )
        self.ltp_url = (
            "https://{}openapi.motilaloswal.com/rest/report/v1/getltpdata".format(uat)
        )
        self.place_order_url = (
            "https://{}openapi.motilaloswal.com/rest/trans/v1/placeorder".format(uat)
        )
        self.get_profile_url = (
            "https://{}openapi.motilaloswal.com/rest/login/v1/getprofile".format(uat)
        )
        self.margin_summary_url = "https://{}openapi.motilaloswal.com/rest/report/v1/getreportmarginsummary".format(
            uat
        )
        self.modify_order_url = (
            "https://{}openapi.motilaloswal.com/rest/trans/v2/modifyorder".format(uat)
        )
        self.order_book_url = (
            "https://{}openapi.motilaloswal.com/rest/book/v1/getorderbook".format(uat)
        )
        self.cancel_order_url = (
            "https://{}openapi.motilaloswal.com/rest/trans/v1/cancelorder".format(uat)
        )
        self.positions_url = (
            "https://{}openapi.motilaloswal.com/rest/book/v1/getposition".format(uat)
        )
        self.holdings_url = (
            "https://{}openapi.motilaloswal.com/rest/report/v1/getdpholding".format(uat)
        )
        self.order_details_url = "https://{}openapi.motilaloswal.com/rest/book/v2/getorderdetailbyuniqueorderid".format(
            uat
        )

        try:
            if headers:
                self.headers = headers
            elif (
                user_id is not None
                and password is not None
                and api_key is not None
                and two_fa is not None
                and totp
            ):
                self.generate_token(user_id, password, api_key, two_fa, totp)
            else:
                raise Exception("Missing Arguments")

            self.user_id = self.headers["vendorinfo"]

        except binascii.Error:
            raise TokenException("Invalid TOTP key provided")
        except InvalidArgumentException:
            raise
        except Exception as e:
            raise RetryableException(str(e))

        if load_instrument:
            self.load_instrument()

        self.order_type_sl = "STOPLOSS"
        self.nfo_exchange = "NSEFO"
        self.exchange_code_map = {"NFO": "NSEFO", "CDS": "NSECD", "BFO": "BSEFO"}

    def load_instrument(self, file_name: str | None = None) -> None:
        try:
            self.symbol_data = InstrumentData.get_instance().load_data(  # type: ignore
                "motilal_instruments"
            )
            Constants.logger.info("[LOADING_INSTRUMENTS] loading data from cache")
        except Exception:
            self.instrument_data = S3Utils.read_csv(
                "quantplay-market-data",
                "symbol_data/motilal_instruments.csv",
            )
            self.initialize_symbol_data(save_as="motilal_instruments")

        self.initialize_broker_symbol_map()

    def get_symbol(self, symbol: str, exchange: ExchangeType | None = None):
        if symbol not in self.quantplay_symbol_map:
            return symbol

        return self.quantplay_symbol_map[symbol]

    def get_motilal_symbol(self, symbol: str):
        if symbol not in self.quantplay_symbol_map:
            return symbol

        return self.quantplay_symbol_map[symbol]

    def get_order_type(self, order_type: OrderTypeType):
        if order_type == OrderType.sl:
            return "STOPLOSS"

        return order_type

    def get_exchange(self, exchange: ExchangeType):
        if exchange in self.exchange_code_map:
            return self.exchange_code_map[exchange]

        return exchange

    def get_product(self, product: ProductType):
        # TODO: Use Maps Instead
        if product == "CNC":
            return "DELIVERY"
        elif product == "NRML":
            return "NORMAL"
        elif product == "MIS":
            return "NORMAL"

        return product

    def place_order_quantity(
        self, quantity: int, tradingsymbol: str, exchange: ExchangeType
    ):
        lot_size = self.get_lot_size(exchange, tradingsymbol)
        quantity_in_lots = int(quantity / lot_size)

        return quantity_in_lots

    def get_lot_size(self, exchange: str, tradingsymbol: str):
        tradingsymbol = self.get_symbol(tradingsymbol)
        if exchange == "NSEFO":
            exchange = "NFO"
        elif exchange == "BSEFO":
            exchange = "BFO"
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

    def generate_token(
        self, user_id: str, password: str, api_key: str, two_fa: str, totp: str
    ):
        current_totp = pyotp.TOTP(str(totp)).now()
        Constants.logger.info("TOTP is {}".format(current_totp))
        # initializing string
        encoded_str = "{}{}".format(password, api_key)
        result = hashlib.sha256(encoded_str.encode())

        data = {
            "userid": user_id,
            "password": result.hexdigest(),
            "2FA": two_fa,
            "totp": current_totp,
        }

        self.headers["ApiKey"] = api_key
        self.headers["vendorinfo"] = user_id
        response = requests.post(self.url, headers=self.headers, data=json.dumps(data))

        resp_json = response.json()
        if "status" in resp_json and resp_json["status"] == "ERROR":
            raise InvalidArgumentException(resp_json["message"])
        Constants.logger.info("login response {}".format(resp_json))
        self.headers["Authorization"] = resp_json["AuthToken"]
        self.user_id = user_id

    def send_otp(self):
        response = requests.post(self.otp_url, headers=self.headers).json()
        Constants.logger.info(response)
        return response

    def verify_otp(self, otp: str):
        data = {"otp": otp}
        response = requests.post(
            self.verify_otp_url, headers=self.headers, data=json.dumps(data)
        ).json()
        Constants.logger.info(response)
        return response

    def ltp(self, exchange: ExchangeType, tradingsymbol: str) -> float:
        tradingsymbol = self.get_symbol(tradingsymbol)
        token = self.symbol_data["{}:{}".format(exchange, tradingsymbol)]["token"]
        motilal_exchange = self.get_exchange(exchange)
        data = {
            "userid": self.user_id,
            "exchange": motilal_exchange,
            "scripcode": token,
        }

        Constants.logger.info(f"[GET_LTP_REQUEST] response {data}")
        response = self.__post_request(self.ltp_url, data)
        Constants.logger.info(f"[GET_LTP_RESPONSE] response {response}")
        return response["data"]["ltp"] / 100.0

    def add_existing_order_details(self, order_to_modify: dict[str, str]):
        order_id = order_to_modify["order_id"]
        orders = self.orders()
        orders = orders.filter(pl.col("order_id") == order_id)

        if len(orders) != 1:
            raise InvalidArgumentException(
                f"Invalid modify request, order_id {order_id} not found"
            )

        order = orders.to_dicts()[0]
        order["last_modified_time"] = str(order["last_modified_time"])

        if "price" in order_to_modify:
            order["price"] = order_to_modify["price"]
        if (
            "trigger_price" in order_to_modify
            and order_to_modify["trigger_price"] is not None  # type:ignore
        ):
            order["trigger_price"] = order_to_modify["trigger_price"]

        if "order_type" in order_to_modify and order_to_modify["order_type"] == "SL":
            order["order_type"] = "STOPLOSS"

        return order

    def modify_price(
        self,
        order_id: str,
        price: float,
        trigger_price: float | None = None,
        order_type: OrderTypeType | None = None,
    ):
        order_to_modify = {
            "order_id": order_id,
            "price": price,
            "trigger_price": trigger_price,
            "order_type": order_type,
        }

        self.modify_order(order_to_modify)  # type: ignore

    def modify_order(self, order: Any) -> str:
        order = copy.deepcopy(order)  # type:ignore
        order = self.add_existing_order_details(order)

        data = {
            "uniqueorderid": order["order_id"],
            "newordertype": order["order_type"].upper(),
            "neworderduration": order["order_duration"].upper(),
            "newquantityinlot": int(order["pending_quantity"] / order["lot_size"]),
            # "newdisclosedquantity": 0,
            "newprice": order["price"],
        }

        if "trigger_price" in order:
            data["newtriggerprice"] = order["trigger_price"]
        if "quantity_traded_today" in order:
            data["qtytradedtoday"] = order["quantity_traded_today"]
        if "last_modified_time" in order:
            data["lastmodifiedtime"] = order["last_modified_time"]

        if "exchange" in order and order["exchange"] == "MCX":
            data["newquantityinlot"] = int(order["totalqtyremaining"])

        try:
            Constants.logger.info("[MODIFYING_ORDER] order [{}]".format(data))
            response = requests.post(
                self.modify_order_url, headers=self.headers, data=json.dumps(data)
            ).json()
            Constants.logger.info("[MODIFY_ORDER_RESPONSE] {}".format(response))
        except Exception as e:
            exception_message = f"[ORDER_MODIFICATION_FAILED] for {data['uniqueorderid']} failed with exception {e}"
            Constants.logger.error("{}".format(exception_message))
        return order["order_id"]

    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=2,
        retry_on_exception=retry_exception,
    )
    def cancel_order(self, order_id: str, variety: str | None = None) -> None:
        data = {"uniqueorderid": order_id}

        try:
            Constants.logger.info("Cancelling order [{}]".format(order_id))
            response = requests.post(
                self.cancel_order_url, headers=self.headers, data=json.dumps(data)
            ).json()
            if "errorcode" in response and response["errorcode"] in ["MO1066"]:
                Constants.logger.info(
                    f"[CANCEL_ORDER_RESPONSE] [{order_id}] already cancelled"
                )
                return
            elif "errorcode" in response and response["errorcode"] in ["MO5002"]:
                raise RetryableException("Retry due to network error")
            elif "errorcode" in response and response["errorcode"] in ["MO1060"]:
                # Invalid order Id
                return
            Constants.logger.info("Cancel order response [{}]".format(response))
        except Exception as e:
            exception_message = (
                "[ORDER_CANCELLATION_FAILED] unique_order_id {} exception {}".format(
                    order_id, e
                )
            )
            Constants.logger.error(exception_message)

    def margins(self) -> MarginsResponse:
        response = self.__post_request(self.margin_summary_url, {})
        margin_summary = response["data"]
        margin_used = 0
        margin_available = 0
        for margin_particular in margin_summary:
            if margin_particular["srno"] in [103]:
                margin_available += margin_particular["amount"]

            if margin_particular["srno"] in [301, 321, 340, 360]:
                margin_used += margin_particular["amount"]

        return {
            "margin_available": margin_available,
            "margin_used": margin_used,
            "total_balance": margin_used + margin_available,
            "cash": 0,
        }

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
    ):
        motilal_order_type = self.get_order_type(order_type)
        motilal_product = self.get_product(product)
        tradingsymbol = self.get_symbol(tradingsymbol)

        actual_exchange = copy.deepcopy(exchange)
        if actual_exchange == "NSEFO":
            actual_exchange = "NFO"
        elif actual_exchange == "BSEFO":
            actual_exchange = "BFO"
        token = self.symbol_data["{}:{}".format(actual_exchange, tradingsymbol)]["token"]

        motilal_exchange = self.get_exchange(exchange)
        quantity = self.place_order_quantity(quantity, tradingsymbol, exchange)

        data = {
            "exchange": motilal_exchange,
            "symboltoken": token,
            "buyorsell": transaction_type,
            "ordertype": motilal_order_type,
            "producttype": motilal_product,
            "orderduration": "DAY",
            "price": price,
            "triggerprice": trigger_price,
            "quantityinlot": quantity,
            "disclosedquantity": 0,
            "amoorder": "N",
            "algoid": "",
            "tag": tag,
        }
        try:
            Constants.logger.info("[PLACING_ORDER] {}".format(json.dumps(data)))
            response = requests.post(
                self.place_order_url, headers=self.headers, data=json.dumps(data)
            ).json()
            if "errorcode" in response and response["errorcode"] in ["100018"]:
                return
            Constants.logger.info(
                "[PLACE_ORDER_RESPONSE] {} input {}".format(response, json.dumps(data))
            )
            if response["status"] == "ERROR":
                raise QuantplayOrderPlacementException(response["message"])
            return response["uniqueorderid"]
        except QuantplayOrderPlacementException as e:
            raise e
        except Exception as e:
            exception_message = "Order placement failed with error [{}]".format(str(e))
            print(exception_message)

    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
        retry_on_exception=retry_exception,
    )
    def __post_request(self, url: str, data: Any):
        if not data:
            data = {"Clientcode": self.headers["vendorinfo"]}
        data = json.dumps(data)

        api_response = requests.post(
            url,
            headers=self.headers,
            data=data,
        ).json()

        if api_response["status"] == "ERROR" and api_response["errorcode"] in [
            "MO8001",
            "MO8002",
            "MO8003",
            "MO8050",
            "MO8051",
            "MO8052",
        ]:
            raise TokenException("Motilal token expired")
        elif api_response["status"] == "ERROR":
            raise RetryableException(api_response["message"])

        return api_response

    def profile(self) -> UserBrokerProfileResponse:
        api_response = self.__post_request(self.get_profile_url, {})

        api_response = api_response["data"]
        response: UserBrokerProfileResponse = {
            "user_id": api_response["clientcode"],
            "full_name": api_response["name"],
            "segments": api_response["exchanges"],
        }

        return response

    def holdings(self, add_ltp: bool = True) -> pl.DataFrame:
        response = self.__post_request(self.holdings_url, {})
        if response["status"] == "ERROR":
            Constants.logger.info(
                "Error while fetching order book [{}]".format(response["message"])
            )
            raise Exception(response["message"])

        holdings = response["data"]

        if holdings is None or len(holdings) == 0:
            return pl.DataFrame(schema=self.holidings_schema)

        holdings_df = pl.DataFrame(holdings)
        holdings_df = holdings_df.rename(
            {
                "scripname": "tradingsymbol",
                "scripisinno": "isin",
                "nsesymboltoken": "token",
                "buyavgprice": "average_price",
                "dpquantity": "quantity",
                "collateralquantity": "pledged_quantity",
            }
        )
        holdings_df = holdings_df.with_columns(pl.lit("NSE").alias("exchange"))
        holdings_df = holdings_df.with_columns(
            pl.struct(["exchange", "tradingsymbol"])
            .map_elements(
                lambda x: int(self.ltp(x["exchange"], x["tradingsymbol"])),
                return_dtype=pl.Float64,
            )
            .alias("price")
        )

        holdings_df = holdings_df.with_columns(
            pl.col("tradingsymbol").str.replace(" EQ", "").alias("tradingsymbol")
        )
        holdings_df = holdings_df.with_columns(
            (pl.col("quantity") * pl.col("price")).alias("value"),
            pl.lit(0).alias("pledged_quantity"),
            (pl.col("quantity") * pl.col("average_price")).alias("buy_value"),
            (pl.col("quantity") * pl.col("price")).alias("current_value"),
            ((pl.col("price") / pl.col("average_price") - 1) * 100).alias("pct_change"),
        )

        return holdings_df[list(self.holidings_schema.keys())].cast(self.holidings_schema)

    def positions(self, drop_cnc: bool = True) -> pl.DataFrame:
        response = self.__post_request(self.positions_url, {})
        if response["status"] == "ERROR":
            Constants.logger.info(
                "Error while fetching positions [{}]".format(response["message"])
            )
            raise Exception(response["message"])

        positions = response["data"]

        if positions is None or len(positions) == 0:
            return pl.DataFrame(schema=self.positions_schema)

        positions_df = pl.DataFrame(positions)
        positions_df = positions_df.rename(
            {
                "symbol": "tradingsymbol",
                "LTP": "ltp",
                "productname": "product",
                "sellquantity": "sell_quantity",
                "buyquantity": "buy_quantity",
                "sellamount": "sell_value",
                "buyamount": "buy_value",
                "optiontype": "option_type",
                "symboltoken": "token",
            }
        )

        positions_df = positions_df.with_columns(
            (pl.col("sell_value") - pl.col("buy_value")).alias("pnl")
        )
        positions_df = positions_df.with_columns(
            (
                pl.col("pnl")
                + (pl.col("buy_quantity") - pl.col("sell_quantity")) * pl.col("ltp")
            ).alias("pnl")
        )
        positions_df = positions_df.with_columns(
            (pl.col("buy_quantity") - pl.col("sell_quantity")).alias("quantity")
        )

        positions_df = positions_df.with_columns(
            pl.when(pl.col("exchange") == "NSEFO")
            .then(pl.lit("NFO"))
            .when(pl.col("exchange") == "BSEFO")
            .then(pl.lit("BFO"))
            .otherwise(pl.col("exchange"))
            .alias("exchange")
        )

        positions_df = positions_df.with_columns(
            pl.col("product").str.replace("NORMAL", "NRML").alias("product")
        )
        positions_df = positions_df.with_columns(
            ((pl.col("buy_value") - pl.col("sell_value")) / pl.col("quantity")).alias(
                "average_price"
            )
        )
        positions_df = positions_df.with_columns(
            pl.when(pl.col("quantity") == 0)
            .then(0)
            .otherwise(pl.col("average_price"))
            .alias("average_price")
        )

        return positions_df[list(self.positions_schema.keys())].cast(
            self.positions_schema
        )

    def orders(self, tag: str | None = None, add_ltp: bool = True) -> pl.DataFrame:
        response = self.__post_request(self.order_book_url, {})
        if response["status"] == "ERROR":
            Constants.logger.info(
                "Error while fetching order book [{}]".format(response["message"])
            )
            raise Exception(response["message"])
        orders = response["data"]

        if orders is None or len(orders) == 0:
            return pl.DataFrame(schema=self.orders_schema)

        orders_df = pl.DataFrame(orders)
        orders_df = orders_df.rename(
            {
                "symbol": "tradingsymbol",
                "producttype": "product",
                "clientid": "user_id",
                "symboltoken": "token",
                "buyorsell": "transaction_type",
                "averageprice": "average_price",
                "uniqueorderid": "order_id",
                "orderstatus": "status",
                "recordinserttime": "order_timestamp",
                "orderqty": "quantity",
                "triggerprice": "trigger_price",
                "totalqtytraded": "filled_quantity",
                "totalqtyremaining": "pending_quantity",
                "orderduration": "order_duration",
                "lastmodifiedtime": "last_modified_time",
                "qtytradedtoday": "quantity_traded_today",
                "lotsize": "lot_size",
                "ordertype": "order_type",
            }
        )
        if add_ltp:
            positions = self.positions()
            positions = positions.sort("product").group_by("tradingsymbol").head(1)

            if "ltp" in orders_df.columns:
                orders_df = orders_df.drop(["ltp"])
            orders_df = orders_df.join(
                positions.select(["tradingsymbol", "ltp"]), on="tradingsymbol", how="left"
            )
        else:
            orders_df = orders_df.with_columns(pl.lit(None).cast(pl.Float64).alias("ltp"))

        orders_df = orders_df.with_columns(
            pl.when(pl.col("product") == "VALUEPLUS")
            .then(pl.lit("MIS"))
            .when(pl.col("product") == "DELIVERY")
            .then(pl.lit("CNC"))
            .when(pl.col("product") == "NORMAL")
            .then(pl.lit("NRML"))
            .otherwise(pl.col("product"))
            .alias("product")
        )

        orders_df = orders_df.filter(pl.col("last_modified_time") != "0")

        orders_df = orders_df.with_columns(
            pl.col("last_modified_time")
            .str.to_datetime("%d-%b-%Y %H:%M:%S")
            .alias("update_timestamp")
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
            pl.when((pl.col("status") == "Confirm") & (pl.col("trigger_price") > 0))
            .then(pl.lit("TRIGGER PENDING"))
            .otherwise(pl.col("status"))
            .alias("status")
        )

        orders_df = orders_df.with_columns(
            pl.when((pl.col("status") == "Confirm") & (pl.col("trigger_price") == 0))
            .then(pl.lit("OPEN"))
            .otherwise(pl.col("status"))
            .alias("status")
        )

        if tag:
            orders_df = orders_df.filter(pl.col("tag") == tag)

        orders_df = orders_df.with_columns(
            pl.when(pl.col("status") == "Traded")
            .then(pl.lit("COMPLETE"))
            .when(pl.col("status") == "Error")
            .then(pl.lit("REJECTED"))
            .when(pl.col("status") == "Cancel")
            .then(pl.lit("CANCELLED"))
            .when(pl.col("status") == "Rejected")
            .then(pl.lit("REJECTED"))
            .otherwise(pl.col("status"))
            .alias("status")
        )

        orders_df = orders_df.with_columns(
            pl.when(pl.col("order_type") == "Stop Loss")
            .then(pl.lit("SL"))
            .otherwise(pl.col("order_type").str.to_uppercase())
            .alias("order_type")
        )

        orders_df = orders_df.with_columns(
            pl.when(pl.col("exchange") == "NSEFO")
            .then(pl.lit("NFO"))
            .when(pl.col("exchange") == "NSECD")
            .then(pl.lit("CDS"))
            .when(pl.col("exchange") == "BSEFO")
            .then(pl.lit("BFO"))
            .otherwise(pl.col("exchange"))
            .alias("exchange")
        )
        orders_df = orders_df.with_columns(
            pl.col("order_timestamp")
            .str.to_datetime("%d-%b-%Y %H:%M:%S")
            .alias("order_timestamp")
        )

        orders_schema = copy.deepcopy(self.orders_schema)
        orders_schema["last_modified_time"] = pl.String
        orders_schema["order_duration"] = pl.String
        orders_schema["quantity_traded_today"] = pl.Int64
        orders_schema["lot_size"] = pl.Int64
        orders_df = orders_df.with_columns(pl.lit("regular").alias("variety"))
        orders_df = orders_df.with_columns(pl.lit("").alias("status_message"))
        orders_df = orders_df.with_columns(pl.lit("").alias("status_message_raw"))

        return orders_df[list(orders_schema.keys())].cast(orders_schema)
