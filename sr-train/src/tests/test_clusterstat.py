"""
Tests for statistics generation.
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

import pytest
from models.cluster import dbscan
from models.clusterstat import main


class TestClusterstat(unittest.TestCase):

    @pytest.mark.fast
    # @todo #240:30min Add test case when clusters are not empty.
    #  We should add one more test case when clustering model generates clusters.
    #  To do so, we need to prepare a bigger dataset for model in order to find
    #  useful centroids and distributed entries close to them.
    def test_generates_report(self):
        with TemporaryDirectory() as temp:
            dbscan(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "resources/to-cluster.csv"
                ),
                temp
            )
            results = os.path.join(temp, "results.txt")
            main(temp, results)
            with open(results, "r") as r:
                content = r.readlines()
            self.assertEqual(
                content,
        ["to-cluster -> clusters: 0 clusters ()\n"]
            )
