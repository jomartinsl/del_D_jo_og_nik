import datetime
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
        while True:
            logging.info(f"Sensor Client {self.did} RUNNING")
            url = f"{common.BASE_URL}sensor/{self.did}/current"
            logging.info(f"Sensor {self.did}: {self.measurement.value}")
            time.sleep(common.TEMPERATURE_SENSOR_CLIENT_SLEEP_TIME)

            time1 = datetime.datetime.now().isoformat() 
            value = self.measurement.get_temperature()
            unit = 'C'

            json_data ={
            "timestamp": time1,
            "value": value,
            "unit": unit
            }
            requests.post(url, json=json_data)

            time.sleep(common.TEMPERATURE_SENSOR_SIMULATOR_SLEEP_TIME)


    def run(self):
        sim_temp_sensor_thread = threading.Thread(target=self.simulator)
        client_temp_sensor_thread = threading.Thread(target=self.client)
        sim_temp_sensor_thread.start()
        client_temp_sensor_thread.start()


