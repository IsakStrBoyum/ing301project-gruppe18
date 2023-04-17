import logging
import threading
import time
import math
import requests
from common import BASE_URL
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

        # TODO START
        # send temperature to the cloud service with regular intervals
        while True:
            logging.info(f"client")
            r = requests.post(BASE_URL+f'smarthouse/sensor/{self.did}/current/', json=str(self.measurement))
            time.thread_time(2)

        logging.info(f"Client {self.did} finishing")

        # TODO END

    def run(self):

        pass
        # TODO START

        # create and start thread simulating physical temperature sensor
        sim_thread = threading.Thread(target=self.simulator())
        # create and start thread sending temperature to the cloud service
        new_thread = threading.Thread(target=self.client())

        new_thread.start()
        sim_thread.start()

        # TODO END

