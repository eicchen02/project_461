import base64
import sys
import os
from git import Repo
import urllib.request as u
import re
import zipfile

def createEncodedFile(url):
    # Grabs the package URL passed in
    packageURL = url
    
    # Checks if the package is already downloaded locally to prevent redownloads
    path = f'./local_cloning/cloned_repos/{os.path.basename(packageURL)}/'

    # Download the package if it does not exist
    if not os.path.exists(path):
        if "github" in packageURL:
            # Clone the github package
            Repo.clone_from(packageURL, "./local_cloning/cloned_repos/" + os.path.basename(packageURL) + "/")
        # If it was not a 'github.com' package (NPM)
        else:
            webUrl = u.urlopen(packageURL)
            if webUrl.getcode() == 200:
                html_cont = webUrl.read().decode("utf-8")
                r1 = r'<span id="repository-link">(.*?)<\/span>'
                try:
                    reg_out = re.search(r1, html_cont)
                    gitLink = "https://" + reg_out.group(1)
                except:
                    raise Exception("Valid GitHub link not found.\n")
            else:
                raise Exception("npm url not able to connect.\n")
        
            # clone the current git URL into a directory named after the current url_num value
            Repo.clone_from(gitLink, "./local_cloning/cloned_repos/" + os.path.basename(gitLink) + "/")

    # After making sure package is cloned, loop through and zip the entire directory
    zipf = zipfile.ZipFile(f'./local_cloning/encoded_repos/{os.path.basename(packageURL)}.zip', 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path):
        zipf.write(root)
        for file in files:
            zipf.write(os.path.join(os.path.relpath(root), file),
                       arcname=os.path.join(root.replace(f'local_cloning/cloned_repos/{os.path.basename(packageURL)}', ""), file))
    
    zipf.close()
    
    # Now Base64 encode the file
    with open(f'./local_cloning/encoded_repos/{os.path.basename(packageURL)}.zip', 'rb') as fin, open(f'./local_cloning/encoded_repos/{os.path.basename(packageURL)}_base64', 'wb') as fout:
        base64.encode(fin, fout)
    
    # Finally, return the base64 and zip filename that has been created
    zipName = f'./local_cloning/encoded_repos/{os.path.basename(packageURL)}.zip'
    encodedName = f'./local_cloning/encoded_repos/{os.path.basename(packageURL)}_base64'
    return zipName, encodedName
