"""
Filter repositories.
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
import markdown
import pandas as pd
from bs4 import BeautifulSoup, ParserRejectedMarkup
from langdetect import DetectorFactory, LangDetectException, detect_langs
from loguru import logger
from sr_data.filtered import filtered


def main(repos, out, rm):
    """
    Filter.
    :param repos: CSV with repositories
    :param out: Output CSV file name
    :return: Filtered CSV
    """
    logger.info("Start filtering...")
    DetectorFactory.seed = 0
    frame = pd.read_csv(repos)
    start = len(frame)
    logger.info(f"Repositories to filter: {start}")
    dnull = frame[frame["readme"].isnull()]
    frame = frame.dropna(subset=["readme"])
    non_null = start - len(frame)
    after_null = len(frame)
    logger.info(f"Filtered out {non_null} repositories with empty README files")
    frame["readme_text"] = frame["readme"].apply(md_to_text)
    deng = frame[~frame["readme_text"].apply(english)]
    frame = frame[frame["readme_text"].apply(english)]
    frame = frame.drop(columns=["readme_text"])
    non_english = after_null - len(frame)
    logger.info(f"Filtered out {non_english} non-english repositories")
    with open(rm, "w") as f:
        filtered(f, dnull["repo"].tolist(), "filter-null-readme")
        filtered(f, deng["repo"].tolist(), "filter-non-english")
    logger.info(f"Total filtered: {non_null + non_english}")
    frame.to_csv(out, index=False)
    logger.info(f"Saved {len(frame)} good repositories to {out}")


def md_to_text(text):
    """
    Markdown to plain text.
    :param text: Markdown string
    :return: Text representation
    """
    try:
        result = BeautifulSoup(
            markdown.markdown(text), "html.parser"
        ).get_text(
            separator=' ',
            strip=True
        )
    except ParserRejectedMarkup:
        result = None
    return result


def english(text):
    """
    Skips non-english text.
    """
    try:
        langs = detect_langs(text)
        result = len(langs) == 1 and langs[0].lang == "en"
    except (LangDetectException, TypeError):
        result = False
    return result
