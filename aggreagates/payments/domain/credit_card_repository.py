from abc import ABC

from pydantic import UUID4

from aggreagates.payments.domain.creditcard import CreditCard


class CreditCardRepository(ABC):
    def get(self, id: UUID4) -> CreditCard:
        pass

    def save(self, model: CreditCard) -> None:
        pass
