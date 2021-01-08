from injector import inject

from common.event_publisher import EventPublisher
from reservations.events import IntegersAdded, integers_added
from reservations.repository import Repository


class SomeKindService:
    @inject
    def __init__(self, repository: Repository, event_publisher: EventPublisher) -> None:
        self.repository = repository
        self.event_publisher = event_publisher

    def add(self, a: int, b: int) -> int:
        print(id(self.repository))
        self.event_publisher.publish(IntegersAdded(num_one=a, num_sec=b))
        integers_added.send(sender=self.__class__, event=IntegersAdded(num_one=a, num_sec=b))
        return a + b
