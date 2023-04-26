from git import Repo  # import git library
import sys  # import sys to use command line arguments
import os
import subprocess
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

    # find the package name in the URL
    package_name = url[url.find("/package/") + 9 :]

    # clone the current npm URL into 'local_cloning/cloned_repos' directory
    subprocess.run(
        ["npm v " + package_name + " dist.tarball | xargs curl | tar -xz"],
        shell=True,
        executable="/bin/bash",
        stdout=DEVNULL,
        stderr=DEVNULL
    )
    subprocess.run(
        ["mv package/ local_cloning/cloned_repos/" + os.path.basename(url)],
        shell=True,
        executable="/bin/bash",
        stdout=DEVNULL,
        stderr=DEVNULL
    )

    # print status update
    log1.write("finished cloning url #" + os.path.basename(url) + "\n")

log1.close()
log2.close()
exit(0)
