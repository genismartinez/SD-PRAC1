import sys

from Publisher import Publisher
from meteo_utils import MeteoDataDetector
import time
import datetime
class WellnessSensor(Publisher):

    def __init__(self, config):
        super().__init__(config)     # We call the constructor of the parent class
        self.detector = MeteoDataDetector() # We create the detector
        self.data = None    # We initialize the data to None

    def generateData(self):
        self.data = self.detector.analyze_air() # We get the pollution data

    def sendData(self):
        self.generateData()     # We generate the data
        self.data["timestamp"] = datetime.datetime.now()
        print("DATA WellnessSensor ->" + str(self.data))
        super().publish('Sensor', 'Sensor', str(self.data))    # We call the sendData method of the parent class


if __name__ == "__main__":
    sensor = WellnessSensor({'host':'localhost', 'port':sys.argv[1]})

    while True:
        time.sleep(float(sys.argv[1]))
        sensor.sendData()

