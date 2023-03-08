class Device:

    def __init__(self, device_id, device_name, device_prod_name, device_model_name, device_type):
        self.device_id = device_id
        self.device_name = device_name
        self.device_prod_name = device_prod_name
        self.device_model_name = device_model_name
        self.device_type = device_type
        self.device_number = None


class Sensor(Device):
    def __init__(self, device_id, device_name, device_prod_name, device_model_name, device_type, current_measurement):
        super().__init__(device_id, device_name, device_prod_name, device_model_name, device_type)
        self.previous_measurements = []
        self.current_measurement = current_measurement
        self.previous_measurements.append(current_measurement) #adds first measurement to list

    def new_measurement(self, new_measurement):
        self.previous_measurements.append(new_measurement)
        self.current_measurement = new_measurement

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

    def get_state(self):
        return self.current_state


    def __repr__(self):
        return f"Aktuator({self.device_id}) TYPE: {self.device_type} STATUS: {self.current_state} PRODUCT DETAILS: {self.device_prod_name} {self.device_model_name}"

        #NICKNAME: {self.device_name}
