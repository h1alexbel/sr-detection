"""
Count of special words in README.
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


def main(repos, out, config):
    frame = pd.read_csv(repos)
    with open(config) as file:
        for line in file:
            word = line.strip()
            stat = f"readme_{word}_count"
            frame[stat] = frame.apply(
                lambda row: word_count(row["repo"], word, row["readme"]),
                axis=1
            )
    frame.to_csv(out, index=False)
    logger.info(f"Saved output to {out}")


def word_count(repo, word, txt) -> int:
    first = word[0]
    regex = fr"[{first.upper()}-{first.lower()}]{word[1:]}"
    pattern = re.compile(regex)
    matches = len(pattern.findall(txt))
    logger.info(f"Repo {repo} contains {matches} '{regex}' words")
    return matches
