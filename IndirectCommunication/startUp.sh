#!/bin/bash

# This script is used to start the IndirectCommunication application

num_terminals=2


# Wake up RabbitMQ Server (the RabbitMQ is set up from Docker Desktop App in port 8000)
#osascript -e 'tell app "Terminal" to do script "docker run -it --rm --name rabbitmq -p 8000:5672 -p 8001:15672 rabbitmq:3.10-management"'

# Wake up Redis Server
osascript -e 'tell app "Terminal" to do script "redis-server --port 8002"'

# Wake up Servers
for _ in {0..1}; do
  osascript -e "tell app \"Terminal\" to do script \"cd /Users/usuario/SD/SD-PRAC1/IndirectCommunication && /usr/bin/python3 Server.py\""
done

# Wake up Sensors
for _ in {1..1}
do
   osascript -e "tell app \"Terminal\" to do script \"cd /Users/usuario/SD/SD-PRAC1/IndirectCommunication && /usr/bin/python3 PollutionSensor.py 8000\""
done

for _ in {1..1}
do
   osascript -e "tell app \"Terminal\" to do script \"cd /Users/usuario/SD/SD-PRAC1/IndirectCommunication && /usr/bin/python3 WellnessSensor.py 8000\""
done

# Wake up Terminal
for ((i = 0 ; i < $num_terminals ; i++)); do
  osascript -e "tell app \"Terminal\" to do script \"cd /Users/usuario/SD/SD-PRAC1/IndirectCommunication && /usr/bin/python3 Terminal.py $i\""
done

# Wake up Proxy
osascript -e "tell app \"Terminal\" to do script \"cd /Users/usuario/SD/SD-PRAC1/IndirectCommunication && /usr/bin/python3 Proxy.py $num_terminals\""
