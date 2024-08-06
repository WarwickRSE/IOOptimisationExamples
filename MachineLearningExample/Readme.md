# Setup

For simplicity, we use a Torch built-in data set, and put all our data
into a subdirectory `data`.
Then the script
get\_example\_dataset.py will download our choice of the
Oxford 102 flowers. Others may work, as long as they're colour and contain
images that PIL can read. Pass this a single parameter for the directory
you want to images to be downloaded under, e.g. `./data` or it will
default to using `./data`

Alternately, we can download without unpacking using `download_data.sh`
which takes one parameter for the directory to download to

We do NOT use the supplied labelling, instead using our own label generated
programaticaly, for fun. 

We have written the folowing simple tools:

# Tool one

A simple heuristic "colour identifier" colourHeuristic.py

This uses a clustering method to select the colour most present in
an image, and then a heuristic method to name this colour

NOTE: for images with a neutral background, this is likely to
be the largest cluster

It also sorts the flat data file into labelled subdirectories so that we can use
ImageFolder in Torch later.

In Folder Original and Filesystem, we sort and write back to disk (in the latter case
we combine into a single file later), and in the CombinedFile we write the data
directly into an HDF5 file.


## How it works
LAB colour space (https://en.wikipedia.org/wiki/CIELAB\_color\_space) expresses colours not in 
Red-Green-Blue space but in terms of their
position along the Red-Green axis (A), the Blue-Yellow axis (B) and the Lightness axis (L)

While it is very imperfect, we can partition this space into something that gets it mostly
right by considering angle in the A-B plane as the colour, and L as the intensity.
We add a circle around the centre of the A-B plane for a balanced grey, and tweak a bit
to introduce pink and brown, in place of "light red" and "dark orange".

The end result is surprisingly OK.

## Running this tool

Once the flowers data set is downloaded, the colourHeuristic.py tool can be used in 3 modes
See the individual folders for the arguments needed.

* show: Plot the given image titled with its dominant colour
* identify: Print the 3 most dominant colours in the given image
* sort: Select some random files from one location, and sort them into another according to their dominant colour

# Tool 2 - A ML model

** NOTE: this is NOT an example of how to do _good_ ML. It is just enough to show the use of
the file modifications **

## Training the model

The basic ML model needs training, and is then saved as weights, then we can classify using it.

As for the first tool, there are versions using files and ones using modified files
to reduce the number we need.

The `Original` folder uses ImageFolder from Torch to load the data. It expects a directory containing
sub-directories, the names of which will be used as the labels. 

The `Filesystem` folder mounts a combined HDF file as a filesystem, then uses the same ImageFolder
idiom.

The `CombinedFile` folder uses a combined HDF file, read using a custom data loader.

All three versions can be called using
`./train_model.py <input location>`. What we specify as input depends on the version and
can be a folder or an HDF file. See Folders for details

## Classifying Images

Once the model has been trained and saved, we can classify images from
the original set. We have to pass the source of the images to classify,
the labels created by the training script, and a count of how many
images we want to classify and show.

For exactly how, see the individual folders, but the gist is:
`classify.py <image source> <labels file> <count>`

Once again, we show this using single files and a combined file,
both as a filesystem and a custom reader.

# Tool 3 - An example Labbook database

For the heuristic classification, we might want to keep track of what we are doing.
We could use various tools to do this: for simplicity here we use a plain database
with sqlite as this is widely available. In the Folder MetaDatabase we demo using
this to store information on how well our classifier worked. See that folder for details.

