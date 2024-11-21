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
import yaml
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
        logger.info(
            f"Repo {repo} has {len(ymls)} *.yml|*.yaml workflows inside .github/workflows")
        for yml in ymls:
            infos.append(
                workflow_info(
                    fetch(
                        f"{repo}/refs/heads/{branch}/.github/workflows/{yml}"
                    )
                )
            )
        tjobs = 0
        oss = []
        steps = 0
        for info in infos:
            tjobs += info["w_jobs"]
            steps += info["w_steps"]
            for os in info["w_oss"]:
                oss.append(os)
        frame.at[idx, "w_jobs"] = tjobs
        frame.at[idx, "w_oss"] = len(set(oss))
        frame.at[idx, "w_steps"] = steps
    frame.to_csv(out, index=False)
    logger.info(f"Saved repositories to {out}")


def fetch(path) -> str:
    return requests.get(f"https://raw.githubusercontent.com/{path}").text


# @todo #75:60min Find release workflow from collected workflows.
#  We should find workflow that releases the repo artifacts to some target platform.
#  After we got parsed workflows, we can try to find one that makes releases. Probably,
#  it can be one, that uses on:push:tags. For instance: <a href="https://github.com/objectionary/eo/blob/master/.github/workflows/telegram.yml">telegram.yml</a>.
def workflow_info(content):
    yml = yaml.safe_load(content)
    jobs = yml["jobs"].items()
    jcount = len(jobs)
    oss = []
    scount = 0
    release = False
    on = yml[True]
    if on is not None:
        if on.get("release"):
            for type in on.get("release").get("types"):
                print(type)
    for job, jdetails in jobs:
        runs = jdetails.get("runs-on")
        if runs is not None and runs.startswith("$"):
            for matrixed in jdetails.get("strategy").get("matrix").get(
                    runs.strip()
                            .replace("${{", "")
                            .replace("}}", "")
                            .split(".")[1].strip()
            ):
                oss.append(matrixed)
        elif runs is not None:
            oss.append(runs)
        steps = jdetails.get("steps")
        if steps is not None:
            scount = len(steps)
    oss = set(oss)
    return {
        "w_jobs": jcount,
        "w_steps": scount,
        "w_oss": sorted(oss),
        "w_release": release
    }


def used_for_releases() -> bool:
    return False
