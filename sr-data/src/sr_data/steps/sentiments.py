"""
Sentiment analysis for a top description of README file.
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
from loguru import logger


# checkpoint = "cardiffnlp/twitter-roberta-base-sentiment-latest"
# tokenizer = AutoTokenizer.from_pretrained(checkpoint)
# model = AutoModelForSequenceClassification.from_pretrained(checkpoint)
# stask = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)


def main(repos, out):
    frame = pd.read_csv(repos)
    frame["sentiment"] = frame["readme"].apply(sentiment)
    frame.to_csv(out, index=False)
    logger.info(f"Saved {len(frame)} repositories with sentiments to {out}")


def sentiment(readme):
    description = top(readme)
    result = None
    try:
        # result = stask(description)
        result = ""
    except RuntimeError:
        logger.error(
            f"Can't parse input description ({len(description)} length)"
        )
        logger.debug(f"Erroneous description: {description}")
    return result


# @todo #153:35min: Extract first 15-20 words from first heading.
#  Instead of extracting just n characters, we should extract an amount of
#  words from the heading that contains not more than n characters.
def top(readme) -> str:
    sections = readme.split("\n#")
    stripped = [section.strip() for section in sections if section.strip()]
    if not stripped:
        result = " ".join(readme.split()[:31])
    else:
        first = stripped[0].strip()
        if len(first) > 512:
            result = first[:512]
        else:
            result = first
    return result.replace("#", "").strip()
