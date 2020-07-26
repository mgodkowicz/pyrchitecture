from datetime import datetime

import inject
from datetimerange import DateTimeRange
from fastapi import Response, HTTPException, FastAPI
from pydantic import UUID4
from starlette import status

from aggreagates.reservations.application.configuration import reservations_config
from aggreagates.reservations.application.services.reserve_resource import ReserveResourceService
from aggreagates.reservations.domain.resource import ResourceId

app = FastAPI()


@app.post("/reservation")
def reservation(resource_id: UUID4, start: datetime, end: datetime):
    result = ReserveResourceService().reserve(ResourceId(id=resource_id), DateTimeRange(start, end))

    if result.is_success():
        return Response(status_code=status.HTTP_200_OK)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.value)


@app.on_event("startup")
async def startup_event():
    inject.configure(reservations_config)
