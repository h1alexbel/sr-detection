"""
Tests for workflows.
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

import pandas as pd
import pytest
import yaml
from sr_data.steps.workflows import workflow_info, main, fetch, used_for_releases, w_score


class TestWorkflows(unittest.TestCase):

    @pytest.mark.fast
    def test_fetches_workflow_information(self):
        info = fetch(
            "h1alexbel/h1alexbel/refs/heads/main/.github/workflows/update-readme.yml",
        )
        expected = "jobs:"
        self.assertTrue(
            expected in info,
            f"Fetched workflow information: {info} does not contain expected string: {expected}"
        )

    @pytest.mark.fast
    def test_outputs_workflow_info_correctly(self):
        info = workflow_info(
            """
name: test
on:
  push:
    branches:
      - master
jobs:
  build:
    strategy:
      matrix:
        os: [ ubuntu-22.04, macos-13, windows-2022, ubuntu-latest, ubuntu-latest ]
    runs-on: ${{ matrix.os }}
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v3
        with:
          python-version: '3.8'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest
            """
        )
        self.assertEqual(
            info["w_jobs"],
            1,
            f"Jobs count in workflow: '{info}' does not match with expected"
        )
        self.assertEqual(
            info["w_oss"],
            ["macos-13", "ubuntu-22.04", "ubuntu-latest", "windows-2022"],
            f"Workflow OSs: '{info}' does not match with expected"
        ),
        self.assertEqual(
            info["w_steps"],
            4,
            f"Steps count in workflow: '{info}' does not match with expected"
        )

    @pytest.mark.nightly
    def test_collects_unique_oss_across_all_files(self):
        with TemporaryDirectory() as temp:
            path = os.path.join(temp, "workflows.csv")
            main(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "resources/to-unique-oss.csv"
                ),
                path
            )
            oss = pd.read_csv(path).iloc[0]["w_oss"]
            expected = 3
            self.assertEqual(
                oss,
                expected,
                f"OSS count: {oss} does not match with expected: {expected}"
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
            self.assertTrue(
                all(
                    col in frame.columns for col in
                    ["has_workflows", "workflows", "w_jobs", "w_oss", "w_steps", "has_release_workflow"]
                ),
                f"Frame {frame.columns} doesn't have expected columns"
            )

    @pytest.mark.nightly
    def test_counts_workflows_correctly(self):
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
            result = frame["workflows"].tolist()
            self.assertEqual(
                result,
                [4, 0, 2, 1, 1, 0, 2, 0, 0, 1, 1, 1, 10, 1],
                "Workflows counts don't match with expected"
            )

    @pytest.mark.nightly
    def test_checks_has_workflows(self):
        with TemporaryDirectory() as temp:
            path = os.path.join(temp, "workflows.csv")
            main(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "resources/to-has-workflows.csv"
                ),
                path
            )
            frame = pd.read_csv(path)
            self.assertEqual(
                frame.iloc[0]["has_workflows"],
                1.0,
                "First repo doesn't have workflows, but it should"
            )
            self.assertEqual(
                frame.iloc[1]["has_workflows"],
                0.0,
                "First repo has workflows, but it shouldn't"
            )

    @pytest.mark.fast
    def test_returns_true_when_workflow_has_type_published(self):
        self.assertTrue(
            used_for_releases(
                yaml.safe_load(
                    """
                    on:
                      release:
                        types: [published]
                    """
                )
            ),
            "Workflow should be used for releases, but it wasn't"
        )

    @pytest.mark.fast
    def test_returns_true_when_workflow_has_push_on_version(self):
        self.assertTrue(
            used_for_releases(
                yaml.safe_load(
                    """
                    on:
                      push:
                        tags:
                          - v*
                    """
                )
            ),
            "Workflow should be used for releases, but it wasn't"
        )

    @pytest.mark.fast
    def test_returns_false_when_no_release(self):
        self.assertFalse(
            used_for_releases(
                yaml.safe_load(
                    """
                    on:
                      push:
                        branches:
                          - master
                    """
                )
            ),
            "Workflow shouldn't be used for releases, but it was"
        )

    @pytest.mark.fast
    def test_returns_false_on_simple_list(self):
        self.assertFalse(
            used_for_releases(
                yaml.safe_load(
                    """
                    on: [push, pull_request]
                    """
                )
            ),
            "Workflow shouldn't be used for releases, but it was"
        )

    @pytest.mark.fast
    def test_outputs_workflow_info_with_nested_expression(self):
        info = workflow_info(
            """
name: test
on:
  push:
    branches:
      - master
