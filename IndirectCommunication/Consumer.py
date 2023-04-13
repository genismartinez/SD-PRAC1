import pika
import abc

class Consumer(abc.ABC):
    def __init__(self, config, exchange_name, binding_key):
        self.config = config
        self.exchange_name = exchange_name
        self.binding_key = binding_key
        self.connection = self.create_connection()

    def create_connection(self):
        return pika.BlockingConnection(pika.ConnectionParameters(host=self.config['host'], port=self.config['port']))


    @abc.abstractmethod
    def callback(self, channel, method, properties, body):  #  Every time a message is received i Server, this method is called
        print("BODY -> " + str(body))
        pass


    def consume(self):
        channel = self.connection.channel()

        channel.exchange_declare(exchange=self.exchange_name, exchange_type='direct')
        result = channel.queue_declare(queue='Sensor', exclusive=False)
        queue_name = result.method.queue
        channel.queue_bind(exchange=self.exchange_name, queue=queue_name, routing_key=self.binding_key)

        channel.basic_consume(queue=queue_name, on_message_callback=self.callback, auto_ack=True)
        print("VALUES -> " + str(self.exchange_name) + " " + str(queue_name) + " " + str(self.binding_key))

        try:
            print(' [*] Waiting for data. Use control + c to exit.\n')
            channel.start_consuming()
        except KeyboardInterrupt:
            print(' [*] Exiting...\n')
            channel.stop_consuming()