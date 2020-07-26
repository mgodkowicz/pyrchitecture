from datetimerange import DateTimeRange
from pydantic import BaseModel


class Reservation(BaseModel):
    period: DateTimeRange

    class Config:
        arbitrary_types_allowed = True
