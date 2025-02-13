"""
Tests for links.
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
import os.path
import unittest
from tempfile import TemporaryDirectory

import pandas as pd
import pytest
from sr_data.steps.links import links, main


class TestLinks(unittest.TestCase):

    @pytest.mark.fast
    def test_counts_links(self):
        found = links(
            """
        [HTTP](http://test.com)
        [HTTPS](https://test.com)
        [Alias][here]
        [Inline]
        """
        )
        expected = [
            "HTTP -> http://test.com",
            "HTTPS -> https://test.com",
            "Alias -> here",
            "Inline"
        ]
        self.assertEqual(
            found,
            expected,
            f"Links: {found} does not match with expected: {expected}"
        )

    @pytest.mark.fast
    def test_skips_document_level_links(self):
        found = links(
            """
            [Good](https://good.link)
            [Anchor in the document](#here)
            [Heading in the document](/here)
            """
        )
        expected = ["Good -> https://good.link"]
        self.assertEqual(
            found,
            expected,
            f"Links: {found} do not match with expected: {expected}"
        )

    @pytest.mark.fast
    def test_counts_for_all(self):
        with TemporaryDirectory() as temp:
            path = os.path.join(temp, "links.csv")
            main(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "resources/to-links.csv"
                ),
                path
            )
            frame = pd.read_csv(path)
            self.assertEqual(
                frame.iloc[0]["readme_links"],
                "['Test', 'Test2 -> ref']"
            )
            self.assertEqual(
                frame.iloc[0]["readme_links_count"],
                2
            )
