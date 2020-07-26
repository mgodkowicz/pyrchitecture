from abc import ABC

from aggreagates.reservations.domain.resource import Resource, ResourceId


class ResourceRepository(ABC):
    def get(self, resource_id: ResourceId) -> Resource:
        pass

    def save(self, resource: Resource) -> None:
        pass
