

class TerminalDisplayer:
    def __init__(self):
        pass

    def receive_data(self, meteo_data, pollution_data):
        print("Received data from Proxy in Terminal")
        print("Meteo data: " + meteo_data)
        print("Pollution data: " + pollution_data)


terminal_displayer = TerminalDisplayer()