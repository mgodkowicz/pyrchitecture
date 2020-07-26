import inject
from datetimerange import DateTimeRange

from aggreagates.common.result import Result
from aggreagates.reservations.domain.repository import ResourceRepository
from aggreagates.reservations.domain.resource import ResourceId


class ReserveResourceService:
    repository = inject.attr(ResourceRepository)

    def reserve(self, resource_id: ResourceId, period: DateTimeRange) -> Result:
        resource = self.repository.get(resource_id)

        result = resource.reserve(period)

        self.repository.save(resource)

        return result
