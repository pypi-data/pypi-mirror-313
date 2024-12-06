from py_vollib.black_scholes.implied_volatility import implied_volatility  # type:ignore
from datetime import date, datetime, time
from typing import Literal


class ImpliedVolatility:
    @staticmethod
    def get_option_type(option_type: Literal["CE", "PE"]) -> Literal["c", "p"]:
        if option_type == "CE":
            return "c"

        elif option_type == "PE":
            return "p"

    @staticmethod
    def time_to_expiry(expiry: date, tick_time: float) -> float:
        expiry_dt = datetime.combine(date=expiry, time=time(15, 30, 0, 0))
        time_to_expiry = (expiry_dt.timestamp() - tick_time) / 31536000

        return time_to_expiry

    @staticmethod
    def iv(
        option_price: float,
        strike: int,
        option_type: Literal["CE", "PE"],
        underlying_price: float,
        tte: float,
    ) -> float:
        rate_of_interest = 0.1

        return (
            implied_volatility(  # type:ignore
                option_price, underlying_price, strike, tte, rate_of_interest, option_type
            )
            * 100
        )
