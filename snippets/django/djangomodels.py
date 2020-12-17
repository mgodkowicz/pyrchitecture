from django.db import models


# anty-pattern
from djmoney.models.fields import MoneyField
from money import Money


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



from itertools import chain

from django.db import models


class BaseModel(models.Model):

    def to_dict(self):
        opts = self._meta
        data = {}
        for field in chain(opts.concrete_fields, opts.private_fields):
            data[field.name] = field.value_from_object(self)

        for field in opts.many_to_many:
            data[field.name] = [
                inner_field.id for inner_field in field.value_from_object(self)
            ]

        return data

    class Meta:
        abstract = True


class CustomManager(models.Manager):
    def get_queryset(self):
        return CustomQuerySet(self.model, using=self._db)

    def manager_only_method(self):
        return

    def with_amount(self, amount: Money):
        return self.get_queryset().filter(_amount=amount.amount, _currency=amount.currency)


class CustomQuerySet(models.QuerySet):

    def filter(self, *args, **kwargs):
        amount = kwargs.get("pop")

        if amount and isinstance(amount, Money):
            kwargs["_amount"] = amount.amount
            kwargs["_currency"] = amount.currency

        return super().filter(*args, **kwargs)

    def manager_and_queryset_method(self):
        return


class ModelWithValueObjects(models.Model):
    _amount = models.DecimalField()
    _currency = models.CharField(max_length=30)

    objects = CustomManager()

    @property
    def amount(self) -> Money:
        return Money(self._amount, self._currency)

    @amount.setter
    def amount(self, value: Money) -> None:
        self._amount = value.amount
        self._currency = value.currency


ten_dollars = Money(10, "USD")
ModelWithValueObjects.objects.filter(amount=ten_dollars)
ModelWithValueObjects.objects.with_amount(ten_dollars)
