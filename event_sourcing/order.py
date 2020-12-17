from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import List, Dict, Callable

from pydantic import UUID4, BaseModel

from aggreagates.common.result import Result
from event_sourcing.events import ItemAdded, Event


class Money(BaseModel):
    amount: float
    currency: str


class OrderItem(BaseModel):
    sku: str
    line_total: Money

    class Config:
        arbitrary_types_allowed = True


class DomainException(Exception):
    pass


@dataclass
class OrderCommandWay:
    order_id: UUID4
    items: List[OrderItem]
    total_amount: Money

    def add_item(self, new_item: OrderItem) -> None:
        if not self.can_add_item(new_item):
            raise DomainException("Unable to add the item")

        self.items.append(new_item)
        self.total_amount += new_item.line_total

    def can_add_item(self, new_item: OrderItem) -> bool:
        pass


class Entity(ABC, BaseModel):
    changes: List = []

    def apply(self, event: object) -> None:
        self.when(event)
        self.changes.append(event)

    @abstractmethod
    def when(self, event: object) -> None:
        pass


class Order(Entity):
    order_id: UUID4
    items: List[OrderItem]
    total_amount: Money

    class Config:
        arbitrary_types_allowed = True

    def add_item(self, new_item: OrderItem) -> Result:
        if new_item in self.items:
            return Result.failure("Unable to add the item")

        total_amount = (self.total_amount + new_item.line_total)
        self.apply(
            ItemAdded(
                order_id=self.order_id,
                item=new_item,
                total=total_amount
            )
        )
        return Result.success()

    def remove_item(self, item: OrderItem) -> Result:
        pass

    def apply_discount(self, amount: Money) -> Result:
        pass

    def when(self, event: Event) -> None:
        events: Dict[event, Callable] = {
            ItemAdded: self.item_added
        }

        events[type(event)](event)

    def item_added(self, event: ItemAdded) -> None:
        self.items.append(event.item)
        self.total_amount = Money(amount=event.total, currency="USD")
