import pandas as pd
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
                workflow_info(f"{repo}/{branch}/.github/workflows/{yml}")
            )
        frame.at[idx, "workflows"] = infos
    frame.to_csv(out, index=False)
    logger.info(f"Saved repositories to {out}")


def workflow_info(path):
    return path
