from injector import Module, Binder

from reservations.repository import Repository, InMemoryRepository


class ReservationsRoot(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(Repository, to=InMemoryRepository)
