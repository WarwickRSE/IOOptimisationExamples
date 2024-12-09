#!/bin/bash

tar_transfer(){
  ssh <remote> 'cd <mydirectory>; tar -cvzf sample1M.tgz sample1M_*;exit'
  scp <remote>:~/<mydirectory>/sample1M.tgz .
  tar -xvf sample1M.tgz
 }

TIMEFORMAT="%2Us vs %2Rs"
time tar_transfer
