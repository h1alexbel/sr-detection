"""
Filter repositories without certain licenses.
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
import pandas as pd
from loguru import logger


def main(repos, out):
    frame = pd.read_csv(repos)
    licenses = ["mit", "apache-2.0", "0bsd"]
    before = len(frame)
    logger.info(f"Checking {before} repositories for licenses: {licenses}")
    frame["license"] = frame["license"].apply(lambda name: str(name).lower())
    frame = frame[frame["license"].isin(licenses)]
    logger.info(
        f"Filtered out {before - len(frame)} repositories without proper license"
    )
    frame.to_csv(out, index=False)
    logger.info(f"Saved {len(frame)} repositories with proper license to {out}")

