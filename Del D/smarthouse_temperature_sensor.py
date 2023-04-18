import logging
import threading
import time
import math
import requests
from messaging import SensorMeasurement
import common


class Sensor:

    def __init__(self, did):
        self.did = did
        self.measurement = SensorMeasurement('0.0')

    def simulator(self):

        logging.info(f"Sensor {self.did} starting")

        while True:
            temp = round(math.sin(time.time() / 10) * common.TEMP_RANGE, 1)

            logging.info(f"Sensor {self.did}: {temp}")
            self.measurement.set_temperature(str(temp))

            time.sleep(common.TEMPERATURE_SENSOR_SIMULATOR_SLEEP_TIME)

    def client(self):
        logging.info(f"Sensor Client {self.did} starting")

        # send temperature to the cloud service with regular intervals
        while True:
            #print(self.measurement.to_json())
            r = requests.post(common.BASE_URL + f'sensor/{self.did}/current/', json={'value': self.measurement.value})
            time.sleep(common.TEMPERATURE_SENSOR_CLIENT_SLEEP_TIME)
        else:
            logging.info(f"Sensor Client {self.did} starting")

    def run(self):

        # create and start thread simulating physical temperature sensor
        sim_thread = threading.Thread(target=self.simulator)
        # create and start thread sending temperature to the cloud service
        cli_thread = threading.Thread(target=self.client)

        sim_thread.start()
        cli_thread.start()

        #sim_thread.join()
