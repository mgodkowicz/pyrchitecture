from django.db import models


# anty-pattern
from djmoney.models.fields import MoneyField
from djmoney.money import Money


class Book(models.Model):
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
    title = models.CharField(max_length=500)
    price = MoneyField()

    def change_price(self, new_price: Money):
        self.price = new_price


class Book(models.Model):
    uuid = models.UUIDField()
    shelf = models.CharField()

    def relocate_to(self, shelf_number):
        pass
