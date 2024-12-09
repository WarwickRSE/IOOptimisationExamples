#!/bin/bash

#Transfer 1 GB as 10 0.1G files
# Capture total time

transfer_10(){
  for i in {1..10};
    do scp <remote>:~/sample01G . ;
  done
}

transfer_1(){
  scp <remote>:~/sample1G . ;
}


TIMEFORMAT="%2Us vs %2Rs"
echo "Transferring as 10x0.1GB"
time transfer_10
echo "Transferring as 1x1GB"
time transfer_1
