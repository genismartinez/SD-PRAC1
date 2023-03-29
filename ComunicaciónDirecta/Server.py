# -------------------------------------- #										 #
# Programador: Genís Martínez   		 #
# Programador: David Tomas               #
# -------------------------------------- #

import sys
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
from Meteo_service import meteo_service


# -------------------------------------- MAIN -------------------------------------- #

if __name__ == "__main__":

    print("Print:"+ sys.argv[1])    # We print the port of the server
    server = SimpleXMLRPCServer(("localhost", int(sys.argv[1])), allow_none=True)  # We create the server

    server.register_instance(meteo_service)  # We register the server
    loadBalancerClient = xmlrpc.client.ServerProxy("http://localhost:8000")  # We create the server proxy
    loadBalancerClient.add_server("http://localhost:"+sys.argv[1])     # We add the server to the load balancer

    print("Server started.")

    try:
        server.serve_forever()  # We start the server

    except KeyboardInterrupt:
        print("Server stopped.")