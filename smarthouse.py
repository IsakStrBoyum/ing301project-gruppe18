from devices import *
from typing import List, Optional


class Room:
    """Representerer et rom i en etasje i ett hus.
        Et rom har et areal og det kan gis et kort navn.
        På et romm kan også registreres smarte enheter."""

    def __init__(self, area: float, name: str = None):
        self.area = area
        self.name = name
        self.devices_in_room = []

    def __repr__(self):
        return f"{self.name} ({self.area} m^2)"

    def add_device(self,device: Device):
        self.devices_in_room.append(device)

    def __iter__(self):
        return self.devices_in_room.__iter__()



class Floor:
    """Representerer en etasje i ett hus.
        En etasje har et entydig nummer og består av flere rom."""

    def __init__(self, floor_no: int):
        self.floor_no = floor_no
        self.rooms = []

    def add_room(self, room:Room):
        self.rooms.append(room)

    def __iter__(self):
        return self.rooms.__iter__()



class SmartHouse:
    """Den sentrale klasse i et smart hus system.
        Den forvalter etasjer, rom og enheter.
        Også styres alle enheter sentralt herifra."""

    def __init__(self):
        self.floors = []
        self.floor_num = 1

    def create_floor(self) -> Floor:
        """Legger til en etasje og gi den tilbake som objekt.
            Denne metoden ble kalt i initialiseringsfasen når
            strukturen av huset bygges opp-."""
        new_floor = Floor(self.floor_num)
        self.floors.append(new_floor)
        self.floor_num +=1
        return new_floor

    def create_room(self, floor_no: int, area: float, name: str = None) -> Room:
        """Legger til et rom i en etasje og gi den tilbake som objekt.
            Denne metoden ble kalt i initialiseringsfasen når
            strukturen av huset bygges opp-."""
        new_room = Room(area,name)
        self.floors[floor_no-1].add_room(new_room)
        return new_room

    def get_no_of_rooms(self) -> int:
        sum = 0
        for floor_ant in self.floors:
            for room_ant in floor_ant:
                sum += 1

        """Gir tilbake antall rom i huset som heltall"""
        return sum





    def get_all_devices(self) -> List[Device]:
        """Gir tilbake en liste med alle enheter som er registrert i huset."""

        tot_device = []
        for floor_ant in self.floors:
            for room_ant in floor_ant:
                for device_ant in room_ant:
                    tot_device.append(device_ant)
        return tot_device

    def get_all_rooms(self) -> List[Room]:
        """Gir tilbake en liste med alle rom i huset."""
        all_Rooms = []
        for floor_ant in self.floors:
            for room_ant in floor_ant:
                all_Rooms.append(room_ant)

        return all_Rooms

    def get_total_area(self) -> float:
        all_Rooms = self.get_all_rooms()
        tot_area = 0
        for rooms in all_Rooms:
            tot_area += rooms.area
        """Regner ut det totale arealet av huset."""
        return tot_area

    def register_device(self, device: Device, room: Room):
        """Registrerer en enhet i et gitt rom."""
        room.add_device(device)
        return

    def get_no_of_devices(self):
        """Gir tilbake antall registrerte enheter i huset."""
        sum = 0
        for floor_ant in self.floors:
            for room_ant in floor_ant:
                for device_ant in room_ant:
                    sum+=1
        return sum

    def get_no_of_sensors(self):
        """Git tilbake antall av registrerte sensorer i huset."""
        all_devices = self.get_all_devices()
        sum = 0
        for device in all_devices:
            if isinstance(device, Sensor):
                sum+= 1

        return sum

    def get_no_of_actuators(self):
        """Git tilbake antall av registrerte aktuatorer i huset."""
        all_devices = self.get_all_devices()
        sum = 0
        for device in all_devices:
            if isinstance(device, Actuator):
                sum += 1
        return sum

    def move_device(self, device: Device, from_room: Room, to_room: Room):
        """Flytter en enhet fra et gitt romm til et annet."""
        for device_in_list in from_room.devices_in_room:
            if device_in_list == device:
                to_room.devices_in_room.append(from_room.devices_in_room.pop(device_in_list))
        return

    def find_device_by_serial_no(self, serial_no: str) -> Optional[Device]:
        """Prøver å finne en enhet blant de registrerte enhetene ved å
        søke opp dens serienummer."""
        return NotImplemented

    def get_room_with_device(self, device: Device):
        """Gir tilbake rommet der en gitt enhet er resitrert."""
        return NotImplemented

    def get_all_devices_in_room(self, room: Room) -> List[Device]:
        """Gir tilbake en liste med alle enheter som er registrert på rommet."""
        return NotImplemented

    def turn_on_lights_in_room(self, room: Room):
        """Slår på alle enheter av type 'Smart Lys' i et gitt rom."""
        return NotImplemented

    def turn_off_lights_in_room(self, room: Room):
        """Slår av alle enheter av type 'Smart Lys' i et gitt rom."""
        return NotImplemented

    def get_temperature_in_room(self, room: Room) -> Optional[float]:
        """Prøver å finne ut temperaturen i et gitt rom ved å finne
        enheter av type 'Temperatursensor' der og gi tilake verdien som kommatall."""
        return NotImplemented

    def set_temperature_in_room(self, room: Room, temperature: float):
        """Prøver å sette temperaturen i et gitt rom ved å sette alle aktuatorer
        som kan påvirke temperatur ('Paneloven', 'Varmepumpe', ...) til ønsket
        temperatur."""


        return NotImplemented
