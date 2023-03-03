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
redisClient = redis.StrictRedis(host='localhost', port=6379, db=0)
server = SimpleXMLRPCServer(("localhost", 8005), allow_none=True)
server.register_introspection_functions()

# ------------------------------ SERVER FUNCTIONS ------------------------------ #

def add_server():
    global SERVER_LIST
    global SERVER_ID
    wkr = mp.Process(target=server.start_server, args=(SERVER_ID,))
    wkr.start()

    id = "S-"+str(SERVER_ID)
    SERVER_LIST[id] = wkr
    SERVER_ID += 1
    return "Worker with ID {} successfully added.".format(id)

def rem_server(x):
    global SERVER_LIST
    log = ""

    for id in x.split(" "):
        if id in SERVER_LIST.keys():
            SERVER_LIST[id].terminate()
            del SERVER_LIST[id]
            log = log +"Worker with ID {} successfully removed.".format(id) + "\n"
        else:
            log = log +"Worker with ID {} not found.".format(id) + "\n"

    return log

def list_servers():
    global SERVER_LIST
    x = ""
    for wkr in SERVER_LIST.keys():
        x = x + wkr + "\n"

    if len(x) == 0:
        x = "No active servers."
    else:
        return x    # We return the list of workers

def submit_task(x,y):
    global JOB_ID
    split_args = y.split('')
    # We save the task in the database (task_queue)
    if(len(split_args) > 1):
        for arg in split_args:
            redisClient.rpush('task_queue', x, JOB_ID)
            redisClient.rpush('arg_queue', "http://localhost:8000/"+arg)

        redisClient.rpush('task_queue', x+str("Merge"), JOB_ID)
        num_elem = len(split_args)
        redisClient.rpush('arg_queue', num_elem)

    else:
        redisClient.rpush('task_queue', x, JOB_ID)
        redisClient.rpush('arg_queue', "http://localhost:8000/"+y)

    JOB_ID = JOB_ID + 1
    return JOB_ID - 1

def check_result(x):
    return redisClient.lpop(x)

# ------------------------------ SERVER REGISTRATION ------------------------------ #

server.register_function(add_server)
server.register_function(rem_server)
server.register_function(list_servers)
server.register_function(submit_task)
server.register_function(check_result)

# ------------------------------ SERVER START (MAIN)------------------------------ #

print("Server started.")

try:
    server.serve_forever()

except KeyboardInterrupt:
    print("Server stopped.")



