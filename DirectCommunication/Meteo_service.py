import redis

from meteo_utils import MeteoDataProcessor
from PollutionData import PollutionData
from MeteoData import MeteoData
class meteo_service:

    def __init__(self):
        self.meteo_data_processor = MeteoDataProcessor()
        self.redisClient = redis.StrictRedis(host='localhost', port=8002, db=0)  # We create the redis client
    def process_meteo_data(self, data):
        print("Sending MeteoData to Redis from Server...")
        print("Data-> " + str(data))
        meteo_data = MeteoData(data["temperature"], data["humidity"], data["timestamp"])    # We create the MeteoData object
        # We convert the data from a dictionary to a class object to satisfy the requirements of the MeteoDataProcessor
        wellness =  self.meteo_data_processor.process_meteo_data(meteo_data)    # We process the data
        print("Wellness-> " + str(wellness))
        self.redisClient.rpush("meteo_data", wellness)
    def process_pollution_data(self, data):
        print("Sending PollutionData to Redis from Server...")
        print("Data-> " + str(data))
        pollutionData = PollutionData(data["co2"], data["timestamp"])
        pollution = self.meteo_data_processor.process_pollution_data(pollutionData)
        print("Pollution-> "+ str(pollution))
        self.redisClient.rpush("pollution_data", pollution)

meteo_service = meteo_service()
