import json
import traceback
from typing import Any

import polars as pl
from dhanhq import dhanhq  # type:ignore
from retrying import retry  # type: ignore

from quantplay.broker.generics.broker import Broker
from quantplay.exception.exceptions import (
    BrokerException,
    InvalidArgumentException,
    TokenException,
    QuantplayOrderPlacementException,
    RetryableException,
    retry_exception,
)
from quantplay.model.broker import (
    ExchangeType,
    MarginsResponse,
    UserBrokerProfileResponse,
)
from quantplay.model.generics import (
    DhanTypes,
    OrderTypeType,
    ProductType,
    TransactionType,
)
from quantplay.utils.constant import Constants, OrderType
from quantplay.utils.pickle_utils import InstrumentData
from quantplay.wrapper.aws.s3 import S3Utils


class Dhan(Broker):
    def __init__(
        self,
        user_id: str,
        access_token: str,
        load_instrument: bool = True,
    ) -> None:
        try:
            self.dhan = dhanhq(
                client_id=user_id,
                access_token=access_token,
            )
            self.user_id = user_id

            if load_instrument:
                self.load_instrument()

        except InvalidArgumentException:
            raise

        except Exception:
            raise BrokerException("Dhan Broker initialization failed")

    def load_instrument(self, file_name: str | None = None) -> None:
        try:
            self.symbol_data = InstrumentData.get_instance().load_data(  # type: ignore
                "dhan_instruments"
            )
            Constants.logger.info("[LOADING_INSTRUMENTS] loading data from cache")
        except Exception:
            self.instrument_data = S3Utils.read_csv(
                "quantplay-market-data",
                "symbol_data/dhan_instruments.csv",
            )
            self.initialize_symbol_data(save_as="dhan_instruments")

        self.initialize_broker_symbol_map()

    def set_username(self, username: str):
        self.username = username

    def get_username(self):
        return self.username

    def modify_order(self, order: Any) -> str:
        order_id = order["order_id"]
        existing_order: dict[str, Any] = self.invoke_dhan_api(
            self.dhan.get_order_by_id,  # type: ignore
            order_id,
        )

        if "quantity" not in order:
            order["quantity"] = existing_order["data"]["quantity"]
        if "trigger_price" not in order:
            order["trigger_price"] = None
        try:
            Constants.logger.info(
                "Modifying order [{}] new price [{}]".format(
                    order["order_id"], order["price"]
                )
            )
            self.dhan.modify_order(  # type: ignore
                order_id,
                order["order_type"],
                None,
                order["quantity"],
                order["price"],
                order["trigger_price"],
                None,
                self.dhan.DAY,
            )

        except Exception as e:
            exception_message = (
                "OrderModificationFailed for {} failed with exception {}".format(
                    order["order_id"], e
                )
            )
            if (
                "Order cannot be modified as it is being processed"
                not in exception_message
            ):
                Constants.logger.error("{}".format(exception_message))
        return order_id

    def cancel_order(self, order_id: str, variety: str | None = "regular"):
        self.dhan.cancel_order(order_id=order_id)  # type: ignore

    def get_order_type(self, order_type: OrderTypeType) -> DhanTypes.OrderTypeType:
        if order_type == OrderType.market:
            return dhanhq.MARKET

        elif order_type == OrderType.sl:
            return dhanhq.SL

        elif order_type == OrderType.slm:
            return dhanhq.SLM

        elif order_type == OrderType.limit:
            return dhanhq.LIMIT

        return order_type

    def get_exchange_segment(self, exchange: ExchangeType):
        if exchange == "NSE":
            return dhanhq.NSE
        elif exchange == "NFO":
            return dhanhq.NSE_FNO
        elif exchange == "BSE":
            return dhanhq.BSE
        elif exchange == "BFO":
            return dhanhq.BSE_FNO
        raise InvalidArgumentException(f"Exchange {exchange} is not supported")

    def get_product(self, product: ProductType) -> DhanTypes.ProductType:
        if product == "NRML":
            return dhanhq.INTRA
        elif product == "CNC":
            return dhanhq.CNC
        elif product == "MIS":
            return dhanhq.INTRA
        return product

    def get_symbol(self, symbol: str, exchange: ExchangeType | None = None):
        if symbol not in self.quantplay_symbol_map:
            return symbol

        return self.quantplay_symbol_map[symbol]

    # @retry(wait_exponential_multiplier=3000, wait_exponential_max=10000, stop_max_attempt_number=3)
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
        try:
            tradingsymbol = self.get_symbol(tradingsymbol)
            security_id = self.symbol_data[f"{exchange}:{tradingsymbol}"]["token"]
            exchange_segment = self.get_exchange_segment(exchange)
            dhan_order_type = self.get_order_type(order_type)
            product_type = self.get_product(product)
            Constants.logger.info(
                f"[DHAN_PLACING_ORDER] {security_id} {exchange} {transaction_type} {quantity} {dhan_order_type} {product_type} {price} {trigger_price}"
            )
            if trigger_price is None:
                trigger_price = 0
            response: dict[str, Any] = self.dhan.place_order(  # type:ignore
                security_id=security_id,  # hdfcbank
                exchange_segment=exchange_segment,
                transaction_type=transaction_type,
                quantity=quantity,
                order_type=dhan_order_type,
                product_type=product_type,
                price=price,
                trigger_price=trigger_price,  # type:ignore
            )

            try:
                return response["data"]["orderId"]  # type:ignore
            except Exception:
                Constants.logger.error(f"Failed to place order in Dhan {response}")
                raise Exception(json.dumps(response))
        except Exception as e:
            raise QuantplayOrderPlacementException(str(e))

    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
    )
    def holdings(self, add_ltp: bool = True) -> pl.DataFrame:
        holdings = self.invoke_dhan_api(self.dhan.get_holdings)
        if holdings is None:
            raise TokenException("Token Expired")

        if not isinstance(holdings["data"], list):
            return pl.DataFrame(schema=self.holidings_schema)

        holdings_df = pl.DataFrame(holdings["data"])
        if len(holdings_df) == 0:
            return pl.DataFrame(schema=self.holidings_schema)

        holdings_df = holdings_df.with_columns(
            pl.col("securityId").alias("token"),
            pl.col("avgCostPrice").alias("average_price"),
            pl.col("totalQty").alias("quantity"),
            pl.col("tradingSymbol").alias("tradingsymbol"),
            pl.lit(0).alias("price"),
        )

        holdings_df = holdings_df.with_columns(
            (pl.col("quantity") * pl.col("price")).alias("value"),
            pl.lit(0).alias("pledged_quantity"),
            (pl.col("quantity") * pl.col("average_price")).alias("buy_value"),
            (pl.col("quantity") * pl.col("price")).alias("current_value"),
            ((pl.col("price") / pl.col("average_price") - 1) * 100).alias("pct_change"),
        )

        return holdings_df[list(self.holidings_schema.keys())].cast(self.holidings_schema)

    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
        retry_on_exception=retry_exception,
    )
    def positions(self, drop_cnc: bool = True) -> pl.DataFrame:
        positions = self.invoke_dhan_api(self.dhan.get_positions)

        positions_df = pl.DataFrame(positions.get("data", {}))  # type:ignore

        if len(positions_df) == 0:
            return pl.DataFrame(schema=self.positions_schema)
        positions_df = positions_df.rename(
            {
                "tradingSymbol": "tradingsymbol",
                "securityId": "token",
                "exchangeSegment": "exchange",
                "productType": "product",
                "buyQty": "buy_quantity",
                "sellQty": "sell_quantity",
                "netQty": "quantity",
                "drvOptionType": "option_type",
            }
        )

        positions_df = positions_df.with_columns()

        positions_df = positions_df.with_columns(
            pl.lit(0.0).alias("ltp"),
            (pl.col("realizedProfit") + pl.col("unrealizedProfit")).alias("pnl"),
            (pl.col("carryForwardBuyValue") + pl.col("dayBuyValue")).alias("buy_value"),
            (pl.col("carryForwardSellValue") + pl.col("daySellValue")).alias(
                "sell_value"
            ),
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

        positions_df = positions_df.with_columns(
            pl.when(pl.col("product") == "INTRADAY").then(pl.lit("MIS")).alias("product"),
            pl.when(pl.col("exchange") == "NSE_FNO")
            .then(pl.lit("NFO"))
            .when(pl.col("exchange") == "BSE_FO")
            .then(pl.lit("BFO"))
            .when(pl.col("exchange") == "NSE_EQ")
            .then(pl.lit("NSE"))
            .when(pl.col("exchange") == "BSE_EQ")
            .then(pl.lit("BSE"))
            .alias("exchange"),
            pl.when(pl.col("option_type") == "PUT")
            .then(pl.lit("PE"))
            .when(pl.col("option_type") == "CALL")
            .then(pl.lit("CE"))
            .alias("option_type"),
        )

        if drop_cnc:
            positions_df = positions_df.filter(pl.col("product") != "CNC")

        return positions_df[list(self.positions_schema.keys())].cast(
            self.positions_schema
        )

    def orders(self, tag: str | None = None, add_ltp: bool = True) -> pl.DataFrame:
        orders = self.invoke_dhan_api(self.dhan.get_order_list)
        if not orders or "data" not in orders or not isinstance(orders["data"], list):
            return pl.DataFrame(schema=self.orders_schema)

        orders_df = pl.DataFrame(orders["data"])
        if len(orders_df) == 0:
            return pl.DataFrame(schema=self.orders_schema)

        orders_df = orders_df.rename(
            {
                "dhanClientId": "user_id",
                "orderId": "order_id",
                "securityId": "token",
                "tradingSymbol": "tradingsymbol",
                "orderStatus": "status",
                "transactionType": "transaction_type",
                "exchangeSegment": "exchange",
                "productType": "product",
                "filled_qty": "filled_quantity",
                "triggerPrice": "trigger_price",
                "orderType": "order_type",
            }
        )
        orders_df = orders_df.with_columns(
            pl.when(pl.col("product") == "INTRADAY")
            .then(pl.lit("MIS"))
            .when(pl.col("product") == "MARGIN")
            .then(pl.lit("NRML"))
            .otherwise(pl.col("product"))
            .alias("product"),
            pl.when(pl.col("exchange") == "NSE_FNO")
            .then(pl.lit("NFO"))
            .when(pl.col("exchange") == "BSE_FNO")
            .then(pl.lit("BFO"))
            .when(pl.col("exchange") == "NSE_EQ")
            .then(pl.lit("NSE"))
            .when(pl.col("exchange") == "BSE_EQ")
            .then(pl.lit("BSE"))
            .otherwise(pl.col("exchange"))
            .alias("exchange"),
            pl.when(pl.col("order_type") == "STOP_LOSS_MARKET")
            .then(pl.lit("SL-M"))
            .when(pl.col("order_type") == "STOP_LOSS")
            .then(pl.lit("SL"))
            .otherwise(pl.col("order_type"))
            .alias("order_type"),
            pl.when(pl.col("status") == "TRADED")
            .then(pl.lit("COMPLETE"))
            .when(pl.col("status") == "PENDING")
            .then(pl.lit("OPEN"))
            .otherwise(pl.col("status"))
            .alias("status"),
        )

        orders_df = orders_df.with_columns(
            pl.when((pl.col("status") == "OPEN") & (pl.col("trigger_price") > 0))
            .then(pl.lit("TRIGGER PENDING"))
            .otherwise(pl.col("status"))
            .alias("status")
        )

        orders_df = orders_df.with_columns(
            pl.lit(None).cast(pl.Float64).alias("ltp"),
            pl.lit(0.0).alias("average_price"),
            pl.lit(0).alias("pending_quantity"),
            pl.lit("regular").alias("variety"),
            pl.col("omsErrorDescription").alias("status_message"),
            pl.col("omsErrorDescription").alias("status_message_raw"),
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
        if "tag" not in orders_df.columns:
            orders_df = orders_df.with_columns(pl.lit(None).alias("tag"))

        orders_df = orders_df.with_columns(
            pl.col("createTime")
            .str.strptime(pl.Datetime, "%Y-%m-%d %H:%M:%S")
            .alias("order_timestamp"),
            pl.col("updateTime")
            .str.strptime(pl.Datetime, "%Y-%m-%d %H:%M:%S")
            .alias("update_timestamp"),
        )

        if tag:
            orders_df = orders_df.filter(pl.col("tag") == tag)

        return orders_df[list(self.orders_schema.keys())]

    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
        retry_on_exception=retry_exception,
    )
    def invoke_dhan_api(
        self, fn: Any, *args: Any, **kwargs: Any
    ) -> dict[str, Any] | None:
        try:
            response = fn(*args, **kwargs)

            if (
                "status" in response
                and response["status"] == "failure"
                and "remarks" in response
            ):
                if (
                    "error_code" in response["remarks"]
                    and response["remarks"]["error_code"] == "RS-9005"
                ):
                    raise TokenException("Token Expired")

            return response
        except Exception:
            traceback.print_exc()
            raise RetryableException("Failed to Receive Data from broker. Retrying Again")

    def margins(self) -> MarginsResponse:
        response = self.invoke_dhan_api(self.dhan.get_fund_limits)
        margin_used = 0
        margin_available = 0
        if response:
            margin_used = float(response["data"]["utilizedAmount"])
            margin_available = float(response["data"]["availabelBalance"])

        return {
            "margin_available": margin_available,
            "margin_used": margin_used,
            "total_balance": margin_used + margin_available,
            "cash": 0,
        }

    def profile(self) -> UserBrokerProfileResponse:
        return {"user_id": self.dhan.client_id}

    def get_exchange(
        self,
        exchange: ExchangeType,
    ) -> Any:
        return exchange

    def ltp(self, exchange: ExchangeType, tradingsymbol: str) -> float:
        return 0.0
