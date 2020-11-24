from aggreagates.payments.application.facade import PaymentsFacade
from aggreagates.payments.application.services import WithdrawService
from aggreagates.payments.infrastructure.repositories import InMemoryCreditCardRepository

payments_repository = InMemoryCreditCardRepository()


def create_payments_facade() -> PaymentsFacade:
    return PaymentsFacade(
        WithdrawService(
            payments_repository
        ),
        payments_repository
    )


payments_facade: PaymentsFacade = create_payments_facade()
