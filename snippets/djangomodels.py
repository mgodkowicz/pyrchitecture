from django.db import models


# anty-pattern
from djmoney.models.fields import MoneyField
from djmoney.money import Money


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
