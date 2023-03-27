from pydantic import BaseModel

from room import Room


class Floor (BaseModel):

    fid: int
    level: int
    rooms: list[Room]
