from pydantic import BaseModel


class Device (BaseModel):

    did : int
    serial_no: str
    producer: str
    product_type: str
    nickname: str

