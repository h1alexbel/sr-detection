"""
Tests for workflows.
"""
import os.path
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
from tempfile import TemporaryDirectory

import pandas as pd
import pytest
from sr_data.steps.workflows import workflow_info, main


class TestWorkflows(unittest.TestCase):

    @pytest.mark.fast
    def test_outputs_workflow_information(self):
        info = workflow_info(
            "h1alexbel/h1alexbel/refs/heads/main/.github/workflows/update-readme.yml"
        )
        expected = "jobs:"
        self.assertTrue(
            expected in info,
            f"Fetched workflow information: {info} does not contain expected string: {expected}"
        )

    @pytest.mark.nightly
    def test_collects_workflows_for_all(self):
        with TemporaryDirectory() as temp:
            path = os.path.join(temp, "workflows.csv")
            main(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "resources/to-workflows.csv"
                ),
                path
            )
            frame = pd.read_csv(path)
            collected = len(frame["workflows"])
            expected = 9
            self.assertEqual(
                collected,
                expected,
                f"Length of collected workflows: {collected} don't match with expected: {expected}"
            )