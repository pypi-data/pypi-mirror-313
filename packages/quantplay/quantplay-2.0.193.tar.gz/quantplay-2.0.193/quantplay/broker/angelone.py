import binascii
import copy
import json
import traceback
from queue import Queue
from typing import Any

import logzero  # type: ignore
import polars as pl
import pyotp
from requests.exceptions import ConnectionError, ConnectTimeout
from retrying import retry  # type: ignore
from SmartApi import SmartConnect  # type: ignore
from SmartApi.smartExceptions import DataException  # type: ignore

from quantplay.broker.generics.broker import Broker
from quantplay.exception.exceptions import (
    BrokerException,
    InvalidArgumentException,
    QuantplayOrderPlacementException,
    RetryableException,
    ServiceException,
    TokenException,
    retry_exception,
)
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
)
from quantplay.model.order_event import OrderUpdateEvent
from quantplay.utils.constant import Constants, OrderType
from quantplay.utils.exchange import Market as MarketConstants
from quantplay.utils.pickle_utils import InstrumentData
from quantplay.wrapper.aws.s3 import S3Utils

logzero.logger.disabled = True


class AngelOne(Broker):
    order_sl = "STOPLOSS_LIMIT"
    order_slm = "STOPLOSS_MARKET"

    def __init__(
        self,
        order_updates: Queue[OrderUpdateEvent] | None = None,
        api_key: str | None = None,
        user_id: str | None = None,
        mpin: str | None = None,
        totp: str | None = None,
        refresh_token: str | None = None,
        feed_token: str | None = None,
        access_token: str | None = None,
        load_instrument: bool = True,
    ) -> None:
        super().__init__()
        self.order_updates = order_updates

        try:
            if refresh_token:
                self.wrapper = SmartConnect(
                    api_key=api_key,
                    access_token=access_token,
                    refresh_token=refresh_token,
                    feed_token=feed_token,
                    timeout=7,
                )
                self.refresh_token = refresh_token
            else:
                if totp is None:
                    raise InvalidArgumentException("TOTP Key is Missing")

                self.wrapper = SmartConnect(api_key=api_key, timeout=30)
                response = self.invoke_angelone_api(
                    self.wrapper.generateSession,  # type: ignore
                    clientCode=user_id,
                    password=mpin,
                    totp=pyotp.TOTP(str(totp)).now(),
                )

                if not response["status"]:
                    if "message" in response:
                        raise InvalidArgumentException(response["message"])
                    raise InvalidArgumentException("Invalid API credentials")

                token_data = self.invoke_angelone_api(
                    self.wrapper.generateToken,  # type: ignore
                    refresh_token=self.wrapper.refresh_token,  # type: ignore
                )
                self.refresh_token = token_data["data"]["refreshToken"]

        except InvalidArgumentException:
            raise

        except binascii.Error:
            raise InvalidArgumentException("Invalid TOTP key provided")

        except Exception as e:
            traceback.print_exc()
            raise RetryableException(str(e))

        self.user_id = user_id
        self.api_key = self.wrapper.api_key  # type: ignore

        if load_instrument:
            self.load_instrument()

    def get_exchange(self, exchange: ExchangeType) -> Any:
        return exchange

    def load_instrument(self, file_name: str | None = None) -> None:
        try:
            instrument_data_instance = InstrumentData.get_instance()
            if instrument_data_instance is not None:
                self.symbol_data = instrument_data_instance.load_data(
                    "angelone_instruments"
                )
            Constants.logger.info("[LOADING_INSTRUMENTS] loading data from cache")
        except Exception:
            self.instrument_data = S3Utils.read_csv(
                "quantplay-market-data",
                "symbol_data/angelone_instruments.csv",
            )

            self.instrument_data["token"] = self.instrument_data["token"].astype(int)
            self.initialize_symbol_data(save_as="angelone_instruments")

        self.initialize_broker_symbol_map()

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

    def get_order_type(self, order_type: OrderTypeType | None):
        if order_type == OrderType.sl:
            return AngelOne.order_sl
        elif order_type == OrderType.slm:
            return AngelOne.order_slm

        return order_type

    def get_product(self, product: ProductType):
        if product == "NRML":
            return "CARRYFORWARD"
        elif product == "CNC":
            return "DELIVERY"
        elif product == "MIS":
            return "INTRADAY"
        elif product in ["BO", "MARGIN", "INTRADAY", "CARRYFORWARD", "DELIVERY"]:
            return product

        raise InvalidArgumentException(f"Product {product} not supported for trading")

    def ltp(self, exchange: ExchangeType, tradingsymbol: str) -> float:
        if tradingsymbol in MarketConstants.INDEX_SYMBOL_TO_DERIVATIVE_SYMBOL_MAP:
            tradingsymbol = MarketConstants.INDEX_SYMBOL_TO_DERIVATIVE_SYMBOL_MAP[
                tradingsymbol
            ]

        symbol_data = self.symbol_data[
            f"{exchange}:{self.get_symbol(tradingsymbol, exchange=exchange)}"
        ]
        symboltoken = symbol_data["token"]

        response = self.invoke_angelone_api(
            self.wrapper.ltpData,  # type: ignore
            exchange=exchange,
            tradingsymbol=tradingsymbol,
            symboltoken=symboltoken,
        )

        return response["data"]["ltp"]

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
        order = {}
        try:
            if trigger_price == 0:
                trigger_price = None

            angelone_order_type = self.get_order_type(order_type)
            angelone_product = self.get_product(product)
            tradingsymbol = self.get_symbol(tradingsymbol, exchange=exchange)

            variety = "NORMAL"
            if order_type in [AngelOne.order_sl, AngelOne.order_slm]:
                variety = "STOPLOSS"

            symbol_data = self.symbol_data[f"{exchange}:{self.get_symbol(tradingsymbol)}"]
            symbol_token = symbol_data["token"]

            order = {
                "transactiontype": transaction_type,
                "variety": variety,
                "tradingsymbol": tradingsymbol,
                "ordertype": angelone_order_type,
                "triggerprice": trigger_price,
                "exchange": exchange,
                "symboltoken": symbol_token,
                "producttype": angelone_product,
                "price": price,
                "quantity": quantity,
                "duration": "DAY",
                "ordertag": tag,
            }

            Constants.logger.info(f"[PLACING_ORDER] {json.dumps(order)}")
            return self.invoke_angelone_api(self.wrapper.placeOrder, orderparams=order)  # type: ignore

        except (TimeoutError, ConnectTimeout):
            Constants.logger.info(f"[ANGELONE_REQUEST_TIMEOUT] {order}")

        except Exception as e:
            traceback.print_exc()
            Constants.logger.error(f"[PLACE_ORDER_FAILED] {e} {order}")
            raise QuantplayOrderPlacementException(str(e))

    def get_variety(self, variety: str):
        if variety == "regular":
            return "NORMAL"
        return variety

    def modify_order(self, order: ModifyOrderRequest) -> str:
        data = copy.deepcopy(order)
        order_id = str(data["order_id"])
        try:
            orders = self.orders()
            filtered_order = orders.filter(pl.col("order_id") == str(data["order_id"]))
            order_data = filtered_order.to_dicts()[0]
            quantity = order_data["quantity"]
            token = order_data["token"]
            exchange = order_data["exchange"]
            product = self.get_product(order_data["product"])
            variety = order_data["variety"]
            order_type = self.get_order_type(data.get("order_type"))

            if "trigger_price" not in data:
                data["trigger_price"] = None

            if "quantity" in data and int(data["quantity"]) > 0:
                quantity = data["quantity"]

            order_id = data["order_id"]

            order_params = {
                "orderid": order_id,
                "variety": variety,
                "price": data.get("price"),
                "triggerprice": data["trigger_price"],
                "producttype": product,
                "duration": "DAY",
                "quantity": quantity,
                "symboltoken": token,
                "ordertype": order_type,
                "exchange": exchange,
                "tradingsymbol": self.get_symbol(
                    order_data["tradingsymbol"], exchange=exchange
                ),
            }

            Constants.logger.info(f"Modifying order [{order_id}] params [{order_params}]")
            response = self.invoke_angelone_api(
                self.wrapper.modifyOrder,  # type: ignore
                orderparams=order_params,
            )
            Constants.logger.info(f"[MODIFY_ORDER_RESPONSE] {response}")
            return order_id
        except Exception as e:
            traceback.print_exc()
            Constants.logger.error(
                f"[MODIFY_ORDER_FAILED] for {data['order_id']} failed with exception {e}"
            )
            raise

    def cancel_order(self, order_id: str, variety: str | None = "NORMAL"):
        self.wrapper.cancelOrder(order_id=order_id, variety=variety)  # type: ignore

    def holdings(self, add_ltp: bool = True) -> pl.DataFrame:
        holdings = self.invoke_angelone_api(self.wrapper.holding)

        if holdings["data"] is None or len(holdings["data"]) == 0:
            return pl.DataFrame(schema=self.holidings_schema)

        holdings = pl.from_dicts(holdings["data"])
        holdings = holdings.rename(
            {
                "averageprice": "average_price",
                "ltp": "price",
                "symboltoken": "token",
            }
        )

        holdings = holdings.with_columns(
            pl.lit(0).alias("pledged_quantity"),
            pl.col("tradingsymbol").str.replace("-EQ", "").alias("tradingsymbol"),
            (pl.col("quantity").mul(pl.col("average_price"))).alias("buy_value"),
            (pl.col("quantity").mul(pl.col("price"))).alias("current_value"),
            (((pl.col("price") / (pl.col("average_price"))).sub(1)).mul(100)).alias(
                "pct_change"
            ),
        )

        return holdings

    def positions(self, drop_cnc: bool = True):
        positions = self.invoke_angelone_api(self.wrapper.position)

        if positions["data"] is None:
            return pl.DataFrame(schema=self.positions_schema)

        positions_df = pl.from_dicts(positions["data"])

        if "optiontype" not in positions_df.columns:
            positions_df = positions_df.with_columns(pl.lit(None).alias("optiontype"))

        positions_df = positions_df.rename(
            {
                "optiontype": "option_type",
                "sellqty": "sell_quantity",
                "buyqty": "buy_quantity",
                "totalsellvalue": "sell_value",
                "totalbuyvalue": "buy_value",
                "producttype": "product",
                "symboltoken": "token",
            },
        )

        positions_df = positions_df.with_columns(
            (
                pl.col("buy_quantity").cast(pl.Int32) + pl.col("cfbuyqty").cast(pl.Int32)
            ).alias("buy_quantity")
        )
        positions_df = positions_df.with_columns(
            (
                pl.col("sell_quantity").cast(pl.Int64)
                + pl.col("cfsellqty").cast(pl.Int64)
            ).alias("sell_quantity")
        )
        positions_df = positions_df.with_columns(
            pl.col("pnl").cast(pl.Float64).alias("pnl"),
            pl.col("ltp").cast(pl.Float64).alias("ltp"),
            (pl.col("buy_quantity") - pl.col("sell_quantity")).alias("quantity"),
        )

        positions_df = positions_df.with_columns(
            pl.when(pl.col("product") == "DELIVERY")
            .then(pl.lit("CNC"))
            .when(pl.col("product") == "CARRYFORWARD")
            .then(pl.lit("NRML"))
            .when(pl.col("product") == "INTRADAY")
            .then(pl.lit("MIS"))
            .otherwise(pl.col("product"))
            .alias("product")
        )

        positions_df = positions_df.with_columns(
            (
                (
                    pl.col("buy_value").cast(pl.Float64)
                    - pl.col("sell_value").cast(pl.Float64)
                )
                / pl.col("quantity").cast(pl.Int32)
            ).alias("average_price")
        )
        positions_df = positions_df.with_columns(
            pl.when(pl.col("quantity") == 0)
            .then(pl.lit(0))
            .otherwise(pl.col("average_price"))
            .alias("average_price")
        )
        return positions_df[list(self.positions_schema.keys())].cast(
            self.positions_schema
        )

    def orders(self, tag: str | None = None, add_ltp: bool = True) -> pl.DataFrame:
        order_book = self.invoke_angelone_api(self.wrapper.orderBook)

        if order_book["data"]:
            orders_df = pl.DataFrame(order_book["data"])

            if len(orders_df) == 0:
                return pl.DataFrame(schema=self.orders_schema)

            if add_ltp:
                positions = self.positions()
                positions = positions.sort("product").group_by("tradingsymbol").head(1)

                if "ltp" in orders_df:
                    orders_df = orders_df.drop(["ltp"])
                orders_df = orders_df.join(
                    positions.select(["tradingsymbol", "ltp"]),
                    on="tradingsymbol",
                    how="left",
                )
            else:
                orders_df = orders_df.with_columns(pl.lit(None).alias("ltp"))

            orders_df = orders_df.rename(
                {
                    "orderid": "order_id",
                    "ordertag": "tag",
                    "averageprice": "average_price",
                    "producttype": "product",
                    "transactiontype": "transaction_type",
                    "triggerprice": "trigger_price",
                    "price": "price",
                    "filledshares": "filled_quantity",
                    "unfilledshares": "pending_quantity",
                    "updatetime": "order_timestamp",
                    "ordertype": "order_type",
                    "symboltoken": "token",
                }
            )

            orders_df = orders_df.with_columns(
                pl.col("order_timestamp")
                .str.to_datetime("%d-%b-%Y %H:%M:%S")
                .alias("order_timestamp")
            )
            orders_df = orders_df.with_columns(
                pl.col("order_timestamp").alias("update_timestamp")
            )

            if tag:
                orders_df = orders_df.filter(pl.col("tag") == tag)

            orders_df = orders_df.with_columns(
                pl.when(pl.col("status") == "open")
                .then(pl.lit("OPEN"))
                .when(pl.col("status") == "cancelled")
                .then(pl.lit("CANCELLED"))
                .when(pl.col("status") == "trigger pending")
                .then(pl.lit("TRIGGER PENDING"))
                .when(pl.col("status") == "complete")
                .then(pl.lit("COMPLETE"))
                .when(pl.col("status") == "rejected")
                .then(pl.lit("REJECTED"))
                .otherwise(pl.col("status"))
                .alias("status"),
                pl.when(pl.col("product") == "DELIVERY")
                .then(pl.lit("CNC"))
                .when(pl.col("product") == "CARRYFORWARD")
                .then(pl.lit("NRML"))
                .when(pl.col("product") == "INTRADAY")
                .then(pl.lit("MIS"))
                .otherwise(pl.col("product"))
                .alias("product"),
                pl.when(pl.col("order_type") == AngelOne.order_sl)
                .then(pl.lit(OrderType.sl))
                .when(pl.col("order_type") == AngelOne.order_slm)
                .then(pl.lit(OrderType.slm))
                .otherwise(pl.col("order_type"))
                .alias("order_type"),
                pl.lit(self.user_id).alias("user_id"),
                pl.col("text").alias("status_message"),
                pl.col("text").alias("status_message_raw"),
            )

            return orders_df.select(list(self.orders_schema.keys())).cast(
                self.orders_schema
            )

        else:
            if "message" in order_book and order_book["message"] == "SUCCESS":
                return pl.DataFrame(schema=self.orders_schema)

            if "errorcode" in order_book and order_book["errorcode"] == "AB1010":
                raise TokenException("Can't Fetch order book because session got expired")

            else:
                Constants.logger.error(order_book)
                traceback.print_exc()
                raise ServiceException("Unknown error while fetching order book [{}]")

    def profile(self):
        profile_data = self.invoke_angelone_api(
            self.wrapper.getProfile,  # type: ignore
            refreshToken=self.refresh_token,
        )

        profile_data = profile_data["data"]
        response: UserBrokerProfileResponse = {
            "user_id": profile_data["clientcode"],
            "full_name": profile_data["name"],
            "email": profile_data["email"],
        }

        return response

    def margins(self) -> MarginsResponse:
        api_margins = self.invoke_angelone_api(self.wrapper.rmsLimit)

        if "data" in api_margins and api_margins["data"] is None:
            if "errorcode" in api_margins and api_margins["errorcode"] == "AB1004":
                raise TokenException("Angelone server not not responding")

            return {
                "margin_used": 0.0,
                "margin_available": 0.0,
                "total_balance": 0.0,
                "cash": 0,
            }

        api_margins = api_margins["data"]

        try:
            margin_used = float(api_margins["utiliseddebits"])
            margin_available = float(api_margins["net"])

            margins: MarginsResponse = {
                "margin_used": margin_used,
                "margin_available": margin_available,
                "cash": float(api_margins["availablecash"]),
                "total_balance": margin_used + margin_available,
            }

            return margins

        except (ConnectionError, ConnectTimeout):
            raise BrokerException("Angelone broker error while fetching margins")

        except Exception as e:
            raise RetryableException(f"Angelone: Failed to fetch margin {e}")

    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
        retry_on_exception=retry_exception,
    )
    def invoke_angelone_api(self, fn: Any, *args: Any, **kwargs: Any) -> Any:
        try:
            response = fn(*args, **kwargs)
            if "errorCode" in response and response["errorCode"] == "AG8001":
                raise TokenException(f"{self.user_id}: Invalid Token")

            elif isinstance(response, bytes):
                raise InvalidArgumentException(
                    "Invalid data response. AngelOne sent incorrect data, Please check."
                )

            return response

        except (TokenException, InvalidArgumentException):
            raise

        except DataException as e:
            if "Access denied because of exceeding access rate" in str(e):
                raise RetryableException(str(e))

            raise BrokerException(str(e))

        except Exception as e:
            traceback.print_exc()
            raise RetryableException(str(e))
