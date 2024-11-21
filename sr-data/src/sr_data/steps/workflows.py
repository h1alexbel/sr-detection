import pandas as pd


def main(repos, out):
    frame = pd.read_csv(repos)
    for idx, row in frame.iterrows():
        repo = row["repo"]
        branch = row["branch"]
        workflows = row["workflows"]
        print(workflows)
        for file in workflows:
            workflow_info(f"{repo}/{branch}/.github/workflows/{file}")

def workflow_info(path):
    return ""
