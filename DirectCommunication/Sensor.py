# -------------------------------------- #										 #
# Programador: Genís Martínez	    	 #
# Programador: David Tomas               #
# -------------------------------------- #
import time
import xmlrpc.client


class Sensor:
    rpcClient = None

    def __init__(self):
        self.rpcClient = xmlrpc.client.ServerProxy("http://localhost:8000")  # We create the server proxy
    def sendData(self):
        print("Sending data to LoadBalancer from Sensor...")
