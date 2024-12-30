"""
Tests for numerical.
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
from sr_data.steps.numerical import main


class TestNumerical(unittest.TestCase):

    @pytest.mark.fast
    def test_creates_csv_with_numerical(self):
        with TemporaryDirectory() as temp:
            path = os.path.join(temp, "numerical.csv")
            main(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "resources/to-numerical.csv"
                ),
                path
            )
            frame = pd.read_csv(path)
            self.assertTrue(
                all(
                    col in frame.columns for col in
                    [
                        "repo",
                        "releases",
                        "pulls",
                        "open_issues",
                        "branches",
                        "workflows",
                        "has_release_workflow",
                        "w_simplicity",
                        "tests"
                    ]
                ),
                f"Frame {frame.columns} doesn't have expected columns"
            )
            self.assertEqual(
                frame.iloc[0]["has_release_workflow"],
                0,
                "has_release_workflow doesn't match with expected"
            )
            self.assertEqual(
                frame.iloc[1]["has_release_workflow"],
                1,
                "has_release_workflow doesn't match with expected"
            )
