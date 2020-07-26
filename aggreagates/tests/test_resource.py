from datetime import timedelta

from datetimerange import DateTimeRange
from pytest import fixture

from aggreagates.reservations.domain.policy import LimitedDurationPolicy
from aggreagates.reservations.domain.resource import Resource, ResourceId


@fixture
def resource() -> Resource:
    return Resource(resource_id=ResourceId())


# @fixture
# def policies() -> Policy:
#     return default_policy


def test_reservation_cant_be_longer_then_given_limit(resource):
    time_period = DateTimeRange('2020-03-01 10:00:00', '2020-03-01 18:00:00')

    result = resource.reserve(time_period, LimitedDurationPolicy(timedelta(hours=3)))

    assert not result.is_success()


def test_reservation_cant_overlap_with_previous_ones(resource):
    # given
    resource.reserve(DateTimeRange('2020-03-01 10:00:00', '2020-03-01 12:00:00'))

    # when
    result = resource.reserve(DateTimeRange('2020-03-01 10:00:00', '2020-03-01 12:00:00'))

    assert not result.is_success()


def test_reservation_may_be_requested_right_after_previous_one(resource):
    resource.reserve(DateTimeRange('2020-03-01 10:00:00', '2020-03-01 12:00:00'))

    resource.reserve(DateTimeRange('2020-03-01 12:00:00', '2020-03-01 14:00:00'))

    assert len(resource.get_reserved_periods()) == 2
