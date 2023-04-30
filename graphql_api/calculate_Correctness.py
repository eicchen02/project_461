import requests
import sys  # import sys to use command line arguments
import json  # import json to parse json file
import os

github_token = os.getenv("GITHUB_TOKEN")

url = sys.argv[1]

file_v2 = open("log/logv1.txt", "w")
file_v3 = open("log/logv2.txt", "w")

names = []
file_v2.write(f"\n\n>>> Extracting information for url {url}\n")
  
repoName = url.partition("github.com/")[2]  # extract "owner/repo"

if not repoName:  # if github.com/ is not found, extract as npmjs package
    url = os.path.basename(url.strip("\n"))
    with open(f"local_cloning/cloned_repos/{url}/package.json") as json_File:
        npmsRepo = json.load(json_File)  # load json file containing repo info
    repoName = npmsRepo["repository"]  # extract repo info

    if not isinstance(repoName, str):  # if a dict is returned instead of str
        repoName = list(repoName.values())[1]  # extract url from dict
        repoName = repoName.partition("github.com/")[2].replace(
            ".git",""
        )  # extract "owner/repo"
  
names.append(
    (repoName.partition("/")[0],repoName.partition("/")[2].replace("\n","")))  # append (owner, repo)

headers = {"Authorization": f"Bearer {github_token}"}  # build the header
# run requests
with open("output/correctness_out.txt", "w") as f:
    for repository in names:
        file_v2.write("\n\n>>> beginning correctness metric with GraphQL api\n")

        file_v3.write("\n\n------------------\n")
        file_v3.write(
            "current analysis of correctness will be done with github GraphQL api\n"
        )
        file_v3.write(
            "beginning retrieval of information from repository %s %s\n" 
            % (repository[0],repository[1])
        )
        file_v3.write("------------------\n")
        # build the query to retrieve needed info using from the given repo
        query = f"""{{repository(owner: "{repository[0]}", name: "{repository[1]}") {{stargazerCount openIssues: issues(states: OPEN) {{totalCount}}}}}}"""
        response = requests.post(
            "https://api.github.com/graphql", json={"query": query}, headers=headers
        )

        if response.status_code == 200:  # extract the result from the response
            file_v2.write("successful graphql api retrieval\n")
            file_v3.write(
                "successful graphQL api retrieval with code %d\n" 
                % response.status_code
            )

            try:
                starCount = response.json()["data"]["repository"]["stargazerCount"]
                openIssuesCount = response.json()["data"]["repository"]["openIssues"][
                    "totalCount"
                ]
                correctness = starCount / (
                    starCount + openIssuesCount * 10
                )  # calculate correctness
                file_v2.write("proper repo format\n")
                file_v3.write("proper repo format - data retrieval successful\n")

                file_v3.write("Number of stars: %i\n" % starCount)
                file_v3.write("Number of open issues: %i\n" % openIssuesCount)
                file_v2.write("Repo had %d stars\n" % starCount)
                file_v3.write(
                    "Correctness score for repo %s owned by %s: %f \n" 
                    % (repository[1], repository[0], correctness)
                )

            except:
                file_v2.write("improper repo format\n")
                file_v3.write("improper repo format - error with repo\n")

            # print("Number of stars: %i" % starCount)
            # print("Number of open issues: %i" % openIssuesCount)
            # print("Correctness score for repo %s owned by %s: %f \n" % (repository[1], repository[0], correctness))

            # write the correctness score to the outputfile
            f.write(str(correctness))
            f.write("\n")
    
        else:  # handle error if response is not received correctly
            # print("Failed to retrieve response using GraphQL by returning code {}.".format(response.status_code))
            file_v2.write("Failed to retrieve response")
            file_v3.write(
                "Failed to retrieve response with code %d\n" 
                % response.status_code
            )

file_v2.close()
file_v3.close()
