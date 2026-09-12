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


if __name__ == "__main__":
    with open("historical_data.json") as f:
        data = json.load(f)

    # test on a real file from your data
    score = get_risk_score("compiler/apps/playground/app/page.tsx", data)
    print("Risk score:", score)

    # test on every file that actually appears, so you can sanity-check the range
    all_files = set()
    for record in data:
        all_files.update(record["changed_files"])

    print(f"\nRisk scores for all {len(all_files)} files seen in history:")
    for f in sorted(all_files):
        print(f"  {get_risk_score(f, data):.2f}  {f}")