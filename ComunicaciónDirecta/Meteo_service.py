import redis

from meteo_utils import MeteoDataProcessor
from PollutionData import PollutionData
class meteo_service:

    def __init__(self):
        self.meteo_data_processor = MeteoDataProcessor()
        self.redisClient = redis.StrictRedis(host='localhost', port=8002, db=0)  # We create the redis client
    def process_meteo_data(self, data):
        print("Sending MeteoData to Redis from Server...")
        print("Data-> " + str(data))
        wellness =  self.meteo_data_processor.process_meteo_data(dict(data))
        print("Wellness-> " + str(wellness))
        self.redisClient.rpush("meteo_data", wellness)
    def process_pollution_data(self, data):
        print("Sending PollutionData to Redis from Server...")
        print("Data-> " + str(data))
        pollutionData = PollutionData(data["co2"])
        pollution = self.meteo_data_processor.process_pollution_data(pollutionData)
        print("Pollution-> "+ str(pollution))
        self.redisClient.rpush("pollution_data", pollution)

meteo_service = meteo_service()
