# -------------------------------------- #										 #
# Programador: Genís Martínez   		 #
# Programador: David Tomas               #
# -------------------------------------- #

import sys

from MeteoConsumer import MeteoConsumer


# -------------------------------------- MAIN -------------------------------------- #

if __name__ == "__main__":

    consumer = MeteoConsumer({'host':'localhost', 'port':8000}, 'workers', 'worker'+sys.argv[1])

    print("Server started.")

    try:
        consumer.consume()  # We start the server

    except KeyboardInterrupt:
        print("Server stopped.")