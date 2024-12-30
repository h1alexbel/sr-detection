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
from collections import Counter

import nltk
import pandas as pd
from loguru import logger
from nltk import WordNetLemmatizer, word_tokenize
from nltk.corpus import stopwords, wordnet

nltk.download("stopwords")
nltk.download("wordnet")
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('omw-1.4')
lemmatizer = WordNetLemmatizer()


def main(repos, out):
    logger.info("Extracting headings from README files...")
    frame = pd.read_csv(repos)
    frame["headings"] = frame["readme"].apply(headings)
    before = len(frame)
    frame = frame.dropna(subset=["headings"])
    headingless = len(frame)
    logger.info(f"Filtered out {before - headingless} repositories that don't have at least one heading (#)")
    frame["readme_hcount"] = frame["headings"].apply(readme_hcount)
    frame["headings"] = frame["headings"].apply(
        lambda readme: remove_stop_words(readme, stopwords.words("english"))
    )
    frame["headings"] = frame["headings"].apply(
        lambda headings: [lemmatize(heading) for heading in headings]
    )
    rword = r"^[a-zA-Z]+$"
    frame["headings"] = frame["headings"].apply(
        lambda headings: filter(headings, rword)
    )
    frame = frame.dropna(subset=["headings"])
    if len(frame) > 0:
        frame = frame[frame["headings"].apply(bool)]
    logger.info(
        f"Filtered out {headingless - len(frame)} repositories that have 0 headings after regex filtering ('{rword}')"
    )
    if "headings" in frame.columns:
        frame["mcw"] = frame["headings"].apply(
            lambda headings: top_words(headings, 5)
        )
    frame.to_csv(out, index=False)
    logger.info(f"Saved {len(frame)} repositories with extracted headings to {out}")


def readme_hcount(headings):
    return len(headings)


def top_words(headings, amount):
    """
    Calculate top words in headings
    :param headings: README headings
    :param amount: Amount of top words to find
    :return: Array of top words
    """
    words = [word for heading in headings for word in word_tokenize(heading)]
    return [word for word, _ in Counter(words).most_common(amount)]


def filter(headings, regex):
    """
    Filter headings
    :param headings: README headings
    :param regex: Regex
    :return: Filtered headings
    """
    words = [word for heading in headings for word in word_tokenize(heading)]
    return [word for word in words if re.match(regex, word)]


def lemmatize(heading):
    """
    Lemmatize heading.
    :param heading: README heading
    :return: Lemmatized README heading
    """
    tokens = word_tokenize(heading)
    tags = nltk.pos_tag(tokens)
    return " ".join(
        [lemmatizer.lemmatize(token.lower(), wordnet_pos(tag)) for token, tag in tags]
    )


def wordnet_pos(tag):
    """
    NLTK POS tag to WordNet POS tag
    :param tag: NLTK POS tag
    :return: WordNet POS tag
    """
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


def remove_stop_words(headings, words):
    """
    Remove stop words
    :param headings: Headings
    :param words: Stop words
    :return: Headings without stop words
    """
    clean = []
    for head in headings:
        clean.append(
            ' '.join([word for word in head.split() if word not in words])
        )
    return clean


def headings(readme):
    """
    Extract all headings
    :param readme: README content
    :return: All README headings
    """
    pattern = re.compile("(#+\\s.+)")
    result = None
    hashless = []
    for match in pattern.findall(readme):
        hashless.append(match.replace("#", "").strip())
    if len(hashless) != 0:
        result = hashless
    return result
