

class TerminalDisplayer:
    def __init__(self):
        pass

    def receive_data(self, meteo_data, pollution_data):
        print("Received data from Proxy in Terminal")
        print("Meteo data: " + str(meteo_data))
        print("Pollution data: " + str(pollution_data))


terminal_displayer = TerminalDisplayer()