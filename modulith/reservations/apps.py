from django.apps import AppConfig

from modulith import container
from reservations import apidrf


class ReservationsConfig(AppConfig):
    name = 'reservations'

    def ready(self):
        container.wire(modules=[apidrf])
