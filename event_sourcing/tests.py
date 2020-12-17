from unittest import TestCase
from uuid import uuid4

from pydantic import UUID4

from event_sourcing.order import Order, OrderItem, Money


class OrderTests(TestCase):

    def test_can_add_only_one_item_with_the_same_sku(self):
        order = Order(order_id=uuid4(), items=[], total_amount=Money(amount=0, currency="USD"))
        item = OrderItem(sku='123', line_total=Money(amount=100, currency="USD"))

        result = order.add_item(item)

        assert result.is_success() is True
