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

import json
from ast import Param
from pathlib import Path
from sys import prefix

import pandas as pd
import skfuzzy
from loguru import logger
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN, HDBSCAN
from sklearn.mixture import GaussianMixture

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
    logger.info(f"Running KMeans clustering for {dataset}...")
    frame = pd.read_csv(dataset)
    kmeans = KMeans(n_clusters=4, random_state=CLUSTERING_RANDOM_STATE)
    if Path(dataset).stem != "scores":
        kmeans.fit(frame.drop(columns=["repo"]))
    else:
        kmeans.fit(frame[["score"]])
    centroids = kmeans.cluster_centers_
    logger.info(f"Centroids: {centroids}")
    save_clustered(kmeans, frame, f"{dir}/{Path(dataset).stem}")


def agglomerative(dataset, dir):
    logger.info(f"Running Agglomerative clustering for {dataset}")
    frame = pd.read_csv(dataset)
    model = AgglomerativeClustering(n_clusters=3)
    model.fit(frame.drop(columns=["repo"]))
    save_clustered(model, frame, f"{dir}/{Path(dataset).stem}")


def dbscan(dataset, dir):
    logger.info(f"Running DBSCAN for {dataset}")
    frame = pd.read_csv(dataset)
    model = DBSCAN(eps=0.5, min_samples=5)
    model.fit(frame.drop(columns=["repo"]))
    save_clustered(model, frame, f"{dir}/{Path(dataset).stem}")


def hdbscan(dataset, dir):
    logger.info(f"Running HDBSCAN for {dataset}")
    frame = pd.read_csv(dataset)
    model = HDBSCAN(min_cluster_size=5)
    model.fit(frame.drop(columns=["repo"]))
    save_clustered(model, frame, f"{dir}/{Path(dataset).stem}")


def gmm(dataset, dir):
    logger.info(f"Running GMM for {dataset}")
    frame = pd.read_csv(dataset)
    model = GaussianMixture(n_components=4, covariance_type="full", random_state=0)
    drop = frame.drop(columns=["repo"])
    model.fit(drop)
    frame["cluster"] = model.predict(drop)
    prefix = f"{dir}/{Path(dataset).stem}"
    Path(f"{prefix}/clusters").mkdir(parents=True, exist_ok=True)
    save_config(prefix, json.dumps(model.get_params(), indent=4), ".json")
    to_txt(frame.groupby("cluster"), f"{prefix}/clusters")


def cmeans(dataset, dir):
    """
    Fuzzy C-Means clustering
    :param dataset: Dataset to cluster
    :param dir: Output directory
    """
    logger.info(f"Running Fuzzy C-Means for {dataset}")
    frame = pd.read_csv(dataset)
    centroids, u, u0, d, jm, p, fpc = skfuzzy.cmeans(
        frame.drop(columns=["repo"]).T,
        c=2,
        m=2.0,
        error=0.005,
        maxiter=1000,
        init=None
    )
    prefix = f"{dir}/{Path(dataset).stem}"
    Path(f"{prefix}/clusters").mkdir(parents=True, exist_ok=True)
    out = f"{prefix}/clusters/srs.csv"
    pd.DataFrame({"repo": frame["repo"], "srs": u[0]}).to_csv(
        out, index=False
    )
    logger.info(f"Saved results to {out}")


def save_clustered(model, frame, prefix):
    frame["cluster"] = model.labels_
    Path(f"{prefix}/clusters").mkdir(parents=True, exist_ok=True)
    save_config(prefix, json.dumps(model.get_params(), indent=4), ".json")
    to_txt(frame.groupby("cluster"), f"{prefix}/clusters")


def save_config(prefix, model, ext):
    full = f"{prefix}/config{ext}"
    with open(full, "w") as file:
        file.write(model)
    logger.info(f"Model settings saved to {full}")


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
    agglomerative(dataset, f"{dir}/agglomerative")
    hdbscan(dataset, f"{dir}/hdbscan")
    dbscan(dataset, f"{dir}/dbscan")
    gmm(dataset, f"{dir}/gmm")
    cmeans(dataset, f"{dir}/cmeans")
