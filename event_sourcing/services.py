from dataclasses import dataclass
from uuid import uuid4

from pydantic import UUID4

from event_sourcing.shared import OrderItem, Money
from event_sourcing.store import MongoOrderStore, EntityStore
from infrastructure.db import db


@dataclass
class OrderService:
    store: EntityStore

    def add_item(self, id: UUID4, sku: str, price: Money):
        order = self.store.load(id)

        result = order.add_item(OrderItem(sku=sku, line_total=price))

        self.store.save(order)

        return result


if __name__ == "__main__":
    service = OrderService(MongoOrderStore(db=db))

    service.add_item(uuid4(), "123", Money(amount=123.40, currency="USD"))
