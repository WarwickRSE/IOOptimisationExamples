
#To transfer all the files in 'mydirectory' on 'remote machine' to
# the current directory on the local machine
ssh <remote> "cd <mydirectory> ; tar -cvzf - *" | tar -xvzf -
#NOTE: the '-' in the first tar command means "send the data to the
# standard output (not to a named tar file)"
# The '-' in the second tar command means "read the data from the
# standard input (not from a named tar file)".
# The '|' between them is a pipe, which hooks those two (standard-out
# and standard-in) together
