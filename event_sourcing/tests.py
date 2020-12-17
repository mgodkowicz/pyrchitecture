from unittest import TestCase
from uuid import uuid4

from event_sourcing.events import ItemAdded
from event_sourcing.order import Order
from event_sourcing.shared import OrderItem, Money


class OrderTests(TestCase):

    def test_can_add_item(self):
        # given
        order = self._order()
        item = self._item()

        # when
        result = order.add_item(item)

        # then
        assert result.is_success()
        # and
        added = result.value
        # and
        assert added == ItemAdded.new(order.order_id, item, item.line_total.amount)

    def test_can_add_only_one_item_with_the_same_sku(self):
        # given
        order = self._order()
        # and
        item = self._item()
        # and
        order.when(ItemAdded.new(order.order_id, item, item.line_total.amount))
        # when
        result = order.add_item(self._item())
        # then
        assert result.is_failure()

    # TODO builders should be customized
    def _order(self, **kwargs) -> Order:
        return Order(order_id=uuid4(), items=[], total_amount=Money(amount=0, currency="USD"))

    def _item(self, **kwargs) -> OrderItem:
        return OrderItem(sku='123', line_total=Money(amount=100, currency="USD"))
