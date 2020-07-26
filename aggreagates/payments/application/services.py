from aggreagates.payments.application.repositories import AccountRepository
from aggreagates.common.result import Result, failure


class PaymentService:
    def __init__(self, repository: AccountRepository):
        self.repository = repository

    def debit(self, name, amount) -> Result:
        something = self.repository.get(name)

        if something is None:
            return failure(f"Account {name} does not exists")

        result = something.pay(amount)

        if result.is_success():
            self.repository.save(something)

        return result
