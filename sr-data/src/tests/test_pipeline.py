"""
Pipeline tests.
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
from sr_data.pipeline import main


class TestPipeline(unittest.TestCase):

    @pytest.mark.fast
    def test_outputs_commands_and_files(self):
        with TemporaryDirectory() as temp:
            steps = os.path.join(temp, "steps.txt")
            files = os.path.join(temp, "files.txt")
            main(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "../../resources/pipeline.json",
                ),
                "pulls,filter,extract,embed",
                steps,
                files
            )
            with open(steps, "r") as f:
                steps = f.readlines()
            with open(files, "r") as f:
                files = f.readlines()
            self.assertEqual(
                steps,
                [
                    'just pulls "../repos.csv" $GH_TOKEN "../repos-with-pulls.csv"\n',
                    'just filter "../repos-with-pulls.csv" "../after-filter.csv"\n',
                    'just extract "../after-filter.csv" "../after-extract.csv"\n',
                    'just embed "../after-extract.csv" "../embeddings"\n',
                    'cp "embeddings-s-bert-384.csv" "sbert.csv"\n',
                    'cp "embeddings-e5-1024.csv" "e5.csv"\n',
                    'cp "embeddings-embedv3-1024.csv" "embedv3.csv"'
                ],
                f"Resulted steps: {steps} don't match with expected"
            )
            self.assertEqual(
                files,
                [
                    'repos.csv\n',
                    'repos-with-pulls.csv\n',
                    'after-filter.csv\n',
                    'after-extract.csv\n',
                    'embeddings-s-bert-384.csv\n',
                    'embeddings-embedv3-1024.csv\n',
                    'embeddings-e5-1024.csv'
                ],
                f"Found files: {files} don't match with expected"
            )

    @pytest.mark.fast
    def test_outputs_pipeline_with_workflows(self):
        with TemporaryDirectory() as temp:
            steps = os.path.join(temp, "steps.txt")
            files = os.path.join(temp, "files.txt")
            main(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "../../resources/pipeline.json",
                ),
                "pulls,filter,workflows",
                steps,
                files
            )
            with open(steps, "r") as f:
                steps = f.readlines()
            with open(files, "r") as f:
                files = f.readlines()
            self.assertEqual(
                steps,
                [
                    'just pulls "../repos.csv" $GH_TOKEN "../repos-with-pulls.csv"\n',
                    'just filter "../repos-with-pulls.csv" "../after-filter.csv"\n',
                    'just workflows "../after-filter.csv" "../after-workflows.csv"',
                ],
                f"Resulted steps: {steps} don't match with expected"
            )
            self.assertEqual(
                files,
                [
                    'repos.csv\n',
                    'repos-with-pulls.csv\n',
                    'after-filter.csv\n',
                    'after-workflows.csv'
                ],
                f"Found files: {files} don't match with expected"
            )
