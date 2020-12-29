from dependency_injector import containers, providers

from common.event_publisher import InMemoryEventPublisher
from reservations.conf_root import ReservationsContainer


class ApplicationContainer(containers.DeclarativeContainer):
    event_publisher = providers.Singleton(
        InMemoryEventPublisher,
    )

    reservations = providers.Container(
        ReservationsContainer,
        event_publisher=event_publisher
    )
