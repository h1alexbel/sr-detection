"""
Tests for filtered.py.
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

import pytest
from sr_data.filtered import filtered


class TestFiltered(unittest.TestCase):

    @pytest.mark.fast
    def test_writes_filtered_repos(self):
        with TemporaryDirectory() as temp:
            path = os.path.join(temp, "filtered.txt")
            with open(path, "w") as f:
                filtered(f, ["jeff/foo", "jeff/bar"], "test")
            with open(path, "r") as f:
                self.assertEqual(
                    f.readlines(),
                    [
                        'Filtered out 2 repositories during (test):\n',
                        '\n',
                        'jeff/foo (test)\n',
                        'jeff/bar (test)\n',
                        '\n'
                    ],
                    f"Content in {filtered} does not match with expected"
                )
