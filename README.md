# IOOptimisationExamples

These are the code files associated with the demonstrations
in the Warwick Scientific Computing RSE workshop on
optimising data flows for HPC.

Under the FileTransferExamples you will find example
scripts to test file transfer rates, and two ways to do the
'compressed tar' transfer.

Under the MachineLearningExample directory you will
find some (quick) ML examples showing a few options
for reducing the number of files in an ML workflow.

## Useful Module commands

For the examples above, you will need to load the following modules:

`ml GCC/11.3.0  OpenMPI/4.1.4 PIP-PyTorch H5VFS Szip SciPy-bundle`

For using just the HDF5-as-a-filesystem tool via the Sulis module system you will need:
`ml GCC/11.3.0 H5VFS Szip/2.1.1`
OR
`ml GCC/13.2.0 H5VFS Szip`

## Related repos and Docs Links

For the HDF5-as-filesystem tool (offered as code "in development") see also:
https://github.com/csbrady-warwick/H5VFS

For the Sulis docs (hopefully you know this by now!) https://sulis-hpc.github.io/

For Sulis support: https://sulis-hpc.github.io/support/

