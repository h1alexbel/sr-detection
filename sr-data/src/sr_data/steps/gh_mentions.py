"""
Count of mentioning GitHub pull request or issue in READMEs.
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
import re

import pandas as pd
from loguru import logger


def main(repos, out):
    frame = pd.read_csv(repos)
    logger.info(
        f"Counting GitHub pull request, and issue mentions in {len(frame)} repositories..."
    )
    if frame.empty:
        frame["readme_pmentions"] = 0
        frame["readme_imentions"] = 0
    else:
        frame[["readme_pmentions", "readme_imentions"]] = (
            frame["readme"].apply(mentions)).apply(pd.Series)
    frame.to_csv(out, index=False)
    logger.info(f"Saved {len(frame)} repositories with issues/pull request mentions to {out}")


def mentions(readme) -> [int, int]:
    return (
        len(re.findall(r"https://github\.com/.+/pull/\d+", readme)),
        len(re.findall(r"https://github\.com/.+/issues/\d+", readme))
    )
