import joblib
import pandas as pd
from loguru import logger
from sklearn.preprocessing import StandardScaler
from sklearn.semi_supervised import LabelPropagation


def main(repos, out):
    frame = pd.read_csv(repos)
    frame['label'] = frame['label'].map({'SR': 1, 'NON': 0}).fillna(-1)
    features = frame.drop(columns=["repo", "label"])
    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)
    model = LabelPropagation()
    model.fit(scaled, frame["label"])
    joblib.dump(model, out)
    logger.info(f"Model {model} saved to {out}")
    probs = model.predict_proba(scaled)
    for i, prob in enumerate(probs):
        rid = frame["repo"].iloc[i]
        logger.info(f"Repo {rid}: {prob[1]:.2f}")
