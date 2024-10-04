"""
Collect maven information for each repo.
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
import json

import pandas as pd
import requests
from loguru import logger
from requests import Response


# @todo #74:45min Exclude repositories that don't have any maven projects.
#  We need to exclude all repositories that don't contain any 'pom.xml' inside.
#  Don't forget to create a unit test for this.
# @todo #74:60min Parse 'build' JSON array of maven projects into most valuable
#  information for embedding step. We should parse all maven projects from JSON
#  array, extract some useful information from each, and merge into single
#  input. For pom.xml parsing we can use XPATH, and XSLT for merging.
def main(repos, out, token):
    frame = pd.read_csv(repos)
    for idx, row in frame.iterrows():
        frame.at[idx, "build"] = pom(row["repo"], row["branch"], token)
    before = len(frame)
    frame = frame[frame.build != "[]"]
    logger.info(f"Skipped {before - len(frame)} repositories with 0 pom.xml files")
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
