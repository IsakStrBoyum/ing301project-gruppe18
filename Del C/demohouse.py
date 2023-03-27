from pathlib import Path
import time

from smarthouse import SmartHouse
from room import Room
from floor import Floor

from device import *
from sensors import *
from actuators import *


def load_demo_house_devices_map():
    file_path = str(Path(__file__).parent.absolute()) + "/demohus-devices.csv"
    result = {}
    with open(file_path, "r") as f:
        f.readline()  # header line: No,Typ,Produsent,Produkt Navn,Serienummer
        for line in f.readlines():
            data = line.split(",")
            result[int(data[0])] = (data[2], data[3], data[4].strip(),data[1])  # Supplier, Product, Serial No
    return result


def build_demo_house() -> SmartHouse:

    # Loading Product information and serial numbers from a CSV file so that I do not have to type them
    devices_map = load_demo_house_devices_map()

    # # Creating 31 devices
    device1 = LightBulb(did=1, serial_no=devices_map[1][2], producer=devices_map[1][0], product_type=devices_map[1][1], nickname=devices_map[1][3])
    device2 = LightBulb(did=2, serial_no=devices_map[2][2], producer=devices_map[2][0], product_type=devices_map[2][1], nickname=devices_map[2][3])
    device3 = HumiditySensor(did=3, serial_no=devices_map[3][2], producer=devices_map[3][0], product_type=devices_map[3][1], nickname=devices_map[3][3], humidity=[68])
    device4 = LightBulb(did=4, serial_no=devices_map[4][2], producer=devices_map[4][0], product_type=devices_map[4][1], nickname=devices_map[4][3])
    device5 = LightBulb(did=5, serial_no=devices_map[5][2], producer=devices_map[5][0], product_type=devices_map[5][1], nickname=devices_map[5][3])
    device6 = SmartCharger(did=6, serial_no=devices_map[6][2], producer=devices_map[6][0], product_type=devices_map[6][1], nickname=devices_map[6][3])
    device7 = HeatOven(did=7, serial_no=devices_map[7][2], producer=devices_map[7][0], product_type=devices_map[7][1], nickname=devices_map[7][3])
    device8 = TemperatureSensor(did=8, serial_no=devices_map[8][2], producer=devices_map[8][0], product_type=devices_map[8][1], nickname=devices_map[8][3], temperature=[1.3])
    device9 = LightBulb(did=9, serial_no=devices_map[9][2], producer=devices_map[9][0], product_type=devices_map[9][1], nickname=devices_map[9][3])
    device10 = LightBulb(did=10, serial_no=devices_map[10][2], producer=devices_map[10][0], product_type=devices_map[10][1], nickname=devices_map[10][3])
    device11 = SmartMeter(did=11, serial_no=devices_map[11][2], producer=devices_map[11][0], product_type=devices_map[1][1], nickname=devices_map[11][3], energy_consumption=[0])
    device12 = TemperatureSensor(did=12, serial_no=devices_map[12][2], producer=devices_map[12][0], product_type=devices_map[12][1], nickname=devices_map[12][3], temperature=[18.1])
    device13 = LightBulb(did=13, serial_no=devices_map[13][2], producer=devices_map[13][0], product_type=devices_map[13][1], nickname=devices_map[13][3])
    device14 = SmartMeter(did=14, serial_no=devices_map[14][2], producer=devices_map[14][0], product_type=devices_map[14][1], nickname=devices_map[14][3], energy_consumption=[1.5])
    device15 = SmartOutlet(did=15, serial_no=devices_map[15][2], producer=devices_map[15][0], product_type=devices_map[15][1], nickname=devices_map[15][3])
    device16 = HeatPump(did=16, serial_no=devices_map[16][2], producer=devices_map[16][0], product_type=devices_map[16][1], nickname=devices_map[16][3])
    device17 = AirQualitySensor(did=17, serial_no=devices_map[17][2], producer=devices_map[17][0], product_type=devices_map[17][1], nickname=devices_map[17][3], air_quality=[0.08])
    device18 = SmartOutlet(did=18, serial_no=devices_map[18][2], producer=devices_map[18][0], product_type=devices_map[18][1], nickname=devices_map[18][3])
    device19 = HeatOven(did=19, serial_no=devices_map[19][2], producer=devices_map[19][0], product_type=devices_map[19][1], nickname=devices_map[19][3])
    device20 = SmartOutlet(did=20, serial_no=devices_map[20][2], producer=devices_map[20][0], product_type=devices_map[20][1], nickname=devices_map[20][3])
    device21 = HumiditySensor(did=21, serial_no=devices_map[21][2], producer=devices_map[21][0], product_type=devices_map[21][1], nickname=devices_map[21][3])
    device22 = Dehumidifier(did=22, serial_no=devices_map[22][2], producer=devices_map[22][0], product_type=devices_map[22][1], nickname=devices_map[22][3])
    device23 = FloorHeatingPanel(did=23, serial_no=devices_map[23][2], producer=devices_map[23][0], product_type=devices_map[23][1], nickname=devices_map[23][3])
    device24 = HeatOven(did=24, serial_no=devices_map[24][2], producer=devices_map[24][0], product_type=devices_map[24][1], nickname=devices_map[24][3])
    device25 = LightBulb(did=25, serial_no=devices_map[25][2], producer=devices_map[25][0], product_type=devices_map[25][1], nickname=devices_map[25][3])
    device26 = LightBulb(did=26, serial_no=devices_map[26][2], producer=devices_map[26][0], product_type=devices_map[26][1], nickname=devices_map[26][3])
    device27 = HeatPump(did=27, serial_no=devices_map[27][2], producer=devices_map[27][0], product_type=devices_map[27][1], nickname=devices_map[27][3])
    device28 = TemperatureSensor(did=28, serial_no=devices_map[28][2], producer=devices_map[28][0], product_type=devices_map[28][1], nickname=devices_map[28][3], temperature=[16.1])
    device29 = LightBulb(did=29, serial_no=devices_map[29][2], producer=devices_map[29][0], product_type=devices_map[29][1], nickname=devices_map[29][3])
    device30 = LightBulb(did=30, serial_no=devices_map[30][2], producer=devices_map[30][0], product_type=devices_map[30][1], nickname=devices_map[30][3])
    device31 = HeatOven(did=31, serial_no=devices_map[31][2], producer=devices_map[31][0], product_type=devices_map[31][1], nickname=devices_map[31][3])

    # floor 1 and rooms

    living = Room(rid=1, area=39.75, name="Living Room / Kitchen", devices=[device1, device2, device11, device12, device15, device16, device17, device18])
    entre = Room(rid=2, area=13.5, name="Entrance", devices=[device8, device9, device10, device13, device14])
    guest1 = Room(rid=3, area=8, name="Guest Room 1", devices=[device4, device7])
    bath1 = Room(rid=4, area=6.3, name="Bathroom 1", devices=[device3])
    garage = Room(rid=5, area=19, name="Garage", devices=[device5, device6])

    floor1 = Floor(fid=1, level=1, rooms=[living, entre, guest1, bath1, garage])

    # floor 2 and rooms

    office = Room(rid=6, area=11.75, name="Office", devices=[device19, device20])
    bath2 = Room(rid=7, area=9.25, name="Bathroom 2", devices=[device21, device22, device23])
    guest2 = Room(rid=8, area=8, name="Guest Room 2", devices=[device24])
    hall = Room(rid=9, area=10, name="Hall", devices=[])
    guest3 = Room(rid=10, area=10, name="Guest Room 3", devices=[device31])
    dress = Room(rid=11, area=4, name="Dressing Room", devices=[device30])
    bed = Room(rid=12, area=17, name="Master Bedroom", devices=[device25, device26, device27, device28, device29])

    floor2 = Floor(fid=2, level=2, rooms=[office, bath2, guest2, hall, guest3, dress, bed])

    # smarthouse

    house = SmartHouse(name = "ING301 SmartHouse", floors=[floor1, floor2])

    return house
