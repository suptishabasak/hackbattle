import json
from risk_scoring import get_risk_score

def get_confidence(file_name, historical_data):
    count = 0
    for record in historical_data:
        if file_name in record["changed_files"]:
            count += 1

    if count >= 3:
        return 0.9
    elif count >= 2:
        return 0.6
    else:
        return 0.2

def apply_safety_mechanism(risk_score, confidence, threshold=0.5):
    combined = risk_score * confidence
    if combined > threshold:
        return "RUN"
    elif confidence < 0.4:
        return "RUN"
    else:
        return "SKIP"

with open("historical_data.json") as f:
    data = json.load(f)

test_file = "packages/react-dom/src/__tests__/ReactDOMFragmentRefs-test.js"

risk = get_risk_score(test_file, data)
conf = get_confidence(test_file, data)
decision = apply_safety_mechanism(risk, conf)

print("Risk score:", risk)
print("Confidence:", conf)
print("Decision:", decision)