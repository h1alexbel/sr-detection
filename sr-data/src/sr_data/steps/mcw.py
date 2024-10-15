"""
Collection of most common words in README.
"""
from collections import Counter

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
from markdown_it import MarkdownIt
from nltk import word_tokenize


def main(repos, out):
    logger.info("Collecting most common words...")
    frame = pd.read_csv(repos)
    frame["rtext"] = frame["readme"].apply(
        lambda readme: to_rtext(readme, MarkdownIt())
    )
    frame["mcw"] = frame["rtext"].apply(most_common)
    frame.to_csv(out, index=False)
    logger.info(f"Saved output to {out}")


# ['the', '.', 'with', ':', 'Keycloak']
# remove stop words
# lemmatize
def to_rtext(readme, mit):
    tokens = mit.parse(readme)
    skip = {"code_block", "fence", "table_open", "table_close", "link_open", "link_close"}
    text = []
    for tkn in tokens:
        if tkn.type == "inline":
            for child in tkn.children:
                if child.type == "text":
                    text.append(child.content)
        elif tkn.type not in skip and tkn.type.endswith("_open"):
            text.append(tkn.content)
    return " ".join(text).strip()


def most_common(text):
    words = word_tokenize(text)
    return [word for word, _ in Counter(words).most_common(5)]
