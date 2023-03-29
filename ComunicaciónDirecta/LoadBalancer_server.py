# -------------------------------------- #										 #
# Programador: Genís Martínez	    	 #
# Programador: David Tomas               #
# -------------------------------------- #

from xmlrpc.server import SimpleXMLRPCServer
from LoadBalancerService import load_balancer

# ---------------------------------- MAIN --------------------------------- #

if __name__ == "__main__":

    server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)  # We create the server

    server.register_instance(load_balancer)  # We register the server

    print("LoadBalancer started.")

    try:
        server.serve_forever()  # We start the server

    except KeyboardInterrupt:
        print("LoadBalancer stopped.")