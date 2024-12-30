"""
Collect pulls for each repo.
"""
# The MIT License (MIT)
#
# Copyright (c) 2024 Aliaksei Bialiauski
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import pandas as pd
import requests
from loguru import logger
from requests import Response


def main(repos, out, token):
    frame = pd.read_csv(repos)
    for idx, row in frame.iterrows():
        frame.at[idx, "pulls"] = pulls(row["repo"], token)
    frame.to_csv(out, index=False)
    logger.info(f"Saved {len(frame)} repositories with pulls to {out}")


def pulls(repo, token) -> int:
    count = 0
    next = True
    cursor = None
    ignored = ["dependabot", "renovate"]
    while next:
        response = request(token, repo, cursor)
        if "message" in response:
            logger.error(f"Error fetching data for {repo}: {response['message']}")
        pulls = response["data"]["repository"]["pullRequests"]
        for pull in pulls["nodes"]:
            if pull["author"] is not None:
                login = pull["author"]["login"]
                if login not in ignored:
                    count += 1
        page = pulls["pageInfo"]
        cursor = page["endCursor"]
        next = page["hasNextPage"]
    logger.info(f"Fetched pulls for {repo}: {count}")
    return count


def request(token, repo, cursor) -> Response:
    owner, name = repo.split("/")
    return requests.post(
        "https://api.github.com/graphql",
        headers={
            "Authorization": f"Bearer {token}",
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
    ).json()
