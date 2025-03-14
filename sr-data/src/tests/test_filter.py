"""
Test case for filter.
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
from sr_data.steps.filter import main
import pytest


class TestFilter(unittest.TestCase):

    @pytest.mark.fast
    def test_filters_input(self):
        """
        Test case for filtering input.
        """
        with TemporaryDirectory() as temp:
            path = os.path.join(temp, "after-filter.csv")
            filtered = os.path.join(temp, "filtered.txt")
            # pylint: disable=redefined-builtin
            main(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "resources/to-filter.csv"
                ),
                path,
                filtered
            )
            out = pd.read_csv(path)["repo"].values.tolist()
            expected = ["blitz-js/blitz", "wasp-lang/wasp"]
            self.assertEqual(
                out,
                expected,
                f"Output CSV {out} does not match with expected {expected}"
            )
            self.assertTrue(
                os.path.exists(filtered),
                f"File {filtered} does not exist, but it should be"
            )
