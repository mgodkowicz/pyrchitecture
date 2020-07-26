from uuid import uuid4

from pydantic import BaseModel, Field
from pydantic import UUID4

from anemic_model.define.room_name import RoomName
from anemic_model.define.seats import MaxNoOfSeats


# When model is anemic it just handle data structure. Behaviours are in services.
class Room(BaseModel):
    room_id: UUID4 = uuid4()
    number_of_seats: int
    name: str

    @classmethod
    def new(cls, name: RoomName, seats: MaxNoOfSeats):
        return cls(name=str(name), number_of_seats=int(seats))


# This object have two valueObjects (MaxNoOfSeats, RoomName) that are responsible for validation
# is this still anemic tho?
class RoomV2(BaseModel):
    room_id: UUID4 = uuid4()
    number_of_seats: MaxNoOfSeats
    name: RoomName

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            MaxNoOfSeats: lambda no: int(no),
            RoomName: lambda room: str(room)
        }

    @classmethod
    def new(cls, name: str, seats: int):
        return cls(
            number_of_seats=MaxNoOfSeats(seats),
            name=RoomName(name)
        )


print(Room(number_of_seats=3, name='str').json())
print(
    RoomV2(number_of_seats=MaxNoOfSeats(2), name=RoomName('sda')).json()
)
