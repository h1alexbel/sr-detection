"""
Generate embeddings.
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


# @todo #9:45min JSONDecodeError Expecting value: line 1 column 1 (char 0) on some records in the CSV.
#  When sending records to the endpoint, some READMEs get rejected with that
#  error. We should identify that rows and possibly remove/recover them.
def main(key, checkpoint, csv, out):
    frame = pd.read_csv(csv)
    print(f"Generating embeddings for {frame}...")
    print(f"Inference checkpoint: {checkpoint}")
    embeddings = pd.DataFrame(infer(frame["readme"].tolist(), checkpoint, key))
    embeddings.insert(0, 'repo', frame["repo"])
    embeddings.to_csv(out, index=False)
    print(f"Generated embeddings {out}")


def infer(texts, checkpoint, key):
    """
    Send texts on inference endpoint.
    :param texts: Number of texts
    :param checkpoint: Inference checkpoint
    :param key: HuggingFace Inference Access Token
    :return: JSON embeddings
    """
    return requests.post(
        f"https://api-inference.huggingface.co/pipeline/feature-extraction/{checkpoint}",
        headers={
            "Authorization": f"Bearer {key}"
        },
        json={
            "inputs": texts,
            "options": {
                "wait_for_model": True
            }
        }
    ).json()
