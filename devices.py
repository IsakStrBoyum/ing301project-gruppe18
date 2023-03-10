from sqlite3 import Connection
from pathlib import Path
class Device:

    def __init__(self, device_id, device_name, device_prod_name, device_model_name, device_type):
        self.device_id = device_id
        self.device_name = device_name
        self.device_prod_name = device_prod_name
        self.device_model_name = device_model_name
        self.device_type = device_type
        self.device_number = None
        self.file_path = str(Path(__file__).parent.absolute()) + "/db.sqlite"
        self.connection = Connection(self.file_path)
        self.cursor = self.connection.cursor()

    def set_state(self,new_state):
        self.cursor.execute("UPDATE states SET state = ? WHERE device = ?", (str(new_state),str(self.device_number)))
        self.cursor.connection.commit()


    def new_db_entry(self):
        self.cursor.execute("SELECT device FROM states GROUP BY device")
        db_output = self.cursor.fetchall()
        check = True
        for d in db_output:
            if d[0] == self.device_number:
                check = False
        if check:
            self.cursor.execute("INSERT INTO states (device,state) VALUES (?,'ON')",(self.device_number,))
            self.cursor.connection.commit()





class Sensor(Device):
    def __init__(self, device_id, device_name, device_prod_name, device_model_name, device_type, current_measurement):
        super().__init__(device_id, device_name, device_prod_name, device_model_name, device_type)
        self.previous_measurements = []
        self.current_measurement = current_measurement
        self.previous_measurements.append(current_measurement) #adds first measurement to list


    def new_measurement(self, new_measurement):
        self.previous_measurements.append(new_measurement)
        self.current_measurement = new_measurement
        super(Sensor, self).set_state(self.current_measurement)

    def get_current_measurement(self):
        return self.current_measurement

    def get_all_measurements(self):
        return self.previous_measurements

    def __repr__(self):
        return f"Sensor({self.device_id}) TYPE: {self.device_type} STATUS: {self.current_measurement} PRODUCT DETAILS: {self.device_prod_name} {self.device_model_name}"


class Actuator(Device):
    def __init__(self, device_id, device_name, device_prod_name, device_model_name, device_type, current_state):
        self.current_state = current_state
        super().__init__(device_id, device_name, device_prod_name, device_model_name, device_type)

    def set_state(self, new_state):
        self.current_state = new_state
        super(Actuator, self).set_state(new_state)


    def get_state(self):
        return self.current_state


    def __repr__(self):
        return f"Aktuator({self.device_id}) TYPE: {self.device_type} STATUS: {self.current_state} PRODUCT DETAILS: {self.device_prod_name} {self.device_model_name}"

        #NICKNAME: {self.device_name}
