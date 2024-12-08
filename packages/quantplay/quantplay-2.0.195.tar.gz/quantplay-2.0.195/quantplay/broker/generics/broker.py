import copy
import io
import json
import math
import os
import platform
import random
import re
import threading
import time
import traceback
import zipfile
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from queue import Queue
from threading import Lock
from typing import Any, Literal, Type

import pandas as pd  # type:ignore
import polars as pl
import requests
from cachetools import TTLCache, cached

from quantplay.exception.exceptions import (
    FeatureNotSupported,
    InvalidArgumentException,
    StaleDataFound,
)
from quantplay.model.broker import (
    ExchangeType,
    MarginsResponse,
    ModifyOrderRequest,
    UserBrokerProfileResponse,
)
from quantplay.model.generics import (
    OrderTypeType,
    ProductType,
    QuantplayOrder,
    TransactionType,
)
from quantplay.model.instrument_data import InstrumentDataType
from quantplay.model.order_event import OrderUpdateEvent
from quantplay.utils.constant import Constants
from quantplay.utils.number_utils import NumberUtils
from quantplay.utils.pickle_utils import InstrumentData, PickleUtils
from quantplay.wrapper.aws.s3 import S3Utils
from quantplay.wrapper.redis import Redis

logger = Constants.logger

status_to_log_map = {
    "error": logger.error,
    "info": logger.info,
    "warn": logger.warning,
    "debug": logger.debug,
}


