from aggreagates.payments.application.facade import PaymentsFacade
from aggreagates.payments.application.services import PaymentService
from aggreagates.payments.infrastructure.repositories import InMemoryPaymentsRepository

payments_repository = InMemoryPaymentsRepository()


def payments_facade() -> PaymentsFacade:
    return PaymentsFacade(
        PaymentService(
            payments_repository
        ),
        payments_repository
    )
