"""
Annotate READMEs with tokens.
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
from openai import OpenAI


def main(key, csv, out):
    """
    Annotate READMEs in csv.
    :param key: Deep Infra API Key
    :param csv: CSV filename
    :param out: Output CSV filename
    :return: Transformed dataframe in out csv
    """
    print(f"Annotating READMEs in {csv}...")
    openai = OpenAI(
        api_key=key,
        base_url="https://api.deepinfra.com/v1/openai",
    )
    frame = pd.read_csv(csv)
    frame["readme"] = frame["readme"].apply(lambda c: talks_to_model(openai, c))
    frame.to_csv(out, index=False)


# @todo #9:35min Develop a prompt for README annotation.
#   We should create a prompt that will help the model annotate repositories
#   with <SR> and <non> tokens. Let's start with one that we specified in paper
#   draft.
def talks_to_model(model, content):
    """
    Talk to the model.
    :param model: Model
    :param content: README content
    :return: Completion
    """
    print(f"README in: {content}")
    completion = model.chat.completions.create(
        model="Phind/Phind-CodeLlama-34B-v2",
        messages=[{"role": "user", "content": "Hello"}]
    )
    out = completion.choices[0].message.content
    print(f"README out: {out}")
    print(f"User tokens spent: {completion.usage.prompt_tokens}")
    print(f"Completion tokens spent: {completion.usage.completion_tokens}")
    print(
        f"Total tokens spent: "
        f"{completion.usage.prompt_tokens + completion.usage.completion_tokens}"
    )
    return out
