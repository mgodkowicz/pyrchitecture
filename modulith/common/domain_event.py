import logging
from abc import ABC
from typing import Any, Generator

from bson import ObjectId
from bson.objectid import InvalidId
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


class DomainEvent(BaseModel, ABC):
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectIdStr: lambda oid: str(oid),
        }

    def dict(self, *args: Any, **kwargs: Any) -> dict:
        data = super().dict(*args, **kwargs)
        data["event"] = str(self.__class__)
        return data
