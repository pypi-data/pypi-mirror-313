import binascii
from queue import Queue

import pyotp

from quantplay.broker.finvasia_utils.fa_noren import FA_NorenApi
from quantplay.broker.noren import Noren
from quantplay.exception.exceptions import (
    InvalidArgumentException,
    RetryableException,
    TokenException,
)
from quantplay.model.order_event import OrderUpdateEvent


class FinvAsia(Noren):
    def __init__(
        self,
        order_updates: Queue[OrderUpdateEvent] | None = None,
        api_secret: str | None = None,
        imei: str | None = None,
        password: str | None = None,
        totp: str | None = None,
        user_id: str | None = None,
        vendor_code: str | None = None,
        user_token: str | None = None,
        load_instrument: bool = True,
    ) -> None:
        super().__init__(order_updates=order_updates, load_instrument=load_instrument)
        self.api = FA_NorenApi(
            "https://api.shoonya.com/NorenWClientTP/",
            "wss://api.shoonya.com/NorenWSTP/",
        )

        try:
            if user_token and user_id:
                self.api.set_session(userid=user_id, usertoken=user_token)
                response = {
                    "susertoken": user_token,
                    "actid": user_id,
                    "email": None,
                    "uname": None,
                }
            elif user_id and password and totp and vendor_code and api_secret and imei:
                totp = pyotp.TOTP(str(totp)).now()
                response = self.login(
                    user_id=user_id,
                    password=password,
                    twoFA=totp,
                    vendor_code=vendor_code,
                    api_secret=api_secret,
                    imei=imei,
                )
            else:
                raise TokenException("Missing Args")

        except TokenException:
            raise

        except binascii.Error:
            raise TokenException("Invalid TOTP key provided")

        except Exception as e:
            raise RetryableException(str(e))

        self.set_attributes(response)

    def login(
        self,
        user_id: str,
        password: str,
        twoFA: str,
        vendor_code: str,
        api_secret: str,
        imei: str,
    ):
        print("Shoonya login")
        response = self.api.login(
            userid=user_id,
            password=password,
            twoFA=twoFA,
            vendor_code=vendor_code,
            api_secret=api_secret,
            imei=imei,
        )

        if response is None:
            raise InvalidArgumentException("Invalid API credentials")

        return response
