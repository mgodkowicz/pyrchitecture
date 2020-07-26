from typing import Optional

from pydantic import UUID4

from aggreagates.reservations.domain.repository import ResourceRepository
from aggreagates.reservations.domain.resource import Resource, ResourceId

initial_resource = Resource(
    resource_id=ResourceId(id=UUID4("0c51b998-e97b-4e8d-9df1-116e2c9eb384")),
    reservations=[]
)


class InMemoryResourceRepository(ResourceRepository):
    def __init__(self):
        self.data = {
            initial_resource.resource_id: initial_resource
        }

    def get(self, resource_id: ResourceId) -> Optional[Resource]:
        return self.data.get(resource_id)

    def save(self, resource: Resource) -> None:
        self.data[resource.resource_id] = resource
