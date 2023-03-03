# -------------------------------------- #										 #
# Programador: Genís Martínez   		 #
# Programador: David Tomas               #
# -------------------------------------- #

import json
import redis
import tasks

id = None
conn = None

# ------------------------------ MERGING FUNCTIONS ------------------------------ #

def process_meteo_data(meteo_data):
    global id
    global conn
    response = tasks.process_meteo_data(meteo_data)
    return response

def process_pollution_data(pollution_data):
    global id
    global conn
    response = tasks.process_pollution_data(pollution_data)
    return response


# -------------------------------------- MAIN -------------------------------------- #

def start_server(x):
    global id
    global conn
    conn = redis.StrictRedis(host='localhost', port=6379, db=0)

    while True:
       job = str(conn.blpop('task_queue')).split("'")[3]
       id = str(conn.blpop('task_queue')).split("'")[1]
       argument = str(conn.blpop('arg_queue')).split("'")[3]

       # We execute the task and we save the result in the database

       if (job == "process_meteo_data"):
           conn.rpush(id, tasks.process_meteo_data(argument))
       elif (job == "process_pollution_data"):
              conn.rpush(id, tasks.process_pollution_data(argument))