import sys
import time
from Publisher import Publisher

import redis
import xmlrpc.client


class Proxy(Publisher):

    def __init__(self, config, num_terminals):
        super().__init__(config)      # We call the constructor of the parent class
        self.num_terminals = num_terminals
        self.redisClient = redis.StrictRedis(host='localhost', port=8002, db=0, charset="utf-8", decode_responses=True)  # We create the redis client

    def send_data_to_queues(self):
        print("Sending data to Queues from Proxy...")
        #meteo_data = self.redisClient.lpop("meteo_data")
        meteo_data = self.redisClient.lrange("meteo_data", 0, -1)
        #pollution_data = self.redisClient.lpop("pollution_data")
        pollution_data = self.redisClient.lrange("pollution_data", 0, -1)
        print("pollution_data: "+ str(pollution_data))
        print("meteo_data: " + str(meteo_data))
        # We calculate the average
        meteo_avg = self.avg(meteo_data)
        pollution_avg = self.avg(pollution_data)
        # We calculate the standard deviation
        meteo_desv = self.std_desv(meteo_data)  # We calculate the standard deviation
        pollution_desv = self.std_desv(pollution_data)  # We calculate the standard deviation
        # We send the data to the queues

        for i in range(int(self.num_terminals)):
            super().publish('Terminal', 'Terminal', str(pollution_avg)+","+str(pollution_desv)+","+str(meteo_avg)+","+str(meteo_desv), "Terminal-"+str(i))


    def avg(self,data):
        suma = 0
        for i in data:
            suma += float(i)
        return suma/len(data)

    def std_desv(self, data):
        mean = self.avg(data)
        std_desv = 0
        for i in data:
            std_desv += (float(i) - mean) ** 2
        std_desv = (std_desv / len(data)) ** 0.5
        return std_desv


if __name__ == "__main__":
    proxy = Proxy({"host": "localhost", "port": "8000"}, sys.argv[1])

    while True:
        time.sleep(10)
        proxy.send_data_to_queues()











