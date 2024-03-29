import pika

class Publisher:
    def __init__(self, config):
        self.config = config
        self.connection = self.create_connection()

    def create_connection(self):
        return pika.BlockingConnection(pika.ConnectionParameters(self.config["host"], self.config["port"]))

    def publish(self, exchange, routing_key, message, queue_name):
        print("VALUES -> " + str(message) + " " + str(exchange) + " " + str(routing_key))
        channel = self.connection.channel()

        channel.queue_declare(queue=queue_name, exclusive=False)  # We create the queue
        channel.exchange_declare(exchange=exchange, exchange_type='direct') # We create the exchange

        channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message) # We send the message to a queue and everyone in the queue recives the message