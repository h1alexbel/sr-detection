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
from sr_data.steps.combination import main
import pytest


class TestCombination(unittest.TestCase):

    @pytest.mark.fast
    def test_combines_into_dataset(self):
        with TemporaryDirectory() as temp:
            main(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "resources/scores.csv"
                ),
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "resources/embeddings.csv"
                ),
                temp,
                "1"
            )
            out = os.path.join(temp, "d1-scores+embeddings.csv")
            combination = pd.read_csv(out)
            cols = 5
            self.assertEqual(
                len(combination.columns.tolist()),
                cols,
                f"Number of columns should be {cols}"
            )
