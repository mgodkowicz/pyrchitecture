from django.apps import AppConfig

from catalog.signals import ClassBasedHandler
from config.root import injector
from reservations.events import integers_added


class CatalogConfig(AppConfig):
    name = 'catalog'

    def ready(self):
        event_handler = injector.get(ClassBasedHandler)
        print('in catalog app')
        integers_added.connect(event_handler.handle_ints_added, dispatch_uid='123456')
