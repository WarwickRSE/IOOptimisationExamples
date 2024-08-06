# Using this version

This is the base version which we go on to modify

## What is wrong with this version

## The colour\_heuristic tool

This version of the tool expects files on disk. 

* show `full_filename`: Plot the given file titled with its dominant colour
* identify `full_filename`: Print the 3 most dominant colours in the given file
* sort `input_dir` `output_dir` `count`: Select count random files from input\_dir, and sort them into subdirectories of output\_dir according to their dominant colour


## Training the model
In this case, the colour\_heuristic tool sorted our data into directories under the
output\_dir we specified. To use this to train the model we do:

`train_model.py data/sorted-flowers/`

This produces the saved model weights, and also a json file mapping
from output weights to labels. This will be named like our input
directory, but with '\' replaced with '_' and ending in "labels.json"

## Classifying with the model

Once the model has been trained and saved, we can classify images from
the original set using e.g.

`classify.py data/flowers-102/jpg/ data_sorted-flowers_labels.json 5`

where the first argument is a folder of images to test, the second
is the labels name file created by the training script, and the
3rd is an integer for how many files to classify and show.

Once again, we show this using single files and a combined file,
both as a filesystem and a custom reader.


