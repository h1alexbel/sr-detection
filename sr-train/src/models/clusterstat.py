"""
Statistics about generated clusters.
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
import os

from loguru import logger


def main(dir, out):
    logger.info(f"Inspecting dir '{dir}'")
    facts = []
    for model in os.listdir(dir):
        if model in ["kmeans", "agglomerative", "dbscan", "gmm"]:
            deep = f"{dir}/{model}"
            if os.path.isdir(deep):
                clusters = []
                noisy = None
                for dataset in os.listdir(deep):
                    if dataset in ["d1-scores", "d2-sbert", "d5-scores+sbert"]:
                        result = f"{dir}/{model}/{dataset}/clusters"
                        if os.path.isdir(result):
                            for cluster in os.listdir(result):
                                path = f"{result}/{cluster}"
                                if os.path.isfile(path):
                                    with open(path, "r") as c:
                                        count = sum(1 for _ in c)
                                        if not cluster == "-1.txt":
                                            clusters.append(count)
                                        else:
                                            noisy = count
                    lines = ", ".join(map(str, clusters))
                    fact = f"{model} -> {dataset}: {len(clusters)} clusters ({lines})"
                    if noisy:
                        fact += f" , +{noisy} noisy repos"
                    facts.append(fact)
    with open(out, "w") as r:
        for fact in facts:
            r.write(fact + "\n")
