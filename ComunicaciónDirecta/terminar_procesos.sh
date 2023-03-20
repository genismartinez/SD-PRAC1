#!/bin/bash

# This script is used to terminate the ComunicaciónDirecta application

 for (( i = 8000; i < 8006; i++ )); do
     kill -9 $(lsof -t -i:$i)
 done



