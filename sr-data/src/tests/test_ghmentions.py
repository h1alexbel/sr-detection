"""
Tests for gh_mentions.
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
from sr_data.steps.gh_mentions import mentions, main


class TestGhMentions(unittest.TestCase):

    @pytest.mark.fast
    def test_returns_github_pull_mentions(self):
        github = mentions("Link to pull: https://github.com/foo/bar/pull/123")
        expected = (1, 0)
        self.assertEqual(
            github,
            expected,
            f"Found mentions: {github} don't match with expected: {expected}"
        )

    @pytest.mark.fast
    def test_returns_github_issue_mentions(self):
        github = mentions("Link to issue: https://github.com/foo/bar/issues/1")
        expected = (0, 1)
        self.assertEqual(
            github,
            expected,
            f"Found mentions: {github} don't match with expected: {expected}"
        )

    @pytest.mark.fast
    def test_returns_github_mentions(self):
        github = mentions(
            "Some links: https://github.com/foo/bar/pull/123, https://github.com/foo/bar/issues/1"
        )
        expected = (1, 1)
        self.assertEqual(
            github,
            expected,
            f"Found mentions: {github} don't match with expected: {expected}"
        )

    @pytest.mark.fast
    def test_founds_mentions(self):
        with TemporaryDirectory() as temp:
            path = os.path.join(temp, "mentions.csv")
            main(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "resources/to-ghmentions.csv"
                ),
                path
            )
            frame = pd.read_csv(path)
            self.assertEqual(frame.iloc[0]["readme_imentions"], 1)
            self.assertEqual(frame.iloc[0]["readme_pmentions"], 1)
