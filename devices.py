class Device:

    def __init__(self,device_id,device_name,device_prod_name,device_model_name,device_location,device_type):
        self.device_id = device_id
        self.device_name = device_name
        self.device_prod_name = device_prod_name
        self.device_model_name = device_model_name
        self.device_location = device_location
        self.device_type = device_type


class Sensor(Device):

    def __init__(self,current_measurement):
        self.current_measurement = current_measurement
        self.previous_measurements = []

    def new_measurement(self,new_measurement):
        self.previous_measurements.append(self.current_measurement)
        self.current_measurement = new_measurement


class Actuator(Device):

    def __init__(self,current_state):
        self.current_state = current_state
    def set_state(self,new_state):
        self.current_state = new_state

    pass
# TODO! Her skal du utvikle din egen design av en klassestruktur med enheter og deres funkjsoner!