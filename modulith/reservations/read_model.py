from functools import singledispatchmethod
from typing import Any

from reservations.events import IntegersAdded


class ExampleReadModel:

    @singledispatchmethod
    def handle(self, event: Any) -> None:
        raise NotImplementedError(f"Cannot handle {type(event)}")

    @handle.register
    def _(self, event: IntegersAdded) -> None:
        print("handling ", event)
