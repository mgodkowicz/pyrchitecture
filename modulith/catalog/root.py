from injector import Module, Binder, singleton

from catalog.signals import ClassBasedHandler


class CatalogRoot(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(ClassBasedHandler, to=ClassBasedHandler, scope=singleton)
