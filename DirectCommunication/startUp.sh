#!/bin/bash

# This script is used to start the DirectCommunication application

# Wake up Redis Server
osascript -e 'tell app "Terminal" to do script "redis-server --port 8002"'

# Wake up Load Balancer
osascript -e 'tell app "Terminal" to do script "cd /Users/usuario/SD/SD-PRAC1/DirectCommunication && /usr/bin/python3 LoadBalancer_server.py"'

# Wake up Servers
for i in {8003..8004}; do
  osascript -e "tell app \"Terminal\" to do script \"cd /Users/usuario/SD/SD-PRAC1/DirectCommunication && /usr/bin/python3 Server.py $i\""
done

# Wake up Sensors
for _ in {1..1}
do
   osascript -e "tell app \"Terminal\" to do script \"cd /Users/usuario/SD/SD-PRAC1/DirectCommunication && /usr/bin/python3 PollutionSensor.py 1\""
done

for _ in {1..1}
do
   osascript -e "tell app \"Terminal\" to do script \"cd /Users/usuario/SD/SD-PRAC1/DirectCommunication && /usr/bin/python3 WellnessSensor.py 1\""
done

# Wake up Terminal
for i in {8010..8011}; do
   osascript -e "tell app \"Terminal\" to do script \"cd /Users/usuario/SD/SD-PRAC1/DirectCommunication && /usr/bin/python3 Terminal.py $i\""
done

# Wake up Proxy
osascript -e "tell app \"Terminal\" to do script \"cd /Users/usuario/SD/SD-PRAC1/DirectCommunication && /usr/bin/python3 Proxy.py 10\""
