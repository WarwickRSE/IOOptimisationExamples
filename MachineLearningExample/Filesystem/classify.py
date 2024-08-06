#! /usr/bin/env python
import json
import torch

from os import listdir
from random import choice
from sys import argv, exit

import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
from torchvision.transforms import ToTensor, ToPILImage

from PIL import Image

from model import NeuralNetwork, _sz

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
        assert len(argv) == 4, "ERROR: supply 3 args, the input folder, the label file and a number of images to classify"
        input_dir = argv[1]
        label_file = argv[2]
        count = int(argv[3])
    except Exception as e:
        print("Error doing inputs {}".format(e))
        exit

    files = listdir(input_dir)

    device, model, labels = setup_classifier(label_file)

    for i in range(count):
        print(i)
        #Pick a random image
        filename = choice(files)
        print(filename)

        #Read an im.
        im = Image.open(input_dir+filename)

        name = classify_image(device, model, im, labels)
        title =  "Dominant colour is {}".format(name)
 
        plot_image(im, title)

