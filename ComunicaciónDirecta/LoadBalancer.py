# -------------------------------------- #										 #
# Programador: Genís Martínez	    	 #
# Programador: David Tomas               #
# -------------------------------------- #

from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client

# ---------------------- --CONNECTION ESTABLISHMENT ------------------------- #

server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)   # We create the server


# ----------------------------- LOAD BALANCER ------------------------------ #

class load_balancer:  # We create the load balancer class

    def __init__(self):
        self.servers = []  # We create the servers list
        self.currentserver = 0  # We create the current server variable

    def add_server(self, url):
        self.servers.append(url)  # We add the server to the dictionary

    def receive_data(self, data):
        print("Sending data to Server from LoadBalancer...")
        currentServerUrl = self.servers[self.currentserver]  # We obtain the current server
        self.currentserver = (self.currentserver + 1) % len(self.servers)  # We increment the current server to create a circular algorithm and choose a different server for the next request
        server_connection = xmlrpc.client.ServerProxy(currentServerUrl)  # We create the server proxy
        multicall = xmlrpc.client.MultiCall(server_connection)
        multicall.process_meteo_data_wrap(data)

def add_server_wrap(url):
    load_balancer.add_server(url)

def receive_data_wrap(data):
    load_balancer.receive_data(data)




# ---------------------------------- MAIN --------------------------------- #

if __name__ == "__main__":

    server.register_introspection_functions()   # We register the introspection functions

    load_balancer = load_balancer()

    server.register_function(add_server_wrap)
    server.register_function(receive_data_wrap)


    print("Server started.")

    try:
        server.serve_forever()  # We start the server

    except KeyboardInterrupt:
        print("Server stopped.")