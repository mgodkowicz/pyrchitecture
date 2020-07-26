from aggreagates.common.result import failure, Result, success
from anemic_model.db.room import Room, RoomV2
from anemic_model.db.room_db import RoomDatabase
from anemic_model.define.room_name import RoomName
from anemic_model.define.seats import MaxNoOfSeats


class DefineRoomService:

    def __init__(self, room_database: RoomDatabase):
        self.room_database = room_database

    def define_regular_room(self, name: str, seats: int) -> Result:
        room_name = RoomName(name)

        if self.room_database.find_by_name(room_name):
            return failure("Room with given name already exist")

        self.room_database.create_new(
            Room.new(seats=MaxNoOfSeats(seats), name=room_name)
        )

        return success()


class DefineRoomV2Service:

    def __init__(self, room_database: RoomDatabase):
        self.room_database = room_database

    def define_regular_room(self, name: str, seats: int) -> Result:
        if self.room_database.find_by_name(RoomName(name)):
            return failure("Room with given name already exist")

        self.room_database.create_new(
            RoomV2.new(seats=seats, name=name)
        )

        return success()
