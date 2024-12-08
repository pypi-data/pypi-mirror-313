import asyncio
import json
import ssl
import threading
import traceback
from typing import Any

import polars as pl
import upstox_client  # type: ignore
import websockets
from retrying import retry  # type: ignore
from upstox_client.rest import ApiException  # type: ignore

from quantplay.broker.generics.broker import Broker
from quantplay.broker.uplink.uplink_utils import UplinkUtils
from quantplay.exception.exceptions import (
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
from quantplay.model.generics import OrderTypeType, ProductType, TransactionType
from quantplay.utils.constant import Constants


class Upstox(Broker):
    exchange_code_map = {
        "NFO": "NSE_FO",
        "CDS": "NSECD",
        "BFO": "BSEFO",
        "NSE": "NSE_EQ",
    }

    def __init__(
        self,
        access_token: str | None = None,
        user_id: str | None = None,
        api_key: str | None = None,
        api_secret: str | None = None,
        totp: str | None = None,
        mobile_number: str | None = None,
        account_pin: str | None = None,
        redirect_url: str | None = None,
        load_instrument: bool = True,
    ) -> None:
        super().__init__()

        if access_token:
            self.set_access_token(access_token)
            self.user_id = user_id
        else:
            raise TokenException("Upstox Session Expired")

        try:
            self.configuration = upstox_client.Configuration()
            self.configuration.access_token = self.access_token
            self.api_version = "2.0"

            self.api_client = upstox_client.ApiClient(self.configuration)
        except Exception:
            raise TokenException("Upstox Session Expired")

        if load_instrument:
            self.load_instrument()

    def load_instrument(self, file_name: str | None = None) -> None:
        super().load_instrument("upstox_instruments")

    def handle_exception(self, e: Any):
        if "Unauthorized" in e.reason:
            raise TokenException("Token Expired")

        if str(e.status) in ["400"]:
            return 400
        raise RetryableException(e.reason)

    def set_access_token(self, access_token: str):
        self.access_token = access_token

    def get_product(self, product: ProductType):
        if product == "NRML":
            return "D"
        elif product == "CNC":
            return "D"
        elif product == "MIS":
            return "I"

        return product

    def get_exchange(self, exchange: ExchangeType):
        if exchange in Upstox.exchange_code_map:
            return Upstox.exchange_code_map[exchange]

        return exchange

    def get_quantplay_exchange(self, exchange: str) -> ExchangeType:
        exchange_map: dict[str, ExchangeType] = {
            "NSE_FO": "NFO",
            "NSECD": "CDS",
            "BSEFO": "BFO",
            "NSE_EQ": "NSE",
        }
        if exchange in exchange_map:
            return exchange_map[exchange]

        return exchange  # type: ignore

    def get_quantplay_symbol(self, symbol: str):
        return symbol

    def get_lot_size(self, exchange: ExchangeType, tradingsymbol: str):
        return int(self.symbol_data["{}:{}".format(exchange, tradingsymbol)]["lot_size"])

    def get_order_type(self, order_type: OrderTypeType) -> Any:
        return order_type

    @retry(
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
        retry_on_exception=retry_exception,
    )
    def ltp(self, exchange: ExchangeType, tradingsymbol: str) -> float:
        api_instance = upstox_client.MarketQuoteApi(self.api_client)

        ltp = 0.0
        try:
            symbol_info = self.symbol_data[f"{exchange}:{tradingsymbol}"]
            # Market quotes and instruments - LTP quotes.
            # TODO:Check Get FN->symbol_info
            api_response = api_instance.ltp(  # type: ignore
                symbol_info.get("instrument_key"), self.api_version
            )

            ltp: float = api_response.data[  # type:ignore
                f"{self.get_exchange(symbol_info['exchange'])}:{tradingsymbol}"
            ].last_price

        except ApiException as e:
            self.handle_exception(e)
            Constants.logger.error("Exception when calling MarketQuoteApi->ltp: %s\n" % e)

        return ltp  # type: ignore

    @retry(
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
        retry_on_exception=retry_exception,
    )
    def modify_order(self, order: ModifyOrderRequest) -> str:
        if "trigger_price" not in order or order["trigger_price"] is None:
            order["trigger_price"] = 0
        api_instance = upstox_client.OrderApi(self.api_client)
        body = upstox_client.ModifyOrderRequest(
            validity="DAY",
            price=order.get("price"),
            order_id=order["order_id"],
            order_type=order.get("order_type"),
            trigger_price=order["trigger_price"],
        )

        try:
            # Modify order
            api_response = api_instance.modify_order(body, self.api_version)  # type: ignore
            return api_response.status  # type:ignore
        except ApiException as e:
            self.handle_exception(e)
            Constants.logger.error(
                "Exception when calling OrderApi->modify_order: %s\n" % e
            )

            Constants.logger.info(
                f"Modifying order [{ order['order_id']}] new price [{order.get('price')}]"
            )
        return order["order_id"]

    def cancel_order(self, order_id: str, variety: str | None = None) -> None:
        api_instance = upstox_client.OrderApi(self.api_client)

        try:
            # Cancel order
            api_response = api_instance.cancel_order(order_id, self.api_version)  # type: ignore
            return api_response.status  # type:ignore
        except ApiException as e:
            if self.handle_exception(e) == 400:
                return
            print("Exception when calling OrderApi->cancel_order: %s\n" % e)

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
        exchange = self.get_quantplay_exchange(exchange)
        try:
            Constants.logger.info(
                f"[PLACING_ORDER] {tradingsymbol} {exchange} {quantity} {tag} {product}"
            )
            upstox_product = self.get_product(product)
            symbol_data = self.symbol_data[f"{exchange}:{self.get_symbol(tradingsymbol)}"]
            if trigger_price is None:
                trigger_price = 0

            api_instance = upstox_client.OrderApi(self.api_client)
            body = upstox_client.PlaceOrderRequest(
                quantity=quantity,
                product=upstox_product,
                validity="DAY",
                price=price,
                instrument_token=f"{symbol_data.get('instrument_key')}",
                order_type=order_type,
                transaction_type=transaction_type,
                disclosed_quantity=0,
                trigger_price=trigger_price,
                is_amo=False,
            )

            api_response = api_instance.place_order(body, self.api_version)  # type: ignore
            return api_response.data.order_id  # type:ignore
        except Exception as e:
            raise QuantplayOrderPlacementException(str(e))

    def generate_token(
        self,
        api_key: str,
        api_secret: str,
        totp: str,
        mobile_number: str,
        account_pin: str,
        redirect_url: str,
    ):
        try:
            code = UplinkUtils.get_request_token(
                api_key,
                redirect_url,
                totp,
                mobile_number,
                account_pin,
            )
            response = UplinkUtils.generate_access_token(
                code,
                api_key,
                api_secret,
                redirect_url,
            )

            return response["access_token"]
        except TokenException as e:
            message = str(e)
            if "Invalid" in message and "checksum" in message:
                raise InvalidArgumentException("Invalid API secret")
            raise
        except Exception as e:
            traceback.print_exc()
            Constants.logger.error(f"Failed to generate upstox token {e}")
            raise e

    @retry(
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
        retry_on_exception=retry_exception,
    )
    def profile(self) -> UserBrokerProfileResponse:
        api_instance = upstox_client.UserApi(self.api_client)

        response: UserBrokerProfileResponse = {"user_id": "", "full_name": ""}
        try:
            # Get profile
            api_response = api_instance.get_profile(self.api_version)  # type: ignore
            profile_data = api_response.data  # type:ignore

            response: UserBrokerProfileResponse = {
                "user_id": profile_data.user_id,  # type: ignore
                "full_name": profile_data.user_name,  # type: ignore
                "exchanges": profile_data.exchanges,  # type: ignore
                "email": profile_data.email,  # type: ignore
            }
            self.email = response["email"]
            self.enabled_exchanges = response["exchanges"]
        except ApiException as e:
            self.handle_exception(e)
            Constants.logger.info("error when calling UserApi->get_profile: %s\n" % e)

        self.user_id = response["user_id"]
        return response

    def holdings(self, add_ltp: bool = True) -> pl.DataFrame:
        api_instance = upstox_client.PortfolioApi(self.api_client)

        holdings_df = pl.DataFrame()
        try:
            # Get Holdings
            api_response = api_instance.get_holdings(self.api_version)  # type: ignore
            holdings = [holding.to_dict() for holding in api_response.data]  # type:ignore
            holdings_df = pl.DataFrame(holdings)
        except ApiException as e:
            self.handle_exception(e)
            Constants.logger.error(
                "Exception when calling PortfolioApi->get_holdings: %s\n" % e
            )

        if len(holdings_df) == 0:
            return pl.DataFrame(schema=self.holidings_schema)

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
            pl.lit(0).alias("pledged_quantity"),
            (pl.col("quantity") * pl.col("average_price")).alias("buy_value"),
            (pl.col("quantity") * pl.col("price")).alias("current_value"),
            ((pl.col("price") / pl.col("average_price") - 1) * 100).alias("pct_change"),
        )
        holdings_df = holdings_df.with_columns(
            pl.struct(["exchange", "tradingsymbol"])
            .map_elements(
                lambda x: int(
                    self.symbol_attribute(x["exchange"], x["tradingsymbol"], "token")
                ),
                return_dtype=pl.Int64,
            )
            .alias("token")
        )
        return holdings_df[list(self.holidings_schema.keys())].cast(self.holidings_schema)

    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
        retry_on_exception=retry_exception,
    )
    def positions(self, drop_cnc: bool = True) -> pl.DataFrame:
        api_instance = upstox_client.PortfolioApi(self.api_client)

        positions_df = pl.DataFrame(schema=self.positions_schema)
        try:
            # Get Positions
            api_response = api_instance.get_positions(self.api_version)  # type: ignore
            positions = [  # type:ignore
                position.to_dict()  # type:ignore
                for position in api_response.data  # type:ignore
            ]
            positions_df = pl.DataFrame(positions)
        except ApiException as e:
            self.handle_exception(e)
            Constants.logger.error(
                "Exception when calling PortfolioApi->get_positions: %s\n" % e
            )

        if len(positions_df) == 0:
            return pl.DataFrame(schema=self.positions_schema)

        positions_df = positions_df.rename({"last_price": "ltp"})
        positions_df = positions_df.with_columns(
            (pl.col("sell_value") - pl.col("buy_value")).alias("pnl")
        )
        positions_df = positions_df.with_columns(
            (pl.col("pnl") + (pl.col("quantity") * pl.col("ltp"))).alias("pnl")
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
        positions_df = positions_df.with_columns(
            pl.col("instrument_token")
            .str.split_exact("|", 1)
            .struct.rename_fields(["upstox_exchange", "token"])
            .alias("fields")
        ).unnest("fields")

        positions_df = positions_df.with_columns(
            (pl.col("overnight_buy_quantity") + pl.col("day_buy_quantity")).alias(
                "buy_quantity"
            )
        )
        positions_df = positions_df.with_columns(
            (pl.col("overnight_sell_quantity") + pl.col("day_sell_quantity")).alias(
                "sell_quantity"
            )
        )

        positions_df = positions_df.with_columns(
            pl.when(pl.col("product") == "I")
            .then(pl.lit("MIS"))
            .when(pl.col("product") == "C")
            .then(pl.lit("CNC"))
            .when(pl.col("product") == "D")
            .then(pl.lit("NRML"))
            .otherwise(pl.col("product"))
            .alias("product")
        )

        if drop_cnc:
            positions_df = positions_df.filter(pl.col("product") != "CNC")

        return positions_df[list(self.positions_schema.keys())].cast(
            self.positions_schema
        )

    @retry(
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
        retry_on_exception=retry_exception,
    )
    def orders(self, tag: str | None = None, add_ltp: bool = True) -> pl.DataFrame:
        api_instance = upstox_client.OrderApi(self.api_client)

        orders_df = pl.DataFrame()
        try:
            # Get order book
            api_response = api_instance.get_order_book(self.api_version)  # type: ignore
            orders = [order.to_dict() for order in api_response.data]  # type:ignore
            orders_df = pl.DataFrame(orders)
        except ApiException as e:
            self.handle_exception(e)
            Constants.logger.error(
                "Exception when calling OrderApi->get_order_book: %s\n" % e
            )

        if len(orders_df) == 0:
            return pl.DataFrame(schema=self.orders_schema)

        if add_ltp:
            positions = self.positions()
            positions = positions.sort("product").group_by("tradingsymbol").head(1)

            orders_df = orders_df.join(
                positions.select(["tradingsymbol", "ltp"]), on="tradingsymbol", how="left"
            )
        else:
            orders_df = orders_df.with_columns(pl.lit(None).cast(pl.Float64).alias("ltp"))
        orders_df = orders_df.rename({"placed_by": "user_id"})

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

        if tag:
            orders_df = orders_df.filter(pl.col("tag") == tag)

        orders_df = orders_df.with_columns(
            pl.when(pl.col("exchange") == "NSE")
            .then(pl.col("tradingsymbol").str.replace("-EQ", ""))
            .otherwise(pl.col("tradingsymbol"))
            .alias("tradingsymbol")
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
            pl.col("order_timestamp")
            .str.strptime(pl.Datetime, "%Y-%m-%d %H:%M:%S")
            .alias("order_timestamp")
        )
        orders_df = orders_df.with_columns(
            pl.col("order_timestamp").alias("update_timestamp")
        )
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
            pl.when(pl.col("product") == "D")
            .then(pl.lit("CNC"))
            .when(pl.col("product") == "I")
            .then(pl.lit("MIS"))
            .otherwise(pl.col("product"))
            .alias("product"),
        )

        orders_df = orders_df.with_columns(
            pl.when(
                (pl.col("product") == "CNC") & (pl.col("exchange").is_in(["NFO", "BFO"]))
            )
            .then(pl.lit("NRML"))
            .otherwise(pl.col("product"))
            .alias("product")
        )

        return orders_df[list(self.orders_schema.keys())].cast(self.orders_schema)

    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
        retry_on_exception=retry_exception,
    )
    def margins(self) -> MarginsResponse:
        api_instance = upstox_client.UserApi(self.api_client)

        segment = "SEC"  # str |  (optional)

        margin_used = 0
        margin_available = 0
        try:
            # Get User Fund And Margin
            api_response = api_instance.get_user_fund_margin(  # type: ignore
                self.api_version, segment=segment
            )
            margin_used: float = float(
                api_response.data["equity"].used_margin  # type:ignore
            )
            margin_available = float(
                api_response.data["equity"].available_margin  # type:ignore
            )
        except ApiException as e:
            self.handle_exception(e)
            Constants.logger.error(
                "Exception when calling UserApi->get_user_fund_margin: %s\n" % e
            )

        return {
            "margin_used": margin_used,
            "margin_available": margin_available,
            "total_balance": margin_used + margin_available,
            "cash": 0,
        }

    def stream_order_data(self):
        th = threading.Thread(target=self.between_callback, daemon=True)
        th.start()

    def between_callback(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(self.fetch_order_updates())
        loop.close()

    async def fetch_order_updates(self):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        # Configure OAuth2 access token for authorization: OAUTH2
        configuration = upstox_client.Configuration()

        self.api_version = "2.0"
        configuration.access_token = self.access_token

        # Get portfolio stream feed authorize
        response = self.get_portfolio_stream_feed_authorize(  # type: ignore
            self.api_version, configuration
        )

        async with websockets.connect(
            response.data.authorized_redirect_uri,  # type:ignore
            ssl=ssl_context,
        ) as websocket:
            print("Connection established")

            # Perform WebSocket operations
            while True:
                message = await websocket.recv()
                self.order_event_handler(json.dumps(message))

    def get_portfolio_stream_feed_authorize(
        self, api_version: str, configuration: upstox_client.Configuration
    ) -> Any:
        api_instance = upstox_client.WebsocketApi(upstox_client.ApiClient(configuration))
        api_response = api_instance.get_portfolio_stream_feed_authorize(api_version)  # type: ignore

        return api_response  # type: ignore

    def get_quantplay_product(self, exchange: ExchangeType, product: str):
        product_map = {"D": "CNC", "I": "MIS"}

        if product in product_map:
            product = product_map[product]

        if product == "CNC" and exchange in ["NFO", "BFO"]:
            product = "NRML"

        return product

    def order_event_handler(self, order: str):
        if self.order_updates is None:
            raise Exception("Event Queue Not Initalised")

        order_data = json.loads(json.loads(order))

        try:
            order_data["status"] = order_data["status"].upper()
            if order_data["exchange"] in ["NSE", "BSE"]:
                order_data["tradingsymbol"] = order_data["tradingsymbol"].replace(
                    "-EQ", ""
                )
            order_data["product"] = self.get_quantplay_product(
                order_data["exchange"], order_data["product"]
            )
            Constants.logger.info("[UPDATE_RECEIVED] {}".format(order_data))
            self.order_updates.put(order_data)

        except Exception as e:
            traceback.print_exc()
            Constants.logger.error("[ORDER_UPDATE_PROCESSING_FAILED] {}".format(e))
