from typing import TypedDict

from quantplay.model.generics import (
    ExchangeType,
    OrderStatusType,
    OrderTypeType,
    ProductType,
    TransactionType,
)


class OrderUpdateEvent(TypedDict):
    username: str
    nickname: str

    tradingsymbol: str
    quantity: int
    order_id: str
    placed_by: str
    price: float
    trigger_price: float | None
    tag: str
    exchange_order_id: str

    product: ProductType
    status: OrderStatusType
    exchange: ExchangeType
    order_type: OrderTypeType
    transaction_type: TransactionType
