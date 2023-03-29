import time

from Sensor import Sensor
from meteo_utils import MeteoDataDetector
class PollutionSensor(Sensor):
    def __init__(self):
        super().__init__()
        self.Detector = MeteoDataDetector()
    def sendData(self):
        super().sendData()
        pollution_data = self.Detector.analyze_pollution()
        self.rpcClient.receive_pollution_data(pollution_data)  # We send the data to the server

if __name__ == "__main__":
    sensor = PollutionSensor()

    while True:
        sensor.sendData()
        time.sleep(1)