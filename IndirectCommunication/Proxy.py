import sys
import time

import redis
import xmlrpc.client

class Proxy:
    def __init__(self):
        self.terminal_clients = []
        for i in range (2):
            self.terminal_clients.append(xmlrpc.client.ServerProxy("http://localhost:" + str(8010+i)))

        self.redisClient = redis.StrictRedis(host='localhost', port=8002, db=0, charset="utf-8", decode_responses=True)  # We create the redis client
    def send_data_to_terminal(self):
        print("Sending data to Terminal from Proxy...")
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
        for terminal_client in self.terminal_clients:
            terminal_client.receive_data((meteo_avg, meteo_desv), (pollution_avg, pollution_desv))
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
    proxy = Proxy()

    if len (sys.argv) != 2:
        print("Error: First argument is seconds of Tumbling Window!")
        sys.exit(1)

    while True:
        time.sleep(float(sys.argv[1]))
        proxy.send_data_to_terminal()











