from Sensor import Sensor
from meteo_utils import MeteoDataDetector
import time
class WellnessSensor(Sensor):

    def __init__(self):
        super().__init__()
        self.detector = MeteoDataDetector()
    def sendData(self):
        super().sendData()
        meteo_data = self.detector.analyze_air()
        self.rpcClient.receive_meteo_data(meteo_data)  # We send the data to the server

if __name__ == "__main__":
    sensor = WellnessSensor()

    while True:
        sensor.sendData()
        time.sleep(1)
