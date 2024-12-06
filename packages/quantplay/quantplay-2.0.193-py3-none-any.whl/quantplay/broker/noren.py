import json
import re
import traceback
from datetime import datetime
from json.decoder import JSONDecodeError
from queue import Queue
from typing import Any

import polars as pl
from retrying import retry  # type: ignore

from quantplay.broker.finvasia_utils.fa_noren import FA_NorenApi
from quantplay.broker.ft_utils.ft_noren import FT_NorenApi
from quantplay.broker.generics.broker import Broker
from quantplay.exception.exceptions import (
    BrokerException,
    InvalidArgumentException,
    QuantplayOrderPlacementException,
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
from quantplay.model.generics import (
    NorenTypes,
    OrderTypeType,
    ProductType,
    TransactionType,
)
from quantplay.model.order_event import OrderUpdateEvent
from quantplay.utils.constant import Constants, OrderType
from quantplay.utils.pickle_utils import InstrumentData
from quantplay.wrapper.aws.s3 import S3Utils

logger = Constants.logger


class Noren(Broker):
    def __init__(
        self,
        load_instrument: bool = True,
        order_updates: Queue[OrderUpdateEvent] | None = None,
    ) -> None:
        super().__init__()

        self.order_updates = order_updates

        if load_instrument:
            self.load_instrument()

        self.order_type_sl = "SL-LMT"
        self.trigger_pending_status = "TRIGGER_PENDING"

        self.api: FA_NorenApi | FT_NorenApi

    def set_attributes(self, response: dict[str, str | None]) -> None:
        self.email = response["email"]
        self.user_id = response["actid"]
        self.full_name = response["uname"]
        self.user_token = response["susertoken"]

    def load_instrument(self, file_name: str | None = None) -> None:
        try:
            self.symbol_data = InstrumentData.get_instance().load_data(  # type: ignore
                "shoonya_instruments"
            )
            Constants.logger.info("[LOADING_INSTRUMENTS] loading data from cache")
        except Exception:
            self.instrument_data = S3Utils.read_csv(
                "quantplay-market-data",
                "symbol_data/shoonya_instruments.csv",
            )
            self.initialize_symbol_data(save_as="shoonya_instruments")

        self.initialize_broker_symbol_map()

    def get_symbol(self, symbol: str, exchange: ExchangeType | None = None):
        if symbol not in self.quantplay_symbol_map:
            return symbol
        if exchange == "NSE" and "-EQ" not in symbol:
            return f"{symbol}-EQ"

        return self.quantplay_symbol_map[symbol]

    def get_transaction_type(
        self, transaction_type: TransactionType
    ) -> NorenTypes.TransactionTypeType:
        if transaction_type == "BUY":
            return "B"
        elif transaction_type == "SELL":
            return "S"

        raise InvalidArgumentException(
            "transaction type {} not supported for trading".format(transaction_type)
        )

    def get_order_type(self, order_type: OrderTypeType) -> NorenTypes.OrderTypeType:
        if order_type == OrderType.market:
            return "MKT"

        elif order_type == OrderType.sl:
            return "SL-LMT"

        elif order_type == OrderType.slm:
            return "SL-MKT"

        elif order_type == OrderType.limit:
            return "LMT"

        return order_type

    def get_product(self, product: ProductType) -> NorenTypes.ProductType:
        if product == "NRML":
            return "M"
        elif product == "CNC":
            return "C"
        elif product == "MIS":
            return "I"
        elif product in ["M", "C", "I"]:
            return product

        raise InvalidArgumentException(f"Product {product} not supported for trading")

    def event_handler_order_update(self, order: Any):
        try:
            order["placed_by"] = order["actid"]
            order["tag"] = order["actid"]
            order["order_id"] = order["norenordno"]
            order["exchange_order_id"] = order["exchordid"]
            order["exchange"] = order["exch"]
            order["tradingsymbol"] = order["tsym"]
            if "remarks" in order:
                order["tag"] = order["remarks"]

            if order["exchange"] == "NSE":
                order["tradingsymbol"] = order["tradingsymbol"].replace("-EQ", "")

            elif order["exchange"] in ["NFO", "MCX"]:
                order["tradingsymbol"] = self.broker_symbol_map[order["tradingsymbol"]]

            order["order_type"] = order["prctyp"]
            if order["order_type"] == "LMT":
                order["order_type"] = "LIMIT"
            elif order["order_type"] == "MKT":
                order["order_type"] = "MARKET"
            elif order["order_type"] == "SL-LMT":
                order["order_type"] = "SL"

            if order["pcode"] == "M":
                order["product"] = "NRML"
            elif order["pcode"] == "C":
                order["product"] = "CNC"
            elif order["pcode"] == "I":
                order["product"] = "MIS"

            if order["trantype"] == "S":
                order["transaction_type"] = "SELL"
            elif order["trantype"] == "B":
                order["transaction_type"] = "BUY"
            else:
                logger.error(
                    "[UNKNOW_VALUE] finvasia transaction type {} not supported".format(
                        order["trantype"]
                    )
                )

            order["quantity"] = int(order["qty"])

            if "trgprc" in order:
                order["trigger_price"] = float(order["trgprc"])
            else:
                order["trigger_price"] = None

            order["price"] = float(order["prc"])

            if order["status"] == "TRIGGER_PENDING":
                order["status"] = "TRIGGER PENDING"
            elif order["status"] == "CANCELED":
                order["status"] = "CANCELLED"

            logger.info(f"[ORDER_FEED] {order}")
            if self.order_updates:
                self.order_updates.put(order)

        except Exception as e:
            logger.error("[ORDER_UPDATE_PROCESSING_FAILED] {}".format(e))

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
        try:
            if trigger_price == 0:
                trigger_price = None

            noren_transaction_type = self.get_transaction_type(transaction_type)
            noren_order_type = self.get_order_type(order_type)
            noren_product = self.get_product(product)
            tradingsymbol = self.get_symbol(tradingsymbol)

            data = {
                "product_type": noren_product,
                "buy_or_sell": noren_transaction_type,
                "exchange": exchange,
                "tradingsymbol": tradingsymbol,
                "quantity": quantity,
                "price_type": noren_order_type,
                "price": price,
                "trigger_price": trigger_price,
                "remarks": tag,
            }
            Constants.logger.info("[PLACING_ORDER] {}".format(json.dumps(data)))
            response = self.api.place_order(
                buy_or_sell=noren_transaction_type,
                product_type=noren_product,
                exchange=exchange,
                tradingsymbol=tradingsymbol,
                quantity=quantity,
                discloseqty=0,
                price_type=noren_order_type,
                price=price,
                trigger_price=trigger_price,
                retention="DAY",
                remarks=tag,
            )

            Constants.logger.info(
                "[PLACE_ORDER_RESPONSE] {} input {}".format(response, json.dumps(data))
            )

            if response is not None and "norenordno" in response:
                return response["norenordno"]
            else:
                raise Exception(response)

        except Exception as e:
            traceback.print_exc()
            exception_message = "Order placement failed with error [{}]".format(str(e))
            raise QuantplayOrderPlacementException(
                f"[PLACE_ORDER_FAILED] {exception_message}"
            )

    def ltp(self, exchange: ExchangeType, tradingsymbol: str) -> float:
        tradingsymbol = self.get_symbol(tradingsymbol, exchange)

        try:
            token = self.symbol_data["{}:{}".format(exchange, tradingsymbol)]["token"]
        except KeyError:
            token = self.symbol_data["{}:{}".format(exchange, tradingsymbol[:-3])][
                "token"
            ]

        quote = self.invoke_noren_api(
            self.api.get_quotes, exchange=exchange, token=str(token)
        )

        if quote is None:
            raise BrokerException("Invaid LTP Response from Broker")

        return float(quote.get("lp", 0))

    def live_data(
        self, exchange: ExchangeType, tradingsymbol: str
    ) -> dict[str, float | None]:
        tradingsymbol = self.get_symbol(tradingsymbol)
        token = self.symbol_data["{}:{}".format(exchange, tradingsymbol)]["token"]
        data = self.api.get_quotes(exchange, str(token))

        if data is None:
            raise BrokerException("Response from Broker for Market Data is Invalid")

        return {
            "ltp": float(data["lp"]),
            "upper_circuit": float(data["uc"]),
            "lower_circuit": float(data["lc"]),
        }

    def order_history(self, order_id: str) -> dict[str, str | Any]:
        order_history = self.api.single_order_history(order_id)

        if order_history is None:
            raise BrokerException("Response from Broker for Order History is Invalid")

        order_details = order_history[0]

        data = {
            "order_id": order_id,
            "order_type": order_details["prctyp"],
            "exchange": order_details["exch"],
            "quantity": order_details["qty"],
            "tradingsymbol": order_details["tsym"],
        }

        return data

    def get_exchange(self, exchange: ExchangeType) -> Any:
        return exchange

    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
    )
    def modify_order(self, order: ModifyOrderRequest) -> str:
        order_id = order["order_id"]
        existing_details = self.order_history(order_id)

        if "trigger_price" not in order:
            order["trigger_price"] = None

        if "order_type" not in order:
            order["order_type"] = existing_details["order_type"]  # type: ignore

        if "quantity" not in order:
            order["quantity"] = int(existing_details["quantity"])

        order["order_type"] = self.get_order_type(order["order_type"])  # type: ignore

        try:
            logger.info(f"[MODIFYING_ORDER] {order}")
            response = self.api.modify_order(  # type:ignore
                orderno=order_id,
                exchange=existing_details["exchange"],  # type: ignore
                tradingsymbol=existing_details["tradingsymbol"],
                newprice_type=order["order_type"],
                newquantity=order["quantity"],
                newprice=order.get("price", 0),
                newtrigger_price=order["trigger_price"],
            )
            logger.info(
                "[MODIFY_ORDER_RESPONSE] order id [{}] response [{}]".format(
                    order["order_id"], response
                )
            )

            if response is None:
                raise Exception("Response is None")

            return response

        except Exception as e:
            exception_message = f"OrderModificationFailed for {order['order_id']} failed with exception {e}"
            Constants.logger.error(f"{exception_message}")
            raise e

    def cancel_order(self, order_id: str, variety: str | None = None):
        self.api.cancel_order(order_id)

    def stream_order_data(self) -> None:
        self.api.start_websocket(order_update_callback=self.event_handler_order_update)

    def profile(self) -> UserBrokerProfileResponse:
        if self.user_id is None:
            raise Exception("User ID is unknown")

        response: UserBrokerProfileResponse = {
            "user_id": self.user_id,
        }

        if self.full_name is not None:
            response["full_name"] = self.full_name

        if self.email is not None:
            response["email"] = self.email

        return response

    def holdings(self, add_ltp: bool = True) -> pl.DataFrame:
        holdings = self.invoke_noren_api(self.api.get_holdings)
        if holdings is None or len(holdings) == 0:
            return pl.DataFrame(schema=self.holidings_schema)

        holdings = [
            {
                "exchange": h["exch_tsym"][0]["exch"],
                "token": h["exch_tsym"][0]["token"],
                "tradingsymbol": h["exch_tsym"][0]["tsym"],
                "isin": h["exch_tsym"][0]["isin"],
                "quantity": int(h["holdqty"])
                + int(h.get("npoadqty", 0))
                + int(h.get("brkcolqty", 0)),
                "pledged_quantity": int(h.get("brkcolqty", 0)),
                "average_price": float(h.get("upldprc", 0)),
            }
            for h in holdings
        ]

        holdings_df = pl.from_dicts(holdings).with_columns(
            pl.col("tradingsymbol").str.replace("-EQ", "").alias("tradingsymbol"),
            pl.lit(0).alias("pledged_quantity"),
            (pl.col("quantity") * pl.col("average_price")).alias("buy_value"),
        )

        if add_ltp:
            holdings_df = holdings_df.with_columns(
                pl.struct(["exchange", "tradingsymbol"])
                .map_elements(
                    lambda x: int(self.ltp(x["exchange"], x["tradingsymbol"])),
                    return_dtype=pl.Float64,
                )
                .alias("price")
            )

            holdings_df = holdings_df.with_columns(
                (pl.col("quantity") * pl.col("price")).alias("value"),
                (pl.col("quantity") * pl.col("price")).alias("current_value"),
                ((pl.col("price") / pl.col("average_price") - 1) * 100).alias(
                    "pct_change"
                ),
            )

        for k in self.holidings_schema:
            if k not in holdings_df.columns:
                holdings_df = holdings_df.with_columns(pl.lit(None).alias(k))

        return holdings_df[list(self.holidings_schema.keys())].cast(self.holidings_schema)

    def positions(self, drop_cnc: bool = True) -> pl.DataFrame:
        positions = self.invoke_noren_api(self.api.get_positions)

        if positions is None or len(positions) == 0:
            return pl.DataFrame(schema=self.positions_schema)

        positions_df = pl.from_dicts(positions)
        positions_df = positions_df.rename(
            {
                "tsym": "tradingsymbol",
                "lp": "ltp",
                "actid": "user_id",
                "prd": "product",
                "exch": "exchange",
                "netavgprc": "average_price",
                "totsellamt": "sell_value",
                "totbuyamt": "buy_value",
            }
        )

        positions_df = positions_df.with_columns(
            (pl.col("rpnl").cast(pl.Float64) + pl.col("urmtom").cast(pl.Float64)).alias(
                "pnl"
            )
        )

        if "dname" not in positions_df.columns:
            positions_df = positions_df.with_columns(pl.lit(None).alias("dname"))
        positions_df = positions_df.with_columns(
            pl.when(pl.col("exchange") == "BFO")
            .then(pl.col("tradingsymbol").str.slice(-2))
            .otherwise(pl.col("dname"))
            .alias("dname")
        )
        positions_df = positions_df.with_columns(
            pl.col("dname").str.strip_chars().alias("dname")
        )
        positions_df = positions_df.with_columns(
            pl.when(pl.col("dname").str.slice(-2) == "PE")
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

        mandatory_columns = ["daybuyqty", "daysellqty", "cfbuyqty", "cfsellqty"]
        for mad_c in mandatory_columns:
            if mad_c not in positions_df.columns:
                positions_df = positions_df.with_columns(pl.lit(None).alias(mad_c))

        positions_df = positions_df.with_columns(
            (
                pl.col("daybuyqty").fill_null(0).cast(pl.Int64)
                + pl.col("cfbuyqty").fill_null(0).cast(pl.Int64)
            ).alias("buy_quantity"),
            (
                pl.col("daysellqty").fill_null(0).cast(pl.Int64)
                + pl.col("cfsellqty").fill_null(0).cast(pl.Int64)
            ).alias("sell_quantity"),
        )

        positions_df = positions_df.with_columns(
            (pl.col("buy_quantity") - pl.col("sell_quantity")).alias("quantity")
        )

        positions_df = positions_df.with_columns(
            pl.when(pl.col("product") == "I")
            .then(pl.lit("MIS"))
            .when(pl.col("product") == "C")
            .then(pl.lit("CNC"))
            .when(pl.col("product") == "M")
            .then(pl.lit("NRML"))
            .otherwise(pl.col("product"))
            .alias("product")
        )

        return positions_df[list(self.positions_schema.keys())].cast(
            self.positions_schema
        )

    def orders(self, tag: str | None = None, add_ltp: bool = True) -> pl.DataFrame:
        orders = self.invoke_noren_api(self.api.get_order_book)

        if orders is None or len(orders) == 0:
            return pl.DataFrame(schema=self.orders_schema)

        orders_df = pl.from_dicts(
            orders,
            schema={
                "tsym": pl.String,
                "norenordno": pl.String,
                "uid": pl.String,
                "exch": pl.String,
                "prd": pl.String,
                "trantype": pl.String,
                "qty": pl.String,
                "prc": pl.String,
                "prctyp": pl.String,
                "norentm": pl.String,
                "fillshares": pl.String,
                "rorgqty": pl.String,
                "trgprc": pl.String,
                "avgprc": pl.String,
                "remarks": pl.String,
                "rejreason": pl.String,
                "ltp": pl.String,
                "token": pl.String,
                "status": pl.String,
            },
        )

        orders_df = orders_df.rename(
            {
                "tsym": "tradingsymbol",
                "norenordno": "order_id",
                "uid": "user_id",
                "exch": "exchange",
                "prd": "product",
                "trantype": "transaction_type",
                "qty": "quantity",
                "prc": "price",
                "prctyp": "order_type",
                "norentm": "order_timestamp",
                "fillshares": "filled_quantity",
                "rorgqty": "pending_quantity",
                "trgprc": "trigger_price",
                "avgprc": "average_price",
                "remarks": "tag",
                "rejreason": "status_message",
            }
        ).cast(
            {
                "filled_quantity": pl.Int64,
                "pending_quantity": pl.Int64,
                "price": pl.Float64,
                "trigger_price": pl.Float64,
                "average_price": pl.Float64,
                "ltp": pl.Float64,
                "quantity": pl.Int64,
                "token": pl.Int64,
            }
        )

        if tag:
            orders_df = orders_df.filter(pl.col("tag").eq(tag))

        if add_ltp:
            positions = self.positions()
            positions = positions.sort("product").group_by("tradingsymbol").head(1)

            orders_df = orders_df.drop(["ltp"]).join(
                positions.select(["tradingsymbol", "ltp"]), on="tradingsymbol", how="left"
            )

        orders_df = (
            orders_df.with_columns(
                pl.lit(None).alias("variety"),
                pl.when(pl.col("transaction_type") == "S")
                .then(pl.lit("SELL"))
                .when(pl.col("transaction_type") == "B")
                .then(pl.lit("BUY"))
                .alias("transaction_type"),
                (
                    pl.col("ltp") * pl.col("filled_quantity")
                    - pl.col("average_price") * pl.col("filled_quantity")
                ).alias("pnl"),
            )
            .with_columns(
                pl.when(pl.col("transaction_type") == "SELL")
                .then(-pl.col("pnl"))
                .otherwise(pl.col("pnl"))
                .alias("pnl"),
                pl.col("order_timestamp")
                .str.strptime(pl.Datetime, "%H:%M:%S %d-%m-%Y")
                .alias("order_timestamp"),
            )
            .with_columns(
                pl.col("order_timestamp").alias("update_timestamp"),
                pl.when(pl.col("status") == "TRIGGER_PENDING")
                .then(pl.lit("TRIGGER PENDING"))
                .when(pl.col("status") == "CANCELED")
                .then(pl.lit("CANCELLED"))
                .otherwise(pl.col("status"))
                .alias("status"),
                pl.when(pl.col("product") == "I")
                .then(pl.lit("MIS"))
                .when(pl.col("product") == "C")
                .then(pl.lit("CNC"))
                .when(pl.col("product") == "M")
                .then(pl.lit("NRML"))
                .otherwise(pl.col("product"))
                .alias("product"),
                pl.when(pl.col("order_type") == "MKT")
                .then(pl.lit("MARKET"))
                .when(pl.col("order_type") == "LMT")
                .then(pl.lit("LIMIT"))
                .when(pl.col("order_type") == "SL-LMT")
                .then(pl.lit("SL"))
                .when(pl.col("order_type") == "SL-MKT")
                .then(pl.lit("SL-M"))
                .otherwise(pl.col("order_type"))
                .alias("order_type"),
                pl.col("status_message").alias("status_message_raw"),
                pl.col("filled_quantity").fill_null(strategy="zero"),
                pl.col("pending_quantity").fill_null(strategy="zero"),
                pl.col("average_price").fill_null(strategy="zero"),
            )
        )

        return orders_df.select(list(self.orders_schema.keys())).cast(self.orders_schema)

    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
        retry_on_exception=retry_exception,
    )
    def invoke_noren_api(self, fn: Any, *args: Any, **kwargs: Any) -> Any | None:
        try:
            response = fn(*args, **kwargs)
            if response is None:
                return response
            if "stat" in response and "not_ok" == response["stat"].lower():
                raise TokenException(response["emsg"] if response is not None else "")

            return response

        except JSONDecodeError:
            raise BrokerException("Failed to Receive Data from broker")
        except TokenException:
            raise
        except Exception:
            traceback.print_exc()
            raise RetryableException("Failed to Receive Data from broker. Retrying Again")

    def basket_margin(self, basket_orders: list[dict[str, Any]]) -> dict[str, Any]:
        basket_orders = [
            {
                "exchange": "NFO",
                "tradingsymbol": "NIFTY2481424500CE",
                "transaction_type": "SELL",
                "variety": "regular",
                "product": "NRML",
                "order_type": "MARKET",
                "quantity": 25,
            },
            {
                "exchange": "NFO",
                "tradingsymbol": "NIFTY2481424500PE",
                "transaction_type": "SELL",
                "variety": "regular",
                "product": "NRML",
                "order_type": "MARKET",
                "quantity": 15,
            },
        ]

        for order in basket_orders:
            exchange = order["exchange"]
            tradingsymbol = order["tradingsymbol"]
            if order["exchange"] not in ["BFO", "NFO"]:
                raise InvalidArgumentException(
                    f"Exchange {exchange} is not supported for basket margin calculation"
                )

            split_regex = r"([A-Z]+)(.{5})([0-9]+)(CE|PE)"

            underlying, expiry, strike, instrument_type = re.findall(  # type:ignore
                split_regex, tradingsymbol
            )[0]
            order["strprc"] = str(strike) + ".00"
            order["symname"] = underlying
            order["instname"] = "OPTIDX"
            order["netqty"] = order["quantity"]
            order["sellqty"] = order["quantity"]
            order["optt"] = instrument_type
            order["prd"] = self.get_product(order["product"])
            order["exch"] = order["exchange"]

            expiry = self.symbol_data[  # type:ignore
                f"{exchange}:{self.get_symbol(tradingsymbol)}"
            ]["expiry"]
            order["exd"] = (
                datetime.strptime(expiry, "%Y-%m-%d")  # type:ignore
                .strftime("%d-%b-%Y")
                .upper()
            )

        if self.user_id is None:
            raise Exception(
                "UserId is not set: Please contact support team and report the issue"
            )
        response = self.api.span_calculator(self.user_id, basket_orders)
        return response

    def margins(self) -> MarginsResponse:
        api_margins = self.invoke_noren_api(self.api.get_limits)

        if api_margins is None:
            raise BrokerException("Invaid Margins Response from Broker")

        try:
            collateral = 0
            if "collateral" in api_margins:
                collateral = api_margins["collateral"]

            holdings_val = 0
            if "grcoll" in api_margins:
                holdings_val = api_margins["grcoll"]

            if "marginused" not in api_margins:
                api_margins["margin_used"] = 0
            else:
                api_margins["margin_used"] = api_margins["marginused"]

            if "payin" not in api_margins:
                api_margins["payin"] = 0

            margin_available = (
                float(api_margins["cash"])
                + float(collateral)
                + float(api_margins["payin"])
                - float(api_margins["margin_used"])
            )

            try:
                cash = float(api_margins["cash"])
            except Exception:
                cash = 0

            margins: MarginsResponse = {
                "margin_used": float(api_margins["margin_used"]),
                "margin_available": margin_available,
                "cash": cash,
                "total_balance": float(cash) + float(holdings_val),
            }

            return margins

        except Exception as e:
            logger.error(f"[NOREN_MARGIN_ERROR] {e}")
            RetryableException("[NOREN] Failed to fetch account margin")

        return {"margin_available": 0, "margin_used": 0, "total_balance": 0, "cash": 0}
