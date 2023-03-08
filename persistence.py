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

    def get_coldest_room(self) -> Room:
        """
        Finds the room, which has the lowest temperature on average.
        """
        self.persistence.cursor.execute("SELECT device, AVG(value) AS avg_val FROM measurements GROUP BY device ORDER BY avg_val ASC LIMIT 1;")
        coldest_room = self.persistence.cursor.fetchall()
        lowest_device_id = (coldest_room[0])[0]

        self.persistence.cursor.execute("SELECT room FROM devices WHERE id = ?;",str(lowest_device_id))
        lowest_room_id = (self.persistence.cursor.fetchall()[0])[0]

        self.persistence.cursor.execute("SELECT area,name FROM rooms WHERE id = ? ",str(lowest_room_id))
        room_vals = self.persistence.cursor.fetchall();

        room = Room(float((room_vals[0])[0]),(room_vals[0])[1])
        #Assuming devices.device_id = measurements.device

        return room

    def get_sensor_readings_in_timespan(self, sensor: Device, from_ts: datetime, to_ts: datetime) -> List[float]:
        """
        Returns a list of sensor measurements (float values) for the given device in the given timespan.
        """
        return NotImplemented()

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
        """
        return NotImplemented()

    def get_hours_when_humidity_above_average(self, room: Room, day: date) -> List[int]:
        """
        This function determines during which hours of the given day
        there were more than three measurements in that hour having a humidity measurement that is above
        the average recorded humidity in that room at that particular time.
        The result is a (possibly empty) list of number respresenting hours [0-23].
        """
        return NotImplemented()
