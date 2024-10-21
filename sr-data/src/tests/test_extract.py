"""
Test cases for extracting README headings (#).
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
import os
import unittest
from tempfile import TemporaryDirectory

import pandas as pd
import pytest
from nltk.corpus import stopwords
from sr_data.steps.extract import headings, remove_stop_words, lemmatize, filter, top_words, main


class TestExtract(unittest.TestCase):

    @pytest.mark.fast
    def test_extracts_headings(self):
        heads = headings(
            """
            # test repo
            This is some test repo.
            ...
            #### How to contribute
            """
        )
        expected = ["test repo", "How to contribute"]
        self.assertEqual(
            heads,
            expected,
            f"README headings extracted: {heads}, but do not match with expected: {expected}"
        )

    @pytest.mark.fast
    def test_removes_stop_words(self):
        self.assertEqual(
            remove_stop_words(["to", "it", "contribute"], stopwords.words("english")),
            ["", "", "contribute"],
            "Stop words was not removed"
        )

    @pytest.mark.fast
    def test_lemmatizes_heading(self):
        self.assertEqual(
            lemmatize("Getting Started"),
            "get start",
            "Heading was not lemmatized"
        )

    @pytest.mark.fast
    def test_filters(self):
        self.assertEqual(
            filter(
                ["get start", ";lt gt", ":;"],
                r"^[a-zA-Z]+$"
            ),
            ["get", "start", "lt", "gt"],
            "Headings were not filtered"
        )

    @pytest.mark.fast
    def test_finds_top_3(self):
        top = top_words(
            ["get", "start", "get", "http", "gt", "gt"],
            3
        )
        expected = ["get", "gt", "start"]
        self.assertEqual(
            top,
            expected,
            f"Top words found: {top}, but didn't match with expected: {expected}"
        )

    @pytest.mark.fast
    def test_filters_repo_with_empty_headings(self):
        with TemporaryDirectory() as temp:
            path = os.path.join(temp, "testing.csv")
            main(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)), "to-extract.csv"
                ),
                path
            )
            self.assertEqual(
                len(pd.read_csv(path)),
                1,
                "Should filter repo with empty headings"
            )

    @pytest.mark.fast
    def test_calculates_hnum_in_readme(self):
        with TemporaryDirectory() as temp:
            path = os.path.join(temp, "extracted.csv")
            main(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)), "to-extract-hnum.csv",
                ),
                path
            )
            frame = pd.read_csv(path)
            self.assertEqual(frame.iloc[0]["hnum"],3)
