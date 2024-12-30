"""
Count of JUnit tests in repo.
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
import pandas as pd
import requests
from loguru import logger
from sr_data.steps.maven import request

TEST_FILE_SUFFIXES = (
    "Test.java", "TestCase.java", "IT.java", "ITCase.java"
)

TEST_ANNOTATIONS = (
    "Test", "ParameterizedTest", "RunWith(Parameterized.class)"
)


def main(repos, out, token):
    frame = pd.read_csv(repos)
    logger.info(f"Counting JUnit tests in {len(frame)} repositories...")
    for idx, row in frame.iterrows():
        frame.at[idx, "tests"] = count_of_tests(
            row["repo"],
            row["branch"],
            token
        )
    frame.to_csv(out, index=False)
    logger.info(f"Saved {len(frame)} repositories with JUnit tests to {out}")


def count_of_tests(repo, branch, token) -> int:
    files = [
        file for file in request(token, repo)["tree"] if file["path"].endswith(
            TEST_FILE_SUFFIXES
        )
    ]
    logger.info(f"Found {len(files)} test files in {repo}")
    found = 0
    for file in files:
        path = file["path"]
        content = requests.get(
            f"https://raw.githubusercontent.com/{repo}/refs/heads/{branch}/{path}"
        ).text
        if content == "404: Not Found":
            logger.error(f"Occurred an error: {content}")
        logger.debug(f"Checking {path}")
        for annotation in TEST_ANNOTATIONS:
            found += content.count(f"@{annotation}")
    logger.debug(f"Found {found} tests in {len(files)} files inside {repo}")
    return found
