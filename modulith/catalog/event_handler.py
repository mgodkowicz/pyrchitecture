from functools import singledispatchmethod
from typing import Any

from reservations.events import IntegersAdded


class EventHandlerInAnotherModule:

    @singledispatchmethod
    def handle(self, event: Any, **kwargs: Any) -> None:
        raise NotImplementedError(f"Cannot handle {type(event)}")

    @handle.register
    def _(self, event: IntegersAdded, **kwargs: Any) -> None:
        print("handling the singal ", event)
