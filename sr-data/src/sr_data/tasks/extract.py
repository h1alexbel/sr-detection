"""
Extract README headings (#).
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
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords


def main(repos, out):
    nltk.download("stopwords")
    nltk.download("wordnet")
    print("Extracting headings from README files...")
    frame = pd.read_csv(repos)
    frame["headings"] = frame["readme"].apply(headings)
    before = len(frame)
    frame = frame.dropna(subset=["headings"])
    print(f"Removed {before - len(frame)} repositories that don't have at least one heading (#)")
    frame["headings"] = frame["headings"].apply(
        lambda readme: remove_stop_words(readme, stopwords.words("english"))
    )
    frame["lem_headings"] = frame["headings"].apply(lemmatize)
    frame.to_csv(out, index=False)


# https://stackoverflow.com/questions/61987040/how-to-lemmatise-a-dataframe-column-python
def lemmatize(headings):
    lemmatized = []
    lemmatizer = WordNetLemmatizer()
    tokenizer = nltk.tokenize.WhitespaceTokenizer()
    s = [lemmatizer.lemmatize(w) for w in tokenizer.tokenize(" ".join(headings).lower())]
    # for head in headings:
    #     lemmatized.append([lemmatizer.lemmatize(w) for w in tokenizer.tokenize(head)])
    return s


def remove_stop_words(headings, words):
    clean = []
    for head in headings:
        clean.append(
            ' '.join([word for word in head.split() if word not in words])
        )
    return clean


def headings(readme):
    pattern = re.compile("(#+\\s.+)")
    result = None
    hashless = []
    for match in pattern.findall(readme):
        hashless.append(match.replace("#", "").strip())
    if len(hashless) != 0:
        result = hashless
    return result
