"""
Test case for cluster step.
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
from sr_data.steps.cluster import kmeans, cmeans, agglomerative, dbscan, gmm, hdbscan


class TestCluster(unittest.TestCase):

    @pytest.mark.fast
    def test_clusters_kmeans_numerical(self):
        with TemporaryDirectory() as temp:
            kmeans(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)), "to-cluster.csv"
                ),
                temp
            )
            path = os.path.join(temp, "to-cluster")
            expected = f"{path}/clusters"
            self.assertTrue(
                os.path.exists(expected),
                f"Directory: {expected} does not exists"
            )
            config = f"{path}/config.json"
            self.assertTrue(
                os.path.exists(config),
                f"File {config} does not exists"
            )

    @pytest.mark.fast
    def test_clusters_with_cmeans(self):
        with TemporaryDirectory() as temp:
            cmeans(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)), "to-cluster.csv"
                ),
                temp
            )
            file = os.path.join(temp, "to-cluster/clusters/srs.csv")
            self.assertTrue(
                os.path.exists(file),
                f"C-Means results was not saved to {file}"
            )

    @pytest.mark.fast
    def test_clusters_with_agglomerative(self):
        with TemporaryDirectory() as temp:
            agglomerative(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)), "to-cluster.csv"
                ),
                temp
            )
            path = os.path.join(temp, "to-cluster")
            expected = f"{path}/clusters"
            self.assertTrue(
                os.path.exists(expected),
                f"Directory: {expected} does not exists"
            )
            config = f"{path}/config.json"
            self.assertTrue(
                os.path.exists(config),
                f"File {config} does not exists"
            )

    @pytest.mark.fast
    def test_clusters_with_dbscan(self):
        with TemporaryDirectory() as temp:
            dbscan(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)), "to-cluster.csv"
                ),
                temp
            )
            path = os.path.join(temp, "to-cluster")
            expected = f"{path}/clusters"
            self.assertTrue(
                os.path.exists(expected),
                f"Directory: {expected} does not exists"
            )
            config = f"{path}/config.json"
            self.assertTrue(
                os.path.exists(config),
                f"File {config} does not exists"
            )

    @pytest.mark.fast
    def test_clusters_with_gmm(self):
        with TemporaryDirectory() as temp:
            gmm(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)), "to-cluster.csv"
                ),
                temp
            )
            path = os.path.join(temp, "to-cluster")
            expected = f"{path}/clusters"
            self.assertTrue(
                os.path.exists(expected),
                f"Directory: {expected} does not exists"
            )
            config = f"{path}/config.json"
            self.assertTrue(
                os.path.exists(config),
                f"File {config} does not exists"
            )

    @pytest.mark.fast
    def test_clusters_with_gmm(self):
        with TemporaryDirectory() as temp:
            hdbscan(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)), "to-cluster.csv"
                ),
                temp
            )
            path = os.path.join(temp, "to-cluster")
            expected = f"{path}/clusters"
            self.assertTrue(
                os.path.exists(expected),
                f"Directory: {expected} does not exists"
            )
            config = f"{path}/config.json"
            self.assertTrue(
                os.path.exists(config),
                f"File {config} does not exists"
            )
