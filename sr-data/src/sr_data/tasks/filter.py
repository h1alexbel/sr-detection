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
from langdetect import DetectorFactory, LangDetectException
from langdetect import detect


def main(csv, out):
    """
    Filter.
    :param csv: CSV filename
    :param out: Output CSV file name
    :return: Filtered CSV
    """
    print("Start filtering...")
    DetectorFactory.seed = 0
    frame = pd.read_csv(csv)
    start = len(frame)
    print(f"Repositories in {start}")
    frame = frame.dropna(subset=["readme"])
    non_null = start - len(frame)
    after_null = len(frame)
    print(f"Skipped {non_null} repositories with NULL READMEs")
    frame["readme"] = frame["readme"].apply(md_to_text)
    frame = frame[frame["readme"].apply(english)]
    non_english = after_null - len(frame)
    print(f"Skipped {non_english} non-english repositories")
    print(f"Total skipped: {non_null + non_english}")
    print(f"Staying with {len(frame)} good repositories")
    print(frame)
    frame.to_csv(out, index=False)


def md_to_text(input):
    """
    Markdown to plain text.
    :param input: Markdown string
    :return: Text representation
    """
    try:
        result = BeautifulSoup(
            markdown.markdown(input), "html.parser"
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
        result = detect(text) == 'en'
    except Exception:
        result = False
    return result
