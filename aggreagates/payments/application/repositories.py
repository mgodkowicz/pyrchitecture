from abc import ABC

from aggreagates.payments.domain.account import Account


class AccountRepository(ABC):
    def get(self, name) -> Account:
        pass

    def save(self, model: Account) -> None:
        pass
