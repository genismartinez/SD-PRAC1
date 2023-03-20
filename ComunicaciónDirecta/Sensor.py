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
    def sendData(self, data):
        print("Sending data to LoadBalancer from Sensor...")
        multicall = xmlrpc.client.MultiCall(self.rpcClient)  # We create connection to the server
        multicall.receive_data_wrap(data)


if __name__ == "__main__":
    sensor = Sensor()

    while True:
        sensor.sendData('')
        time.sleep(1)
