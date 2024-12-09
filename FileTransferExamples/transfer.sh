#!/bin/bash

#Transfer 30 MB as 30 1M files
# Capture total time

transfer_30(){
  for i in {1..30};
    do scp <remote>:~/sample1M . ;
  done
}

transfer_1(){
  scp <remote>:~/sample30M .
}


# Run the function and time it
TIMEFORMAT="%2Us vs %2Rs"
echo "Transfering as 30x1MB"
time transfer_30
echo "Transfering as 1x30MB"
time transfer_1
