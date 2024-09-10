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

models = {
    "s-bert-384": "sentence-transformers/all-MiniLM-L6-v2",
    "e5-1024": "intfloat/e5-large"
}


def main(repos, prefix, key):
    """
    Embed.
    :param key: HuggingFace token
    :param repos: Source CSV
    :param prefix: Prefix for output CSV with embeddings
    """
    frame = pd.read_csv(repos)
    for model, checkpoint in models.items():
        print(f"Generating {model} embeddings for {frame}...")
        print(f"Inference checkpoint: {checkpoint}")
        embeddings = pd.DataFrame(infer(frame["top"].tolist(), checkpoint, key))
        embeddings.insert(0, 'repo', frame["repo"])
        embeddings.to_csv(f"{prefix}-{model}", index=False)
        print(f"Generated embeddings {prefix}-{model}")


def infer(texts, checkpoint, key):
    """
    Send texts on inference endpoint.
    :param texts: Number of texts
    :param checkpoint: Inference checkpoint
    :param key: HuggingFace Inference Access Token
    :return: JSON embeddings
    """
    return requests.post(
        # pylint: disable=line-too-long
        f"https://api-inference.huggingface.co/pipeline/feature-extraction/{checkpoint}",  # noqa: E501
        headers={
            "Authorization": f"Bearer {key}"
        },
        json={
            "inputs": texts,
            "options": {
                "wait_for_model": True
            }
        },
        timeout=300
    ).json()
