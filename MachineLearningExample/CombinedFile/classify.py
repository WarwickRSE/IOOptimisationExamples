#! /usr/bin/env python
import json
import torch

from os import listdir
from os.path import splitext
from random import choice
from sys import argv, exit

import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
from torchvision.transforms import ToTensor, ToPILImage

from PIL import Image

from model import NeuralNetwork, _sz

import tarfile
from io import BytesIO
from PIL import Image 

import HDFVFS


from plot_wrapper import *

def setup_classifier(label_file):

    #Read the label mapping
    with open(label_file, 'r') as labelfile:
        labelDict = json.loads(labelfile.read())

    #Reverse lookup
    
    reverseDict = {}
    for key, val in labelDict.items():
        reverseDict[val] = key

    n_labels = len(labelDict)

    device = (
        "cuda"
        if torch.cuda.is_available()
        else "mps"
        if torch.backends.mps.is_available()
        else "cpu"
    )
    print(f"Using {device} device")


    model = NeuralNetwork(n_labels).to(device)
    model.load_state_dict(torch.load('model_weights.pth', weights_only=True))

    print(model)

    model.eval()

    return device, model, reverseDict


def classify_image(device, model, im_in, labels):
    """Classify a single image using given model and label strings"""

    eval_transform = transforms.Compose([
        transforms.Resize((_sz, _sz)),
        transforms.ToTensor()
        ])
 
    im = eval_transform(im_in)
    im = torch.unsqueeze(im, 0)
    with torch.no_grad():
        outputs = model(im.to(device))
    output_label = torch.topk(outputs, 1)

    cls = labels[int(output_label.indices)]
    return cls

if __name__ == "__main__":

    # Input dir for images, label_file, count
    try:
        assert len(argv) == 4, "ERROR: supply 3 args, the input file, the label file and a number of images to classify"
        input_file = argv[1]
        label_file = argv[2]
        count = int(argv[3])
    except Exception as e:
        print("Error doing inputs {}".format(e))
        exit()

    nam,ext = splitext(input_file)
    
    if ext == ".h5":
        hfile = HDFVFS.VFS() 
        hfile.open(input_file)
        files = list(hfile.get_data_names())
    elif ext == ".tgz":
        tfile = tarfile.open(input_file, 'r:gz')
        files = tfile.getnames()

    device, model, labels = setup_classifier(label_file)

    for i in range(count):
        print(i)
        #Pick a random image
        filename = choice(files)
        print(filename)

        #Read an im.
        if ext == ".h5":
            bb = hfile.get(filename)
        elif ext == ".tgz":
            f=tfile.extractfile(filename)
            bb=f.read()
        file_data=BytesIO(bb)
        im = Image.open(file_data)

        name = classify_image(device, model, im, labels)
        title =  "Dominant colour is {}".format(name)
 
        plot_image(im, title)

