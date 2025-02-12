"""
SR command-line toolchain.
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

import argparse
import importlib.metadata
import importlib.resources
import json
from loguru import logger
import os
import shutil
import sr_data.steps.pulls as pulls


def pull_requests():
    logger.info("Calculating the number of pull requests in each repo...")
    with importlib.resources.files("sr.resources").joinpath("toolchain.json").open("r") as spec:
        tlc = json.load(spec)
        config = tlc["pulls"]
        out = config["out"]
        os.makedirs(os.path.dirname(out), exist_ok=True)
        pulls.main(config["repos"], out, os.environ[config["token"].replace("$", "")])


PIPE_MAPPING = {
    "pulls": pull_requests
}


def prepare_out():
    out = "sr/target"
    shutil.rmtree(out)
    logger.debug(f"Cleaned {out}")
    os.makedirs(out, exist_ok=True)
    logger.debug(f"Created output directory in {out}")


def register(steps):
    pipes = []
    logger.info(f"Registering steps: {steps.replace(',', ', ')}")
    with importlib.resources.files("sr.resources").joinpath("toolchain.json").open("r") as spec:
        tlc = json.load(spec)
        defined = tlc["goal"]
    for step in steps.split(","):
        if step not in defined:
            logger.error(
                f"Step '{step}' cannot be recognized. List of available steps: {", ".join(defined)}"
            )
            exit(-1)
        pipes.append(step)
    logger.info("Steps registered")
    return pipes


def validate():
    if not os.path.exists("repos.csv"):
        raise RuntimeError(
            "File 'repos.csv' is not present at run dir. Please generate this file with 'just collect..' script"  # noqa: E501
        )


def main():
    parser = argparse.ArgumentParser(description="SR toolchain")
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {importlib.metadata.version("sr-filter")}"
    )
    parser.add_argument(
        "--steps",
        type=str,
        default="pulls,filter,workflows,junit,package,cluster,stats",
        help="Comma separated steps to execute"
    )
    args = parser.parse_args()
    validate()
    prepare_out()
    for pipe in register(args.steps):
        worker = PIPE_MAPPING.get(pipe)
        if worker:
            worker()
        else:
            raise RuntimeError(f"Cannot find worker for pipe '{pipe}'")
