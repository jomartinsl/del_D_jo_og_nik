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

        
        get_url = f"http://127.0.0.1:8000/smarthouse/actuator/{self.did}/current"
        response = requests.get(get_url)
        data = response.json()
        actuator_value = data['state']
        self.state = ActuatorState(init_state=actuator_value)

 

        logging.info(f"Client {self.did} finishing")
        time.sleep(common.LIGHTBULB_CLIENT_SLEEP_TIME)

      

    def run(self):


        logging.info(f"Actuator {self.did} starting")
        sim_lightbulb_thread = threading.Thread(target=self.simulator)
        client_lightbulb_thread = threading.Thread(target=self.client)

        sim_lightbulb_thread.start()
        client_lightbulb_thread.start()
       


