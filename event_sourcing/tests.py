from unittest import TestCase
from uuid import uuid4

from event_sourcing.events import ItemAdded
from event_sourcing.order import Order
from event_sourcing.services import OrderService
from event_sourcing.shared import OrderItem, Money
from event_sourcing.store import InMemoryOrderStore


class OrderTests(TestCase):
    def setUp(self) -> None:
        self.order_repository = InMemoryOrderStore()
        self.order_service = OrderService(self.order_repository)

    def usd_100(self):
        return Money(amount=100, currency="USD")

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
        assert added == ItemAdded.new(order.order_id, item, item.line_total)

    def test_can_add_only_one_item_with_the_same_sku(self):
        # given
        order = self._order()
        # and
        item = self._item()
        # and
        order.when(ItemAdded.new(order.order_id, item, item.line_total))
        # when
        result = order.add_item(self._item())
        # then
        assert result.is_failure()

    def test_should_remove_existing_item(self):
        # given
        order = self._order()
        item = self._item()
        # and
        order.add_item(item)
        # when
        result = order.remove_item(item)
        # then
        assert result.is_success()

    def test_item_have_to_be_added_to_remove_it(self):
        pass

    # TODO builders should be customized
    def _order(self, **kwargs) -> Order:
        return Order(
            order_id=uuid4(), items=[], total_amount=Money(amount=0, currency="USD")
        )

    def _item(self, **kwargs) -> OrderItem:
        return OrderItem(sku="123", line_total=Money(amount=100, currency="USD"))

    # FIXME integration stuff
    def test_should_add_item(self):
        order_id = uuid4()
        result = self.order_service.add_item(order_id, "123445", self.usd_100())

        assert result.is_success()

    def test_should_save_and_load(self):
        # given
        order = self._order()
        # and
        order.add_item(self._item())
        # and
        self.order_repository.save(order)
        # when
        load = self.order_repository.load(order.order_id)
        # then
        assert load.add_item(self._item()).is_failure()
