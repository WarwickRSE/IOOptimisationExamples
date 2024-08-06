#! /usr/bin/env python
#Helper script - does the downloading of our selected sample DB

from torchvision import datasets
from sys import argv

if len(argv) > 1:
    #Assume that first is a filepath for destination
    data_dir = argv[1]
else:
    data_dir = "data"

#Select data set and download it to "data" folder
data = datasets.Flowers102(
    root=data_dir,
    download=True,
)

