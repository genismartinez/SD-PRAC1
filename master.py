# -------------------------------------- #										 #
# Programador: Genís Martínez	    	 #
# Programador: David Tomas               #
# -------------------------------------- #

import server
import  multiprocessing as mp
from xmlrpc.server import SimpleXMLRPCServer
import redis

SERVER_LIST = {}
SERVER_ID = 0
JOB_ID = 1

# ------------------------------ CONNECTION ESTABLISHMENT ------------------------------ #

print("Starting server...")
redisClient = redis.StrictRedis(host='localhost', port=6379, db=0)  # We create the redis client
server = SimpleXMLRPCServer(("localhost", 8005), allow_none=True)   # We create the server
server.register_introspection_functions()   # We register the introspection functions

# ------------------------------ SERVER FUNCTIONS ------------------------------ #

def add_server():
    global SERVER_LIST
    global SERVER_ID
    srv = mp.Process(target=server.start_server, args=(SERVER_ID,)) # We create the server
    srv.start() # We start the server

    id = "S-"+str(SERVER_ID)    # We create the id
    SERVER_LIST[id] = srv   # We add the server to the list
    SERVER_ID += 1  # We increment the id
    return "Worker with ID {} successfully added.".format(id)   # We return the id

def rem_server(x):
    global SERVER_LIST
    log = ""

    for id in x.split(" "):
        if id in SERVER_LIST.keys():    # We check if the server exists
            SERVER_LIST[id].terminate() # We terminate the server
            del SERVER_LIST[id]         # We remove the server from the list
            log = log +"Worker with ID {} successfully removed.".format(id) + "\n"
        else:
            log = log +"Worker with ID {} not found.".format(id) + "\n"

    return log

def list_servers():
    global SERVER_LIST
    x = ""
    for srv in SERVER_LIST.keys():  # We iterate through the list of servers
        x = x + srv + "\n"          # We add the id to the list

    if len(x) == 0:
        x = "No active servers."
    else:
        return x    # We return the list of servers

def submit_task(x,y):
    global JOB_ID
    split_args = y.split('')    # We split the arguments
    # We save the task in the database (task_queue)
    if(len(split_args) > 1):    # If there are more than one argument
        for arg in split_args:  # We iterate through the arguments
            redisClient.rpush('task_queue', x, JOB_ID)  # We save the task
            redisClient.rpush('arg_queue', "http://localhost:8000/"+arg)    # We save the argument

        redisClient.rpush('task_queue', x+str("Merge"), JOB_ID) # We save the merge task
        num_elem = len(split_args)  # We get the number of elements
        redisClient.rpush('arg_queue', num_elem)    # We save the number of elements

    else:
        # If there is only one argument
        redisClient.rpush('task_queue', x, JOB_ID)  # We save the task
        redisClient.rpush('arg_queue', "http://localhost:8000/"+y)  # We save the argument

    JOB_ID = JOB_ID + 1 # We increment the job id
    return JOB_ID - 1   # We return the job id

def check_result(x):
    return redisClient.lpop(x)  # We return the result of the job

# ------------------------------ SERVER REGISTRATION ------------------------------ #

server.register_function(add_server)
server.register_function(rem_server)
server.register_function(list_servers)
server.register_function(submit_task)
server.register_function(check_result)

# ------------------------------ SERVER START (MAIN)------------------------------ #

print("Server started.")

try:
    server.serve_forever()  # We start the server

except KeyboardInterrupt:
    print("Server stopped.")



