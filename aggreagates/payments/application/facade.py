from aggreagates.payments.domain.credit_card_repository import CreditCardRepository
from aggreagates.payments.application.services import WithdrawService


class PaymentsFacade:
    def __init__(self, payments_service: WithdrawService, payments_repository: CreditCardRepository):
        self.payments_service = payments_service
        self.payments_repository = payments_repository

    def make_payment(self, name, amount):
        return self.payments_service.withdraw(name, amount)

    def find_payment_by_name_or_something(self, something):
        return self.payments_repository.get(something)
