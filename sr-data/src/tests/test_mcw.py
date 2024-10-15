"""
Tests for collecting most common words.
"""
import os
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

import pytest
from markdown_it import MarkdownIt
from sr_data.steps.mcw import to_words


class TestMcw(unittest.TestCase):

    @pytest.mark.fast
    def test_transforms_readme_to_words(self):
        with open(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)), "to-words.md"
                ),
                "r"
        ) as readme:
            words = len(
                to_words(
                    readme.read(),
                    MarkdownIt()
                )
            )
            expected = 91
            self.assertEqual(
                words,
                expected,
                f"Parsed words size: {words} don't match with expected: {expected}"
            )
