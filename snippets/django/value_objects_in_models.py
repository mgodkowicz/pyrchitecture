from django.db import models
from money import Money


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
