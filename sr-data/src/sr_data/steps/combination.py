"""
Combination of two datasets.
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

import pandas as pd
from loguru import logger


def main(scores, embeddings, dir, identifier):
    """
    Combination of datasets.
    :param scores: Dataset with SR-score
    :param embeddings: Dataset with embeddings
    :param dir: Output directory
    :param identifier Dataset identifier
    :return:
    """
    logger.info(f"Combining {scores} + {embeddings}")
    out = (
        f"{dir}/{identifier}-{os.path.splitext(os.path.basename(scores))[0]}"
        f"+{os.path.splitext(os.path.basename(embeddings))[0]}.csv"
    )
    pd.merge(
        pd.read_csv(scores), pd.read_csv(embeddings), on="repo"
    ).to_csv(
        out,
        index=False
    )
    logger.info(f"Output dataset saved to {out}")
