import json

import pandas as pd
import requests
from loguru import logger
from requests import Response


def main(repos, out, token):
    frame = pd.read_csv(repos)
    for idx, row in frame.iterrows():
        frame.at[idx, "build"] = pom(row["repo"], row["branch"], token)
    frame.to_csv(out, index=False)

def pom(repo, branch, token):
    files = request(token, repo)
    poms = [file for file in files['tree'] if file['path'].endswith('pom.xml')]
    build = []
    for project in poms:
        path = project["path"]
        content = requests.get(
            f"https://raw.githubusercontent.com/{repo}/refs/heads/{branch}/{path}"
        ).text
        build.append(
            {
                "path": path,
                "content": content
            }
        )
    logger.info(f"Found {len(build)} pom.xml files in {repo}")
    return json.dumps(build)

def request(token, repo) -> Response:
    return requests.get(
        f"https://api.github.com/repos/{repo}/git/trees/HEAD?recursive=1",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
    ).json()
