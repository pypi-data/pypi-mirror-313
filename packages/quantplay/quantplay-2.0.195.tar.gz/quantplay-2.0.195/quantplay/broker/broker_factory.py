import codecs
import os
import pickle
import traceback
from dataclasses import dataclass
from typing import Any

from quantplay.broker.aliceblue import Aliceblue
from quantplay.broker.angelone import AngelOne
from quantplay.broker.dhan import Dhan
from quantplay.broker.five_paisa import FivePaisa
from quantplay.broker.flattrade import FlatTrade
from quantplay.broker.icici_direct import ICICI
from quantplay.broker.iifl_xts import IIFL as IIFL_XTS
from quantplay.broker.jainam_xts import Jainam
from quantplay.broker.kotak import Kotak
from quantplay.broker.motilal import Motilal
from quantplay.broker.shoonya import FinvAsia
from quantplay.broker.upstox import Upstox
from quantplay.broker.zerodha import Zerodha
from quantplay.exception.exceptions import InvalidArgumentException, TokenException
from quantplay.utils.caching import InstrumentCache
from quantplay.utils.pickle_utils import PickleUtils

BrokerType = (
    Aliceblue
    | AngelOne
    | FlatTrade
    | Motilal
    | FinvAsia
    | Upstox
    | Zerodha
    | IIFL_XTS
    | FivePaisa
    | Kotak
    | Dhan
    | Jainam
    | ICICI
)

instrument_cache = InstrumentCache()


@dataclass
class Broker:
    ZERODHA = "Zerodha"
    UPSTOX = "Upstox"
    ALICEBLUE = "Aliceblue"
    FIVEPAISA_OPENAPI = "5Paisa_OpenAPI"
    FINVASIA = "Finvasia"
    FLATTRADE = "Flattrade"
    IIFL_XTS = "IIFL_XTS"
    JAINAM = "Jainam"
    MOTILAL = "Motilal"
    ANGELONE = "Angelone"
    KOTAK = "Kotak"
    DHAN = "Dhan"
    ICICI = "ICICI"


broker_instruments_map = {
    Broker.ZERODHA: "zerodha_instruments",
    Broker.FINVASIA: "shoonya_instruments",
    Broker.FLATTRADE: "shoonya_instruments",
    Broker.IIFL_XTS: "xts_instruments",
    Broker.JAINAM: "xts_instruments",
    Broker.MOTILAL: "motilal_instruments",
    Broker.ANGELONE: "angelone_instruments",
    Broker.ALICEBLUE: "aliceblue_instruments",
    Broker.UPSTOX: "upstox_instruments",
    Broker.DHAN: "dhan_instruments",
    Broker.KOTAK: "kotak_instruments",
    Broker.FIVEPAISA_OPENAPI: "5paisa_instruments",
    Broker.ICICI: "icici_instruments",  # TODO: Fix
}

broker_required_args = {
    Broker.ZERODHA: set(["user_id", "zerodha_wrapper"]),
    Broker.FINVASIA: set(["user_id", "user_token"]),
    Broker.FLATTRADE: set(["user_id", "user_token"]),
    Broker.IIFL_XTS: set(["user_id", "wrapper", "md_wrapper"]),
    Broker.ICICI: set(["api_key", "api_secret", "session_token"]),
    Broker.JAINAM: set(["user_id", "wrapper", "md_wrapper"]),
    Broker.MOTILAL: set(["user_id", "headers"]),
    Broker.ALICEBLUE: set(["user_id", "client"]),
    Broker.UPSTOX: set(["user_id", "access_token"]),
    Broker.DHAN: set(["user_id", "access_token"]),
    Broker.FIVEPAISA_OPENAPI: set(["user_id", "client"]),
    Broker.KOTAK: set(["user_id", "configuration"]),
    Broker.ANGELONE: set(
        [
            "user_id",
            "api_key",
            "access_token",
            "refresh_token",
            "feed_token",
        ]
    ),
}

broker_generate_args = {
    Broker.ZERODHA: set(["user_id", "api_key", "api_secret"]),
    Broker.FLATTRADE: set(["user_id", "api_secret", "password", "totp", "api_key"]),
    Broker.IIFL_XTS: set(["api_key", "api_secret", "md_api_key", "md_api_secret"]),
    Broker.ICICI: set(["api_key", "api_secret", "session_token"]),
    Broker.JAINAM: set(["api_key", "api_secret", "md_api_key", "md_api_secret"]),
    Broker.MOTILAL: set(["user_id", "password", "api_key", "two_fa", "totp"]),
    Broker.ALICEBLUE: set(["user_id", "api_key"]),
    Broker.DHAN: set(["user_id", "access_token"]),
    Broker.FIVEPAISA_OPENAPI: set(
        [
            "app_source",
            "app_user_id",
            "app_password",
            "user_key",
            "encryption_key",
            "client_id",
            "totp",
            "pin",
        ]
    ),
    Broker.ANGELONE: set(["user_id", "api_key", "mpin", "totp"]),
    Broker.FINVASIA: set(
        ["api_secret", "imei", "password", "totp", "user_id", "vendor_code"]
    ),
    Broker.UPSTOX: set(["user_id", "access_token"]),
    Broker.KOTAK: set(["consumer_key", "consumer_secret", "mobilenumber", "password"]),
}


