import pickle
import pandas as pd

def run_test_selection(time_budget_sec=5.0):
    # Load model and dataset
    with open("models/model.pkl", "rb") as f:
        model = pickle.load(f)
    
    df = pd.read_csv("data/hackathon_test_dataset.csv")
    
    feature_cols = [
        "graph_distance", "impacted_nodes_count", "lines_changed",
        "historical_failure_rate", "test_execution_time_sec", "is_high_risk_feature"
    ]
    
    # Predict probabilities (Class 1 = Fail)
    probabilities = model.predict_proba(df[feature_cols])[:, 1]
    df["risk_prob"] = probabilities
    
    results = []
    accumulated_time = 0.0
    
    for idx, row in df.iterrows():
        risk = row["risk_prob"]
        exec_time = row["test_execution_time_sec"]
        
        # Criteria logic
        if risk < 0.20:
            action = "SKIP"
            reason = f"Low failure risk ({risk*100:.1f}%). Independent path."
        elif (accumulated_time + exec_time) > time_budget_sec:
            action = "SKIP"
            reason = f"Risk profile valid ({risk*100:.1f}%), skipped to fit budget."
        else:
            action = "RUN"
            reason = f"High risk profile ({risk*100:.1f}%). Direct code impact."
            accumulated_time += exec_time
            
        results.append({
            "focal_target": row["focal_target"],
            "test_target": row["test_target"],
            "graph_distance": row["graph_distance"],
            "lines_changed": row["lines_changed"],
            "hist_fail_rate": row["historical_failure_rate"],
            "high_risk_flag": row["is_high_risk_feature"],
            "predicted_risk": f"{risk*100:.1f}%",
            "exec_time_sec": exec_time,
            "action": action,
            "decision_reason": reason
        })
        
    return pd.DataFrame(results), accumulated_time

if __name__ == "__main__":
    # Configure Pandas to print all columns cleanly without truncation
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 1000)
    pd.set_option("display.max_colwidth", None)
    
    results_df, total_time = run_test_selection(time_budget_sec=5.0)
    
    print("\n=================== TEST SELECTION ENGINE RESULTS ===================")
    print(results_df.to_string(index=False))
    print("=====================================================================")
    print(f"Total Selected CI Suite Time: {total_time:.2f} seconds\n")