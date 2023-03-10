from smarthouse import SmartHouse
from devices import *
import codecs
from persistence import SmartHousePersistence
from pathlib import Path


def load_demo_house(persistence: SmartHousePersistence) -> SmartHouse:
    result = SmartHouse()
    result.create_floor()
    result.create_floor()

    persistence.cursor.execute("SELECT * FROM rooms;")
    all_rooms = persistence.cursor.fetchall()
    persistence.cursor.execute("SELECT * FROM devices")
    all_devices = persistence.cursor.fetchall()
    room_counter = 0
    for room in all_rooms:
        new_room =result.create_room(int(room[1]),float(room[2]),room[3])
        room_counter = room_counter+1
        for device in all_devices:
            if room_counter == int(device[1]):
                if device[2] == 'Fuktighetssensor' or device[2] == 'Temperatursensor' or device[2] == 'Strømmåler' or device[2] == 'Luftkvalitetssensor':
                    new_device = Sensor(device[5], device[2], device[3], device[4], device[2],None)
                else:
                    new_device = Actuator(device[5],device[2],device[3],device[4],device[2],None) # finne en god måte å hente ut om det er aktuator eller sensor.. mulig vi må endre på klassane
                new_device.device_number = int(device[0])
                new_device.new_db_entry()
                new_room.add_device(new_device)

    #update states from database

    persistence.cursor.execute("SELECT device, state FROM states")
    output_db = persistence.cursor.fetchall()
    counter = 0
    device_list = result.get_all_devices()
    for line in output_db:
        device_id = output_db[counter][0]
        device_state = output_db[counter][1]
        for device in device_list:
            if device_id == device.device_number:
                device.set_state(device_state)
        counter += 1








    # read rooms, devices and their locations from the database
    return result


def build_demo_house() -> SmartHouse:
    house = SmartHouse()
    house.create_floor()
    house.create_floor()

    house.create_room(1, 39.75, "Livingroom/Kitchen")
    house.create_room(1, 13.5, "Entrance")
    house.create_room(1, 6.3, "Bathroom 1")
    house.create_room(1, 8, "Guestroom 1")
    house.create_room(1, 19, "Garage")

    house.create_room(2, 11.75, "Office")
    house.create_room(2, 9.25, "Bathroom 2")
    house.create_room(2, 8, "Guestroom 2")
    house.create_room(2, 10, "Gang")
    house.create_room(2, 10, "Guestroom 3")
    house.create_room(2, 4, "Dressing Room")
    house.create_room(2, 17, "Master Bedroom")

    list_of_units = []

    counter = 0
    f = codecs.open('Data/List-of-units2', 'r', 'UTF-8')
    for line in f:
        list_of_units.append(line)
    f.close()

    for unit in list_of_units:
        list_of_units[counter] = unit.split('\t')
        counter += 1
        
    list_of_measurement = []
    counter = 0
    f = codecs.open('Data/Sensor-data', 'r', 'UTF-8')
    for line in f:
        list_of_measurement.append(line)
    f.close()

    for meas in list_of_measurement:
        list_of_measurement[counter] = meas.split('\t')
        counter += 1

    #print(list_of_units)
    #print(list_of_measurement)
    for unit_info in list_of_units:
        if int(unit_info[0]) in (1, 2, 4, 5, 6, 7, 9, 10, 13, 15, 16, 18, 19, 20, 22, 23, 24, 25, 26, 27, 29, 30, 31):
            if int(unit_info[0]) == 13:
                house.register_device(
                    Actuator(unit_info[4], unit_info[5], unit_info[2], unit_info[3], unit_info[1], "ON")
                    , house.get_all_rooms()[int(unit_info[6].strip())])
            else:
                house.register_device(
                    Actuator(unit_info[4], unit_info[5], unit_info[2], unit_info[3], unit_info[1], "OFF")
                    , house.get_all_rooms()[int(unit_info[6].strip())])
        else:
            for meas_info in list_of_measurement:
                if int(meas_info[0]) == int(unit_info[0]):
                    house.register_device(
                        Sensor(unit_info[4], unit_info[5], unit_info[2], unit_info[3], unit_info[1], meas_info[1].strip())
                        , house.get_all_rooms()[int(unit_info[6].strip())])


    # TODO! her skal du legge inn etasjer, rom og enheter som at resultatet tilsvarer demo huset!
    return house


def do_device_list(smart_house: SmartHouse):
    print("Listing Devices...")
    idx = 0
    for d in smart_house.get_all_devices():
        print(f"{idx}: {d}")
        idx += 1


def do_room_list(smart_house: SmartHouse):
    print("Listing Rooms...")
    idx = 0
    for r in smart_house.get_all_rooms():
        print(f"{idx}: {r}")
        idx += 1


def do_find(smart_house: SmartHouse):
    print("Please enter serial no: ")
    serial_no = input()
    device = smart_house.find_device_by_serial_no(serial_no)
    if device:
        devices = smart_house.get_all_devices()
        rooms = smart_house.get_all_rooms()
        room = smart_house.get_room_with_device(device)
        device_idx = devices.index(device)
        room_idx = rooms.index(room)
        print(f"Device No {device_idx}:")
        print(device)
        print(f"is located in room No {room_idx}:")
        print(room)
    else:
        print(f"Could not locate device with serial no {serial_no}")


def do_move(smart_house):
    devices = smart_house.get_all_devices()
    rooms = smart_house.get_all_rooms()
    print("Please choose device:")
    device_id = input()
    device = None
    if device_id.isdigit():
        device = devices[int(device_id)]
    else:
        device = smart_house.find_device_by_serial_no(device_id)
    if device:
        print("Please choose target room")
        room_id = input()
        if room_id.isdigit() and rooms[int(room_id)]:
            to_room = rooms[int(room_id)]
            from_room = smart_house.get_room_with_device(device)
            smart_house.move_device(device, from_room, to_room)
        else:
            print(f"Room with no {room_id} does not exist!")
    else:
        print(f"Device wit id '{device_id}' does not exist")


def main(smart_house: SmartHouse):
    print("************ Smart House Control *****************")
    print(f"No of Rooms:       {smart_house.get_no_of_rooms()}")
    print(f"Total Area:        {smart_house.get_total_area()}")
    print(
        f"Connected Devices: {smart_house.get_no_of_devices()} ({smart_house.get_no_of_sensors()} Sensors | {smart_house.get_no_of_actuators()} Actuators)")
    print("**************************************************")
    print()
    print("Management Interface v.0.1")
    while (True):
        print()
        print("Please select one of the following options:")
        print("- List all devices in the house (l)")
        print("- List all rooms in the house (r) ")
        print("- Find a device via its serial number (f)")
        print("- Move a device from one room to another (m)")
        print("- Quit (q)")
        char = input()
        if char == "l":
            do_device_list(smart_house)
        elif char == "r":
            do_room_list(smart_house)
        elif char == "f":
            do_find(smart_house)
        elif char == "m":
            do_move(smart_house)
        elif char == "q":
            break
        else:
            print(f"Error! Could not interpret input '{char}'!")




if __name__ == '__main__':
    #house = build_demo_house()
    file_path = str(Path(__file__).parent.absolute()) + "/db.sqlite"
    p = SmartHousePersistence(file_path)
    house = load_demo_house(p)
    main(house)
