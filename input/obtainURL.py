import base64
import zipfile
import sys
import json
import os

def main():
    input = sys.argv[1]
    try:
        data = open(input, 'rb').read()
        if(base64.b64encode(base64.b64decode(data))):  # Test to see if can encode/decode the input -> Encoded file
            # If Encoded, first decode, then obtain the URL from the package.json file, if it exists
            with open('temp.zip', 'wb') as result:
                result.write(base64.b64decode(data))
            zip_ref = zipfile.ZipFile('temp.zip', 'r')
            zip_ref.extractall(f'local_cloning/cloned_repos/{input}')
            zip_ref.close()
            
            os.remove("temp.zip")
            
            # Find the URL file from package.json
            package = open(f'local_cloning/cloned_repos/{input}/package.json')
            jsonData = json.load(package)
            if "url" in jsonData["repository"]:
                # URL exists in package
                url = jsonData["repository"]["url"]
                print(url)
            else:
                #! Should return error 400 through REST API, once it has been set up
                print("-1")
    except:  # Otherwise, it's just a URL
        print(input)

if __name__ == "__main__":
    main()