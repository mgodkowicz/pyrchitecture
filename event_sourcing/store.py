from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Any, get_args, Dict, List

from pydantic import UUID4
from pymongo.database import Database

from event_sourcing.order import Order

T = TypeVar("T")


class EntityStore(ABC, Generic[T]):
    model_class: T

    def __new__(cls, *args: Any, **kwargs: Any) -> "EntityStore":
        """
        Get model from type annotations.
        """
        # TODO Make it bulletproof.
        types_arguments = get_args(cls.__orig_bases__[0])  # type: ignore
        model_class = types_arguments[0]

        class_ = super().__new__(cls, *args, **kwargs)  # type: ignore

        class_.model_class = model_class
        return class_

    @abstractmethod
    def save(self, entity: T) -> None:
        pass

    @abstractmethod
    def load(self, id: str) -> T:
        pass


class MongoOrderStore(EntityStore[Order]):
    def __init__(self, db: Database) -> None:
        self.collection = db["orders"]

    def save(self, entity: T) -> None:
        changes = entity.changes
        # TODO parsing from domain event to inf event
        self.collection.insert_many()

    def load(self, id_: str) -> T:
        db_events = self.collection.find({"order_id": id_})
        # TODO parsing
        if not db_events:
            return self.model_class()

        entity = self.model_class()
        for event in db_events:
            entity.when(event)

        return entity


class InMemoryOrderStore(EntityStore[Order]):
    def __init__(self):
        self.stored_events: Dict[UUID4, List] = {}

    def save(self, entity: T) -> None:
        current_stream = self.stored_events.setdefault(entity.order_id, [])
        current_stream.extend(list(entity.pending_events))
        self.stored_events[entity.order_id] = current_stream
        entity.flush_events()

    def load(self, id: str) -> T:
        return self.model_class.recreate_from(
            self.stored_events.get(id, []), self.model_class.initial(id)
        )
