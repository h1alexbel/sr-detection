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
import cohere
import numpy as np
from loguru import logger

models = {
    "s-bert-384": "sentence-transformers/all-MiniLM-L6-v2",
    "e5-1024": "intfloat/e5-large",
    "cohere": ""
}


def main(repos, prefix, hf, cohere):
    """
    Embed.
    :param repos: Source CSV
    :param prefix: Prefix for output CSV with embeddings
    :param hf: HuggingFace token
    :param cohere Cohere token
    """
    frame = pd.read_csv(repos)
    frame["mcw"] = frame["mcw"].apply(
        lambda words:
        words.replace("[", "").replace("]", "").replace("'", "")
    )
    for model, checkpoint in models.items():
        logger.info(
            f"Generating {model} embeddings for {repos} ({len(frame)}r x {len(frame.columns)}c)..."
        )
        if model == "cohere":
            embed_cohere(cohere, frame, prefix)
        else:
            logger.debug(f"Inference checkpoint: {checkpoint}")
            embeddings = pd.DataFrame(infer(frame["mcw"].tolist(), checkpoint, hf))
            embeddings.insert(0, 'repo', frame["repo"])
            embeddings.to_csv(f"{prefix}-{model}.csv", index=False)
        logger.info(
            f"Generated {len(embeddings)} embeddings saved to {prefix}-{model}.csv ({len(embeddings)}r x {len(embeddings.columns)}c)"
        )


def embed_cohere(key, texts, prefix):
    client = cohere.Client(key)
    embeddings = pd.DataFrame(
        np.asarray(
            client.embed(
                texts=texts["mcw"].tolist(), input_type="search_document", model="embed-english-v3.0"
            ).embeddings
        )
    )
    embeddings.insert(0, "repo", texts["repo"])
    embeddings.to_csv(f"{prefix}-embedv3-1024.csv", index=False)


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
