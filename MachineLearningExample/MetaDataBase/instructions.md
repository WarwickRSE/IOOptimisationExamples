
# Using A Database for Metadata

In the previous examples we just threw away all the ifo from our
colour heuristic mapper. Suppose we wanted to keep that in some
sort of labbook. This example shows a basic Sqlite3 database
which stores image filenames, the time we ran the identification,
the colours we identified, and some metadata about how well
the clustering worked. 


## Running the example

Because this is just an example, I don't handle table creation
in the code. Instead, you should run
`sqlite3 labbook.db
.read setup.txt`

to create the relevant tables. Then if you run the sort or
identify parts of the colourHeuristic code, you should
get some data written about the process. You can view this
at the sqlite command line, or using the 
`dump_labbook(filename)` method in `writeLabbook.py`


##Disclaimer

The Database code here is all safe from attacks, but it
is not as good as it could be. In particular:
* it doesn't deal well with filenames, only taking the last part of them. 
* it makes no attempt to pick the latest records
* it doesn't check for tables existing
* it doesn't create its own tables, relying on setup.txt instead

Things it does do well are:
* Avoiding injection attacks by not pasting strings together
* Handling dates in an ISO standard format
* Minimising (mostly) the DB transactions using JOINs
* Mostly normalising the data, and giving it a logical separation into tables


