from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import List, Dict, Callable

from pydantic import UUID4, BaseModel

from aggreagates.common.result import Result
from event_sourcing.events import ItemAdded, Event, ItemRemoved
from event_sourcing.shared import OrderItem, Money


class DomainException(Exception):
    pass


# @dataclass
# class OrderCommandWay:
#     order_id: UUID4
#     items: List[OrderItem]
#     total_amount: Money
#
#     def add_item(self, new_item: OrderItem) -> None:
#         if not self.can_add_item(new_item):
#             raise DomainException("Unable to add the item")
#
#         self.items.append(new_item)
#         self.total_amount += new_item.line_total
#
#     def can_add_item(self, new_item: OrderItem) -> bool:
#         pass


class Entity(ABC, BaseModel):
    changes: List = []

    @classmethod
    def recreate_from(cls, domain_events: List[Event], initial_state: "Entity"):
        for event in domain_events:
            initial_state.apply(event)
        return initial_state

    def apply(self, event: object) -> None:
        self.when(event)
        self.changes.append(event)

    def flush_events(self) -> None:
        self.changes.clear()

    @property
    def pending_events(self) -> tuple:
        return tuple(self.changes.copy())

    @abstractmethod
    def when(self, event: object) -> None:
        pass


class Order(Entity):
    order_id: UUID4
    items: List[OrderItem]
    total_amount: Money

    class Config:
        arbitrary_types_allowed = True

    def when(self, event: Event) -> None:
        events: Dict[event, Callable] = {
            ItemAdded: self.item_added,
            ItemRemoved: self.item_removed,
        }
        events[type(event)](event)

    @classmethod
    def initial(cls, order_id: UUID4) -> "Order":
        return cls(
            order_id=order_id, items=[], total_amount=Money(amount=0, currency="USD")
        )

    def add_item(self, new_item: OrderItem) -> Result:
        if new_item in self.items:
            return Result.failure("Item already in order.")

        total_amount = self.total_amount + new_item.line_total

        event = ItemAdded(order_id=self.order_id, item=new_item, total=total_amount)
        self.apply(event)
        return Result.success(event)

    def remove_item(self, item: OrderItem) -> Result:
        if item not in self.items:
            return Result.failure("Item not in order.")

        total_amount = self.total_amount - item.line_total

        event = ItemRemoved(order_id=self.order_id, item=item, total=total_amount)
        self.apply(event)
        return Result.success(event)

    def apply_discount(self, amount: Money) -> Result:
        # TODO
        pass

    def item_added(self, event: ItemAdded) -> None:
        self.items.append(event.item)
        self.total_amount = event.total

    def item_removed(self, event: ItemRemoved) -> None:
        self.items.remove(event.item)
        self.total_amount = event.total
