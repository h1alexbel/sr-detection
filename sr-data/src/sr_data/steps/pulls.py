import pandas as pd
import requests
from loguru import logger


def main(repos, out):
    frame = pd.read_csv(repos)
    for idx, row in frame.iterrows():
        frame.at[idx, "pulls"] = pulls(row["repo"])
    frame.to_csv(out, index=False)


def pulls(repo):
    logger.info(f"Fetching pulls for {repo}")
    owner, name = repo.split("/")
    count = 0
    next = True
    cursor = None
    while next:
        response = requests.post(
            "https://api.github.com/graphql",
            headers={
                "Authorization": f"Bearer x",
                "Content-Type": "application/json"
            },
            json={
                "query": """
                query ($owner: String!, $name: String!, $after: String) {
                    repository(owner: $owner, name: $name) {
                        pullRequests(first: 100, after: $after) {
                            nodes {
                                author {
                                    login
                                }
                            }
                            pageInfo {
                                endCursor
                                hasNextPage
                            }
                        }
                    }
                }            
                """,
                "variables": {
                    "owner": owner,
                    "name": name,
                    "after": cursor
                }
            }
        )
        response_data = response.json()
        if "errors" in response_data:
            print(f"Error fetching data for {repo}: {response_data['errors']}")
            break

        pull_requests = response_data["data"]["repository"]["pullRequests"]
        for pr in pull_requests["nodes"]:
            if pr["author"]["login"] != "renovate[bot]":
                count += 1

        page_info = pull_requests["pageInfo"]
        cursor = page_info["endCursor"]
        next = page_info["hasNextPage"]
    logger.info(f"Found {count} pulls")
    return count
