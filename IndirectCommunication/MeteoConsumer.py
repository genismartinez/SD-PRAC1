import redis

from Consumer import Consumer
import sys
from MeteoService import MeteoService


class MeteoConsumer(Consumer):
    def callback(self, channel, method, properties, body):
        print(" [x] Received new message %r" % (body))

        body = body.decode()    # We decode the message
        body = dict(body)   # We convert the message to a dictionary

        # We check the type of data we are receiving and process it accordingly

        meteo_service = MeteoService()
        if 'co2' in body:
            data = meteo_service.process_pollution_data(body)
            redis_client.rpush("pollution_data", data)
        else:
            data = meteo_service.process_meteo_data(body)
            redis_client.rpush("meteo_data", data)


redis_client = redis.Redis(host='localhost', port=8002, db=0)   # We create the redis client
consumer_name = MeteoConsumer({'host':'localhost', 'port':8000}, 'workers', 'worker'+sys.argv[1])   # We create the consumer
consumer_name.consume() # We start the consumer
