import json
import uuid
from decimal import Decimal
from typing import Optional, Union

from django.db import models
from pydantic import UUID4, BaseModel

from common.result import Result


class Money(BaseModel):
    amount: Decimal
    currency: str

    def __add__(self, other):
        if isinstance(other, Money):
            if other.currency == self.currency:
                return Money(amount=self.amount + other.amount, currency=self.currency)
            else:
                raise ValueError("no no ")
        raise ValueError("no no ")

    def __sub__(self, other):
        if isinstance(other, Money):
            if other.currency == self.currency:
                return Money(amount=self.amount - other.amount, currency=self.currency)
            else:
                raise ValueError("no no ")
        raise ValueError("no no ")


class CreditCard(BaseModel):
    id: UUID4
    balance: Money

    class Config:
        orm_mode = True

    def withdraw(self, withdraw_amount: Money) -> Result:
        # logic ...
        pass


class CreditCardORM(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    balance_amount = models.DecimalField(
        max_digits=19, decimal_places=2
    )
    balance_currency = models.CharField(
        max_length=10
    )

    @property
    def balance(self) -> Money:
        return Money(amount=self.balance_amount, currency=self.balance_currency)

    @balance.setter
    def balance(self, value: Union[Money, dict]) -> None:
        data = value
        if isinstance(value, Money):
            data = value.dict()

        self.balance_amount = data.get("amount")
        self.balance_currency = data.get("currency")


class CreditCardJsonORM(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    timestamp = models.DateTimeField(auto_now=True, auto_created=True)
    data = models.JSONField()


class CreditCardRepository:

    def find(self, card_id: UUID4) -> Optional[CreditCard]:
        card_data = CreditCardORM.objects.filter(id=card_id).first()
        return CreditCard.from_orm(card_data) if card_data else None

    def save(self, card: CreditCard) -> None:
        card_snapshot = card.dict()
        card_id = card_snapshot.pop("id")
        CreditCardORM.objects.update_or_create(id=card_id, defaults=card_snapshot)


class CreditCardJsonRepository:

    def find(self, card_id: UUID4) -> Optional[CreditCard]:
        try:
            credit_card_model = CreditCardJsonORM.objects.get(id=card_id)
            return CreditCard.parse_obj(credit_card_model.data)
        except CreditCardJsonORM.DoesNotExist:
            return None

    def save(self, card: CreditCard) -> None:
        card_snapshot = json.loads(card.json())
        CreditCardJsonORM.objects.update_or_create(
            id=card.id, data=card_snapshot
        )


class TestD(TestCase):

    def setUp(self) -> None:
        self.repo = CreditCardRepository()
        self.json_repo = CreditCardJsonRepository()

    def test_agg(self):
        amount = Money(amount=Decimal(200), currency="USD")
        m = CreditCardORM(balance_amount=Decimal(100), balance_currency="USD")
        m.save()
        domain = self.repo.find(m.id)

        domain.balance = amount
        self.repo.save(domain)

        m2 = self.repo.find(m.id)
        assert m2.balance == amount

    def test_json_aggregate(self):
        balance = Money(amount=Decimal(200), currency="USD")
        credit_card = CreditCard(id=uuid.uuid4(), balance=balance)

        self.json_repo.save(credit_card)

        saved_card = self.json_repo.find(credit_card.id)
        assert saved_card.balance == balance
