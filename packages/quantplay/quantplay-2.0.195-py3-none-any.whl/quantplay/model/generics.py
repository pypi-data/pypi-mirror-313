from typing import Literal, TypedDict

ExchangeType = Literal["NSE", "BSE", "NFO", "BFO", "CDS", "BCD", "MCX"]
ProductType = Literal["NRML", "MIS", "CNC"]
OrderTypeType = Literal["MARKET", "LIMIT", "SL", "SL-M"]
TransactionType = Literal["SELL", "BUY"]
InstrumentType = Literal["CE", "PE", "EQ", "FUT"]
OrderStatusType = Literal["COMPLETE", "REJECTED", "CANCELLED", "TRIGGER PENDING", "OPEN"]


class ZerodhaTypes:
    ExchangeType = Literal["NSE", "BSE", "NFO", "BFO", "CDS", "BCD", "MCX"]
    TransactionTypeType = Literal["BUY", "SELL"]
    OrderTypeType = Literal["MARKET", "LIMIT", "SL", "SL-M"]
    ProductType = Literal["CNC", "MIS", "NRML"]
    ValidityType = Literal["DAY", "IOC", "TTL"]
    OrderVarietyTypes = Literal["regular", "amo", "co", "iceberg", "auction"]

    HistoricalIntervalType = Literal[
        "minute",
        "day",
        "3minute",
        "5minute",
        "10minute",
        "15minute",
        "30minute",
        "60minute",
    ]


class AliceblueTypes:
    ExchangeType = Literal[
        "NSE",
        "NFO",
        "CDS",
        "BSE",
        "BFO",
        "BCD",
        "MCX",
    ]


class NorenTypes:
    OrderTypeType = Literal["MKT", "LMT", "SL-MKT", "SL-LMT"]
    ProductType = Literal["M", "C", "I", "B", "H"]
    TransactionTypeType = Literal["B", "S"]


class DhanTypes:
    OrderTypeType = Literal["MARKET", "LIMIT", "STOP_LOSS", "STOP_LOSS_MARKET"]
    ProductType = Literal["CNC", "INTRADAY", "MARGIN"]


XTSExchangeSegmentType = Literal[1, 2, 3, 11, 12]


class XTSInstrumentType(TypedDict):
    exchangeSegment: XTSExchangeSegmentType
    exchangeInstrumentID: str | int


class XTSTypes:
    ExchangeSegmentType = XTSExchangeSegmentType
    XTSMessageCodeType = Literal[1501, 1502, 1505, 1507, 1510, 1512, 1105]
    PublishFormatType = Literal["JSON", "Binary"]
    ExchangeType = Literal["NSECM", "NSEFO", "NSECD", "BSECM", "BSEFO"]
    InstrumentType = XTSInstrumentType
    SeriesType = str
    OrderSide = Literal["BUY", "SELL"]
    OrderType = Literal["Market", "StopLimit", "StopMarket", "Limit"]
    ProductType = Literal["CO", "CNC", "MIS", "NRML"]
    PositionSqureOffModeType = Literal["DayWise", "NetWise"]
    PositionSquareOffQuantityTypeType = Literal["Percentage", "ExactQty"]
    DayOrNetType = Literal["DAY", "NET"]


class QuantplayOrder(TypedDict):
    exchange: ExchangeType
    transaction_type: TransactionType
    tradingsymbol: str
    quantity: int
    product: ProductType
