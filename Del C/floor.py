from pydantic import BaseModel

from room import Room


class Floor(BaseModel):
    fid: int
    level: int
    rooms: list[Room]

    def get_room(self, rid: int):
        for room in self.rooms:
            if int(room.rid) == int(rid):
                return room

        return None

