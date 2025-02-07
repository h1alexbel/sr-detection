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
import json
from loguru import logger


"""
Register steps.
"""
def register(steps):
    logger.info(f"Registering steps: {steps.replace(",", ", ")}")
    with open("resources/toolchain.json", "r") as spec:
        tlc = json.load(spec)
        defined = tlc["goal"]
    for step in steps.split(","):
        if not step in defined:
            logger.error(f"Step '{step}' cannot be recongnized by sr-filter");
            exit(-1);
    logger.info("Steps registered");


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
        default="mine,pulls,filter,workflows,junit,package,cluster,stats",
        help="Comma separeted steps to execute"
    )
    args = parser.parse_args()
    register(args.steps)
