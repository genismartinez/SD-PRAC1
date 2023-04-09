# -------------------------------------- #										 #
# Programador: Genís Martínez	    	 #
# Programador: David Tomas               #
# -------------------------------------- #
import time
import xmlrpc.client

import pika
from Publisher import Publisher


class Sensor(Publisher):    # We inherit from Publisher
    def __init__(self, config):
        super().__init__(config)    # We call the constructor of the parent class
        self.Detector = None
        self.data = None

    def sendData(self):
        self.generateData()     # We generate the data
        super().publish(' ', ' ', self.data)    # We call the sendData method of the parent class

    def generateData(self):
        pass




