import sqlite3
from datetime import datetime

# An example of using a Database as a Lab-book
# This is intended to store the results, and extra info,
# from our colour Identifying procedure, in case we wanted to see
# what we did

# This example shows the sort of thing you can do, but does not
# store everything we might want!

class dbLabbook:
    def __init__(self, filename="labbook.db"):
        """Connect etc"""
        # Probably we should check the tables are present and correct here
        # but in this example I will not
        self.connect(filename)

    def make_image_id(self, name):
        """Add image entry, returning it's id. If it exists, just return id"""
        # Table: CREATE table imageList(id integer primary key, filename text);
        data = {"filename":name}
        #Insert if new, else ignore
        self.cursor.execute("INSERT INTO imageList VALUES(NULL, :filename) on CONFLICT(filename) DO NOTHING", data)
        self.connec.commit()
        return self.cursor.lastrowid

    def make_colour_id(self, name):
        """Store colour name, returning id. If it exists, just return id"""
        # Table: CREATE table colourMap(id integer primary key, name TEXT UNIQUE);
        data = {"cname":name}
        #Insert if new, else ignore
        self.cursor.execute("INSERT INTO colourMap VALUES(NULL, :cname) on CONFLICT(name) DO NOTHING", data)
        self.connec.commit()
        return self.cursor.lastrowid
       

    def store_run(self, filename, colours, inertia, n_clusters):
        """Store all the info"""
        #Tables: CREATE table imageColour(imageId integer NOT NULL, genTime TEXT, c1 integer, c2 integer, c3 integer);
        #      : CREATE table classifierMeta(imageId integer NOT NULL, colourResultId integer NOT NULL, inertia REAL, n_clusters integer CHECK(n_clusters > 0));


        # Get current time in correct format
        dateStr = datetime.now().isoformat()

        #First get the id for the filename
        res = self.cursor.execute("SELECT * from imageList WHERE filename == :filename", {'filename':filename})
        the_id, tmp = res.fetchone()

        ins_data_C={"imageId":the_id} #One dict for each insert for simplicity
        ins_data_M={"imageId":the_id}

        c_ids = []
        for i in range(3):
            #Look up the colours
            try:
                c_name = '_'.join(colours[i])
                res = self.cursor.execute("SELECT * from colourMap WHERE name = :c_name", {"c_name":c_name})
                d = res.fetchone()
                if d is None:
                    c_id = self.make_colour_id(c_name)
                else:
                    c_id = d[0]
                c_ids.append(c_id)
            except KeyError as e:
                raise RuntimeError( "Please supply 3 colours for inserts")
            except Exception as e:
                #Something else went wrong
                raise e

        ins_data_C["time"] = dateStr
        ins_data_C["c1"] = c_ids[0]
        ins_data_C["c2"] = c_ids[1]
        ins_data_C["c3"] = c_ids[2]
        self.cursor.execute("INSERT into imageColour VALUES(:imageId, :time, :c1,:c2,:c3)", ins_data_C)

        ins_data_M["CRId"] = self.cursor.lastrowid
        ins_data_M["inertia"] = inertia
        ins_data_M["n_clusters"] = n_clusters

        self.cursor.execute("INSERT into classifierMeta VALUES(:imageId, :CRId, :inertia, :n_clusters)", ins_data_M)

        self.connec.commit()

    def get_image_list(self):
        res= self.cursor.execute('SELECT filename from imageList')
        data = res.fetchall()
        #Strip tuple-hood
        data = [item [0] for item in data]
        return data

    def print_image_data(self, name, complete=True):
        """Print all the info about a filename"""

        res = self.cursor.execute("SELECT * from imageList WHERE filename == :filename", {"filename":name})
        the_id, dat = res.fetchone()
        

        #Getting the colour info, restoring names as we go
        # This is slightly tricky: we need to restore 3 ids so we need to join the colourMap table 3 times
        # Alternately, you could get the imageColour record and look up the ids -> colourNames one by one
        res = self.cursor.execute("SELECT imageColour.genTime, c1.name, c2.name, c3.name, imageColour.imageId from imageColour INNER JOIN colourMap as c1 INNER JOIN colourMap as c2 INNER JOIN colourMap as c3  ON imageColour.c1 == c1.id and imageColour.c2 == c2.id and imageColour.c3 == c3.id  WHERE imageId == :id", {"id":the_id})
        dat = res.fetchone()
        time = dat[0]
        colours = (dat[1], dat[2], dat[3])
        CRId = dat[4]
        print("Image {} classified at {}: 1st colour {}, 2nd colour {}, 3rd colour {}".format(name, time, colours[0], colours[1], colours[2]))

        if complete:
            #Add info about the clustering that got those colours
            res = self.cursor.execute("SELECT inertia, n_clusters from classifierMeta WHERE colourResultId = :CRId", {"CRId":CRId})
            meta=res.fetchone()

            print("Found {} clusters, final inertia {}".format(meta[1], meta[0]))

    def connect(self, filename):
        """Handles connecting to a new db"""
        self.connec = sqlite3.connect(filename)
        self.cursor = self.connec.cursor()
        
def dump_labbook(db_name):
    
    theBook = dbLabbook(db_name)

    ims = theBook.get_image_list()
    for item in ims:
        theBook.print_image_data(item)

