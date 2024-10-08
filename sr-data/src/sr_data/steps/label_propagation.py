"""
Label Propagation model training.
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
import joblib
import pandas as pd
from loguru import logger
from sklearn.preprocessing import StandardScaler
from sklearn.semi_supervised import LabelPropagation


def main(repos, out):
    frame = pd.read_csv(repos)
    frame['label'] = frame['label'].map({'SR': 1, 'NON': 0}).fillna(-1)
    scaled = StandardScaler().fit_transform(
        frame.drop(columns=["repo", "label"])
    )
    model = LabelPropagation()
    model.fit(scaled, frame["label"])
    joblib.dump(model, out)
    logger.info(f"Model {model} saved to {out}")
    probs = model.predict_proba(scaled)
    for i, prob in enumerate(probs):
        rid = frame["repo"].iloc[i]
        logger.info(f"Repo {rid}: {prob[1]:.2f}")
