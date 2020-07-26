from abc import ABC

from pydantic import BaseModel


class AggregateBase(BaseModel, ABC):
    version: int = 0