class BrokerFactory:
    def __init__(self) -> None:
        self.client_broker_data: dict[str, BrokerType] = {}

    def get_broker_key(self, username: str, broker_name: str) -> str:
        return f"{username}:{broker_name}"

    def validate_broker_args(
        self, user_broker_account: dict[str, Any], is_generator_args: bool = False
    ) -> None:
        broker = user_broker_account["broker"]
        broker_data = user_broker_account["broker_data"]

        compare_map = broker_generate_args if is_generator_args else broker_required_args

        if broker not in compare_map.keys():
            raise InvalidArgumentException(f"Unsupported Broker: '{broker}'")

        if not compare_map[broker].issubset(broker_data.keys()):
            raise TokenException(
                f"Missing Arguments for {user_broker_account['username']}:{user_broker_account['nickname']} in broker '{broker}' -> {compare_map[broker].difference(broker_data.keys())}"
            )

    def generate_token(
        self, user_broker_account: dict[str, Any]
    ) -> dict[str, BrokerType | Any]:
        broker_client: BrokerType | None = None

        broker_data = user_broker_account["broker_data"]
        broker = user_broker_account["broker"]

        broker_client: BrokerType | None = None
        self.validate_broker_args(user_broker_account, is_generator_args=True)

        if broker == Broker.MOTILAL:
            broker_client = Motilal(
                user_id=broker_data["user_id"],
                password=broker_data["password"],
                api_key=broker_data["api_key"],
                two_fa=broker_data["two_fa"],
                totp=broker_data["totp"],
                load_instrument=False,
            )
            broker_data["headers"] = broker_client.headers

        elif broker == Broker.DHAN:
            broker_client = Dhan(
                user_id=broker_data["user_id"],
                access_token=broker_data["access_token"],
                load_instrument=False,
            )

        elif broker == Broker.KOTAK:
            broker_client = Kotak(
                user_id=broker_data["user_id"],
                consumer_key=broker_data["consumer_key"],
                consumer_secret=broker_data["consumer_secret"],
                mobilenumber=broker_data["mobilenumber"],
                password=broker_data["password"],
                otp=broker_data.get("otp"),
                load_instrument=False,
            )

            broker_data["configuration"] = broker_client.configuration

        elif broker == Broker.ZERODHA:
            if "password" in broker_data:
                broker_client = Zerodha(
                    user_id=broker_data["user_id"],
                    api_key=broker_data["api_key"],
                    api_secret=broker_data["api_secret"],
                    password=broker_data["password"],
                    totp=broker_data["totp"],
                    load_instrument=False,
                )

                broker_data["zerodha_wrapper"] = codecs.encode(
                    pickle.dumps(broker_client.wrapper), "base64"
                ).decode()

            else:
                broker_client = Zerodha(
                    wrapper=broker_data["zerodha_wrapper"],
                    load_instrument=False,
                )

        elif broker == Broker.ANGELONE:
            broker_client = AngelOne(
                api_key=broker_data["api_key"],
                user_id=broker_data["user_id"],
                mpin=broker_data["mpin"],
                totp=broker_data["totp"],
                load_instrument=False,
            )

            broker_data["refresh_token"] = broker_client.wrapper.refresh_token  # type: ignore
            broker_data["access_token"] = broker_client.wrapper.access_token  # type: ignore
            broker_data["feed_token"] = broker_client.wrapper.feed_token  # type: ignore

        elif broker == Broker.ALICEBLUE:
            broker_client = Aliceblue(
                user_id=broker_data["user_id"],
                api_key=broker_data["api_key"],
                load_instrument=False,
            )

            broker_data["client"] = codecs.encode(
                pickle.dumps(broker_client.alice), "base64"
            ).decode()

        elif broker == Broker.UPSTOX:
            broker_client = Upstox(
                user_id=broker_data["user_id"],
                access_token=broker_data["access_token"],
            )

            broker_data["access_token"] = broker_client.configuration.access_token

        elif broker == Broker.FINVASIA:
            broker_client = FinvAsia(
                api_secret=broker_data["api_secret"],
                imei=broker_data["imei"],
                password=broker_data["password"],
                totp=broker_data["totp"],
                user_id=broker_data["user_id"],
                vendor_code=broker_data["vendor_code"],
                load_instrument=False,
            )

            broker_client.api.close_websocket()
            broker_data["user_token"] = broker_client.user_token

        elif broker == Broker.ICICI:
            if "password" in broker_data:
                broker_client = ICICI(
                    api_key=broker_data["api_key"],
                    api_secret=broker_data["api_secret"],
                    user_id=broker_data["user_id"],
                    password=broker_data["password"],
                    totp=broker_data["totp"],
                    session_token=broker_data["session_token"],
                    load_instrument=False,
                )
            else:
                broker_client = ICICI(
                    api_key=broker_data["api_key"],
                    api_secret=broker_data["api_secret"],
                    session_token=broker_data["session_token"],
                    load_instrument=False,
                )
            broker_data["session_token"] = broker_client.session_token

        elif broker == Broker.FLATTRADE:
            broker_client = FlatTrade(
                user_id=broker_data["user_id"],
                api_secret=broker_data["api_secret"],
                password=broker_data["password"],
                totp=broker_data["totp"],
                api_key=broker_data["api_key"],
                load_instrument=False,
            )

            broker_client.api.close_websocket()
            broker_data["user_token"] = broker_client.user_token

        elif broker == Broker.FIVEPAISA_OPENAPI:
            broker_client = FivePaisa(
                app_source=broker_data["app_source"],
                app_user_id=broker_data["app_user_id"],
                app_password=broker_data["app_password"],
                user_key=broker_data["user_key"],
                encryption_key=broker_data["encryption_key"],
                client_id=broker_data["client_id"],
                totp=broker_data["totp"],
                pin=broker_data["pin"],
                load_instrument=False,
            )

            broker_data["client"] = broker_client.get_client()
            broker_data["user_id"] = broker_client.user_id

        elif broker == Broker.IIFL_XTS:
            broker_client = IIFL_XTS(
                api_secret=broker_data["api_secret"],
                api_key=broker_data["api_key"],
                md_api_key=broker_data["md_api_key"],
                md_api_secret=broker_data["md_api_secret"],
                load_instrument=False,
            )
            broker_data["user_id"] = broker_client.wrapper.userID

            broker_data["wrapper"] = codecs.encode(
                pickle.dumps(broker_client.wrapper), "base64"
            ).decode()

            broker_data["md_wrapper"] = codecs.encode(
                pickle.dumps(broker_client.md_wrapper), "base64"
            ).decode()

        elif broker == Broker.JAINAM:
            broker_client = Jainam(
                api_secret=broker_data["api_secret"],
                api_key=broker_data["api_key"],
                md_api_key=broker_data["md_api_key"],
                md_api_secret=broker_data["md_api_secret"],
                is_dealer=broker_data.get("is_dealer", False),
                XTS_type=broker_data.get("XTS_type", "A"),
                load_instrument=False,
            )
            broker_data["user_id"] = broker_client.wrapper.userID

            broker_data["wrapper"] = codecs.encode(
                pickle.dumps(broker_client.wrapper), "base64"
            ).decode()

            broker_data["md_wrapper"] = codecs.encode(
                pickle.dumps(broker_client.md_wrapper), "base64"
            ).decode()

        else:
            raise InvalidArgumentException(f"Broker '{broker}' not supported")

        return {
            "broker_client": broker_client,
            "broker_data": broker_data,
        }

    def store_broker_client(
        self,
        user_broker_account: dict[str, Any],
        load_instrument: bool = True,
        verify_config: bool = True,
    ) -> BrokerType | None:
        username = user_broker_account["username"]
        nickname = user_broker_account["nickname"]

        self.validate_broker_args(user_broker_account)

        broker_key = self.get_broker_key(username, nickname)

        broker_data = user_broker_account["broker_data"]
        broker = user_broker_account["broker"]

        broker_client: BrokerType | None = None

        if broker == Broker.MOTILAL:
            broker_client = Motilal(
                headers=broker_data["headers"],
                load_instrument=load_instrument,
            )

        elif broker == Broker.DHAN:
            broker_client = Dhan(
                user_id=broker_data["user_id"],
                access_token=broker_data["access_token"],
                load_instrument=load_instrument,
            )

        elif broker == Broker.KOTAK:
            broker_client = Kotak(
                user_id=broker_data["user_id"],
                configuration=broker_data["configuration"],
                otp=broker_data.get("otp"),
                load_instrument=load_instrument,
                verify_config=verify_config,
            )
        elif broker == Broker.ZERODHA:
            broker_client = Zerodha(
                wrapper=broker_data["zerodha_wrapper"],
                load_instrument=load_instrument,
            )

        elif broker == Broker.ANGELONE:
            broker_client = AngelOne(
                user_id=broker_data["user_id"],
                api_key=broker_data["api_key"],
                access_token=broker_data["access_token"],
                refresh_token=broker_data["refresh_token"],
                feed_token=broker_data["feed_token"],
                load_instrument=load_instrument,
            )

        elif broker == Broker.ALICEBLUE:
            broker_client = Aliceblue(
                client=broker_data["client"],
                load_instrument=load_instrument,
            )

        elif broker == Broker.UPSTOX:
            broker_client = Upstox(
                access_token=broker_data["access_token"],
                user_id=broker_data["user_id"],
                load_instrument=load_instrument,
            )

        elif broker == Broker.FINVASIA:
            broker_client = FinvAsia(
                user_id=broker_data["user_id"],
                user_token=broker_data["user_token"],
                load_instrument=load_instrument,
            )

        elif broker == Broker.ICICI:
            broker_client = ICICI(
                api_key=broker_data["api_key"],
                api_secret=broker_data["api_secret"],
                session_token=broker_data["session_token"],
                load_instrument=load_instrument,
            )

        elif broker == Broker.FLATTRADE:
            broker_client = FlatTrade(
                user_id=broker_data["user_id"],
                user_token=broker_data["user_token"],
                load_instrument=load_instrument,
            )

        elif broker == Broker.FIVEPAISA_OPENAPI:
            broker_client = FivePaisa(
                client=broker_data["client"],
                load_instrument=load_instrument,
            )

        elif broker == Broker.IIFL_XTS:
            broker_client = IIFL_XTS(
                wrapper=broker_data["wrapper"],
                md_wrapper=broker_data["md_wrapper"],
                client_id=broker_data["user_id"],
                load_instrument=load_instrument,
            )

        elif broker == Broker.JAINAM:
            broker_client = Jainam(
                wrapper=broker_data["wrapper"],
                md_wrapper=broker_data["md_wrapper"],
                client_id=broker_data["user_id"],
                is_dealer=broker_data.get("is_dealer", False),
                XTS_type=broker_data.get("XTS_type", "A"),
                load_instrument=load_instrument,
            )

        else:
            raise InvalidArgumentException(f"Broker '{broker}' not supported")

        if not load_instrument:
            broker_client = self.set_broker_instruments(
                broker_name=broker, broker=broker_client
            )

        broker_client.username = user_broker_account["username"]
        broker_client.nickname = user_broker_account["nickname"]
        broker_client.broker_name = user_broker_account["broker"]
        broker_client.user_id = broker_data["user_id"]

        self.client_broker_data[broker_key] = broker_client

        return broker_client

    def get_broker_client(
        self, user_broker_account: dict[str, Any], verify_config: bool = True
    ) -> BrokerType:
        username = user_broker_account["username"]
        nickname = user_broker_account["nickname"]

        broker_key = self.get_broker_key(username, nickname)

        if broker_key in self.client_broker_data:
            return self.client_broker_data[broker_key]

        broker_client = self.store_broker_client(
            user_broker_account, load_instrument=False, verify_config=verify_config
        )

        if broker_client is not None:
            return broker_client
        else:
            raise InvalidArgumentException("Invalid broker API configuration")

    def set_broker_instruments(self, broker_name: str, broker: BrokerType) -> BrokerType:
        symbol_data_key = f"{broker_name}_instruments"
        quantplay_symbol_key = f"{broker_name}_qplay_symbols"
        broker_symbol_key = f"{broker_name}_broker_symbols"

        symbol_data = instrument_cache.get(symbol_data_key)
        quantplay_symbol_map = instrument_cache.get(quantplay_symbol_key)
        broker_symbol_map = instrument_cache.get(broker_symbol_key)

        if symbol_data is not None:
            broker.symbol_data = symbol_data

            if broker_name != "Zerodha":
                if quantplay_symbol_map is not None and broker_symbol_map is not None:
                    broker.quantplay_symbol_map = quantplay_symbol_map
                    broker.broker_symbol_map = broker_symbol_map

                else:
                    broker.initialize_broker_symbol_map()
                    instrument_cache.set(
                        quantplay_symbol_key, broker.quantplay_symbol_map
                    )
                    instrument_cache.set(broker_symbol_key, broker.broker_symbol_map)

            return broker

        try:
            symbol_data = PickleUtils.load_data(broker_instruments_map[broker_name])
            broker.symbol_data = symbol_data

            if broker_name != "Zerodha":
                broker.initialize_broker_symbol_map()
                instrument_cache.set(quantplay_symbol_key, broker.quantplay_symbol_map)

            instrument_cache.set(symbol_data_key, symbol_data)

        except Exception:
            traceback.print_exc()

            if broker_name != "Zerodha":
                broker.load_instrument(broker_instruments_map[broker_name])
            else:
                broker.initialize_symbol_data()

        return broker

    def clear_instrument_cache(self, broker: str) -> None:
        symbol_data_key = f"{broker}_instruments"
        instrument_cache.delete(symbol_data_key)

        file_name = broker_instruments_map[broker]
        os.system(f"rm /tmp/{file_name}*")
