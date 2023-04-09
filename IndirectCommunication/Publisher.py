import pika

class Publisher:
    def __init__(self, config):
        self.config = config
        self.connection = self.create_connection()

    def __del__(self):
        self.connection.close()

    def create_connection(self):
        return pika.BlockingConnection(pika.ConnectionParameters(host=self.config['host'], port=self.config['port']))

    def publish(self, exchange, routing_key, message):
        channel = self.connection.channel()

        channel.exchange_declare(exchange=exchange, exchange_type='direct')

        channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)