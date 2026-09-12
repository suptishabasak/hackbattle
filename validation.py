"""
validation.py

Combines risk_scoring.py (Suptisha) + confidence_safety.py (Tarini)
to run the full validation: how many tests would we select, and how
many real historical failures would we have caught.

This file exists separately from risk_scoring.py to avoid a circular
import, since confidence_safety.py already imports get_risk_score
FROM risk_scoring.py.
"""

import json
from risk_scoring import get_risk_score, mock_get_affected_tests
from confidence_safety import get_confidence, apply_safety_mechanism


def get_test_decisions(changed_files, historical_data, get_affected_tests):
    """
    For each changed file -> each affected test, computes risk + confidence,
    then calls apply_safety_mechanism to decide RUN or SKIP.

    Returns: { test_name: "RUN" or "SKIP" }
    """
    decisions = {}

    for file_name in changed_files:
        risk = get_risk_score(file_name, historical_data)
        confidence = get_confidence(file_name, historical_data)
        affected_tests = get_affected_tests(file_name)

        for test_name in affected_tests:
            decision = apply_safety_mechanism(risk, confidence)
            # if ANY file affecting this test says RUN, keep it as RUN
            if decisions.get(test_name) != "RUN":
                decisions[test_name] = decision

    return decisions


def validate_against_history(historical_data, get_affected_tests):
    """
    Loops through every historical PR, uses the combined risk+confidence+
    safety decision to predict which tests would run, and checks that
    against what actually happened (did the PR fail?).
    """
    failed_prs = [r for r in historical_data if r["status"] == "fail"]
    caught = 0
    total_if_all = 0
    total_selected = 0

    for record in historical_data:
        changed_files = record["changed_files"]

        all_tests = set()
        for f in changed_files:
            all_tests.update(get_affected_tests(f))
        total_if_all += len(all_tests)

        decisions = get_test_decisions(changed_files, historical_data, get_affected_tests)
        selected = [t for t, d in decisions.items() if d == "RUN"]
        total_selected += len(selected)

        if record["status"] == "fail" and len(selected) > 0:
            caught += 1

    reduction_pct = 100 * (1 - total_selected / total_if_all) if total_if_all else 0
    recall_pct = 100 * caught / len(failed_prs) if failed_prs else None

    return {
        "test_reduction_pct": round(reduction_pct, 1),
        "regression_recall_pct": round(recall_pct, 1) if recall_pct is not None else None,
    }


if __name__ == "__main__":
    with open("historical_data.json") as f:
        data = json.load(f)

    results = validate_against_history(data, mock_get_affected_tests)
    print("Validation results (using combined risk + confidence + safety mechanism):")
    print(results)