from aggreagates.reservations.domain.repository import ResourceRepository
from aggreagates.reservations.infrastructure.repositories.in_memory import InMemoryResourceRepository


def reservations_config(binder):
    binder.bind(ResourceRepository, InMemoryResourceRepository())
