from collections.abc import Callable
from datetime import datetime, date, timedelta
from typing import Any, Literal, Dict
from breeze_connect import BreezeConnect  # type: ignore

from quantplay.broker.breeze.breeze_utils import BreezeUtils
from quantplay.exception import QuantplayOrderPlacementException, InvalidArgumentException

from quantplay.broker.generics.broker import Broker
import polars as pl

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
from quantplay.utils.constant import Constants
from quantplay.utils.pickle_utils import InstrumentData
from quantplay.wrapper.aws.s3 import S3Utils

api_key = "2721)7972f2cxz733k4NGt933$23h17D"
api_secret = "4e620^i919469f7~1709*066#d384&5y"
session_token = "47204416"


class RateLimitExcededException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class NoDataException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


logger = Constants.logger


class ICICI(Broker):
    index_map = {
        "FINNIFTY": "NIFFIN",
        "BANKNIFTY": "CNXBAN",
        "MIDCPNIFTY": "NIFSEL",
    }

    def __init__(
        self,
        api_key: str | None = None,
        api_secret: str | None = None,
        session_token: str | None = None,
        user_id: str | None = None,
        password: str | None = None,
        totp: str | None = None,
        load_instrument: bool = True,
    ) -> None:
        if api_key and user_id and password and totp:
            self.set_session_token(api_key, user_id, password, totp)
        else:
            self.session_token = session_token

        if api_key and api_secret and self.session_token:
            self.wrapper = BreezeConnect(api_key)  # type:ignore
            self.wrapper.generate_session(api_secret, self.session_token)  # type: ignore
        else:
            raise InvalidArgumentException(
                "ICICI token generation failed, missing arguments"
            )
        if load_instrument:
            self.load_instrument()

    def set_session_token(
        self,
        api_key: str,
        user_id: str,
        password: str,
        totp: str,
    ) -> None:
        session_token = BreezeUtils.get_session_code(api_key, user_id, password, totp)
        self.session_token = session_token

    def load_instrument(self, file_name: str | None = None) -> None:
        try:
            self.symbol_data = InstrumentData.get_instance().load_data(  # type: ignore
                "icici_instruments"
            )
            Constants.logger.info("[LOADING_INSTRUMENTS] loading data from cache")
        except Exception:
            inst_data_df = S3Utils.get_parquet(
                "quantplay-market-data/symbol_data/icici_instruments.parquet"
            )
            self.instrument_data = inst_data_df
            self.initialize_symbol_data_v2(save_as="icici_instruments")

        self.initialize_broker_symbol_map()

    def get_historical_data(
        self,
        interval: Literal["1second", "1minute", "5minute", "30minute", "1day"],
        from_date: datetime,
        to_date: datetime,
        stock_code: str,
        exch_code: Literal["NSE", "NFO", "BSE", "NDX", "MCX"],
        product_type: Literal["Cash", "Options", "Futures"] | None,
        expiry_date: date | None,
        right: Literal["Call", "Put", "Others"] | None,
        strike_price: int | None,
    ) -> pl.DataFrame:
        from_date_str = from_date.isoformat()[:19] + ".000Z"
        to_date_str = to_date.isoformat()[:19] + ".000Z"

        expiry_date_str = expiry_date.isoformat()[:19] + ".000Z" if expiry_date else ""

        historical_fetch_fn = (
            self.wrapper.get_historical_data_v2
            if interval == "1second"
            else self.wrapper.get_historical_data
        )

        data = self.invoke_wrapper(
            historical_fetch_fn,
            interval=interval,
            from_date=from_date_str,
            to_date=to_date_str,
            stock_code=stock_code,
            exchange_code=exch_code,
            product_type=product_type,
            expiry_date=expiry_date_str,
            right=right,
            strike_price=str(strike_price),
        )

        if data is None or len(data) == 0:
            raise NoDataException(f"Historical Data For {data}")

        return pl.from_dicts(data)

    def get_symbol(self, symbol: str, exchange: ExchangeType | None = None) -> str:
        if symbol not in self.quantplay_symbol_map:
            return symbol

        return self.quantplay_symbol_map[symbol]

    def orders_by_exchange(self, exchange: ExchangeType):
        to_date = datetime.now().isoformat()[:19] + ".000Z"
        from_date = (datetime.now() - timedelta(hours=10)).isoformat()[:19] + ".000Z"

        orders: Dict[str, Any] = self.wrapper.get_order_list(  # type:ignore
            exchange_code=exchange,
            from_date=from_date,
            to_date=to_date,
        )
        if "Success" in orders and orders["Success"] is None:
            return pl.DataFrame(schema=self.orders_schema)
        orders_df = pl.DataFrame(orders["Success"])
        orders_df = orders_df.rename(
            {
                "order_datetime": "order_timestamp",
                "action": "transaction_type",
                "exchange_code": "exchange",
                "expiry_date": "expiry",
                "strike_price": "strike",
                "user_remark": "tag",
            }
        )
        orders_df = orders_df.with_columns(
            pl.col("expiry").str.strptime(pl.Date, format="%d-%b-%Y").alias("expiry"),
            pl.col("order_timestamp")
            .str.strptime(pl.Datetime(time_unit="ms"), format="%d-%b-%Y %H:%M:%S")
            .alias("order_timestamp"),
            pl.col("order_type").str.to_uppercase().alias("order_type"),
            pl.col("transaction_type").str.to_uppercase().alias("transaction_type"),
            pl.col("status").str.to_uppercase().alias("status"),
            pl.when(pl.col("right") == "Call")
            .then(pl.lit("CE"))
            .when(pl.col("right") == "Put")
            .then(pl.lit("PE"))
            .alias("instrument_type"),
        )

        orders_df = orders_df.with_columns(
            (
                pl.col("stock_code")
                + "-"
                + pl.col("expiry").dt.date().cast(pl.String)
                + "-"
                + pl.col("strike").cast(pl.String)
                + "-"
                + pl.col("instrument_type").cast(pl.String)
            ).alias("tradingsymbol")
        )

        orders_df = orders_df.with_columns(
            pl.struct(["exchange", "tradingsymbol"])
            .map_elements(
                lambda x: int(
                    self.symbol_attribute(x["exchange"], x["tradingsymbol"], "token")
                ),
                return_dtype=pl.Int64,
            )
            .alias("token")
        )

        orders_df = orders_df.with_columns(
            pl.lit(None).alias("user_id"),
            pl.lit("NRML").alias("product"),
            pl.lit("regular").alias("variety"),
            pl.lit("default").alias("tag"),
            pl.lit(None).alias("trigger_price"),
            pl.lit(None).alias("ltp"),
            pl.lit(None).alias("filled_quantity"),
            pl.lit(None).alias("status_message"),
            pl.lit(None).alias("status_message_raw"),
            pl.col("order_timestamp").alias("update_timestamp"),
        )
        orders_df = orders_df[list(self.orders_schema.keys())].cast(self.orders_schema)
        orders_df = orders_df.with_columns(
            pl.when(pl.col("status") == "EXECUTED")
            .then(pl.lit("COMPLETE"))
            .when(pl.col("status") == "ORDERED")
            .then(pl.lit("OPEN"))
            .otherwise(pl.col("status"))
            .alias("status")
        )

        return orders_df

    def orders(self, tag: str | None = None, add_ltp: bool = True) -> pl.DataFrame:
        nfo_orders = self.orders_by_exchange("NFO")
        bfo_orders = self.orders_by_exchange("BFO")

        return pl.concat([nfo_orders, bfo_orders])

    def positions(self, drop_cnc: bool = True) -> pl.DataFrame:
        positions: Dict[str, Any] = self.wrapper.get_portfolio_positions()  # type:ignore

        if "Success" in positions and positions["Success"] is None:
            return pl.DataFrame(schema=self.positions_schema)
        positions_df = pl.DataFrame(positions["Success"])
        if "realized_profit" not in positions_df:
            positions_df = positions_df.with_columns(pl.lit(0.0).alias("realized_profit"))
        positions_df = positions_df.filter(pl.col("exchange_code").is_in(["NFO", "BFO"]))
        positions_df = positions_df.rename(
            {
                "exchange_code": "exchange",
                "expiry_date": "expiry",
                "strike_price": "strike",
                "product_type": "product",
            }
        )
        positions_df = positions_df.with_columns(
            pl.col("quantity").cast(pl.Int32).alias("quantity")
        )
        positions_df = positions_df.with_columns(
            pl.col("strike").cast(pl.Float32).alias("strike"),
            pl.col("expiry").str.strptime(pl.Date, format="%d-%b-%Y").alias("expiry"),
            pl.when(pl.col("right") == "Call")
            .then(pl.lit("CE"))
            .when(pl.col("right") == "Put")
            .then(pl.lit("PE"))
            .alias("instrument_type"),
            pl.when(pl.col("action") == "Sell")
            .then(abs(pl.col("quantity").cast(pl.Float32)) * -1)
            .otherwise(abs(pl.col("quantity").cast(pl.Float32)))
            .alias("quantity"),
            pl.lit(0).alias("pnl"),
            pl.col("average_price").cast(pl.Float32).alias("average_price"),
        )

        positions_df = positions_df.with_columns(
            (
                pl.col("stock_code")
                + "-"
                + pl.col("expiry").dt.date().cast(pl.String)
                + "-"
                + pl.col("strike").cast(pl.String)
                + "-"
                + pl.col("instrument_type").cast(pl.String)
            ).alias("tradingsymbol")
        )

        positions_df = positions_df.with_columns(
            pl.struct(["exchange", "tradingsymbol"])
            .map_elements(
                lambda x: int(
                    self.symbol_attribute(x["exchange"], x["tradingsymbol"], "token")
                ),
                return_dtype=pl.Int64,
            )
            .alias("token")
        )

        positions_df = positions_df.with_columns(
            pl.when(pl.col("quantity") < 0)
            .then(pl.col("quantity").abs() * pl.col("average_price"))
            .when(pl.col("quantity") == 0)
            .then(pl.col("realized_profit"))
            .otherwise(pl.lit(0))
            .alias("sell_value"),
            pl.when(pl.col("quantity") > 0)
            .then(pl.col("quantity").abs() * pl.col("average_price"))
            .otherwise(pl.lit(0))
            .alias("buy_value"),
            pl.lit(0).alias("ltp"),
            pl.when(pl.col("quantity") < 0)
            .then(pl.col("quantity").abs())
            .otherwise(pl.lit(0))
            .alias("sell_quantity"),
            pl.when(pl.col("quantity") > 0)
            .then(pl.col("quantity").abs())
            .otherwise(pl.lit(0))
            .alias("buy_quantity"),
            pl.lit("NRML").alias("product"),
            pl.col("instrument_type").alias("option_type"),
        )
        return positions_df[list(self.positions_schema.keys())].cast(
            self.positions_schema
        )

    def get_right(self, symbol_data: Dict[str, Any]) -> str:
        instrument_type = symbol_data["instrument_type"]
        if instrument_type == "CE":
            return "call"
        elif instrument_type == "PE":
            return "put"
        raise InvalidArgumentException(f"{instrument_type} not supported")

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
        if tag is None:
            tag = ""
        icici_tradingsymbol = self.get_symbol(tradingsymbol)
        try:
            symbol_data: Dict[str, Any] = self.symbol_data[  # type:ignore
                f"{exchange}:{icici_tradingsymbol}"
            ]
        except KeyError:
            raise QuantplayOrderPlacementException(
                f"Failed to find tradingsymbol {tradingsymbol}"
            )
        icici_product = "cash"
        if exchange in ["NFO", "BFO"]:
            icici_product = "futures"
            if tradingsymbol[-2:] in ["PE", "CE"]:
                icici_product = "options"
        if icici_product == "cash":
            response = self.wrapper.place_order(  # type:ignore
                stock_code=icici_tradingsymbol,
                exchange_code=exchange,
                product="cash",
                action=transaction_type.lower(),
                order_type=order_type.lower(),
                stoploss="",
                quantity=str(quantity),
                price=str(price),
                validity="day",
                user_remark=tag,
            )
        else:
            response: Dict[str, Any] = self.wrapper.place_order(  # type:ignore
                stock_code=symbol_data["symbol_code"],
                exchange_code=exchange,
                product=icici_product,
                action=transaction_type.lower(),
                order_type=order_type.lower(),
                stoploss="",
                quantity=str(quantity),
                price=str(price),
                validity="day",
                expiry_date=str(symbol_data["expiry"]) + "T06:00:00.000Z",
                right=self.get_right(symbol_data),
                strike_price=str(symbol_data["strike"]),
                user_remark=tag,
            )
        if "Success" in response and "order_id" in response["Success"]:
            return response["Success"]["order_id"]
        elif "Error" in response:
            raise QuantplayOrderPlacementException(response["Error"])
        else:
            raise QuantplayOrderPlacementException(
                f"ICICI: order placement failed {response}"
            )

    def modify_order(self, order: ModifyOrderRequest) -> str:
        return ""

    def cancel_order(self, order_id: str, variety: str | None = None) -> None:
        orders = self.orders()
        order = orders.filter(pl.col("order_id") == order_id)
        if len(order) == 0:
            return
        order_details = order.to_dicts()[0]
        self.wrapper.cancel_order(  # type:ignore
            exchange_code=order_details["exchange"], order_id=order_id
        )
        return

    def holdings(self, add_ltp: bool = True) -> pl.DataFrame:
        return pl.DataFrame(schema=self.holidings_schema)

    def margins(self) -> MarginsResponse:
        margins = self.invoke_wrapper(self.wrapper.get_funds)

        return {
            "total_balance": float(margins["total_bank_balance"]),
            "margin_available": (
                float(margins["allocated_equity"])
                + float(margins["allocated_fno"])
                + float(margins["allocated_commodity"])
                + float(margins["allocated_currency"])
            ),
            "margin_used": (
                float(margins["block_by_trade_equity"])
                + float(margins["block_by_trade_fno"])
                + float(margins["block_by_trade_commodity"])
                + float(margins["block_by_trade_currency"])
            ),
            "cash": float(margins["unallocated_balance"]),
        }

    def ltp(self, exchange: ExchangeType, tradingsymbol: str) -> float:
        return 0.0

    def profile(self) -> UserBrokerProfileResponse:
        return {
            "user_id": "",
        }

    def get_exchange(self, exchange: ExchangeType) -> ...:
        return exchange

    def get_product(self, product: ProductType) -> ...:
        return

    def get_order_type(self, order_type: OrderTypeType) -> ...:
        return

    def get_icici_symbol_param(self):
        pass

    def invoke_wrapper(self, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        try:
            data = fn(*args, **kwargs)

            if data["Status"] > 200:
                if data["Error"] == "Limit exceed: API call per day: ":
                    raise RateLimitExcededException(data["Error"])

                raise Exception(data["Error"])

            return data.get("Success", None)

        except Exception as e:
            raise (e)
