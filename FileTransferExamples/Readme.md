# Scripts and demos for File Transfers

Assume the remote machine, called remote, has the relevant files
In this and the scripts, replace `<string>` with the string required, such
as the remote machine name, a filename etc

To create them
```truncate --size <size>

- transfer : try to fetch 30MB as 30x1MB files and 1x30MB files
- transfer2 : try to fetch 1GB as 10x0.1GB and 1x10GB
- transfer3 : fetch 30x1MB by ssh, tar and scp
- tarpipe : model for the tar idea.


