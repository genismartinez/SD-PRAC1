
import xmlrpc.client
class LoadBalancerService:  # We create the load balancer class

    def __init__(self):
        self.servers = []  # We create the servers list
        self.currentserver = 0  # We create the current server variable

    def add_server(self, url):
        self.servers.append(url)  # We add the server to the dictionary

    def receive_meteo_data(self, data):
        if len(self.servers) == 0:  # If there are no servers, we return an error
            print("Data was recived, but no servers available!")
            return "Error"
        print("Sending data to Server from LoadBalancer...")
        currentServerUrl = self.servers[self.currentserver]  # We obtain the current server
        self.currentserver = (self.currentserver + 1) % len(self.servers)  # We increment the current server to create a circular algorithm and choose a different server for the next request
        server_connection = xmlrpc.client.ServerProxy(currentServerUrl)  # We create the server proxy
        server_connection.process_meteo_data(data)

    def receive_pollution_data(self, data):
        if len(self.servers) == 0:  # If there are no servers, we return an error
            print("Data was recived, but no servers available!")
            return "Error"
        print("Sending data to Server from LoadBalancer...")
        currentServerUrl = self.servers[self.currentserver]  # We obtain the current server
        self.currentserver = (self.currentserver + 1) % len(self.servers)  # We increment the current server to create a circular algorithm and choose a different server for the next request
        server_connection = xmlrpc.client.ServerProxy(currentServerUrl)  # We create the server proxy
        server_connection.process_pollution_data(data)


load_balancer = LoadBalancerService()  # We create the load balancer

