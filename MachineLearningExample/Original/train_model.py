#! /usr/bin/env python
import json
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import datasets
import torchvision.transforms as transforms
import torch.nn as nn

from sys import argv
from os import listdir

from model import NeuralNetwork, _sz

#Partly cribbed from https://pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html
#ImageFolder from https://debuggercafe.com/pytorch-imagefolder-for-training-cnn-models/

def setup_and_train(input_dir, n_labels):
    
    #Sensible default
    BATCH_SIZE = 64

    #Size the images down
    sz =_sz

    # Resizing, applying some random perturbations which WONT change the answer
    # NOTE: cropping in general will!

    transform_set = transforms.Compose([
        transforms.Resize((sz, sz)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomVerticalFlip(p=0.5),
        transforms.RandomRotation(degrees=(30, 70)),
        transforms.ToTensor()
    ])

    # Using the ImageFolder built-in which associates labels to images according
    # to their directory name
    dataset = datasets.ImageFolder(root=input_dir, transform = transform_set)
    loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

    #output the label mapping
    with open(input_dir.replace('/', '_')+'labels.json', 'w') as labelfile:
        labelfile.write(json.dumps(dataset.class_to_idx))

    #Ask for and verify that we're using CUDA (from tutorial)
    device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
    )
    print(f"Using {device} device")

    #Creating model
    model = NeuralNetwork(n_labels).to(device)
    print(model)

    loss_fn = nn.CrossEntropyLoss()

    #Training mode
    model.train()
    for data in enumerate(loader):
        image, labels = data[1]
        image = image.to(device)
        labels = labels.to(device)
        outputs = model(image)
        loss = loss_fn(outputs, labels)
        print(loss.item())

    #Save the model
    outfile = 'model_weights.pth'
    torch.save(model.state_dict(), outfile)
    print("Model saved to {}".format(outfile))


if __name__ == "__main__":

    try:
        input_dir = argv[1]
    except:
        print("ERROR: supply an input directory as first arg")

    try:
        n_labels = len(listdir(input_dir))
        setup_and_train(input_dir, n_labels)
    except Exception as e:
        #print("Something went wrong: {}".format(e))
        raise e