jobs:
  build:
    strategy:
      matrix:
        platform:
          - runner: ubuntu-latest
            target: x86_64
          - runner: ubuntu-latest
            target: x86
    runs-on: ${{ matrix.platform.runner }}
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v3
        with:
          python-version: '3.8'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest
            """
        )
        self.assertEqual(
            info["w_oss"],
            ["ubuntu-latest@x86", "ubuntu-latest@x86_64"],
            f"Workflow OSs: '{info}' does not match with expected"
        )
        self.assertEqual(
            info["w_jobs"],
            1,
            f"Jobs count in workflow: '{info}' does not match with expected"
        )
        self.assertEqual(
            info["w_steps"],
            4,
            f"Steps count in workflow: '{info}' does not match with expected"
        )

    @pytest.mark.fast
    def test_skips_matrix_as_text(self):
        info = workflow_info(
            """
on: push
jobs:
  plan:
    strategy:
        matrix: ${{ fromJson(needs.plan.outputs.val).ci.github.artifacts_matrix }}
    runs-on: ubuntu-latest
            """
        )
        self.assertEqual(
            info["w_oss"],
            ["ubuntu-latest"],
            f"Workflow OSs: '{info}' does not match with expected"
        )
        self.assertEqual(
            info["w_jobs"],
            1,
            f"Jobs count in workflow: '{info}' does not match with expected"
        )
        self.assertEqual(
            info["w_steps"],
            0,
            f"Steps count in workflow: '{info}' does not match with expected"
        )

    @pytest.mark.fast
    def test_parses_runs_as_list(self):
        info = workflow_info(
            """
on:
  pull_request:
    types: [opened, synchronize]
jobs:
  ensure_changelog_exists:
    name: Ensure that .changeset is not empty
    runs-on: [ubuntu-latest]
    strategy:
      matrix:
        node-version: ["20.x"]
        pnpm-version: ["9.x"]
            """
        )
        self.assertEqual(
            info["w_oss"],
            ["ubuntu-latest"],
            f"Workflow OSs: '{info}' does not match with expected"
        )
        self.assertEqual(
            info["w_jobs"],
            1,
            f"Jobs count in workflow: '{info}' does not match with expected"
        )
        self.assertEqual(
            info["w_steps"],
            0,
            f"Steps count in workflow: '{info}' does not match with expected"
        )

    @pytest.mark.fast
    def test_parses_on_as_string(self):
        info = workflow_info(
            """
"on":
  pull_request:
    types: [push]
jobs:
  ensure_changelog_exists:
    name: test
    runs-on: [ubuntu-latest]
            """
        )
        self.assertEqual(
            info["w_oss"],
            ["ubuntu-latest"],
            f"Workflow OSs: '{info}' does not match with expected"
        )
        self.assertEqual(
            info["w_jobs"],
            1,
            f"Jobs count in workflow: '{info}' does not match with expected"
        )
        self.assertEqual(
            info["w_steps"],
            0,
            f"Steps count in workflow: '{info}' does not match with expected"
        )

    @pytest.mark.fast
    def test_parses_none_matrix(self):
        info = workflow_info(
            """
on: push
name: test
jobs:
  build:
    runs-on: ${{ inputs.platform }}
            """
        )
        self.assertEqual(
            info["w_oss"],
            [],
            f"Workflow OSs: '{info}' does not match with expected"
        )
        self.assertEqual(
            info["w_jobs"],
            1,
            f"Jobs count in workflow: '{info}' does not match with expected"
        )
        self.assertEqual(
            info["w_steps"],
            0,
            f"Steps count in workflow: '{info}' does not match with expected"
        )

    @pytest.mark.fast
    def test_parses_oss_as_list_in_matrix(self):
        info = workflow_info(
            """
name: test
on: push
jobs:
  build:
    strategy:
      matrix:
        os:
          - [self-hosted]
    runs-on: ${{ matrix.os }}
            """
        )
        self.assertEqual(
            info["w_oss"],
            ["self-hosted"],
            f"Workflow OSs: '{info}' does not match with expected"
        )
        self.assertEqual(
            info["w_jobs"],
            1,
            f"Jobs count in workflow: '{info}' does not match with expected"
        )
        self.assertEqual(
            info["w_steps"],
            0,
            f"Steps count in workflow: '{info}' does not match with expected"
        )

    @pytest.mark.fast
    def test_calculates_simplicity_score(self):
        scores = pd.read_csv(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "resources/to-wscore.csv"
            )
        )
        self.assertEqual(
            w_score(scores.iloc[0]),
            -0.85,
            "Calculated score does not match with expected"
        )

    @pytest.mark.fast
    def test_parses_commented_workflow(self):
        info = workflow_info(
            """
# name: test
# on: push
# jobs:
#  build:
#    strategy:
#      matrix:
#        os:
#          - [self-hosted]
#    runs-on: ${{ matrix.os }}
            """
        )
        self.assertEqual(
            info["w_oss"],
            [],
            "Workflow OSs are not empty, but they should"
        )
        self.assertEqual(
            info["w_jobs"],
            0,
            "Jobs count in workflow is not zero, but should be"
        )
        self.assertEqual(
            info["w_steps"],
            0,
            "Steps count in workflow is not zero, but should be"
        )
