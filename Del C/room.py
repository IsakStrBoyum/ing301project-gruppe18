from pydantic import BaseModel

from device import Device


class Room(BaseModel):

    rid: int
    area: float
    name: str
    devices: list[Device]

