from abc import ABC
from decimal import Decimal

from pydantic import BaseModel, UUID4

# class Money(BaseModel):
#     amount: float
#     currency: str
from event_sourcing.shared import OrderItem


class DiscountAppliedToOrder(BaseModel):
    oder_id: str
    discount_amount: float
    new_total_amount: float


# class OrderItem(BaseModel):
#     line_total: float


class Event(ABC, BaseModel):
    pass


class ItemAdded(Event):
    order_id: UUID4
    item: OrderItem
    total: float

    @classmethod
    def new(cls, order_id: UUID4, item: OrderItem, total: float) -> "ItemAdded":
        return ItemAdded(order_id=order_id, item=item, total=total)
