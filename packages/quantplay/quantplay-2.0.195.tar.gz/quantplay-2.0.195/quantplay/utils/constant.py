import decimal
import logging
from datetime import datetime
from typing import Any, Literal

import numpy as np

formatter = logging.Formatter(
    "%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"
)


class LoggerUtils:
    @staticmethod
    def get_log_file_path(file_name: str) -> str:
        today_date = datetime.now()

        return f"/tmp/{file_name}-{today_date.strftime('%Y-%m-%d:01')}.log"

    @staticmethod
    def setup_logger(
        logger_name: str, log_file: str, level: int = logging.DEBUG
    ) -> logging.Logger:
        log_file = LoggerUtils.get_log_file_path(log_file)
        """Function setup as many loggers as you want"""

        handler = logging.FileHandler(log_file)
        handler.setFormatter(formatter)

        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        logger.addHandler(handler)
        logger.propagate = False
        logger.disabled = False

        return logger


class Constants:
    logger = LoggerUtils.setup_logger("main_logger", "trading")
    latency_logger = LoggerUtils.setup_logger("latency", "latency")
    order_execution_logger = LoggerUtils.setup_logger(
        "order_execution", "order_execution"
    )
    historical_data_logger = LoggerUtils.setup_logger(
        "hist_data_looger", "historical_data"
    )
    tick_logger = LoggerUtils.setup_logger("tick_logger", "tick")

    @staticmethod
    def myconverter(o: Any):
        if isinstance(o, datetime):
            return o.__str__()
        if isinstance(o, decimal.Decimal):
            return float(o)
        if isinstance(o, np.int64):  # type:ignore
            return int(o)  # type: ignore

    @staticmethod
    def round_to_tick(number: int | float) -> float:
        return round(number * 20) / 20


class OrderType:
    market: Literal["MARKET"] = "MARKET"
    slm: Literal["SL-M"] = "SL-M"
    sl: Literal["SL"] = "SL"
    limit: Literal["LIMIT"] = "LIMIT"


class OrderStatus:
    complete = "COMPLETE"
    cancelled = "CANCELLED"
    open = "OPEN"
    rejected = "REJECTED"
    trigger_pending = "TRIGGER PENDING"
    modify_validation_pending = "MODIFY VALIDATION PENDING"
    validation_pending = "VALIDATION PENDING"
