from sql_header import *
import json
import re
from os import listdir
from sqlalchemy.orm import sessionmaker
import sys
from datetime import datetime

def upload():
    #Get data from output file
    f = open('output/output.json')
    data = json.load(f)[0]
    f.close()

    repo_url = data["URL"]

    repo_name = re.search(r'.+\/(.+)$', repo_url)
    if repo_name is None:
        raise("No valid name found from link")
    PackageName = repo_name[1]

    readme_dir = 'local_cloning/cloned_repos/{}'.format(repo_name[1])
    dir_list = listdir(readme_dir)
    readme_regex = re.compile(r'readme.', flags=re.IGNORECASE)
    for item in dir_list:
        if readme_regex.search(item):
            readme_file = item 

    try:
        with open(readme_dir + '/' + readme_file) as f3:
            readme_content = str()
            for count, line in enumerate(f3):
                if(count < 200):
                    readme_content = readme_content + line
                    # print(line)
                else: 
                    break
    except:
        raise("Error reading readme")
    
    try:
        package = open(f'local_cloning/cloned_repos/{PackageName}/package.json')
        jsonData = json.load(package)
        if "version" in jsonData:
            # URL exists in package
            version = jsonData["version"]
        else:
            raise("Error getting version")
    except:
          raise("Error getting version")
    
    exist = exists(table.c.PackageLink, data["URL"])

    if exist is False:
        #Doesnt exist, upload 
        print("It doesn't exist! Uploading", file = sys.stderr)
        query = table.insert().values(
                    PackageLink = data["URL"], 
                    NetScore = data["NET_SCORE"],
                    RampUp = data["RAMP_UP_SCORE"],
                    UpdatedCode = data["UPDATED_CODE_SCORE"],
                    Pinning = data["PINNING_PRACTICE_SCORE"],
                    Correctness = data["CORRECTNESS_SCORE"],
                    BusFactor = data["BUS_FACTOR_SCORE"],
                    Responsiveness = data["RESPONSIVE_MAINTAINER_SCORE"],
                    Licensing = data["LICENSE_SCORE"],
                    PackageName = PackageName,
                    Readme = readme_content,
                    LastModified = datetime.now(),
                    Version = version
                )

    else:
        #Exists, update
        print("It does exist! Updating", file = sys.stderr)
        query = table.update().where(table.c.PackageLink == data["URL"]).values(
                    PackageLink = data["URL"], 
                    NetScore = data["NET_SCORE"],
                    RampUp = data["RAMP_UP_SCORE"],
                    UpdatedCode = data["UPDATED_CODE_SCORE"],
                    Pinning = data["PINNING_PRACTICE_SCORE"],
                    Correctness = data["CORRECTNESS_SCORE"],
                    BusFactor = data["BUS_FACTOR_SCORE"],
                    Responsiveness = data["RESPONSIVE_MAINTAINER_SCORE"],
                    Licensing = data["LICENSE_SCORE"],
                    PackageName = PackageName,
                    Readme = readme_content,
                    LastModified = datetime.now(),
                    Version = version
                )

    result = connection.execute(query)
    connection.commit()
    print("Upload/Update Complete!", file = sys.stderr)

if __name__ == "__main__":
    upload()
    