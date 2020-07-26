from abc import ABC, abstractmethod

from anemic_model.db.room import Room
from anemic_model.define.room_name import RoomName


class RoomDatabase(ABC):

    @abstractmethod
    def create_new(self, room: Room) -> Room:
        pass

    @abstractmethod
    def update(self, room: Room) -> Room:
        pass

    @abstractmethod
    def find_by_name(self, name: RoomName) -> Room:
        pass


class SQLRoomDatabase(RoomDatabase):
    def __init__(self, db):
        self.db = db

    def create_new(self, room: Room) -> Room:
        self.db.execute(
            """
            INSERT INTO rooms (room_id, name, number_of_seats)
            VALUES (room_id, name, number_of_seats)
            """,
            room.json()
        )
