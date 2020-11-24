from typing import Optional

from pydantic import UUID4

from aggreagates.payments.domain.credit_card_repository import CreditCardRepository
from aggreagates.payments.domain.creditcard import CreditCard
from aggreagates.payments.infrastructure.orm_models import CreditCardORM


class InMemoryCreditCardRepository(CreditCardRepository):
    def __init__(self, data=None):
        self.data = data or {}

    def get(self, id: UUID4) -> Optional[CreditCard]:
        return self.data.get(id)

    def save(self, model: CreditCard) -> None:
        self.data[model.id] = model


class DjangoCreditCardRepository(CreditCardRepository):

    def get(self, id: UUID4) -> CreditCard:
        credit_card = CreditCardORM.objects.filter(id=id)
        return credit_card.to_domain() if credit_card else credit_card

    def save(self, credit_card: CreditCard) -> None:
        CreditCardORM.update_from_domain(credit_card=credit_card)
