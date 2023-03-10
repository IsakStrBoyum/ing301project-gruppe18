import sqlite3
from sqlite3 import Connection
from devices import *
from smarthouse import Room
from typing import Optional, List, Dict, Tuple
from datetime import date, datetime


class SmartHousePersistence:

    def __init__(self, db_file: str):
        self.db_file = db_file
        self.connection = Connection(db_file)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.rollback()
        self.connection.close()

    def save(self):
        self.connection.commit()

    def reconnect(self):
        self.connection.close()
        self.connection = Connection(self.db_file)
        self.cursor = self.connection.cursor()

    def check_tables(self) -> bool:
        self.cursor.execute("SELECT name FROM sqlite_schema WHERE type = 'table';")
        result = set()
        for row in self.cursor.fetchall():
            result.add(row[0])
        return 'rooms' in result and 'devices' in result and 'measurements' in result


class SmartHouseAnalytics:

    def __init__(self, persistence: SmartHousePersistence):
        self.persistence = persistence

    def get_most_recent_sensor_reading(self, sensor: Device) -> Optional[float]:
        """
        Retrieves the most recent (i.e. current) value reading for the given
        sensor device.
        Function may return None if the given device is an actuator or
        if there are no sensor values for the given device recorded in the database.
        """
        result = None
        if isinstance(sensor, Sensor):
            sid = sensor.device_number
            self.persistence.cursor.execute("SELECT value "
                                            "FROM measurements "
                                            "WHERE "
                                            "time_stamp = (SELECT MAX(time_stamp) FROM measurements WHERE device = ?) "
                                            "AND device = ? LIMIT 1;",(sid, sid))
            """
            Limit ensures that we only get one returned value. Since we are only assigning one measured value,
            and we assume that one sensor cant have two measurements at the same time it is not necessary, but 
            nice to have.
            """
            result = self.persistence.cursor.fetchone()[0]
            #print(result)
            return result
        else:
            return None

        """
        try:
            sensor_id = sensor.device_number
            self.persistence.cursor.execute(
                "SELECT device FROM measurements WHERE device = ? GROUP BY device;", (str(sensor_id),))
            check = self.persistence.cursor.fetchall()
            if int((check[0])[0]) == sensor_id:
                self.persistence.cursor.execute(
                    "SELECT value FROM measurements WHERE device = ? ORDER BY time_stamp DESC LIMIT 1;",(str(sensor_id),))
                result = float(((self.persistence.cursor.fetchall())[0])[0]) # (()[0])[0] gir tallet ut fetchall[0] gir (x, ),der x er et tall
                # ORDER BY time_stamp DESC LIMIT 1 will take the last timestamp from all values where device = id
        except:
            result = None

        return result
        """

    def get_coldest_room(self) -> Room:
        """
        Finds the room, which has the lowest temperature on average.

        Kva om eit rom har fleire temp sensorar!?
        Tested, and works!?:
        """
        self.persistence.cursor.execute("SELECT rooms.id, rooms.floor, rooms.area, rooms.name "
                                        "FROM (SELECT devices.room as superroom , device, min(avgTemp) "
                                        "FROM (SELECT measurements.device, AVG(measurements.value) as avgTemp "
                                        "FROM devices, measurements "
                                        "WHERE devices.id = measurements.device and devices.type = 'Temperatursensor' "
                                        "group by device), devices WHERE devices.id = device), rooms "
                                        "WHERE rooms.id = superroom")
        room_vals = self.persistence.cursor.fetchall()
        #print(room_vals)
        room = Room(float((room_vals[0])[2]), str((room_vals[0])[3]))

        """
        self.persistence.cursor.execute(
            "SELECT device, AVG(value) AS avg_val FROM measurements GROUP BY device ORDER BY avg_val ASC LIMIT 1;")
        coldest_room = self.persistence.cursor.fetchall()
        lowest_device_id = (coldest_room[0])[0]

        self.persistence.cursor.execute("SELECT room FROM devices WHERE id = ?;", str(lowest_device_id))
        lowest_room_id = (self.persistence.cursor.fetchall()[0])[0]

        self.persistence.cursor.execute("SELECT area,name FROM rooms WHERE id = ? ", str(lowest_room_id))
        room_vals = self.persistence.cursor.fetchall();

        room = Room(float((room_vals[0])[0]), (room_vals[0])[1])
        # Assuming devices.device_id = measurements.device
        """
        #får feil når eg returnerar via repr?! men ikkje med .name. why?????!!!!
        return str(room)

    def get_sensor_readings_in_timespan(self, sensor: Device, from_ts: datetime, to_ts: datetime) -> List[float]:
        """
        Returns a list of sensor measurements (float values) for the given device in the given timespan.
        """
        self.persistence.cursor.execute("SELECT value FROM measurements "
                                        "WHERE device = ? "
                                        "AND DATETIME(time_stamp) >= DATETIME(?) "
                                        "AND DATETIME(time_stamp) <= DATETIME(?)", (sensor.device_number, from_ts, to_ts))
        readings = [item[0] for item in self.persistence.cursor.fetchall()]
        #print(readings)
        return readings

    def describe_temperature_in_rooms(self) -> Dict[str, Tuple[float, float, float]]:
        """
        Returns a dictionary where the key are room names and the values are triples
        containing three floating point numbers:
        - The first component [index=0] being the _minimum_ temperature of the room.
        - The second component [index=1] being the _maximum_ temperature of the room.
        - The third component [index=2] being the _average_ temperature of the room.

        This function can be seen as a simplified version of the DataFrame.describe()
        function that exists in Pandas:
        https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html?highlight=describe


        1. hente ut liste med romnummer og namn på rom med tempsensor
        2. hent ut min temp til kvart rom med tempsensor
        3. hent ut max temp til kvart rom med tempsensor
        4. hent ut avg temp til kvart rom med tempsensor
        """
        temp_in_rooms = dict
        self.persistence.cursor.execute("SELECT rooms.name, min(measurements.value), MAX(measurements.value), AVG(measurements.value) "
                                        "FROM measurements, devices, rooms "
                                        "WHERE  devices.id = measurements.device "
                                        "and devices.type = 'Temperatursensor' "
                                        "and rooms.id = devices.room "
                                        "GROUP BY measurements.device")

        max_min_avg_dict = dict((item[0], (item[1], item[2], item[3])) for item in self.persistence.cursor.fetchall())

        return max_min_avg_dict

    def get_hours_when_humidity_above_average(self, room: Room, day: date) -> List[int]:
        """
        This function determines during which hours of the given day
        there were more than three measurements in that hour having a humidity measurement that is above
        the average recorded humidity in that room at that particular time.
        The result is a (possibly empty) list of number respresenting hours [0-23].
        """
        self.persistence.cursor.execute("SELECT strftime('%H', measurements.time_stamp) AS hours, "
                                        "COUNT(strftime('%H', measurements.time_stamp)) AS h_count "
                                        "FROM measurements, devices, rooms "
                                        "WHERE measurements.device = devices.id "
                                        "AND devices.type = 'Fuktighetssensor' "
                                        "AND rooms.id = devices.room "
                                        "AND rooms.name = ? "
                                        "AND measurements.time_stamp >= date(?) "
                                        "AND measurements.time_stamp <  date(?, '+1 day') "
                                        "AND measurements.value > (SELECT AVG(measurements.value) "
                                        "FROM measurements, devices, rooms "
                                        "WHERE measurements.device = devices.id "
                                        "AND devices.type = 'Fuktighetssensor' "
                                        "AND rooms.id = devices.room "
                                        "AND rooms.name = ? "
                                        "AND measurements.time_stamp >= date(?) "
                                        "AND measurements.time_stamp <  date(?, '+1 day')) "
                                        "GROUP BY hours "
                                        "HAVING h_count > 3",
                                        (room, day, day, room, day, day))

        output_db = [int(item[0]) for item in self.persistence.cursor.fetchall()]

        return output_db
