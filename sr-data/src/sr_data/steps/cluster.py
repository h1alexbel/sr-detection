"""
Cluster.
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

from pathlib import Path

import pandas as pd
from loguru import logger
from sklearn.cluster import KMeans

"""
Clustering random state.
"""
CLUSTERING_RANDOM_STATE = 1


def kmeans(dataset, dir):
    """
    KMeans clustering.
    :param dataset: Dataset to cluster
    :param dir: Output directory
    """
    logger.info("Running KMeans clustering...")
    frame = pd.read_csv(dataset)
    kmeans = KMeans(n_clusters=8, random_state=CLUSTERING_RANDOM_STATE)
    kmeans.fit(frame[["score"]])
    centroids = kmeans.cluster_centers_
    logger.info(f"Centroids: {centroids}")
    frame["cluster"] = kmeans.labels_
    prefix = f"{dir}/{Path(dataset).stem}/clusters"
    Path(prefix).mkdir(parents=True, exist_ok=True)
    to_txt(frame.groupby("cluster"), prefix)


def to_txt(clusters, prefix):
    for label, members in clusters:
        full = f"{prefix}/{label}.txt"
        with open(full, "w") as file:
            for repo in members["repo"]:
                file.write(f"{repo}\n")
        logger.info(f"Cluster {label} members were saved to {label}.txt")


def main(dataset, dir):
    """
    Run clustering.
    :param dataset: Dataset to cluster
    :param dir: Output directory
    """
    kmeans(dataset, f"{dir}/kmeans")
