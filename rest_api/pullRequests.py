"""
Name: Matthew Nale
	Date of Last Edit: 3/25/2023

	Purpose: Obtains amount of files introduced through pull requests

	Details: Using the PyGithub API, obtains the needed information for the total commit changes from pull requests over the total number of changes

"""
import requests
import urllib.request as url
import re
import sys
import os


def getGithubURLs(repo):
    webUrl = url.urlopen(repo)
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
    return gitLink


def main():
    givenUrl = sys.argv[1]
    if givenUrl == "":
        print("0.0")
        return

    if "npmjs.com/" in givenUrl:
        gitURL = getGithubURLs(givenUrl)
    else:
        gitURL = givenUrl

    github_token = os.environ.get("GITHUB_TOKEN")
    names = (gitURL.split("github.com/", 1)[1]).split("/")
    
    headers = {"Authorization": f"Bearer {github_token}"}

    query = """
    {
      repository(owner: "%s", name: "%s") {
        pullRequests(states: MERGED, last: 100) {
          nodes {
            additions
          }
        }
        commitComments(last: 100) {
          nodes {
            commit {
              additions
            }
          }
        }
      }
    }
    """ % (
	names[0],
	names[1]
    )

    json = {"query": query}

    response = requests.post(url="https://api.github.com/graphql", json=json, headers=headers)
    if response.status_code == 200:
        try:
            newCode = 0
            totalCommits = 0
            for pull in response.json()["data"]["repository"]["pullRequests"]["nodes"]:
                try:
                    newCode += pull["additions"]
                except:
                    newCode += 0
            for commit in response.json()["data"]["repository"]["commitComments"][
		    "nodes"
	    ]:
                try:
                  totalCommits += commit["commit"]["additions"]
                except:
                  totalCommits += 0
        except:
            newCode = 0
            totalCommits = 1
        if(newCode == 0 and totalCommits == 0):
              print("0.0")
        else:
          print(f"{round(newCode/(newCode + totalCommits), 2)}")
    else:
        print("0.0")


if __name__ == "__main__":
    main()
