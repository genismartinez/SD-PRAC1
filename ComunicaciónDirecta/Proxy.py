import sys
import time

import redis
import xmlrpc.client

class Proxy:
    def __init__(self):
        self.terminal_clients = []
        for i in range (10):
            self.terminal_clients.append(xmlrpc.client.ServerProxy("http://localhost:" + str(8010+i)))

        self.redisClient = redis.StrictRedis(host='localhost', port=8002, db=0)  # We create the redis client
    def send_data_to_terminal(self):
        print("Sending data to Terminal from Proxy...")
        meteo_data = self.redisClient.lpop("meteo_data")
        pollution_data = self.redisClient.lpop("pollution_data")
        for terminal_client in self.terminal_clients:
            terminal_client.receive_data(meteo_data, pollution_data)

if __name__ == "__main__":
    proxy = Proxy()

    if len (sys.argv) != 2:
        print("Error: First argument is seconds of Tumbling Window!")
        sys.exit(1)

    while True:
        proxy.send_data_to_terminal()
        time.sleep(float(sys.argv[1]))










