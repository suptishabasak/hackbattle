"""
ml_risk_scoring.py

Uses the trained model (models/model.pkl) to predict risk for a PR,
based on the same features used in train_model.py. This is REAL ML —
the model was trained on historical_data.json, not hardcoded rules.
"""

import json
import pickle
from train_model import build_file_history, build_features


def load_model(model_path="models/model.pkl"):
    with open(model_path, "rb") as f:
        return pickle.load(f)


def get_ml_risk_score(changed_files, historical_data, model):
    """
    Given a list of changed files (like a new PR), predicts the
    probability of failure using the trained model.
    Returns a float between 0 and 1 (higher = riskier).
    """
    appearances, failures = build_file_history(historical_data)

    fake_record = {"changed_files": changed_files}
    features = build_features(fake_record, appearances, failures)

    # predict_proba returns [prob_of_class_0, prob_of_class_1]
    # class 1 = "fail", so we want that probability
    probability_of_fail = model.predict_proba([features])[0][1]

    return probability_of_fail


if __name__ == "__main__":
    with open("historical_data.json") as f:
        data = json.load(f)

    model = load_model()

    # test on a real file from your data
    test_files = ["compiler/apps/playground/app/page.tsx"]
    risk = get_ml_risk_score(test_files, data, model)
    print(f"ML-predicted risk for {test_files}: {risk:.2f}")