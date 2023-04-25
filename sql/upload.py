from sql_header import *
import json
from sqlalchemy.orm import sessionmaker

#Get data from output file
f = open('output/output.json')
data = json.load(f)
f.close()

Session = sessionmaker(bind = pool)
session = Session()

connection = pool.connect()
metadata = db.MetaData()
test = db.Table('TestData', metadata, autoload_with=pool)

#Check if url exists already
query = db.select(test).where(test.c.URL == data["URL"])
result = connection.execute(query)
connection.commit()
exists = bool(result.fetchone())

if exists is None:
    #Doesnt exist, upload 
    print("It doesn't exist! Uploading")
    query = test.insert().values(URL = data["URL"], 
               NET_SCORE = data["NET_SCORE"],
               RAMP_UP_SCORE = data["RAMP_UP_SCORE"],
               UPDATED_CODE_SCORE = data["UPDATED_CODE_SCORE"],
               PINNING_PRACTICE_SCORE = data["PINNING_PRACTICE_SCORE"],
               CORRECTNESS_SCORE = data["CORRECTNESS_SCORE"],
               BUS_FACTOR_SCORE = data["BUS_FACTOR_SCORE"],
               RESPONSIVE_MAINTAINER_SCORE = data["RESPONSIVE_MAINTAINER_SCORE"],
               LICENSE_SCORE = data["LICENSE_SCORE"])
else:
    #Exists, update
    print("It does exist! Updating")
    query = test.update().values(URL = data["URL"], 
               NET_SCORE = data["NET_SCORE"],
               RAMP_UP_SCORE = data["RAMP_UP_SCORE"],
               UPDATED_CODE_SCORE = data["UPDATED_CODE_SCORE"],
               PINNING_PRACTICE_SCORE = data["PINNING_PRACTICE_SCORE"],
               CORRECTNESS_SCORE = data["CORRECTNESS_SCORE"],
               BUS_FACTOR_SCORE = data["BUS_FACTOR_SCORE"],
               RESPONSIVE_MAINTAINER_SCORE = data["RESPONSIVE_MAINTAINER_SCORE"],
               LICENSE_SCORE = data["LICENSE_SCORE"])

result = connection.execute(query)
connection.commit()
print("Upload/Update Complete!")