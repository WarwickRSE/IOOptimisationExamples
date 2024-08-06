#! /usr/bin/env python
import json
import torch
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
import torch.nn as nn

from sys import argv
from os import listdir
from os.path import basename, dirname

from model import NeuralNetwork, _sz

import tarfile
from io import BytesIO
from PIL import Image 

import HDFVFS

#Partly cribbed from https://pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html
#ImageFolder from https://debuggercafe.com/pytorch-imagefolder-for-training-cnn-models/


class HDF5_Dataset(Dataset):
    def __init__(self, hdf5_name, transform=None):
        
        self.hfile=HDFVFS.VFS()
        self.hfile.open(hdf5_name)
        
        self.data_set_list = list(self.hfile.get_data_names())
        self.label_list = self.hfile.get_toplevel_groups()
        self.class_to_idx = self.get_label_map()
        self.transform = transform
        #self.target_transform = target_transform

    def __del__(self):
        self.hfile.close()

    def __len__(self):
        return len(self.data_set_list)

    def __getitem__(self, idx):

        #Get the data as bytes
        item = self.data_set_list[idx]
        bb = self.hfile.get(item)
        file_data=BytesIO(bb)
        
        #Open as image
        im = Image.open(file_data)

        #Extract label
        label = self.label_list.index(dirname(item).strip('/'))
        
        #Transforms
        if self.transform:
            im = self.transform(im)

        return im, label

    def get_label_map(self):
        vals = {}
        for i in range(len(self.label_list)):
            vals[self.label_list[i]] = i
        return vals

def setup_and_train(input_file):
    
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

    #Writing a simple custom dataset and loader
    #Uses our HDF5 file as source. Script now needs filename as input

    #dataset = datasets.ImageFolder(root=input_dir, transform = transform_set)
    dataset = HDF5_Dataset(input_file, transform = transform_set)
    loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

    # Number of labels
    n_labels = len(dataset.label_list)


    #output the label mapping
    with open(input_file.replace('.', '_').replace('/', '_')+'_labels.json', 'w') as labelfile:
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
        input_file = argv[1]
    except:
        print("ERROR: supply an input directory as first arg")
        exit

    try:
        setup_and_train(input_file)
    except Exception as e:
        #print("Something went wrong: {}".format(e))
        raise e
