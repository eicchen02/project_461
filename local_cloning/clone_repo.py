from git import Repo  # import git library
import sys  # import sys to use command line arguments
import os
import re
import urllib.request as u
from subprocess import DEVNULL

# open the command line argument file
url = sys.argv[1]

# make a directory named 'cloned_repos' to put the cloned repos in
os.mkdir("local_cloning/cloned_repos/")

log1 = open("log/logv1.txt", "w")
log2 = open("log/logv2.txt", "w")

# if it was a git URL, clone it
if "github" in url:

    # clone the current git URL into a directory named after the current url_num value
    Repo.clone_from(url, "local_cloning/cloned_repos/" + os.path.basename(url) + "/")

    # print status update
    # print("finished cloning url #" + str(url_num))
    log1.write("finished cloning url #" + str(os.path.basename(url)) + "\n")

# if it was not a git URL, that means it was an npm URL
else:

    webUrl = u.urlopen(url)
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
    Repo.clone_from(gitLink, "local_cloning/cloned_repos/" + os.path.basename(gitLink) + "/")
    
    # print status update
    log1.write("finished cloning url #" + os.path.basename(gitLink) + "\n")

log1.close()
log2.close()
exit(0)
