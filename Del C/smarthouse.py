from pydantic import BaseModel

from floor import Floor


class SmartHouse (BaseModel):

    name: str
    floors: list[Floor]






