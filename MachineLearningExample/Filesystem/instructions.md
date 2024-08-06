# Using an HDF5 Mount

In this example, we replace the many data files of the original
with a single HDF5 file. We then use our tool, H5VFS 
(for H5-Virtual-File-System) to mount this file as if it
was a directory. HDF5 datasets are mapped to folders and with the
tool we
can read them just as if they were individual files.

Mounting refers to associating one filesystem, image or set of files
with a specific name in your main filesystem (i.e. a directory). Just like
when you plug in a USB stick, which lets you access the files on it
at a Path usually starting something like `/media/` or `/Volumes/`
depending on your system. We say the device has been "mounted under"
that root directory.

For Warwick users, you are probably already familiar with this as
when you use your shared SCRTP Linux desktop system
Home and Storage file spaces,
they physically exist on one computer, and are mounted under certain
names on the login and compute nodes for Taskfarm or the HPC.
See https://docs.scrtp.warwick.ac.uk/hpc-pages/hpc-storage.html#scrtp-linux-storage
for a reminder of how this works on Warwick's HPC clusters.


## What's FUSE for?
Behind the scenes this tool uses a package called FUSE, which you'll
need to build it on your own Linux-based systems. Check docs for
your distro to see if you need to install it, and how.

FUSE (Filesystem in Userspace) lets a normal user mount a filesystem,
without needing admin privilege. This is good, because on shared systems
we don't have those, and on our own systems we should avoid using them
unless necessary (less chances to make irreparable mistakes).

## Using the Mount tool

**IMPORTANT - if you were listening earlier you know that network
provided filesystems are finicky things. On our Clusters, please
only mount into /tmp/**

**Second note: tmp space is shared, but files you create there are owned
by you. If you create /tmp/mnt then nobody else can until you delete it
or the cleanup processes run. Here we are going to use our usercode
to make a unique name - you could also use a system tool called
`mktemp` which will make a unique name for you**

Like any other mount, we need to specify two things, and can specify
some others. The essentials are the thing we want to mount, and the
location we want to mount it, named the "image" and the
"mountpoint" respectively. 

The mounting options are mostly specific things aimed at performance
on "weird" filesystems, or limiting what the system is allowed to do. 
One is worth mentioning here - "ro" which mounts as read-only
and means no write operations will be permitted. 

To mount an HDF5 file called "flower-data.h5" in a subdirectory called
"Data", under a subdirectory in tmp called "mnt" (we call it this for
convenience, we can use any directory name, including existing ones)
we do
`h5vfs ./Data/sorted-flowers.h5 /tmp/$USER/mnt/`
and then `ls /tmp/$USER/mnt/sorted-flowers/` should show us the files and folders
in the dataset.

## Using the Mounted Files

Now the file is mounted, we don't have to change anything in our code.
The ImageFolder class from PyTorch will see the files and folders exactly
like before, as long as we pass the correct file path - which is now
`/tmp/$USER/mnt/sorted-flowers/`

## Creating the File
In this approach, the only tricky bit is creating the combined HDF5 file.

**NOTE: In this example we create many files and then combine them. This is
not perfect, as we still have a large amount temporarily.** However, 
if, instead of one dataset of 10k images, we had 50 such, then this approach
of generating one, combining it, removing the unpacked files, and then going to the next,
would at least leave us using 10k files at a time, not 500k!

Also, we can do all of this in the `/tmp` directory and avoid thrasing
our home or storage space. 

Our tool toHDF5, take a directory and builds an HDF5 file from it and all its
subdirectories. We can optionally specify patterns for files/folders to include
or to exclude too. Let's keep it simple and just pack all of our sorted flowers
images into one file. Suppose we have them all in subdirectories
of `./Data/sorted-flowers`, like we produced in the previous example.
Then we do this using
`toHDF5 ./Data/sorted-flowers/` which gives us a file, `sorted-flowers.h5`
which we can then mount like above and use.

## The Code versus the Original code
Because we're using the mounts, the code here is identical to that in 
the Original folder. We just have an extra copy in case we want
to make tweaks.

Similarly, all instructions for running the training and classifying steps
remain the same.

