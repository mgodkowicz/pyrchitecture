from typing import Optional

from aggreagates.payments.application.repositories import AccountRepository
from aggreagates.payments.domain.account import Account


class InMemoryPaymentsRepository(AccountRepository):
    def __init__(self, data=None):
        self.data = data or {}

    def get(self, name) -> Optional[Account]:
        return self.data.get(name)

    def save(self, model: Account) -> None:
        self.data[model.name] = model
