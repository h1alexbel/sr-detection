"""
Tests for special words count in README.
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
from tempfile import TemporaryDirectory, TemporaryFile

import pandas as pd
import pytest
from sr_data.steps.swc import word_count, main


class TestSwc(unittest.TestCase):

    @pytest.mark.fast
    def test_counts_example_word(self):
        count = word_count(
            "foo/bar", "example", "This is test Example. Example is good, examples are good. Examples are awesome"
        )
        expected = 4
        self.assertEqual(
            count,
            expected,
            f"Found 'example' word count: {count} does not matches with expected: {expected}"
        )

    @pytest.mark.fast
    def test_saves_counts(self):
        with TemporaryDirectory() as temp:
            path = os.path.join(temp, "swc.csv")
            config = os.path.join(temp, "swc-config.txt")
            with open(config, "w") as f:
                f.write("example\n")
                f.write("sample\n")
                f.write("demo\n")
            main(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "to-swc.csv"
                ),
                path,
                config
            )
            out = pd.read_csv(path)
            self.assertEqual(out.iloc[0]["example_wc"], 4)
            self.assertEqual(out.iloc[0]["sample_wc"], 0)
            self.assertEqual(out.iloc[0]["demo_wc"], 14)
