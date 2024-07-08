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
import subprocess

default = {
    "search": "stars:>10 language:java size:>=20 mirror:false template:false",
    "start": "2019-01-01",
    "end": "2024-05-01",
    "tokens": "tokens"
}


def main(config=default):
    """
    Collect repositories.
    :param config: Configuration to use
    """
    if config is None:
        config = default
    print("Collecting GitHub repositories using GitHub API...")
    print(f"Using config: {config}")
    cmd = f"""
    ghminer --query "{config["search"]}" \
            --start "{config["start"]}" \
            --end "{config["end"]}" \
            --tokens {config["tokens"]}
    """
    try:
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        err = process.stderr.read()
        if err:
            print(f"Error: {err.strip()}")
        process.wait()
        if process.returncode != 0:
            raise subprocess.CalledProcessError(
                process.returncode,
                cmd,
                output=process.stdout.read(),
                stderr=err
            )
    except subprocess.CalledProcessError as e:
        print(f"Something went wrong: {e.stderr}")
