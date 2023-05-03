import base64
import json
import os
import re
import urllib.request as url
from urllib.parse import urlparse
import sys
import requests

class BadRequest(Exception):
    '''Define bad request exception'''

def getGithubURLs(repo):
    '''Transform npm links to github links'''
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

def count_pinned_dependencies(repo_url):
    '''Counts the pinned dependencies'''
    # Parse the repository owner and name from the URL
    path = urlparse(repo_url).path
    match = re.match(r'/([\w-]+)/([\w-]+)', path)
    if not match:
        raise BadRequest('Invalid repository URL')
    owner = match.group(1)
    repo_name = match.group(2)

    # Fetch the repository metadata from the GitHub API
    token = os.environ.get('GITHUB_TOKEN')
    headers = {'Authorization': f'token {token}'}
    api_url = f'https://api.github.com/repos/{owner}/{repo_name}/contents/package.json'
    response = requests.get(api_url, headers=headers, timeout=120)
    if response.status_code != 200:
        return 0.0
        """
        if response.status_code == 401:
            raise BadRequest('Failed to authenticate with GitHub API. Please check your personal access token.')
        elif response.status_code == 403:
            raise BadRequest('Failed to access repository. Please ensure your personal access token has the necessary permissions.')
        else:
            raise BadRequest(f'Failed to fetch package.json. Error {response.status_code}: {response.reason}')
        """
    # Parse the contents of package.json and count the number of pinned dependencies
    contents = json.loads(base64.b64decode(response.json()['content']).decode('utf-8'))
    count = 0
    pinned = 0
    if 'dependencies' in contents:
        for dep, version in contents['dependencies'].items():
            count += 1
            if re.match(r'^\^\d+\.\d+\.+', version) or re.match(r'^\d+\.\d+\.+', version) or re.match(r'^~\d+\.\d+\.+', version):
                pinned += 1
    else:
        return 1.0
    if pinned == 0:
        return 1.0
    else:
        return pinned / count
    
    
def main():
    '''Main function'''
    urlInput = sys.argv[1]
    if "npmjs.com/" in urlInput:
        gitURL = getGithubURLs(urlInput)
    else:
        gitURL = urlInput
    count_dep = count_pinned_dependencies(gitURL)
    print(f'{count_dep}')


if __name__ == "__main__":
    main()
    
