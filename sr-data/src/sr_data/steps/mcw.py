"""
Collection of most common words in README.
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
from collections import Counter

import pandas as pd
from loguru import logger
from markdown_it import MarkdownIt
from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords
from sr_data.steps.extract import wordnet_pos, filter


# @todo #137:35min Resolve code duplication in preprocessing methods.
#  Ideally, we should reuse `remove_stop_words`, `lemmatize` methods from
#  extract.py step. Now we are duplicating logic, only slightly changing it to
#  fit the input, will be more traceable to reuse existing methods located in
#  extract.py.
def main(repos, out):
    frame = pd.read_csv(repos)
    logger.info(f"Collecting MCW from {len(frame)} repositories...")
    frame["words"] = frame["readme"].apply(
        lambda readme: to_words(readme, MarkdownIt())
    )
    frame["words"] = frame["words"].apply(
        lambda words: remove_stop_words(words, stopwords.words("english"))
    )
    frame["words"] = frame["words"].apply(lemmatize)
    rword = r"^[a-zA-Z]+$"
    frame["words"] = frame["words"].apply(
        lambda words: filter(words, rword)
    )
    before = len(frame)
    frame = frame[frame["words"].apply(bool)]
    logger.info(
        f"Filtered out {before - len(frame)} repositories that have 0 words after regex filtering ('{rword}')"
    )
    frame["readme_mcw"] = frame["words"].apply(most_common)
    frame.to_csv(out, index=False)
    logger.info(f"Saved {len(frame)} repositories with MCW to {out}")


def to_words(readme, mit):
    tokens = mit.parse(readme)
    skip = {
        "code_block",
        "fence",
        "table_open",
        "table_close",
        "link_open",
        "link_close"
    }
    text = []
    for tkn in tokens:
        if tkn.type == "inline":
            for child in tkn.children:
                if child.type == "text":
                    text.append(child.content)
        elif tkn.type not in skip and tkn.type.endswith("_open"):
            text.append(tkn.content)
    return word_tokenize(" ".join(text))


def remove_stop_words(words, stopwords):
    return [word for word in words if word.lower() not in stopwords]


def lemmatize(words):
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(" ".join(words))
    return [
        lemmatizer.lemmatize(word.lower(), wordnet_pos(word))
        for word in tokens
    ]


def most_common(text):
    words = word_tokenize(" ".join(text))
    return [word for word, _ in Counter(words).most_common(5)]
