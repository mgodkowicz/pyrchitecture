from injector import Injector, Module, Binder, singleton

from catalog.root import CatalogRoot
from common.event_publisher import EventPublisher, InMemoryEventPublisher
from reservations import ReservationsRoot


class EventPublisherConfig(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(EventPublisher, to=InMemoryEventPublisher, scope=singleton)


injector = Injector([EventPublisherConfig(), ReservationsRoot(), CatalogRoot()])
