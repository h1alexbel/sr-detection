"""
Tests for junit_tests.
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
from sr_data.steps.junit_tests import count_of_tests, main


class TestJunitTests(unittest.TestCase):

    @pytest.mark.nightly
    def test_returns_count(self):
        tests = count_of_tests(
            "eo-cqrs/eo-kafka",
            "master",
            os.environ["GH_TESTING_TOKEN"]
        )
        self.assertEqual(tests, 187)

    @pytest.mark.nightly
    def test_returns_zero_for_repo_without_tests(self):
        self.assertTrue(
            count_of_tests(
                "h1alexbel/h1alexbel",
                "master",
                os.environ["GH_TESTING_TOKEN"]
            ) == 0,
            "Tests count should be 0"
        )

    @pytest.mark.nightly
    def test_counts_junit_tests_in_csv(self):
        with TemporaryDirectory() as temp:
            path = os.path.join(temp, "tests.csv")
            main(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "resources/to-count-tests.csv"
                ),
                path,
                os.environ["GH_TESTING_TOKEN"]
            )
            frame = pd.read_csv(path)
            self.assertEqual(frame.iloc[0]["junit_tests"], 0)
            self.assertEqual(frame.iloc[1]["junit_tests"], 0)
