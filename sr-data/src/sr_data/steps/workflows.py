import pandas as pd


def main(repos, out):
    frame = pd.read_csv(repos)
    frame["workflows"] = frame["workflows"].fillna("")
    for idx, row in frame.iterrows():
        repo = row["repo"]
        branch = row["branch"]
        workflows = row["workflows"]
        if workflows and not isinstance(workflows, float):
            for file in workflows.split(","):
                if file.endswith((".yml", ".yaml")):
                    workflow_info(f"{repo}/{branch}/.github/workflows/{file}")


def workflow_info(path):
    return ""
