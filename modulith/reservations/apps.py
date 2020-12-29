from django.apps import AppConfig

from common.event_publisher import EventPublisher
from config.root import injector
from reservations.events import IntegersAdded
from reservations.read_model import ExampleReadModel


class ReservationsConfig(AppConfig):
    name = 'reservations'

    def ready(self):
        read_model = injector.get(ExampleReadModel)
        event_publisher = injector.get(EventPublisher)
        handle = read_model.handle
        event_publisher.subscribe(IntegersAdded, handle)