class Broker(ABC):
    orders_schema: dict[
        Any,
        Type[pl.String] | Type[pl.Float64] | Type[pl.Int64] | pl.Datetime,
    ] = {
        "user_id": pl.String,
        "order_id": pl.String,
        "exchange": pl.String,
        "tradingsymbol": pl.String,
        "product": pl.String,
        "variety": pl.String,
        "status": pl.String,
        "order_type": pl.String,
        "transaction_type": pl.String,
        "tag": pl.String,
        "price": pl.Float64,
        "average_price": pl.Float64,
        "trigger_price": pl.Float64,
        "ltp": pl.Float64,
        "order_timestamp": pl.Datetime(time_unit="ms"),
        "update_timestamp": pl.Datetime(time_unit="ms"),
        "token": pl.Int64,
        "quantity": pl.Int64,
        "pending_quantity": pl.Int64,
        "filled_quantity": pl.Int64,
        "status_message": pl.String,
        "status_message_raw": pl.String,
    }

    positions_schema: dict[
        Any,
        Type[pl.String] | Type[pl.Float64] | Type[pl.Int64],
    ] = {
        "tradingsymbol": pl.String,
        "sell_value": pl.Float64,
        "average_price": pl.Float64,
        "quantity": pl.Int64,
        "buy_value": pl.Float64,
        "product": pl.String,
        "ltp": pl.Float64,
        "pnl": pl.Float64,
        "token": pl.Int64,
        "exchange": pl.String,
        "sell_quantity": pl.Int64,
        "option_type": pl.String,
        "buy_quantity": pl.Int64,
    }

    holidings_schema: dict[
        Any,
        Type[pl.String] | Type[pl.Float64] | Type[pl.Int64],
    ] = {
        "tradingsymbol": pl.String,
        "exchange": pl.String,
        "token": pl.Int64,
        "isin": pl.String,
        "quantity": pl.Int64,
        "pledged_quantity": pl.Int64,
        "average_price": pl.Float64,
        "price": pl.Float64,
        "buy_value": pl.Float64,
        "current_value": pl.Float64,
        "pct_change": pl.Float64,
    }
    redis_client = Redis.get_instance()

    def __init__(self) -> None:
        self.instrument_data = pd.DataFrame()
        self.quantplay_symbol_map: dict[str, str] = {}
        self.broker_symbol_map: dict[str, str] = {}

        self.order_type_sl = "SL"
        self.nfo_exchange = "NFO"

        self.user_id: str | None = None
        self.username: str | None = None
        self.nickname: str | None = None
        self.broker_name: str | None = None

        self.order_updates: Queue[OrderUpdateEvent] | None = Queue()

        self.trigger_pending_status = "TRIGGER PENDING"
        self.lock = Lock()
        self.square_off_lock = Lock()

    def symbol_attribute(self, exchange: ExchangeType, symbol: str, value: str) -> Any:
        try:
            return_value: Any = self.symbol_data[f"{exchange}:{symbol}"][value]
            return return_value

        except KeyError:
            logger.error(
                f"[MISSING_SYMBOL_DATA] for [{exchange}:{symbol}] attribute {value}"
            )
            raise StaleDataFound(f"Couldn't find symbol data for [{exchange}:{symbol}]")

    def initialize_symbol_data_v2(self, save_as: str | None = None) -> None:
        instruments_df: pl.DataFrame = self.instrument_data  # type:ignore
        instruments: list[InstrumentDataType] = instruments_df.to_dicts()  # type: ignore

        self.symbol_data: dict[str, InstrumentDataType] = {}
        for instrument in instruments:
            exchange = instrument["exchange"]
            tradingsymbol = instrument["broker_symbol"]

            if tradingsymbol:
                instrument_data = copy.deepcopy(instrument)
                self.symbol_data[f"{exchange}:{tradingsymbol}"] = instrument_data

        if save_as:
            PickleUtils.save_data(self.symbol_data, save_as)

    def initialize_symbol_data(self, save_as: str | None = None) -> None:
        instruments_df = self.instrument_data
        instruments: list[InstrumentDataType] = instruments_df.to_dict("records")  # type: ignore

        self.symbol_data: dict[str, InstrumentDataType] = {}
        for instrument in instruments:
            exchange = instrument["exchange"]
            tradingsymbol = instrument["broker_symbol"]

            instrument_data = copy.deepcopy(instrument)
            self.symbol_data[f"{exchange}:{tradingsymbol}"] = instrument_data

        if save_as:
            PickleUtils.save_data(self.symbol_data, save_as)

    def initialize_broker_symbol_map(self) -> None:
        self.broker_symbol_map = {}
        for a in self.symbol_data:
            self.broker_symbol_map[self.symbol_data[a]["broker_symbol"]] = (
                self.symbol_data[a]["tradingsymbol"]
            )
        platform_version = platform.python_version().split(".")
        if (
            len(platform_version) >= 2
            and platform_version[0] == "3"
            and platform_version[1] == "8"
        ):
            self.quantplay_symbol_map: dict[str, str] = {}
            for k in self.broker_symbol_map:
                v = self.broker_symbol_map[k]
                self.quantplay_symbol_map[v] = k
        else:
            self.quantplay_symbol_map = {v: k for k, v in self.broker_symbol_map.items()}

    def data_with_quantplay_symbol(self, data: pl.DataFrame) -> pl.DataFrame:
        data = data.with_columns(
            pl.struct(["tradingsymbol"])
            .map_elements(
                lambda x: self.get_quantplay_symbol(x["tradingsymbol"]),
                return_dtype=pl.String,
            )
            .alias("tradingsymbol")
        )
        return data

    def load_instrument(self, file_name: str) -> None:
        try:
            instrument_data_instance = InstrumentData.get_instance()

            if instrument_data_instance is not None:
                self.symbol_data = instrument_data_instance.load_data(file_name)

            Constants.logger.info("[LOADING_INSTRUMENTS] loading data from cache")
        except Exception:
            self.instrument_data = S3Utils.read_csv(
                "quantplay-market-data",
                f"symbol_data/{file_name}.csv",
            )
            self.initialize_symbol_data(save_as=file_name)

        self.initialize_broker_symbol_map()

    def round_to_tick(self, number: int | float) -> float:
        return round(number * 20) / 20

    def get_df_from_zip(self, url: str) -> pd.DataFrame:
        response = requests.get(url, timeout=10)
        z = zipfile.ZipFile(io.BytesIO(response.content))

        directory = "/tmp/"
        z.extractall(path=directory)
        file_name = url.split(".txt")[0].split("/")[-1]
        os.system(f"cp /tmp/{file_name}.txt /tmp/{file_name}.csv")
        time.sleep(2)

        return pd.read_csv(f"/tmp/{file_name}.csv")  # type: ignore

    @cached(cache=TTLCache(maxsize=1, ttl=2))  # type: ignore
    def cached_orders(self, tag: str | None = None, add_ltp: bool = True) -> pl.DataFrame:
        return self.orders(tag, add_ltp)

    @cached(cache=TTLCache(maxsize=1, ttl=2))  # type: ignore
    def cached_positions(self, drop_cnc: bool = True) -> pl.DataFrame:
        return self.positions(drop_cnc)

    def get_symbol(self, symbol: str, exchange: ExchangeType | None = None) -> str:
        return symbol

    """
        Input  : quantplay exchange
        Output : broker exchange
    """

    def live_data(
        self, exchange: ExchangeType, tradingsymbol: str
    ) -> dict[str, float | None]:
        return {
            "ltp": self.ltp(exchange, tradingsymbol),
            "upper_circuit": None,
            "lower_circuit": None,
        }

    def basket_margin(self, basket_orders: list[Any]) -> dict[str, Any]:
        raise FeatureNotSupported("Margin calculator not supported by broker")

    def verify_rms_square_off(
        self,
        stoploss: float | None,
        target: float | None,
        keep_hedges: bool = False,
        ticks: int = 1,
    ) -> dict[str, bool | float]:
        positions = self.positions()
        pnl = positions["pnl"].sum()

        positions = positions.filter(pl.col("product") != "CNC")
        if keep_hedges:
            positions = positions.filter(
                ~(pl.col("option_type").is_in(["CE", "PE"]) & (pl.col("quantity").gt(0)))
            )

        if len(positions.filter(pl.col("quantity").ne(0))) == 0:
            return {"should_exit": False, "pnl": pnl}
        # Account level stoploss

        if stoploss is not None and pnl < stoploss:
            if ticks > 0:
                time.sleep(1)
                return self.verify_rms_square_off(stoploss, target, ticks=ticks - 1)
            logger.critical(
                f"[RMS_WARNING] pnl[{pnl}] went below stoploss [{stoploss}] for user {self.profile()}"
            )
            return {"should_exit": True, "pnl": pnl}
        if target is not None and pnl > target:
            if ticks > 0:
                time.sleep(1)
                return self.verify_rms_square_off(stoploss, target, ticks=ticks - 1)
            logger.critical(
                f"[RMS_WARNING] pnl[{pnl}] went above target[{target}] for user {self.profile()}"
            )
            return {"should_exit": True, "pnl": pnl}

        return {"should_exit": False, "pnl": pnl}

    def place_order_quantity(
        self, quantity: int, tradingsymbol: str, exchange: ExchangeType
    ) -> int:
        lot_size = self.get_lot_size(exchange, tradingsymbol)
        quantity_in_lots = int(quantity / lot_size)

        return quantity_in_lots * lot_size

    def get_lot_size(self, exchange: ExchangeType, tradingsymbol: str) -> int:
        tradingsymbol = self.get_symbol(tradingsymbol, exchange=exchange)
        broker_exchange = self.get_exchange(exchange)
        if broker_exchange == "BSE" or broker_exchange == "NSE":
            return 1
        try:
            return int(
                self.symbol_data["{}:{}".format(broker_exchange, tradingsymbol)][
                    "lot_size"
                ]
            )
        except Exception:
            logger.error(
                f"[GET_LOT_SIZE] unable to get lot size for {broker_exchange} {tradingsymbol}"
            )
            raise

    def filter_orders(
        self, orders: pl.DataFrame, tag: str | None = None, status: str | None = None
    ) -> pl.DataFrame:
        if tag:
            orders = orders.filter(pl.col("tag") == tag)

        if status:
            orders = orders.filter(pl.col("status") == status)

        return orders

    def exit_all_trigger_orders(
        self,
        tag: str = "ALL",
        symbol_contains: str | None = None,
        order_timestamp: str | None = None,
        modify_sleep_time: float = 10,
    ) -> None:
        stoploss_orders = self.orders()
        stoploss_orders = stoploss_orders.filter(pl.col("status") == "TRIGGER PENDING")

        if len(stoploss_orders) == 0:
            Constants.logger.info("All stoploss orders have been already closed")
            return

        if tag != "ALL":
            stoploss_orders = stoploss_orders.filter(pl.col("tag") == tag)

        if symbol_contains is not None:
            symbol_contains = self.get_symbol(symbol_contains)
            stoploss_orders = stoploss_orders.filter(
                pl.col("tradingsymbol").str.contains(symbol_contains)
            )

        if order_timestamp is not None:
            stoploss_orders = stoploss_orders.with_columns(
                pl.struct(["order_timestamp"])
                .map_elements(
                    lambda x: x["order_timestamp"].replace(second=0),
                    return_dtype=pl.Datetime,
                )
                .alias("order_timestamp")
            )

            stoploss_orders = stoploss_orders.filter(
                pl.col("order_timestamp").dt.strftime("%Y-%m-%d %H:%M:%S")
                == order_timestamp
            )

        if len(stoploss_orders) == 0:
            Constants.logger.info("All stoploss orders have been already closed")
            return

        orders_to_close = list(stoploss_orders["order_id"].unique())

        stoploss_orders = stoploss_orders.to_dicts()
        for stoploss_order in stoploss_orders:
            exchange = stoploss_order["exchange"]
            tradingsymbol = stoploss_order["tradingsymbol"]

            ltp = self.ltp(exchange, tradingsymbol)
            stoploss_order["order_type"] = "LIMIT"
            stoploss_order["price"] = self.round_to_tick(ltp)
            stoploss_order["trigger_price"] = None

            self.modify_order(stoploss_order)  # type: ignore
            time.sleep(0.1)

        self.modify_orders_till_complete(orders_to_close, sleep_time=modify_sleep_time)
        Constants.logger.info("All order have been closed successfully")

    def market_protection_price(
        self,
        price: float,
        transaction_type: Literal["BUY", "SELL"],
        market_protection: float = 0.02,
    ) -> float:
        if transaction_type == "BUY":
            price = self.round_to_tick(price * (1 + market_protection))
            return price + 1

        elif transaction_type == "SELL":
            return self.round_to_tick(price * (1 - market_protection))

    def split_order(
        self,
        exchange: ExchangeType,
        tradingsymbol: str,
        quantity: int,
        max_qty: int | None = None,
    ) -> list[int]:
        max_lots = self.symbol_max_lots(exchange, tradingsymbol)
        lot_size = self.get_lot_size(exchange, tradingsymbol)

        quantity_in_lots = int(quantity / lot_size)
        if max_qty:
            max_lots = max_qty / lot_size

        split_into = int(math.ceil(quantity_in_lots / max_lots))
        split_array = NumberUtils.split(abs(quantity_in_lots), abs(split_into))
        return [a * lot_size for a in split_array]

    def cancel_open_orders(self, tradingsymbols: list[str] | None = None):
        open_orders = self.orders()
        open_orders = open_orders.filter(
            pl.col("status").is_in(["OPEN", "TRIGGER PENDING"])
        )

        if tradingsymbols is not None:
            tradingsymbols = list(set(tradingsymbols))
            open_orders = open_orders.filter(
                pl.col("tradingsymbol").is_in(tradingsymbols)
            )

        order_ids = open_orders["order_id"].to_list()
        for order_id in order_ids:
            self.cancel_order(order_id)
            time.sleep(0.1)

    def square_off_all(
        self,
        dry_run: bool = True,
        contains: str | None = None,
        option_type: Literal["CE", "PE"] | None = None,
        sleep_time: float = 0.1,
        keep_hedges: bool = False,
        modify_sleep_time: float = 5,
        max_modification_count: int = 10,
        market_protection: float = 0.02,
    ) -> list[dict[str, Any]]:
        positions = self.positions()
        positions = positions.filter(pl.col("product") != "CNC")

        if option_type and "option_type" in positions.columns:
            positions = positions.filter(pl.col("option_type") == option_type)

        if contains:
            positions = positions.filter(pl.col("tradingsymbol").str.contains(contains))

        positions = positions.with_columns(
            (pl.col("buy_quantity") - pl.col("sell_quantity")).alias("net_quantity")
        )
        positions = positions.filter(pl.col("net_quantity") != 0)

        if keep_hedges:
            positions = positions.filter(
                ~((pl.col("option_type").is_in(["CE", "PE"])) & (pl.col("quantity") > 0))
            )
        if len(positions) == 0:
            print("Positions are already squared off")
            return []

        positions = positions.with_columns(
            pl.when(pl.col("quantity") < 0)
            .then(pl.lit("BUY"))
            .otherwise(pl.lit("SELL"))
            .alias("transaction_type")
        )

        positions = positions.with_columns(
            pl.struct(["exchange", "tradingsymbol"])
            .map_elements(
                lambda x: int(self.get_lot_size(x["exchange"], x["tradingsymbol"])),
                return_dtype=pl.Int64,
            )
            .alias("lot_size")
        )

        positions = positions.with_columns(
            pl.struct(["exchange", "tradingsymbol"])
            .map_elements(
                lambda x: float(self.ltp(x["exchange"], x["tradingsymbol"])),
                return_dtype=pl.Float64,
            )
            .alias("price")
        )

        positions = positions.to_dicts()
        orders_to_close: list[dict[str, Any]] = []
        for position in positions:
            quantity = abs(position["net_quantity"])
            exchange = position["exchange"]
            tradingsymbol = position["tradingsymbol"]
            transaction_type = position["transaction_type"]

            quantity_in_lots = int(quantity / self.get_lot_size(exchange, tradingsymbol))

            max_lots = self.symbol_max_lots(exchange, tradingsymbol)
            split_into = int(math.ceil(quantity_in_lots / max_lots))
            split_array = NumberUtils.split(abs(quantity_in_lots), abs(split_into))

            for q in split_array:
                orders_to_close.append(
                    {
                        "symbol": tradingsymbol,
                        "exchange": exchange,
                        "transaction_type": transaction_type,
                        "quantity_in_lots": q,
                        "product": position["product"],
                        "price": position["price"],
                    }
                )

        random.shuffle(orders_to_close)
        orders_to_close = sorted(orders_to_close, key=lambda d: d["transaction_type"])

        tradingsymbols = [a["symbol"] for a in orders_to_close]
        if not dry_run:
            self.cancel_open_orders(tradingsymbols)

        orders_placed: list[str] = []
        for order in orders_to_close:
            quantity = int(
                order["quantity_in_lots"]
                * self.get_lot_size(order["exchange"], order["symbol"])
            )
            order["price"] = self.market_protection_price(
                order["price"],
                order["transaction_type"],
                market_protection=market_protection,
            )
            print(
                order["symbol"],
                order["exchange"],
                order["transaction_type"],
                quantity,
                order["price"],
            )
            if not dry_run:
                order_id = self.place_order(
                    tradingsymbol=order["symbol"],
                    exchange=order["exchange"],
                    quantity=quantity,
                    order_type="LIMIT",
                    transaction_type=order["transaction_type"],
                    tag="killall",
                    product=order["product"],
                    price=order["price"],
                )
                orders_placed.append(str(order_id))
                time.sleep(sleep_time)
        if not dry_run:
            self.modify_orders_till_complete(
                orders_placed,
                sleep_time=modify_sleep_time,
                max_modification_count=max_modification_count,
            )

        return orders_to_close

    def convert_to_event(self, order: Any) -> None:
        if self.order_updates is None:
            raise Exception("Event Queue Not Initalised")

        order = copy.deepcopy(order)
        order["placed_by"] = self.user_id

        order["exchange_order_id"] = order["order_id"]
        order["quantity"] = int(order["quantity"])
        order["tradingsymbol"] = self.get_quantplay_symbol(order["tradingsymbol"])

        order["order_timestamp"] = str(order["order_timestamp"])
        order["update_timestamp"] = str(order["update_timestamp"])

        if "trigger_price" in order and order["trigger_price"] != 0:
            order["trigger_price"] = float(order["trigger_price"])
        else:
            order["trigger_price"] = None
        Constants.logger.info(f"[ORDER_EVENT] {order}")

        if order["status"] == "COMPLETE":
            order["status"] = "OPEN"
            self.order_updates.put(copy.deepcopy(order))
            order["status"] = "COMPLETE"
            time.sleep(1)

        self.order_updates.put(order)

    def get_quantplay_symbol(self, symbol: str) -> str:
        return self.broker_symbol_map[symbol]

    def stream_order_updates(self) -> None:
        self.order_log: dict[str, Any] = {}
        while 1:
            try:
                orders = self.orders(add_ltp=False)

                if len(orders) > 0:
                    delta_time = str(
                        datetime.now().replace(microsecond=0) - timedelta(seconds=120)
                    )
                    orders = orders.filter(
                        pl.col("update_timestamp").dt.strftime("%Y-%m-%d %H:%M:%S")
                        >= delta_time
                    )

                    orders = orders.to_dicts()
                    orders = sorted(orders, key=lambda d: d["transaction_type"])
                    for order in orders:
                        order_id = order["order_id"]
                        if "status" in order and order["status"].lower() in [
                            "partly executed"
                        ]:
                            continue

                        if order_id not in self.order_log:
                            self.convert_to_event(order)
                        else:
                            update_timestamp = str(order["update_timestamp"])
                            last_log_time = str(
                                self.order_log[order_id]["update_timestamp"]
                            )

                            if update_timestamp != last_log_time:
                                self.convert_to_event(order)

                        self.order_log[order_id] = copy.deepcopy(order)
                time.sleep(3)
            except Exception:
                traceback.print_exc()
                print(f"Unable to process order stream for {self.user_id}")
                time.sleep(5)

    def stream_order_data(self) -> None:
        th = threading.Thread(target=self.stream_order_updates, daemon=True)
        th.start()

    def underlying_config(
        self, underlying_symbol: str, expiry: str | None = None
    ) -> dict[str, int]:
        if underlying_symbol in ["BANKNIFTY", "BANKEX"]:
            return {"max_lots": 60, "lot_size": 15, "strike_gap": 100}
        elif underlying_symbol == "FINNIFTY":
            return {"max_lots": 72, "lot_size": 25, "strike_gap": 50}
        elif underlying_symbol == "SENSEX":
            return {"max_lots": 100, "lot_size": 10, "strike_gap": 100}
        elif underlying_symbol == "NIFTY":
            return {"max_lots": 72, "lot_size": 25, "strike_gap": 50}
        elif underlying_symbol == "MIDCPNIFTY":
            return {"max_lots": 56, "lot_size": 50, "strike_gap": 25}

        raise Exception(f"Underlying {underlying_symbol} symbol not supported")

    def symbol_max_lots(self, exchange: ExchangeType, symbol: str) -> int:
        try:
            if symbol in self.broker_symbol_map:
                symbol = self.broker_symbol_map[symbol]
            if "BANKNIFTY" in symbol and exchange == "NFO":
                return self.underlying_config("BANKNIFTY")["max_lots"]
            elif "FINNIFTY" in symbol and exchange == "NFO":
                return self.underlying_config("FINNIFTY")["max_lots"]
            elif "MIDCPNIFTY" in symbol and exchange == "NFO":
                return self.underlying_config("MIDCPNIFTY")["max_lots"]
            elif "NIFTY" in symbol and exchange == "NFO":
                return self.underlying_config("NIFTY")["max_lots"]
            elif "BANKEX" in symbol and exchange == "BFO":
                return self.underlying_config("BANKEX")["max_lots"]
            elif "SENSEX" in symbol and exchange == "BFO":
                return self.underlying_config("SENSEX")["max_lots"]
            elif exchange == "NSE":
                max_qty = int(500000 / self.ltp(exchange, symbol))
                if max_qty == 0:
                    return 1
                return max_qty
            return 36
        except Exception:
            traceback.print_exc()
            logger.error(f"Couldn't compute freeze quantity for {exchange} {symbol}")
            return 25

    def square_off_by_tag(
        self, tag: str, dry_run: bool = True, sleep_time: float = 0.05
    ) -> list[dict[str, Any]]:
        self.exit_all_trigger_orders(tag=tag)
        orders = self.orders(tag=tag)

        if len(orders) == 0:
            logger.info(
                f"All positions with tag {tag} are already squared-off for {self.profile()}"
            )
        orders = orders.with_columns(
            pl.when(pl.col("transaction_type") == "BUY")
            .then(-pl.col("filled_quantity"))
            .otherwise(pl.col("filled_quantity"))
            .alias("exit_quantity")
        )

        exit_orders = orders.group_by("tradingsymbol").agg(
            [
                pl.sum("exit_quantity").alias("exit_quantity"),
                pl.col("exchange").first().alias("exchange"),
                pl.col("product").first().alias("product"),
            ]
        )

        orders_to_close: list[dict[str, Any]] = []
        exit_orders = exit_orders.filter(pl.col("exit_quantity") != 0)
        positions = exit_orders.to_dicts()
        for position in positions:
            exchange = position["exchange"]
            tradingsymbol = position["tradingsymbol"]
            quantity = position["exit_quantity"]

            transaction_type = "SELL"
            if quantity == 0:
                continue
            elif quantity > 0:
                transaction_type = "BUY"

            quantity = abs(quantity)
            quantity_in_lots = int(quantity / self.get_lot_size(exchange, tradingsymbol))

            split_into = int(math.ceil(quantity_in_lots / 25))
            split_array = NumberUtils.split(abs(quantity_in_lots), abs(split_into))

            for q in split_array:
                orders_to_close.append(
                    {
                        "tradingsymbol": tradingsymbol,
                        "exchange": exchange,
                        "transaction_type": transaction_type,
                        "quantity_in_lots": q,
                        "product": position["product"],
                    }
                )

        random.shuffle(orders_to_close)
        orders_to_close = sorted(orders_to_close, key=lambda d: d["transaction_type"])
        for order in orders_to_close:
            tradingsymbol = order["tradingsymbol"]
            exchange = order["exchange"]
            transaction_type = order["transaction_type"]
            product = order["product"]
            quantity = order["quantity_in_lots"] * self.get_lot_size(
                exchange, tradingsymbol
            )
            quantity = self.place_order_quantity(quantity, tradingsymbol, exchange)

            print(tradingsymbol, exchange, transaction_type, quantity)
            if not dry_run:
                self.place_order(
                    tradingsymbol=tradingsymbol,
                    exchange=exchange,
                    quantity=quantity,
                    order_type="MARKET",
                    transaction_type=transaction_type,
                    tag=tag,
                    product=product,
                    price=0,
                )
                time.sleep(sleep_time)

        return orders_to_close

    def modify_price(
        self,
        order_id: str,
        price: float,
        trigger_price: float | None = None,
        order_type: OrderTypeType | None = None,
    ) -> None:
        data = {
            "order_id": order_id,
            "price": price,
            "order_type": order_type,
            "variety": "regular",
            "trigger_price": trigger_price,
        }

        self.modify_order(data)  # type: ignore

    def reverse_transaction_type(
        self, transaction_type: Literal["BUY", "SELL"]
    ) -> Literal["SELL", "BUY"]:
        if transaction_type == "BUY":
            return "SELL"
        elif transaction_type == "SELL":
            return "BUY"
        raise Exception(f"unknown transaction type [{transaction_type}]")

    def place_large_orders(self, orders: list[QuantplayOrder]) -> list[str | None]:
        order_ids: list[str | None] = []
        orders = sorted(orders, key=lambda d: d["transaction_type"])
        for order in orders:
            exchange = order["exchange"]
            tradingsymbol = order["tradingsymbol"]
            quantity = order["quantity"]
            quantity_list = self.split_order(exchange, tradingsymbol, quantity)
            if len(quantity_list) > 10:
                raise InvalidArgumentException(
                    "Number of orders limit [10] exceeded, please reduce quantity"
                )

            for quantity in quantity_list:
                order_id = self.place_order(
                    tradingsymbol=tradingsymbol,
                    exchange=exchange,
                    quantity=quantity,
                    order_type="MARKET",
                    transaction_type=order["transaction_type"],
                    tag="move_stk",
                    product=order["product"],
                    price=0,
                    trigger_price=None,
                )
                order_ids.append(order_id)

        return order_ids

    def move_strike(
        self,
        tradingsymbol: str,
        exchange: ExchangeType,
        product: ProductType,
        transaction_type: TransactionType,
        quantity: int,
        strike_factor: int | None,
        new_strike: int | None,
    ) -> list[str | None]:
        split_regex = r"([A-Z]+)(.{5})([0-9]+)(CE|PE)"

        underlying, expiry, strike, instrument_type = re.findall(
            split_regex, tradingsymbol
        )[0]
        strike = int(strike)

        config = self.underlying_config(underlying, expiry)
        strike_gap = config["strike_gap"]

        if strike_factor is not None:
            new_strike = strike + (strike_gap * strike_factor)

        new_trading_symbol = f"{underlying}{expiry}{new_strike}{instrument_type}"

        orders: list[QuantplayOrder] = [
            {
                "tradingsymbol": tradingsymbol,
                "exchange": exchange,
                "transaction_type": self.reverse_transaction_type(transaction_type),
                "quantity": quantity,
                "product": product,
            },
            {
                "tradingsymbol": new_trading_symbol,
                "exchange": exchange,
                "transaction_type": transaction_type,
                "quantity": quantity,
                "product": product,
            },
        ]

        return self.place_large_orders(orders)

    def modify_orders_till_complete(
        self,
        orders_placed: list[str],
        sleep_time: float = 10,
        max_modification_count: int = 10,
    ) -> None:
        modification_count = {}
        skip_first_sleep = True
        while 1:
            if not skip_first_sleep:
                time.sleep(sleep_time)
                skip_first_sleep = False

            orders = self.orders()

            orders = orders.filter(pl.col("order_id").is_in(orders_placed))
            orders = orders.filter(
                ~pl.col("status").is_in(["REJECTED", "CANCELLED", "COMPLETE"])
            )

            if len(orders) == 0:
                Constants.logger.info("ALL orders have been completed")
                break

            orders_dict = orders.to_dicts()
            for order in orders_dict:
                order_id = order["order_id"]
                if "PENDING" in order["status"]:
                    continue

                if order_id not in modification_count:
                    modification_count[order_id] = 0
                else:
                    modification_count[order_id] += 1

                ltp = self.ltp(order["exchange"], order["tradingsymbol"])

                market_protection = 0.02
                if modification_count[order_id] > 5:
                    market_protection = 0.05

                order["price"] = self.market_protection_price(
                    ltp, order["transaction_type"], market_protection=market_protection
                )

                order["order_type"] = "LIMIT"
                self.modify_order(order)  # type: ignore

                time.sleep(0.1)

                if modification_count[order_id] > max_modification_count:
                    order["order_type"] = "MARKET"
                    order["price"] = 0
                    Constants.logger.info(f"Placing MARKET order [{order}]")
                    self.modify_order(order)  # type: ignore

                elif modification_count[order_id] > 20:
                    self.cancel_order(order_id)
                    Constants.logger.error(
                        f"Max Modification Limit Exceeded : [{order_id}]"
                    )

    def log_event(
        self,
        event: dict[str, Any],
        status: Literal["error", "info", "warn", "debug"] = "info",
    ) -> None:
        """Logs Strategy Events in Standard Format

        Format: [username][strategy_name][event_type]: [event as JSON String]

        Args:
            event (dict[str, str]): Event as a Dictionary
            status (Literal['error', 'info', 'warn', 'debug'], optional): Logging Level. Defaults to 'info'.
        """
        status_to_log_map[status](
            f"[{self.username}][{self.nickname}][{self.broker_name}] {json.dumps(event, default=Constants.myconverter)}"
        )

    def ltp_from_token(self, token: int) -> float | None:
        return self.redis_client.get(str(token))  # type:ignore

    def ltp_from_tokens(self, tokens: list[int]) -> float | None:
        return self.redis_client.mget(tokens)  # type:ignore

    def token_converter(self, token: int, exchange: ExchangeType) -> int:
        exchangeMap = {
            "NSE": 1,
            "NFO": 2,
            "NCD": 3,
            "BSE": 4,
            "BFO": 5,
            "BCD": 6,
            "MFO": 7,
            "MCX": 8,
            "Indices": 9,
        }

        return token * 256 + exchangeMap[exchange]

    # **
    # ** Generics
    # **

    @abstractmethod
    def orders(self, tag: str | None = None, add_ltp: bool = True) -> pl.DataFrame:
        """Return user orders from the specified broker

        Args:
            tag (str | None, optional): orders tag. Defaults to None.
            add_ltp (bool, optional): want LTP or not. Defaults to True.

        Returns:
            pd.DataFrame: returns user orders
        """
        ...

    @abstractmethod
    def positions(self, drop_cnc: bool = True) -> pl.DataFrame:
        """Returns user position from the specified broker

        Args:
            drop_cnc (bool, optional): CNC positions to be dropped or not. Defaults to True.

        Returns:
            pl.DataFrame: returns user positions
        """
        ...

    @abstractmethod
    def modify_order(self, order: ModifyOrderRequest) -> str:
        """Modifies Existing Order place on exchange

        Args:
            order (ModifyOrderRequest): Order to be modified

        Returns:
            str: returns order_id
        """
        ...

    @abstractmethod
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
        """Function for Place Order to exchange

        Args:
            tradingsymbol (str): TradingSymbol to place order
            exchange (ExchangeType): exchange
            quantity (int): number
            order_type (OrderType): order Type
            transaction_type (TransactionType): Transaction Type
            tag (str | None): order tag
            product (ProductType): product
            price (float): price
            trigger_price (float | None): trigger price

        Returns:
            str: Return orders_id
        """
        ...

    @abstractmethod
    def ltp(self, exchange: ExchangeType, tradingsymbol: str) -> float:
        """_summary_

        Args:
            exchange (ExchangeType): Exchange
            tradingsymbol (str): Tradingsymbol

        Returns:
            float: Returns ltp of the tradingsymbol
        """
        ...

    @abstractmethod
    def cancel_order(self, order_id: str, variety: str | None = None) -> None:
        """Cancels order for the given order_id

        Args:
            order_id (str): Order ID
        """
        ...

    @abstractmethod
    def profile(self) -> UserBrokerProfileResponse:
        """Returns user broker profile

        Returns:
            UserBrokerProfile: contains exchange user_id full_name and email
        """
        ...

    @abstractmethod
    def holdings(self, add_ltp: bool = True) -> pl.DataFrame:
        """Returns User Broker Holdings

        Returns:
            UserBrokerProfile: contains exchange user_id full_name and email
        """
        ...

    @abstractmethod
    def margins(self) -> MarginsResponse:
        """Returns User Margin Summary"""
        ...

    @abstractmethod
    def get_order_type(self, order_type: OrderTypeType) -> ...: ...

    @abstractmethod
    def get_exchange(self, exchange: ExchangeType) -> ...: ...

    @abstractmethod
    def get_product(self, product: ProductType) -> ...: ...
