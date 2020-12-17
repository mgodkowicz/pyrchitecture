from dataclasses import dataclass
from uuid import uuid4

from pydantic import UUID4

from event_sourcing.shared import OrderItem, Money
from event_sourcing.store import MongoOrderStore
from infrastructure.db import db


@dataclass
class OrderService:
    store: MongoOrderStore

    def add_item(self, id: UUID4, sku: str, price: Money):
        order = self.store.load(id)

        order.add_item(OrderItem(sku=sku, line_total=price))

        self.store.save(order)


if __name__ == "__main__":
    service = OrderService(MongoOrderStore(db=db))

    service.add_item(uuid4(), "123", Money(amount=123.40, currency="USD"))

