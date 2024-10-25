"""
Tests for lens.
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
from sr_data.steps.lens import rlen, avg_slen, avg_wlen, main


class TestLens(unittest.TestCase):

    @pytest.mark.fast
    def test_calculates_rlen(self):
        length = rlen("This is test readme. Foo bar")
        expected = 28
        self.assertEqual(
            length,
            expected,
            f"Calculated rlen: {length} does not match with expected: {expected}"
        )

    @pytest.mark.fast
    def test_calculates_avg_slen(self):
        length = avg_slen(
            "This is another test readme. Very very long sentence. Short."
        )
        expected = 3.3333333333333335
        self.assertEqual(
            length,
            expected,
            f"Calculated avg_slen: {length} does not match with expected: {expected}"
        )

    @pytest.mark.fast
    def test_calculates_avg_wlen(self):
        length = avg_wlen("This is test readme for avg_wlen test.")
        expected = 4.428571428571429
        self.assertEqual(
            length,
            expected,
            f"Calculated avg_wlen: {length} does not match with expected: {expected}"
        )

    @pytest.mark.fast
    def test_calculates_all_lengths(self):
        with TemporaryDirectory() as temp:
            path = os.path.join(temp, "lens.csv")
            main(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "resources/to-lens.csv"
                ),
                path
            )
            frame = pd.read_csv(path)
            self.assertEqual(frame.iloc[0]["readme_len"], 2487)
            self.assertEqual(frame.iloc[0]["readme_avg_slen"], 24.666666666666668)
            self.assertEqual(frame.iloc[0]["readme_avg_wlen"], 5.1567567567567565)
