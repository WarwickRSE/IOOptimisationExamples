#! /usr/bin/env python
from sklearn.cluster import KMeans
import numpy as np
from PIL import Image

from sys import argv, exit
from os.path import basename
from shutil import copy
from random import choice, random

import tarfile
from io import BytesIO

from plot_wrapper import *
import LABColourNamer as Namer

import HDFVFS

def identify_dominant(im, quiet=False):
    """Accepts a PIL Image (any mode) and returns the top 3 dominant colour strings"""
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
    return names


def categorise_and_file(filename, hfile, im, bb, quiet=False):
    """Accepts a PIL image, identifies the dominant colour name and writes into hfile at mockpath `colourname`/filename"""

    # Get dominant colour names
    names = identify_dominant(im, quiet)
    name = names[0]

    #Construct "pseudo-directory" name
    dir_name = name[0].strip(' ')+'_'+name[1].strip(' ')+'/'+basename(filename)
    hfile.put(dir_name, bb)


def sort_n_ims(tarname, outfile, count, chunk_sz, quiet=False):
    """Select count random ims from prefix and categorise them into outdir by colour name"""

    #Open tarfile
    t=tarfile.open(tarname, 'r:gz')
    
    #Open HDF file for output
    hfile=HDFVFS.VFS()
    hfile.open(outfile)

    #List contents of tarfile
    files = t.getnames()

    chunks = int(count/chunk_sz)

    for i in range(chunks):
        print("Processing chunk {}".format(i))
	    #Pick a random file and the next n after it in file
        # For each: extract it, classify it, then pipe into HDF5 file
        pick = choice(files)
        ind = files.index(pick)

        for i in range(chunk_sz):
            pick = files[ind+i]

            f=t.extractfile(pick)
            bb=f.read()
            file_data=BytesIO(bb)

            im = Image.open(file_data)
 
            if not quiet: print("Image {}, picked {}".format(i, pick))

            # Run the categorising
            categorise_and_file(pick, hfile, im, bb, quiet)

    hfile.close()

def partition_ims(tarname, outfile_train, outfile_test, prob, quiet=False):
    """Partition the given tarfile into train and test outputs, with prob chance of being in the former"""

    #Open tarfile
    t=tarfile.open(tarname, 'r:gz')
    
    #Open HDF file for output
    hfile_train=HDFVFS.VFS()
    hfile_train.open(outfile_train)

    hfile_test=HDFVFS.VFS()
    hfile_test.open(outfile_test)

    #List contents of tarfile
    files = t.getnames()
    for i in range(1,len(files)): # A hack - first entry is the subdir name
        # For each: extract it, classify it, then pipe into HDF5 file

        pick = files[i]
        print(pick)
        r = random()
        if r > prob:
            hfile = hfile_test
            flg = "test"
        else:
            hfile = hfile_train
            flg = "train"

        f=t.extractfile(pick)
        bb=f.read()
        file_data=BytesIO(bb)

        im = Image.open(file_data)
 
        if not quiet: print("Image {}, {} is: {}".format(i, pick, flg))

        # Run the categorising
        categorise_and_file(pick, hfile, im, bb, quiet)

    hfile.close()


def categorise_single(tarname, base_filename, plot=True):
    """Categorise a single image by colour, optionally plotting it"""
    #Image is assumed to be contained in a tarball and filename
    # has to be the full name in there
    
    #Open tarfile
    t=tarfile.open(tarname, 'r:gz')
    #Read im.
    f=t.extractfile(base_filename)
    bb=f.read()
    file_data=BytesIO(bb)

    im = Image.open(file_data)
    # Either we plot, or we should print for sure
    names = identify_dominant(im, not plot)
    name = names[0]
    title =  "Dominant colour is {}{}".format(name[0], name[1])
    if(plot): plot_image(im, title)


if __name__ == "__main__":

    try:
        mode = argv[1]
        assert(mode in ["show", "sort", "identify", "partition"])
    except:
        print("ERROR: First argument should be 'show' to show an image by filename, 'identify' to print the 3 dominant colours in image or 'sort' to categorise many")
        exit()

    if mode in ["show", "identify"]:
        #Need two parameters, the tarfile and the filename
        assert len(argv) == 4, "ERROR: This mode requires a tarfile and  a filename input"
        tarfilen = argv[2]
        filename = argv[3]
        if mode == "show":
            categorise_single(tarfilen, filename, plot=True)
        else:
            categorise_single(tarfilen,filename, plot=False)
    elif mode in ["sort"]:
        #Need an input tarfile, output prefix and count of how many
        assert len(argv) == 6, "ERROR: This mode requires an input tarfile, output HDF mock directory, a count and a chunk size"
        in_file = argv[2]
        out_dir = argv[3]
        try:
            count = int(argv[4])
            chunk_sz = int(argv[5])
        except:
            print("ERROR: Parameter not convertible to integer")
            exit()
        sort_n_ims(in_file, out_dir, count, chunk_sz, quiet=False)       
    elif mode in ["partition"]:
        #Need an input tarfile, two output files for train and test and prob for which target
        assert len(argv) == 6, "ERROR: This mode requires an input tarfile, two output HDF mock directorys, and a probability for picking the first one"
        in_file = argv[2]
        out_file1 = argv[3]
        out_file2 = argv[4]
        try:
            prob = float(argv[5])
            assert 0 <= prob and prob <= 1, "Prob must be in range [0,1]"
        except:
            print("ERROR: Parameter not convertible to float or not in [0,1]")
            exit()
        partition_ims(in_file, out_file1, out_file2, prob, quiet=False)       

