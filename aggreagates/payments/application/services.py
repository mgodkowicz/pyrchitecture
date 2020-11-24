from aggreagates.payments.domain.credit_card_repository import CreditCardRepository
from aggreagates.common.result import Result, failure


class WithdrawService:
    def __init__(self, repository: CreditCardRepository):
        self.repository = repository

    def withdraw(self, id, amount) -> Result:
        credit_card = self.repository.get(id)

        if credit_card is None:
            return failure(f"Account {id} does not exists")

        result = credit_card.withdraw(amount)

        self.repository.save(credit_card)

        return result
