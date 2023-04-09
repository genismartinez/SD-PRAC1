import sys
import time
import datetime

from Sensor import Sensor
from meteo_utils import MeteoDataDetector
class PollutionSensor(Sensor):  # We inherit from Sensor
    def __init__(self, config):
        super().__init__(config)      # We call the constructor of the parent class
        self.Detector = MeteoDataDetector() # We create the detector
        self.data = None    # We initialize the data to None
    def generateData(self):
        self.data = self.Detector.analyze_pollution()  # We get the pollution data

if __name__ == "__main__":
    sensor = PollutionSensor({'host':'localhost', 'port':sys.argv[1]})  # We create the sensor

    while True:
        time.sleep(float(sys.argv[1]))  # We wait for the time specified in the arguments
        sensor.sendData()   # We send the data
