"""
train_model.py

Trains a real ML model (logistic regression) on historical_data.json
to predict whether a PR will fail, based on simple features about the
files it changed. Saves the trained model to models/model.pkl.
"""

import json
import pickle
import os
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


def build_file_history(historical_data):
    appearances = {}
    failures = {}

    for record in historical_data:
        for f in record["changed_files"]:
            appearances[f] = appearances.get(f, 0) + 1
            if record["status"] == "fail":
                failures[f] = failures.get(f, 0) + 1

    return appearances, failures


def build_features(record, appearances, failures):
    changed_files = record["changed_files"]
    num_files = len(changed_files)

    fail_rates = []
    for f in changed_files:
        total = appearances.get(f, 0)
        fails = failures.get(f, 0)
        rate = fails / total if total > 0 else 0.3
        fail_rates.append(rate)

    avg_fail_rate = sum(fail_rates) / len(fail_rates) if fail_rates else 0.3
    max_fail_rate = max(fail_rates) if fail_rates else 0.3

    return [num_files, avg_fail_rate, max_fail_rate]


def train_and_save_model(data_path="historical_data.json", model_out="models/model.pkl"):
    with open(data_path) as f:
        data = json.load(f)

    appearances, failures = build_file_history(data)

    X = []
    y = []
    for record in data:
        features = build_features(record, appearances, failures)
        label = 1 if record["status"] == "fail" else 0
        X.append(features)
        y.append(label)

    X = np.array(X)
    y = np.array(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LogisticRegression()
    model.fit(X_train, y_train)

    train_acc = model.score(X_train, y_train)
    test_acc = model.score(X_test, y_test)
    print(f"Train accuracy: {train_acc:.2f}")
    print(f"Test accuracy: {test_acc:.2f}")

    os.makedirs(os.path.dirname(model_out), exist_ok=True)
    with open(model_out, "wb") as f:
        pickle.dump(model, f)

    print(f"Model saved to {model_out}")


if __name__ == "__main__":
    train_and_save_model()