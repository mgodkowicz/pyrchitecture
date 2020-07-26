from typing import List
from uuid import uuid4

from datetimerange import DateTimeRange
from pydantic import BaseModel, UUID4

from aggreagates.common.aggregate_base import AggregateBase
from aggreagates.common.result import Result, success
from aggreagates.reservations.domain.policy import Policy, default_policy
from aggreagates.reservations.domain.reservation import Reservation


class ResourceId(BaseModel):
    id: UUID4 = uuid4()

    def __hash__(self):
        return hash(self.id)

    @classmethod
    def from_string(cls, id: str):
        return cls(id=UUID4(id))


class Resource(AggregateBase):
    resource_id: ResourceId
    reservations: List[Reservation] = []

    def reserve(self, period: DateTimeRange, policy: Policy = default_policy) -> Result:
        result = policy.is_satisfied(period, self.get_reserved_periods())

        if result.is_success():
            reservation = Reservation(period=period)
            self.reservations.append(reservation)
            return success(reservation)

        return result

    def get_reserved_periods(self) -> List[DateTimeRange]:
        return [
            reservation.period for reservation in self.reservations
        ]
