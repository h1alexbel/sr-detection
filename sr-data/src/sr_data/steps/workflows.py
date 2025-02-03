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
    frame["workflows"] = frame["workflows"].fillna(0)
    for idx, row in frame.iterrows():
        repo = row["repo"]
        branch = row["branch"]
        workflows = row["workflows"]
        infos = []
        ymls = []
        if workflows and not isinstance(workflows, float):
            ymls = [
                file
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
        releases = False
        for info in infos:
            tjobs += info["w_jobs"]
            steps += info["w_steps"]
            for os in info["w_oss"]:
                oss.append(os)
            if info["w_release"]:
                releases = True
        frame.at[idx, "has_workflows"] = 1 if len(ymls) > 1 else 0
        frame.at[idx, "workflows"] = len(ymls)
        frame["workflows"] = frame["workflows"]
        frame.at[idx, "w_jobs"] = tjobs
        frame.at[idx, "w_oss"] = len(set(oss))
        frame.at[idx, "w_steps"] = steps
        frame.at[idx, "has_release_workflow"] = int(releases)
        frame.at[idx, "w_simplicity"] = w_score(frame.loc[idx])
    frame.to_csv(out, index=False)
    logger.info(f"Saved {len(frame)} repositories with workflows to {out}")

wscope = ["workflows", "w_jobs", "w_oss", "w_steps", "has_release_workflow"]
weights = {
    "workflows": 0.3,
    "w_jobs": 0.25,
    "w_steps": 0.25,
    "w_oss": 0.1,
    "has_release_workflow": 0.1,
}

def w_score(row) -> int:
    """
    Workflow simplicity score.
    :return: Calculated metric for workflow simplicity score.
    @todo #244:35min Enhance workflow simplicity score with min and max adjustment.
     Currently, we just subtract collected value from 1. We should adjust it with
     min and max values from the dataset. So formula should look like:
     1 - (row - min) / (max - min).
    """
    normalized = {
        "workflows": 1 - row["workflows"],
        "w_jobs": 1 - row["w_jobs"],
        "w_steps": 1 - row["w_steps"],
        "w_oss": 1 - row["w_oss"],
        "has_release_workflow": 1 - row["has_release_workflow"],
    }
    return sum(normalized[key] * weights[key] for key in weights)


def fetch(path) -> str:
    return requests.get(f"https://raw.githubusercontent.com/{path}").text


def workflow_info(content):
    yml = yaml.safe_load(
        '\n'.join(line for line in content.splitlines() if not line.strip().startswith('#')).strip()
    )
    jcount = 0
    scount = 0
    oss = []
    w_release = False
    if yml is not None:
        jobs = yml["jobs"].items()
        jcount = len(jobs)
        oss = []
        scount = 0
        for job, jdetails in jobs:
            runs = jdetails.get("runs-on")
            if runs is not None and not isinstance(runs, dict):
                if isinstance(runs, list):
                    for r in runs:
                        oss.append(r)
                if not isinstance(runs, list) and runs.startswith("$"):
                    if jdetails.get("strategy"):
                        matrix = jdetails.get("strategy").get("matrix")
                        if matrix is not None:
                            if isinstance(matrix, str):
                                oss.append(runs)
                            else:
                                keys = [
                                    key.strip() for key in
                                    runs.strip().replace("${{", "").replace("}}", "")
                                    .split(".")[1:]
                                ]
                                if len(keys) == 1:
                                    if matrix.get(keys[0]):
                                        for matrixed in matrix.get(keys[0]):
                                            if isinstance(matrixed, list):
                                                for r in matrixed:
                                                    oss.append(r)
                                            else:
                                                oss.append(matrixed)
                                elif len(keys) > 1:
                                    for system in dot_values(keys, matrix):
                                        oss.append(system)
                                elif matrix.get("include"):
                                    for include in matrix.get("include"):
                                        oss.append(
                                            include.get(
                                                runs.strip()
                                                .replace("${{", "")
                                                .replace("}}", "")
                                                .split(".")[1].strip()
                                            )
                                        )
                elif not isinstance(runs, list):
                    oss.append(runs)
            elif isinstance(runs, dict):
                if runs.get("group"):
                    oss.append(runs.get("group"))
            elif runs is not None:
                oss.append(runs)
            steps = jdetails.get("steps")
            if steps is not None:
                scount = len(steps)
        oss = set(oss)
        w_release = used_for_releases(yml)
    return {
        "w_jobs": jcount,
        "w_steps": scount,
        "w_oss": sorted(oss),
        "w_release": w_release
    }


def dot_values(keys, matrix) -> list:
    result = []
    current = matrix
    for i, k in enumerate(keys):
        if isinstance(current, dict):
            if k in current:
                current = current[k]
            else:
                return []
        elif isinstance(current, list):
            if i == len(keys) - 1:
                for item in current:
                    if isinstance(item, dict) and k in item:
                        system = item.get(k)
                        if system:
                            extra = [key for key in item if key != k]
                            suffix = "@" + "".join(
                                str(item.get(d, "")) for d in extra
                            )
                            result.append(system + suffix)
            else:
                for item in current:
                    if isinstance(item, dict) and k in item:
                        current = item[k]
        else:
            return []
    return result


def used_for_releases(yml) -> bool:
    result = False
    if "on" in list(yml.keys()):
        on = yml["on"]
    else:
        on = yml[True]
    if on and not isinstance(on, str) and not isinstance(on, list):
        if on.get("release"):
            for type in on.get("release").get("types"):
                if type == "published":
                    result = True
        elif on.get("push"):
            if on.get("push").get("tags"):
                if len(on.get("push").get("tags")) >= 1:
                    result = True
    return result
