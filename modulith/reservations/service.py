from injector import inject

from common.domain_event import DomainEvent
from common.event_publisher import EventPublisher
from reservations.repository import Repository


class SomeKindService:
    @inject
    def __init__(self, repository: Repository, event_publisher: EventPublisher) -> None:
        self.repository = repository
        self.event_publisher = event_publisher

    def add(self, a: int, b: int) -> int:
        print(id(self.repository))
        self.event_publisher.publish({'ds': 1})
        return a + b


class SomeKindServiceDI2:
    def __init__(self, repository: Repository, event_publisher: EventPublisher) -> None:
        self.repository = repository
        self.event_publisher = event_publisher

    def add(self, a: int, b: int) -> int:
        print(self.__class__, id(self.repository))
        self.event_publisher.publish({'ds': 1})
        return a + b
