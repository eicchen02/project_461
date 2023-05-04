import base64
import zipfile
import sys
import json
import os
from urllib.parse import urlparse

def main():
    input = sys.argv[1]
    try:
        data = open(input, 'r').read()
        if(base64.b64encode(base64.b64decode(data))):  # Test to see if can encode/decode the input -> Encoded file
            # If Encoded, first decode, then obtain the URL from the package.json file, if it exists
            with open('temp.zip', 'wb') as result:
                result.write(base64.b64decode(data))
            zip_ref = zipfile.ZipFile('./temp.zip', 'r')
            zip_ref.extractall('local_cloning/cloned_repos/')
            zip_ref.close()
            
            relativepath, = zipfile.Path(zip_ref).iterdir()
            
            os.remove("temp.zip")
            
            # Find the URL file from package.json
            package = open(f'local_cloning/cloned_repos/{relativepath.name}/package.json')
            jsonData = json.load(package)
            if "url" in jsonData["repository"]:
                # URL exists in package
                url = jsonData["repository"]["url"]
                netloc = urlparse(url).scheme + '://' + urlparse(url).netloc
                path = urlparse(url).path
                print(netloc + os.path.splitext(path)[0])
            else:
                #! Should return error 400 through REST API, once it has been set up
                print("-1")
    except:  # Otherwise, it's just a URL
        with open(input, 'r') as data:
            print(data.read())

if __name__ == "__main__":
    main()