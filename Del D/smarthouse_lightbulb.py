import logging
import threading
import time
import requests

from messaging import ActuatorState
import common


class Actuator:

    def __init__(self, did):
        self.did = did
        self.state = ActuatorState('False')

    def simulator(self):

        logging.info(f"Actuator {self.did} starting")

        while True:

            logging.info(f"Actuator {self.did}: {self.state.state}")

            time.sleep(common.LIGHTBULB_SIMULATOR_SLEEP_TIME)

    def client(self):

        logging.info(f"Actuator Client {self.did} starting")

        # TODO START
        # send request to cloud service with regular intervals and
        # set state of actuator according to the received response
        while True:
            r = requests.get(common.BASE_URL + f'actuator/{self.did}/current/')
            r_js = r.json()
            up_actuator_state = ActuatorState.json_decoder(r_js)
            self.state = up_actuator_state
            time.sleep(common.LIGHTBULB_CLIENT_SLEEP_TIME)
        else:
            logging.info(f"Client {self.did} finishing")

        # TODO END

    def run(self):
        # TODO START

        # start thread simulating physical light bulb
        sim_thread = threading.Thread(target=self.simulator)

        # start thread receiving state from the cloud
        cli_thread = threading.Thread(target=self.client)

        sim_thread.start()
        cli_thread.start()

        # TODO END


