import redis

from Consumer import Consumer
import sys
from MeteoService import MeteoService
import datetime


class MeteoConsumer(Consumer):

    def parse_data(self, body):
        parsed_body = {}
        parts = body.split(",")
        if len(parts) == 9: # Wellness Sensor
            parsed_body["temperature"] = float(parts[0].split(":")[1])
            parsed_body["humidity"] = float(parts[1].split(":")[1])
            datetime_values = "".join(parts[2:]).split(":")[1].split("(")[1].split(" ")
            parsed_body["timestamp"] = datetime.datetime(int(datetime_values[0]), int(datetime_values[1]),
                                                         int(datetime_values[2]), int(datetime_values[3]),
                                                         int(datetime_values[4]), int(datetime_values[5]),
                                                         int(datetime_values[6].split(")")[0]))


        elif len(parts) == 8: # Pollution Sensor
            parsed_body["co2"] = float(parts[0].split(":")[1])
            datetime_values = "".join(parts[1:]).split(":")[1].split("(")[1].split(" ")
            parsed_body["timestamp"] = datetime.datetime(int(datetime_values[0]), int(datetime_values[1]), int(datetime_values[2]), int(datetime_values[3]), int(datetime_values[4]), int(datetime_values[5]), int(datetime_values[6].split(")")[0]))
        else:
            print("Error: Unknown data format!")
            sys.exit(1)

        return parsed_body





        pass
    def callback(self, channel, method, properties, body):
        print(" [x] Received new message %r" % (body))

        body = body.decode()    # We decode the message
        print("BODY -> " + str(body))

        body = self.parse_data(body)

        #body = dict(body)   # We convert the message to a dictionary

        # We check the type of data we are receiving and process it accordingly

        meteo_service = MeteoService()
        if 'co2' in body:
            data = meteo_service.process_pollution_data(body)
            redis_client.rpush("pollution_data", data)
        else:
            data = meteo_service.process_meteo_data(body)
            redis_client.rpush("meteo_data", data)


redis_client = redis.Redis(host='localhost', port=8002, db=0)   # We create the redis client
consumer_name = MeteoConsumer({'host':'localhost', 'port':8000}, 'Sensor', 'Sensor')   # We create the consumer
consumer_name.consume() # We start the consumer
