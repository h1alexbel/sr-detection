import pandas as pd
from loguru import logger


def main(repos, out):
    frame = pd.read_csv(repos)
    frame["workflows"] = frame["workflows"].fillna("")
    for idx, row in frame.iterrows():
        repo = row["repo"]
        branch = row["branch"]
        workflows = row["workflows"]
        if workflows and not isinstance(workflows, float):
            ymls = [
                file.strip()
                for file in workflows.split(",")
                if file.endswith((".yml", ".yaml"))
            ]
            logger.info(f"Repo {repo} has {len(ymls)} *.yml|*.yaml workflows inside .github/workflows")
            for yml in ymls:
                workflow_info(f"{repo}/{branch}/.github/workflows/{yml}")


def workflow_info(path):
    return ""
