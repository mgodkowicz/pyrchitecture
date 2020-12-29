from dependency_injector import containers, providers
from injector import Module, Binder

from reservations.repository import Repository, InMemoryRepository
from reservations.service import SomeKindServiceDI2


class ReservationsRoot(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(Repository, to=InMemoryRepository)


# different DI framework test:
class ReservationsContainer(containers.DeclarativeContainer):
    event_publisher = providers.Dependency()

    repository = providers.Factory(
        InMemoryRepository,
    )

    service = providers.Factory(
        SomeKindServiceDI2,
        repository=repository,
        event_publisher=event_publisher,
    )
