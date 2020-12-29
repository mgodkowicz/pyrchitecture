from injector import Injector, Module, Binder

from common.event_publisher import EventPublisher, InMemoryEventPublisher
from reservations import ReservationsRoot


class EventPublisherConfig(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(EventPublisher, to=InMemoryEventPublisher)


injector = Injector([EventPublisherConfig()])
injector.create_child_injector(ReservationsRoot())
