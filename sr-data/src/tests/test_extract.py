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
import unittest

from nltk.corpus import stopwords
from sr_data.tasks.extract import headings, remove_stop_words


class TestExtract(unittest.TestCase):

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

    def test_removes_stop_words(self):
        self.assertEqual(
            remove_stop_words(["to", "it", "contribute"], stopwords.words("english")),
            ["", "", "contribute"],
            "Stop words was not removed"
        )
