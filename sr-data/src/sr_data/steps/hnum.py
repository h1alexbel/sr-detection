import pandas as pd
from loguru import logger


def main(repos, out):
    frame = pd.read_csv(repos)
    logger.info(f"Calculating `hnum` for {len(frame)} repositories")
