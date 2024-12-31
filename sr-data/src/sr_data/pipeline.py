"""
SR Pipeline.
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
import json

from loguru import logger

def main(representation, steps, pipes, out):
    commands = []
    lout = None
    files = ["repos.csv"]
    with open(representation, "r") as meta:
        origin = json.load(meta)
    for step in steps.split(","):
        if step == "embed":
            files.append("embeddings-s-bert-384.csv")
            files.append("embeddings-embedv3-1024.csv")
            files.append("embeddings-e5-1024.csv")
        params = origin[step]
        command = f"just {step}"
        if "repos" in params:
            repos = params["repos"]
            if repos == "@in":
                if lout is not None:
                    repos = lout
                else:
                    raise ValueError(
                        "We can't decode @in attribute, as there is no previous output"
                    )
            command += f" \"{repos}\""
        if "prefix" in params:
            pref = params["prefix"]
            command += f" \"{pref}\""
        if "token" in params:
            token = params["token"]
            command += f" {token}"
        if "filtered" in params:
            filtered = params["filtered"]
            command += f" \"{filtered}\""
        if "out" in params:
            output = params["out"]
            command += f" \"{output}\""
            lout = output
            files.append(output.replace("../", ""))
        commands.append(command)
        if "extras" in params:
            for extra in params["extras"]:
                commands.append(extra)
        logger.debug(f"Built step: {command}")
    with open(pipes, "w") as f:
        f.write("\n".join(commands))
    with open(out, "w") as f:
        f.write("\n".join(files))
    logger.info(f"The following commands will be executed:\n {commands}")
    logger.info(f"We expect the following files to be generated: {files}")
