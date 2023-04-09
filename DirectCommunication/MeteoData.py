

class MeteoData:

    temperature = None
    humidity = None
    timestamp = None

    def __init__(self, temperature, humidity, timestamp):
        self.temperature = temperature
        self.humidity = humidity
        self.timestamp = timestamp