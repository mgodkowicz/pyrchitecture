import uuid

from django.db import models

from aggreagates.payments.domain.creditcard import CreditCard, Money


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

    def to_domain(self) -> CreditCard:
        return CreditCard(
            self.id,
            Money(self.balance_amount, self.balance_currency)
        )

    @staticmethod
    def update_from_domain(credit_card: CreditCard) -> None:
        CreditCardORM.objects.update_or_create(
            id=credit_card.id,
            defaults={
                "balance_amount": credit_card.balance.amount,
                "balance_currency":  credit_card.balance.currency
            }

        )
