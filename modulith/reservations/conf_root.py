from injector import Module, Binder, singleton

from reservations.read_model import ExampleReadModel
from reservations.repository import Repository, InMemoryRepository


class ReservationsRoot(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(Repository, to=InMemoryRepository, scope=singleton)
        binder.bind(ExampleReadModel, to=ExampleReadModel)
