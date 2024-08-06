#! /usr/bin/env python
from sklearn.cluster import KMeans
import numpy as np
from PIL import Image

from sys import argv, exit
from os import listdir, mkdir
from os.path import basename
from shutil import copy
from random import choice

from plot_wrapper import *
import LABColourNamer as Namer
from writeLabbook import *

def identify_dominant(im, quiet=False):
    """Accepts a PIL Image (any mode) and returns the top 3 dominant colour strings, and metadata about the fit"""
    #Uses KMeans clustering to find N groups of pixel colours and then selects the
    # 3 largest clusters and names the colour at their center
    #Naming uses a simple heuristic from LABColourNamer
    
    im=im.convert('LAB') #Make sure we're in LAB colour space
    data = im.getdata()
    sz = im.size
    kmeans = KMeans() #The KMeans clustering object

    kmeans.fit(data) #Do a default fit

    #Get the most common cluster value
    labels = kmeans.labels_
    counts = np.bincount(labels[labels>=0])

    top_labels = np.argsort(-counts)

    #Now get the colours
    names = []
    for i in range(3, 0, -1):
        cc = kmeans.cluster_centers_[top_labels][i]
        ct = (cc[0], cc[1], cc[2])
        #Now name it
        name = Namer.nameColourLAB(ct)
        if not quiet: print("{}th dominant colour is {} {}".format(i, name[0], name[1]))
        names.append(name)

    return {"names":names, "fitData":{'inertia':kmeans.inertia_, 'n_clusters':len(labels)}}


def categorise_and_file(filename, prefix, outdir, im, labbook, quiet=False):
    """Accepts a PIL image, identifies the dominant colour name and copies prefix+filename to outdir_`colourname`/filename. Also records to the labbook"""

    # Get dominant colour names
    data = identify_dominant(im, quiet)
    names = data["names"]
    name = names[0]

    #Write to labbook
    labbook.make_image_id(filename)
    labbook.store_run(filename, names, data['fitData']['inertia'], data['fitData']['n_clusters'])

    #Construct the directory name
    dir_name = name[0].strip(' ')+'_'+name[1].strip(' ')+'/'
    try:
        listdir(outdir + dir_name)
    except FileNotFoundError as e:
        if not quiet: print("Creating directory {}".format(dir_name))
        mkdir(outdir + dir_name)

    copy(prefix+filename, outdir+dir_name+filename)


def sort_n_ims(prefix, outdir, count, labbook, quiet=False):
    """Select count random ims from prefix and categorise them into outdir by colour name"""
    files = listdir(prefix)

    for i in range(count):
        #Pick a random image
        filename = choice(files)
        if not quiet: print("Image {}, picked {}".format(i, filename))

        #Read an im.
        im = Image.open(prefix+filename)

        # Run the categorising
        categorise_and_file(filename, prefix, outdir, im, labbook, quiet)

def categorise_single(full_filename, labbook, plot=True):
    """Categorise a single image by colour, optionally plotting it"""

    #Read im.
    im = Image.open(full_filename)
    
    # Either we plot, or we should print for sure
    data = identify_dominant(im, not plot)
    names = data["names"]
    name = names[0]
    
    #Write to labbook
    a_filename = basename(filename)
    labbook.make_image_id(a_filename)
    labbook.store_run(a_filename, names, data['fitData']['inertia'], data['fitData']['n_clusters'])

    title =  "Dominant colour is {}{}".format(name[0], name[1])
    if(plot): plot_image(im, title)


if __name__ == "__main__":

    try:
        mode = argv[1]
        assert(mode in ["show", "sort", "identify"])
    except:
        print("ERROR: First argument should be 'show' to show an image by filename, 'identify' to print the 3 dominant colours in image or 'sort' to categorise many")
        exit()

    theBook = dbLabbook()

    if mode in ["show", "identify"]:
        #Need one parameter, the filename
        assert len(argv) == 3, "ERROR: This mode requires a filename input"
        filename = argv[2]
        if mode == "show":
            categorise_single(filename, theBook, plot=True)
        else:
            categorise_single(filename, theBook, plot=False)
    elif mode in ["sort"]:
        #Need an input dir, output prefix and count of how many
        assert len(argv) == 5, "ERROR: This mode requires an input directory, output directory and a count"
        in_dir = argv[2]
        out_dir = argv[3]
        try:
            count = int(argv[4])
        except:
            print("ERROR: Parameter 4 not convertible to integer")
            exit()
        sort_n_ims(in_dir, out_dir, count, theBook, quiet=False)       

