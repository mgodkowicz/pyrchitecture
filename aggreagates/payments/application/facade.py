from aggreagates.payments.application.repositories import AccountRepository
from aggreagates.payments.application.services import PaymentService


class PaymentsFacade:
    def __init__(self, payments_service: PaymentService, payments_repository: AccountRepository):
        self.payments_service = payments_service
        self.payments_repository = payments_repository

    def make_payment(self, name, amount):
        return self.payments_service.debit(name, amount)

    def find_payment_by_name_or_something(self, something):
        return self.payments_repository.get(something)
