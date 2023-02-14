class Device:

    def __init__(self, device_id, device_name, device_prod_name, device_model_name, device_type):
        self.device_id = device_id
        self.device_name = device_name
        self.device_prod_name = device_prod_name
        self.device_model_name = device_model_name
        self.device_type = device_type


class Sensor(Device):
    def __init__(self, device_id, device_name, device_prod_name, device_model_name, device_type, current_measurement):
        super().__init__(device_id, device_name, device_prod_name, device_model_name, device_type)
        self.previous_measurements = []
        self.current_measurement = current_measurement

    def new_measurement(self, new_measurement):
        self.previous_measurements.append(new_measurement)
        self.current_measurement = new_measurement

    def get_current_measurement(self):
        return self.current_measurement

    def get_all_measurements(self):
        return self.previous_measurements

    def __repr__(self):
        return f"Sensor {self.device_id} Type: {self.device_type} Status: {self.current_measurement}  Product details: {self.device_type} {self.device_name} "


class Actuator(Device):
    def __init__(self, device_id, device_name, device_prod_name, device_model_name, device_type, current_state):
        super().__init__(device_id, device_name, device_prod_name, device_model_name, device_type)
        self.current_state = current_state

    def set_state(self, new_state):
        self.current_state = new_state
        return

    def __repr__(self):
        return f"Sensor {self.device_id} Type: {self.device_type} Status: {self.current_state}  Product details: {self.device_type} {self.device_name}"
