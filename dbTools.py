from tinydb import TinyDB, Query
import os
dbLocation = os.getcwd() + "/SRdb.json"
print("using database at", dbLocation)
db = TinyDB(dbLocation)

#db.purge()