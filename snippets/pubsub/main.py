import logging
from abc import ABC, abstractmethod
from typing import Any, Generator, Optional

from bson import ObjectId
from bson.errors import InvalidId
from pydantic import BaseModel


logger = logging.getLogger(__name__)


class ObjectIdStr(str):
    """
    Use this Field object in PyDantic models to
     easily parse mongo objects it to str in API
    """

    @classmethod
    def __get_validators__(cls) -> Generator:
        yield cls.validate

    @classmethod
    def validate(cls, value: Any) -> ObjectId:
        try:
            return ObjectId(str(value))
        except InvalidId:
            raise ValueError("Not a valid ObjectId")

    @classmethod
    def new(cls) -> "ObjectIdStr":
        return cls(ObjectId())


class Event(BaseModel, ABC):
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectIdStr: lambda oid: str(oid),
        }

    def dict(self, *args: Any, **kwargs: Any) -> dict:
        data = super().dict(*args, **kwargs)
        data["event"] = str(self.__class__)
        return data


class EventPublisher(ABC):
    @abstractmethod
    def publish(self, event: Event) -> None:
        pass


class InMemoryEventPublisher(EventPublisher):
    def __init__(self, handlers: Optional[dict] = None) -> None:
        self.handlers = handlers

    def subscribe(self, event: Event, callback: callable):
        if not callable(callback):
            raise ValueError("callback must be callable")

        if not event:
            raise ValueError("Event cant be empty")

        if event not in self.handlers:
            self.handlers[event] = [callback]
        else:
            self.handlers[event].append(callback)

    def publish(self, event: Event) -> None:
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

# class CeleryEventPublisher(EventPublisher):
#     def __init__(self, handlers: CeleryEventsHandlers) -> None:
#         self.handlers = handlers
#
#     def publish(self, event: Event) -> None:
#         try:
#             handlers = [
#                 celery_app.signature(handler, kwargs=event.dict())
#                 for handler in self.handlers[type(event)]
#             ]
#             logger.info(
#                 "Publishing event %s %s to handlers %s",
#                 type(event),
#                 event.dict(),
#                 handlers,
#             )
#
#             group(handlers).apply_async()
#         except KeyError:
#             logger.warning("Event %s do not have any handlers", type(event))
