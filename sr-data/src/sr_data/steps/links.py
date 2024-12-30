"""
Links count in READMEs.
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
    logger.info(f"Counting links in {len(frame)} repositories...")
    frame["readme_links"] = frame["readme"].apply(links)
    frame["readme_links_count"] = frame["readme_links"].apply(len)
    frame.to_csv(out, index=False)
    logger.info(f"Saved {len(frame)} repositories with links to {out}")


def links(readme):
    found = []
    http = re.findall(r"\[(.*?)]\((http[s]?://.*?)\)", readme)
    for text, url in http:
        if url:
            found.append(f"{text} -> {url}")
    aliased = re.findall(r"\[(.+?)](?:\[\s*(.*?)\s*]|(?!\s*\(.*?\)))", readme)
    for text, alias in aliased:
        if re.match(r"^(?![0-9]+$)[\w\s]+$", text):
            if alias:
                found.append(f"{text} -> {alias}")
            else:
                found.append(text)
    return found
