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
import xml.etree.ElementTree as ET

import pandas as pd
import requests
from loguru import logger
from requests import Response

# XML namespaces for Maven pom.xml file.
namespaces = {
    "pom": "http://maven.apache.org/POM/4.0.0"
}


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
    return json.dumps(merge(build, repo))


def merge(build, repo):
    good = []
    plugins = []
    packgs = []
    for project in build:
        path = project["path"]
        logger.debug(f"Checking {repo}: {path}")
        root = ET.fromstring(project["content"])
        print(ET.dump(root))
        if len(
                root.findall(
                    ".//pom:dependency[pom:groupId='@project.groupId@']",
                    namespaces
                )
        ) > 0:
            logger.info(f"Skipping {path}, since it contains @project dependency")
        else:
            profile = {}
            for packaging in root.findall(".//pom:packaging", namespaces):
                packgs.append(packaging.text)
            for plugin in root.findall(".//pom:plugin", namespaces):
                print(ET.dump(plugin))
                group = plugin.find("./pom:groupId", namespaces)
                artifact = plugin.find("./pom:artifactId", namespaces)
                plugins.append(f"{group.text}:{artifact.text}")
            good.append(profile)
    used = len(good)
    logger.info(f"Found {used} good Maven projects in {repo}")
    return {
        "projects": used,
        "plugins": list(set(plugins)),
        "packages": {
            "wars": len(list(filter(lambda p: p == "war", packgs))),
            "jars": len(list(filter(lambda p: p == "jar", packgs))),
            "poms": len(list(filter(lambda p: p == "pom", packgs)))
        }
    }


def request(token, repo) -> Response:
    return requests.get(
        f"https://api.github.com/repos/{repo}/git/trees/HEAD?recursive=1",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
    ).json()
