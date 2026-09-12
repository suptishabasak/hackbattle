"""
risk_scoring.py  (Suptisha's part of Person 3)
"""

import json


def get_risk_score(file_name, historical_data):
    total = 0
    fails = 0

    for record in historical_data:
        if file_name in record["changed_files"]:
            total += 1
            if record["status"] == "fail":
                fails += 1

    if total == 0:
        return 0.3  # no history, default medium-low risk

    return fails / total


def mock_get_affected_tests(file_name):
    """
    TEMPORARY stand-in for Person 1's real get_affected_tests(file_name).
    Replace this with: from dependency_graph import get_affected_tests
    once Person 1's module is ready. Everything else stays the same.
    """
    short_name = file_name.split("/")[-1].split(".")[0]
    return [f"test_{short_name}_basic", f"test_{short_name}_edge_case"]


def get_test_risk_scores(changed_files, historical_data, get_affected_tests):
    """
    Given a list of changed files, returns { test_name: risk_score }.
    If a test is affected by multiple changed files, it gets the MAX
    risk score among them.
    """
    test_scores = {}

    for file_name in changed_files:
        file_risk = get_risk_score(file_name, historical_data)
        affected_tests = get_affected_tests(file_name)

        for test_name in affected_tests:
            current = test_scores.get(test_name, 0.0)
            test_scores[test_name] = max(current, file_risk)

    return test_scores


def validate_against_history(historical_data, get_affected_tests, risk_threshold=0.5):
    """
    Returns test_reduction_pct and regression_recall_pct across all
    historical PRs, using risk_threshold to decide which tests get
    "selected" to run.
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

        scores = get_test_risk_scores(changed_files, historical_data, get_affected_tests)
        selected = [t for t, s in scores.items() if s >= risk_threshold]
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

    # --- 1. basic file risk score ---
    score = get_risk_score("compiler/apps/playground/app/page.tsx", data)
    print("Risk score for one file:", score)

    # --- 2. test-level ranking (using MOCK tests for now) ---
    test_scores = get_test_risk_scores(
        ["compiler/apps/playground/app/page.tsx"], data, mock_get_affected_tests
    )
    print("\nTest risk scores (mocked test names):")
    for test_name, s in sorted(test_scores.items(), key=lambda x: x[1], reverse=True):
        print(f"  {s:.2f}  {test_name}")

    # --- 3. validation metrics (using MOCK tests for now) ---
    results = validate_against_history(data, mock_get_affected_tests)
    print("\nValidation results (mocked):", results)