import logging
from abc import ABC, abstractmethod
from typing import Optional

from common.domain_event import DomainEvent


logger = logging.getLogger(__name__)


class EventPublisher(ABC):
    @abstractmethod
    def publish(self, event: DomainEvent) -> None:
        pass


class InMemoryEventPublisher(EventPublisher):
    def __init__(self, handlers: Optional[dict] = None) -> None:
        self.handlers = handlers or {}

    def subscribe(self, event: DomainEvent, callback: callable):
        if not callable(callback):
            raise ValueError("callback must be callable")

        if not event:
            raise ValueError("Event cant be empty")

        if event not in self.handlers:
            self.handlers[event] = [callback]
        else:
            self.handlers[event].append(callback)

    def publish(self, event: DomainEvent) -> None:
        try:
            for handler in self.handlers[type(event)]:
                logger.info(
                    "Publishing event %s %s with handler %s",
                    type(event),
                    event.dict(),
                    handler,
                )
                handler(**event.dict())

        except KeyError:
            logger.warning("Event %s do not have any handlers", type(event))


event_publisher = InMemoryEventPublisher()
