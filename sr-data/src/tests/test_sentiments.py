"""
Tests for sentiments.
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
import os.path
import unittest
from tempfile import TemporaryDirectory

import pandas as pd
import pytest
from sr_data.steps.sentiments import top, sentiment, main


# @todo #207:60min Enable tests for sentiments.py when rultor will be able to install torch and
#  transformers. Currently, when rultor tries to install torch and transformers dependencies to
#  be able to run steps/sentiments.py it fails with exit code 137. Versions were
#  used: torch = "2.2.2", and transformers = "4.41.2". You can check the example
#  of such build
#  <a href="https://github.com/h1alexbel/sr-detection/pull/233#issuecomment-2497707744">here<a/>.
#  After issue will be resolved, we should enable uncomment lines in `sentiments.py`,
#  and enable respective tests in test_sentiments.py.
@pytest.mark.skip
class TestSentiments(unittest.TestCase):

    @pytest.mark.fast
    def test_returns_top_description_for_readme(self):
        description = top("# Top\n# The latter")
        expected = "Top"
        self.assertEqual(
            description,
            expected,
            f"Extracted description: {description} does not match with expected: {expected}"
        )

    @pytest.mark.fast
    def test_returns_first_512_chars_when_top_is_big(self):
        extracted = top(
            """# Top
            Lorem Ipsum is simply dummy text of the printing and
            typesetting industry. Lorem Ipsum has been the industry's standard
            dummy text ever since the 1500s, when an unknown printer took a
            galley of type and scrambled it to make a type specimen book.
            It has survived not only five centuries, but also the leap into
            electronic typesetting, remaining essentially unchanged. It was
            popularised in the 1960s with the release of Letraset sheets
            containing Lorem Ipsum passages, and more recently with desktop
            publishing software like Aldus PageMaker including versions of
            Lorem Ipsum. It is a long established fact that a reader will be
            distracted by the readable content of a page when looking at its
            layout. The point of using Lorem Ipsum is that it has a
            more-or-less normal distribution of letters, as opposed to using
            'Content here, content here', making it look like readable English.
             Many desktop publishing packages and web page editors now use
            Lorem Ipsum as their default model text, and a search for
            'lorem ipsum' will uncover many web sites still in their infancy.
            Various versions have evolved over the years, sometimes by
            accident, sometimes on purpose (injected humour and the like).
            There are many variations of passages of Lorem Ipsum available, but
            the majority have suffered alteration in some form, by injected
            humour, or randomised words which don't look even slightly
            believable.
"""
        )
        size = len(extracted)
        expected = 510
        self.assertEqual(
            size,
            expected,
            f"Extracted description: {extracted}, has size: {size}, but should: {expected}"
        )

    @pytest.mark.fast
    def test_returns_words_for_empty_sections(self):
        expected = "There is no sections at all"
        extracted = top(expected)
        self.assertEqual(
            extracted,
            expected,
            f"Extracted description: {extracted} does not match with expected: {expected}"
        )

    @pytest.mark.fast
    def test_runs_sentiment(self):
        result = sentiment("# Testing sentiment pipeline")
        self.assertTrue(
            result[0] is not None,
            "Sentiment result is NULL, but it should not!"
        )

    @pytest.mark.fast
    def test_runs_sentiments_for_all(self):
        with TemporaryDirectory() as temp:
            path = os.path.join(temp, "sentiments.csv")
            main(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "resources/to-sentiments.csv"
                ),
                path
            )
            frame = pd.read_csv(path)
            self.assertTrue(
                len(frame["sentiment"].tolist()) != 0,
                "Sentiments are empty, but they should not!"
            )
