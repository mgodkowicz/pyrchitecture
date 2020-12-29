from datetime import datetime, timedelta
from unittest import TestCase

from datetimerange import DateTimeRange
from django.db import models, transaction
from django.utils import timezone

from djmoney.models.fields import MoneyField
from pydantic import UUID4

from aggreagates.common.result import Result


class Book(models.Model):
    uuid = models.UUIDField()
    title = models.CharField(max_length=500)
    is_sold = models.BooleanField(default=False)

    def sell(self):
        self.is_sold = True
        # logic

    @classmethod
    def change_prices(cls, title: str, new_price):
        # operuje na swoim zestawie danych ale istnieje złozonosc ktora nie istnieje w katalogu
        for book in Book.objects.with_title(title).filter(is_sold=False):
            book.change_price(new_price)

    def relocate_to(self, shelf_number):
        # operuje na swoim zestawie danych
        # ale
        if self.is_sold:  # zlozonosc ktora nie istnieje w magazynie
            pass


class Book(models.Model):
    uuid = models.UUIDField()
    title = models.CharField(max_length=500)
    price = MoneyField()

    def change_price(self, new_price: Money):
        self.price = new_price


class Book(models.Model):
    uuid = models.UUIDField()
    shelf = models.CharField()

    def relocate_to(self, shelf_number):
        pass



import uuid

from django.db import models
from djmoney.models.fields import MoneyField


## Similar example can be created for car object.


class Car(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    registration_number = models.CharField(max_length=10)
    color = models.CharField(max_length=50)
    seats = models.PositiveSmallIntegerField()
    engine = models.CharField(max_length=50)  # TODO choice field?
    price = MoneyField(default_currency="USD", max_digits=14, decimal_places=2)
    air_condition = models.BooleanField()

    def reserve(self, booker, start, end):
        if Reservation.is_available(self, start, end):
            Reservation.objects.create(booker_id=booker, start=start, end=end)

    @classmethod
    def change_price(cls, new_price):
        return cls.objects.update(price=new_price)


class Reservation(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    booker_id = models.UUIDField(
        default=uuid.uuid4
    )
    start = models.DateTimeField()
    end = models.DateTimeField()

    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="reservations")

    @staticmethod
    def is_available(car, start, end):
        return Reservation.objects.filter(
            car=car,
            start__lte=end,
            end__gte=start
        ).exists()


# How to make it look more like an aggregate?
class CarAggregateRoot(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )

    @property
    def reservations_mem(self):
        return list(self.reservations.all())

    # transaction decorator should be on service layer
    @transaction.atomic()
    def reserve(self, booker: UUID4, period: DateTimeRange):
        result = self.overlaps(period)

        if result.is_success():
            self.reservations.create(
                booker_id=booker,
                period=period
            )
            return Result.success()

        return result

    def overlaps(self, period: DateTimeRange) -> Result:
        if any(
            period in reservation.period
            for reservation in self.reservations.all()
        ):
            return Result.failure("Reservation cant overlap with previous ones")

        return Result.success()


class ReservationEntity(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    booker_id = models.UUIDField(
        default=uuid.uuid4
    )
    _start = models.DateTimeField()
    _end = models.DateTimeField()

    car = models.ForeignKey("CarAggregateRoot", on_delete=models.CASCADE, related_name="reservations")

    @property
    def period(self):
        return DateTimeRange(self._start, self._end)

    @period.setter
    def period(self, value: DateTimeRange):
        self._start = value.start_datetime
        self._end = value.end_datetime


class TestAggregate(TestCase):

    def setUp(self) -> None:
        tz = timezone.now().tzinfo
        self.start = datetime(2020, 1, 1, 19, 0, tzinfo=tz)
        self.end = self.start + timedelta(days=1)
        self.booker_id: UUID4 = uuid.uuid4()
        self.period = DateTimeRange(self.start, self.end)

    def test_smth(self):
        aggregate = CarAggregateRoot()

        result = aggregate.reserve(self.booker_id, self.period)
        aggregate.save()

        assert result.is_success()
        assert len(aggregate.reservations.all()) == 1

    def test_can_not_reserve_two_times(self):
        aggregate = CarAggregateRoot()
        aggregate.reserve(self.booker_id, self.period)

        result = aggregate.reserve(self.booker_id, self.period)
        aggregate.save()

        assert result.is_failure()


# Another implementations
# - use one model for storage and many objects for logic
# - Save data in json fileds and parse to pydantic objects
