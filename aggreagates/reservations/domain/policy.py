from abc import ABC, abstractmethod
from datetime import timedelta

from typing import List

from datetimerange import DateTimeRange

from aggreagates.common.result import success, failure, Result


class Policy(ABC):

    @abstractmethod
    def is_satisfied(self, period: DateTimeRange, reserved_periods: List[DateTimeRange]) -> Result:
        pass


class LimitedDurationPolicy(Policy):
    def __init__(self, max_duration: timedelta):
        self.max_duration = max_duration

    def is_satisfied(self, period: DateTimeRange, reserved_periods: List[DateTimeRange]) -> Result:
        if period.timedelta < self.max_duration:
            return success()
        return failure("Duration limited exceeded")


class NoOverlappingPolicy(Policy):

    def is_satisfied(self, period: DateTimeRange, reserved_periods: List[DateTimeRange]) -> Result:
        if any(
            period in reserved_period
            for reserved_period in reserved_periods
        ):
            return failure("Reservation cant overlap with previous ones")

        return success()


class CompositePolicyCheck(Policy):
    def __init__(self, policies: List[Policy]):
        self.policies = policies

    def is_satisfied(self, period: DateTimeRange, reserved_periods: List[DateTimeRange]) -> Result:
        for policy in self.policies:
            if not (result := policy.is_satisfied(period, reserved_periods)).is_success():
                return result
        return success()


default_policy = CompositePolicyCheck(
    [
        LimitedDurationPolicy(timedelta(hours=3)),
        NoOverlappingPolicy(),
    ]
)
