#!/bin/bash

# This script is used to terminate the DirectCommunication application

 for (( i = 8000; i < 8020; i++ )); do
     kill -9 $(lsof -t -i:$i)
 done

 pkill -a Terminal



