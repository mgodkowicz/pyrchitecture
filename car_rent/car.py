from typing import List
from uuid import uuid4

from datetimerange import DateTimeRange
from pydantic import BaseModel, UUID4

# from aggreagates.common.aggregate_base import AggregateBase
from pydantic.dataclasses import dataclass

from aggreagates.common.result import Result, success, failure
from aggreagates.reservations.domain.policy import Policy, default_policy


@dataclass(frozen=True)
class BookerId(BaseModel):
    id: UUID4 = uuid4()

    def __hash__(self):
        return hash(self.id)


class CarId(BaseModel):
    id: UUID4 = uuid4()

    def __hash__(self):
        return hash(self.id)

    @classmethod
    def from_string(cls, id: str):
        return cls(id=UUID4(id))


class Reservation(BaseModel):
    period: DateTimeRange
    booker_id: BookerId
    #
    # def __contains__(self, item):
    #     if isinstance(item, Reservation):

    class Config:
        arbitrary_types_allowed = True


class Car(BaseModel):
    car_id: CarId
    reservations: List[Reservation] = []

    def reserve(self, period: DateTimeRange, booker_id: BookerId) -> Result:
        if any(
            period in reserved_period
            for reserved_period in self.get_reserved_periods()
        ):
            return failure("Reservation cant overlap with previous ones")

        reservation = Reservation(period=period, booker_id=booker_id)
        self.reservations.append(reservation)
        return success(reservation)

    def get_reserved_periods(self) -> List[DateTimeRange]:
        return [
            reservation.period for reservation in self.reservations
        ]
