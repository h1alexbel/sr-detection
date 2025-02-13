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
from sr_data.steps.scores import main


class TestScores(unittest.TestCase):

    @pytest.mark.fast
    def test_calculates_score(self):
        with TemporaryDirectory() as temp:
            path = os.path.join(temp, "scores.csv")
            main(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "resources/to-score.csv"
                ),
                path
            )
            scores = pd.read_csv(path)
            cols = 2
            self.assertEqual(
                len(scores.columns.tolist()),
                cols,
                f"Number of columns should be {cols}"
            )
            score = 102.5
            self.assertEqual(
                scores["score"].tolist()[0],
                score,
                f"SR score should be {score}"
            )
