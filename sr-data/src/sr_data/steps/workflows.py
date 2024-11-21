"""
Collect information about GitHub workflows in the repo.
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


def main(repos, out):
    frame = pd.read_csv(repos)
    frame["workflows"] = frame["workflows"].fillna("")
    for idx, row in frame.iterrows():
        repo = row["repo"]
        branch = row["branch"]
        workflows = row["workflows"]
        infos = []
        ymls = []
        if workflows and not isinstance(workflows, float):
            ymls = [
                file.strip()
                for file in workflows.split(",")
                if file.endswith((".yml", ".yaml"))
            ]
        logger.info(f"Repo {repo} has {len(ymls)} *.yml|*.yaml workflows inside .github/workflows")
        for yml in ymls:
            infos.append(
                workflow_info(
                    f"{repo}/refs/heads/{branch}/.github/workflows/{yml}"
                )
            )
        frame.at[idx, "workflows"] = infos
    frame.to_csv(out, index=False)
    logger.info(f"Saved repositories to {out}")


def workflow_info(path) -> str:
    return requests.get(f"https://raw.githubusercontent.com/{path}").text
