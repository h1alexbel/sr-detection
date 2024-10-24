"""
Tests for snippets.
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
from sr_data.steps.snippets import snippets, main


class TestSnippets(unittest.TestCase):

    @pytest.mark.fast
    def test_counts_snippets(self):
        count = snippets("""
        # test
        ```bash
        sh test1.sh
        ```
        
        ```bash
        sh test2.sh
        ```
        
        ```bash
        sh test3.sh
        ```
        """)
        expected = 3
        self.assertEqual(
            count,
            expected,
            f"Found {count} snippets, but it does not match with expected: {expected}"
        )

    @pytest.mark.fast
    def test_returns_zero_for_no_snippets(self):
        self.assertEqual(
            snippets("no snippets"),
            0,
            "Found snippets should be equal to zero, but it was not"
        )

    @pytest.mark.fast
    def test_counts_snippets_for_all(self):
        with TemporaryDirectory() as temp:
            path = os.path.join(temp, "snippets.csv")
            main(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "resources/to-snippets.csv"
                ),
                path
            )
            frame = pd.read_csv(path)
            self.assertEqual(frame.iloc[0]["snippets"], 0)
            self.assertEqual(frame.iloc[1]["snippets"], 16)
