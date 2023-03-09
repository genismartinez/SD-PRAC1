# -------------------------------------- #										 #
# Programador: Genís Martínez   		 #
# Programador: David Tomas               #
# -------------------------------------- #

import json
import redis    # We import the redis library
import meteo_utils    # We import the tasks library

id = None       # We define the id variable
conn = None     # We define the conn variable

# ------------------------------ MERGING FUNCTIONS ------------------------------ #

def process_meteo_data(meteo_data):
    global id
    global conn
    response = meteo_utils.process_meteo_data(meteo_data)
    return response

def process_pollution_data(pollution_data):
    global id
    global conn
    response = meteo_utils.process_pollution_data(pollution_data)
    return response


# -------------------------------------- MAIN -------------------------------------- #

def start_server(x):
    global id
    global conn
    conn = redis.StrictRedis(host='localhost', port=6379, db=0)

    while True:
       job = str(conn.blpop('task_queue')).split("'")[3]    # We get the task
       id = str(conn.blpop('task_queue')).split("'")[1]     # We get the id
       argument = str(conn.blpop('arg_queue')).split("'")[3]    # We get the argument

       # We execute the task and we save the result in the database

       if (job == "process_meteo_data"):
           conn.rpush(id, meteo_utils.process_meteo_data(argument))
       elif (job == "process_pollution_data"):
              conn.rpush(id, meteo_utils.process_pollution_data(argument))