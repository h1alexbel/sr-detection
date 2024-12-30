"""
Calculate length metrics for READMEs.
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

import nltk
import pandas as pd
from loguru import logger


def main(repos, out):
    frame = pd.read_csv(repos)
    logger.info(
        f"Calculating `rlen`, `avg_slen`, `avg_wlen` for {len(frame)} repositories"
    )
    frame["readme_len"] = frame["readme"].apply(rlen)
    frame["readme_avg_slen"] = frame["readme"].apply(avg_slen)
    frame["readme_avg_wlen"] = frame["readme"].apply(avg_wlen)
    frame.to_csv(out, index=False)
    logger.info(f"Saved {len(frame)} repositories with length metrics to {out}")


def rlen(readme):
    return len(readme)


def avg_slen(readme):
    sentences = nltk.sent_tokenize(readme)
    total = sum(len(re.findall(r'\w+', sentence)) for sentence in sentences)
    result = 0
    if sentences:
        result = total / len(sentences)
    return result


def avg_wlen(readme):
    words = re.findall(r'\w+', readme)
    total = sum(len(word) for word in words)
    result = 0
    if words:
        result = total / len(words)
    return result
