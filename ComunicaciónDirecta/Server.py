# -------------------------------------- #										 #
# Programador: Genís Martínez   		 #
# Programador: David Tomas               #
# -------------------------------------- #

import sys
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client

import redis  # We import the redis library
from meteo_utils import MeteoDataProcessor


class server:

    # ------------------------------ MERGING FUNCTIONS ------------------------------ #

    redisClient = None;
    def __init__(self):
        self.MeteoDataProcessor = MeteoDataProcessor()  # We create the meteo data processor
        self.redisClient = redis.StrictRedis(host='localhost', port=8002, db=0) # We create the redis client
        loadBalancerClient = xmlrpc.client.ServerProxy("http://localhost:8000")  # We create the server proxy
        multicall = xmlrpc.client.MultiCall(loadBalancerClient)    # We create connection to the server
        multicall.append_server_wrap("http://localhost:"+sys.argv[1])   # We add the server to the load balancer

    def process_meteo_data(self, meteo_data):
        print("Processing meteo data in Server and sending to Redis...")
        air_wellness = self.MeteoDataProcessor.process_meteo_data(meteo_data)   # We process the meteo data
        self.redisClient.rpush('air_wellness', air_wellness)    # We send the processed data to the redis server

    def process_pollution_data(self, pollution_data):
        co2_wellness = self.MeteoDataProcessor.process_pollution_data(pollution_data)   # We process the pollution data
        self.redisClient.rpush('co2_wellness', co2_wellness)    # We send the processed data to the redis server



# -------------------------------------- MAIN -------------------------------------- #

def process_meteo_data_wrap(meteo_data):

    server.process_meteo_data(meteo_data)

def process_pollution_data_wrap(pollution_data):

    server.process_pollution_data(pollution_data)

if __name__ == "__main__":

    server = server()

    print("Print:"+ sys.argv[1])
    server = SimpleXMLRPCServer(("localhost", int(sys.argv[1])), allow_none=True)  # We create the server

    server.register_introspection_functions()  # We register the introspection functions

    server.register_function(process_meteo_data_wrap)
    server.register_function(process_pollution_data_wrap)


    print("Server started.")

    try:
        server.serve_forever()  # We start the server

    except KeyboardInterrupt:
        print("Server stopped.")