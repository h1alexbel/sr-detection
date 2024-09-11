"""
Test case for embed.
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
from pathlib import Path

import pandas as pd
from sr_data.steps.embed import infer, main


class TestEmbed(unittest.TestCase):
    """
    Test cases for embed.
    """

    def test_returns_embeddings(self):
        """
        Test case for returning embeddings for text.
        """
        embeddings = infer(
            ["some dummy text"],
            "sentence-transformers/all-MiniLM-L6-v2",
            os.environ["HF_TESTING_TOKEN"]
        )
        frame = pd.DataFrame(embeddings)
        columns = len(frame.columns)
        cexpected = 384
        rows = len(frame)
        rexpected = 1
        self.assertEqual(
            rows,
            rexpected,
            f"Generated embeddings rows count {rows} does not match with"
            f" expected {rexpected}"
        )
        self.assertEqual(
            columns,
            cexpected,
            f"Generated embeddings columns count {columns} does not match with"
            f" expected {cexpected}"
        )

    def test_returns_e5_embeddings(self):
        embeddings = infer(
            ["some dummy text"],
            "intfloat/e5-large",
            os.environ["HF_TESTING_TOKEN"]
        )
        frame = pd.DataFrame(embeddings)
        columns = len(frame.columns)
        cexpected = 1024
        rows = len(frame)
        rexpected = 1
        self.assertEqual(
            rows,
            rexpected,
            f"Generated embeddings rows count {rows} does not match with"
            f" expected {rexpected}"
        )
        self.assertEqual(
            columns,
            cexpected,
            f"Generated embeddings columns count {columns} does not match with"
            f" expected {cexpected}"
        )

    # @todo #9:30min Use ExtendsWith analogue or some temp directory for 'out'.
    #  We shouldn't manage removal of output files directly, instead, let's use
    #  more elegant solution - temp directory or something like extensions from
    #  JUnit. We should fix the same problem in test_filter.py as well.
    def test_creates_csv_with_embeddings(self):
        """
        Test case for checking generated CSV file with embeddings.
        """
        main(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "embed.csv"
            ),
            "t-embeddings",
            os.environ["HF_TESTING_TOKEN"],
            os.environ["COHERE_TESTING_TOKEN"]
        )
        e5 = "t-embeddings-e5-1024.csv"
        sbert = "t-embeddings-s-bert-384.csv"
        cohere = "t-embeddings-embedv3-1024.csv"
        self.assertTrue(Path(e5).is_file())
        self.assertTrue(Path(sbert).is_file())
        self.assertTrue(Path(cohere).is_file())
        os.remove(e5)
        os.remove(sbert)
        os.remove(cohere)
