"""
Merge dataset folders into one.
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
import os.path
from io import StringIO

import pandas as pd
import requests
from loguru import logger

DATASETS = [
    "d1-scores.csv",
    "d2-sbert.csv",
    "d3-e5.csv",
    "d4-embedv3.csv",
    "d5-scores+sbert.csv",
    "d6-scores+e5.csv",
    "d7-scores+embedv3.csv"
]


def main(datasets, out):
    logger.info("Start merging...")
    logger.info(f"Folders={datasets}")
    candidates = {}
    for folder in datasets.split(","):
        candidates[folder] = contents(folder)
    merged = merge(candidates)
    for file, df in merged.items():
        path = os.path.join(out, file)
        df.to_csv(path, index=False)
        logger.info(f"Saved merged file '{file}' to {path}")


def merge(candidates):
    merged = {}
    for file in DATASETS:
        combined = []
        for folder, files in candidates.items():
            if file in files:
                df = files[file]
                combined.append(df)
        if combined:
            merged[file] = pd.concat(combined, ignore_index=True)
            logger.info(f"Merged file: {file} ({len(merged[file])} rows)")
    return merged


def contents(folder):
    result = {}
    for file in DATASETS:
        content = requests.get(
            f"https://raw.githubusercontent.com/h1alexbel/sr-detection/refs/heads/gh-pages/{folder}/{file}"
        ).text
        result[file] = pd.read_csv(StringIO(content), sep=",")
        logger.info(f"Fetched {folder}/{file} ({len(result[file])} rows)")
    return result
