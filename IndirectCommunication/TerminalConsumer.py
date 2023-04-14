from Consumer import Consumer
from TerminalDisplayer import TerminalDisplayer


class TerminalConsumer(Consumer):
    def __init__(self, config, exchange_name, binding_key, queue_name):
        super().__init__(config, exchange_name, binding_key, queue_name)
        self.displayer = TerminalDisplayer()



    def callback(self, channel, method, properties, body):
        print("Received data from Proxy in Terminal")
        print("Unparsed Data: " + str(body))
        # We parse the data
        body = body.decode("utf-8")
        pollution_avg = float(body.split(",")[0])
        pollution_desv = float(body.split(",")[1])
        meteo_avg = float(body.split(",")[2])
        meteo_desv = float(body.split(",")[3])
        print("Parsed Data: " + str(pollution_avg))
        self.displayer.receive_data("Meteo Data = Average =" + str(meteo_avg)+","+ " Standard Deviation = " +str(meteo_desv)+"\n","Pollution Data = Average = " + str(pollution_avg)+","+ "Standard Deviation = " + str(pollution_desv))


