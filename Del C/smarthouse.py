from pydantic import BaseModel

from floor import Floor


class SmartHouse(BaseModel):
    name: str
    floors: list[Floor]

    def get_floor(self, fid: int):
        for floor in self.floors:
            if int(floor.fid) == int(fid):
                return floor

        return None

    def get_device_list(self):
        device_list = []
        for floor in self.floors:
            for room in floor.rooms:
                for device in room.devices:
                    device_list.append(device)

        return device_list

    def get_device(self, did: int):
        for device in self.get_device_list():
            if device.did == did:
                return device

        return None

    def read_devices(self):

        floors = self.floors
        devices = list()

        for floor in floors:

            rooms = floor.rooms

            for room in rooms:
                devices.extend(room.devices)

        return devices

    def read_device(self, did):

        devices = self.read_devices()

        for device in devices:

            if device.did == did:
                return device
