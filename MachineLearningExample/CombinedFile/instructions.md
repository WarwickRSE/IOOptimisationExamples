# Using a Custom HDF5 File

In this example, we show the on-the-fly creation and use of a
combined HDF5 datafile, instead of many files. 

This closes the "gap" in the Filesystem approach where we
had a lot of files briefly. Generating the file on-the-fly
is ideal for the case where we are producing the data by
tranformation or procedural generation etc. 

**NOTE: Here we are random-accessing into a compressed tar
file. This is not a nice file access pattern and we do
not generally recommend it.** For this example it is the easiest
way to process a random subset of the files such that we can
re-run and add more, new files. This lets us test with a few
and then build a better training set if we want to actually try out
the machine learning part.

## SIDE NOTE:
This folder contains an HDFVFS Python script which we use
to mock up a similar interface to an HDF5 file. This is designed
to work well enough for the examples here, but is not
being presented as excellent, robust, code. If you use it for anything
"real", consider yourself duly warned.  

## Producing the Data File

The colourHeuristic.py code has been changed. You should now:
* Download, without unpacking, the flowers data as a tgz to /tmp. 
	* Note:/tmp is shared by anybody using the node. I like to insert my username to make the names more distinct
	* You can use `./download_data.sh /tmp/$USER/` to do this
* Use the `sort` option, giving it the tarfile we just grabbed, and an output directory
	* The output directory wont need to exist - it's the name of the HDF5 dataset now
	* Now there are two count parameters - one for the total number of files to sort and a second for how many to sort at once
* After running this, you should get an .h5 file. We can test this using the mount tool
	* `h5vfs <filename> /tmp/$USER/mnt/` should mount the file and let you list some images in it
	* `fusermount -u /tmp/$USER/mnt`

Now we have effectively produced the same HDF5 file we did in the previous example, but without
every unpacking the entire tarball, OR duplicating files in the sorting process.

We also show example code to partition the entire file into train and test sets, although
for 8000 images this takes a long time! For reference it is
`./colourHeuristic.py partition <tarfile> <training set hdf5 filename> <test set hdf5 name> <probability of selecting for training set (fraction)>`


## Using the Data File

We could follow the previous example, mount the file like we just did to test with
and keep using the ImageFolder idiom. However, in some cases we might want to do
something different, so here the `train.py` script demonstrates using a custom
DataLoader reading from our HDF5 file directly. 

The modified `train_model.py` code does this. We give it one argument,
the name of the hdf5 training data set.

As before, this outputs the labels as json file, and the model weights for
use by the classifier.

## Classifying Images

For the classifier in this example we have two options: use the original tarball
and pick random images from it directly, or use the partition tool above to create
a test data set h5 file. This script selects based on file-extension and handles either.


