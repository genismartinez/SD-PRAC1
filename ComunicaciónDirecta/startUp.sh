#!/bin/bash

# This script is used to start the ComunicaciónDirecta application

# Wake up Redis Server
redis-server --port 8002 &

# Wake up Servers
for i in {8003..8005}
do
   python3 Server.py $i &> output.txt &
done

# Wake up Load Balancer
python3 LoadBalancer.py &> output.txt &

# Wake up Sensors
for i in {1..2}
do
   python3 Sensor.py &> output.txt &
done

# Wake up Terminal
#python3 terminal.py &

less +F -f -r output.txt