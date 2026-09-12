import os
import pickle
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

def train():
    df = pd.read_csv("data/hackathon_test_dataset.csv")
    
    feature_cols = [
        "graph_distance", "impacted_nodes_count", "lines_changed",
        "historical_failure_rate", "test_execution_time_sec", "is_high_risk_feature"
    ]
    
    X = df[feature_cols]
    y = df["test_result"]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    model = XGBClassifier(
        n_estimators=50,
        max_depth=3,
        learning_rate=0.1,
        random_state=42
    )
    
    model.fit(X_train, y_train)
    
    train_acc = model.score(X_train, y_train)
    test_acc = model.score(X_test, y_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_pred_proba)
    
    print("\n================ MODEL PERFORMANCE ================")
    print(f"Train Accuracy : {train_acc*100:.1f}%")
    print(f"Test Accuracy  : {test_acc*100:.1f}%")
    print(f"ROC-AUC Score  : {auc:.3f}")
    print("===================================================\n")
    
    os.makedirs("models", exist_ok=True)
    with open("models/model.pkl", "wb") as f:
        pickle.dump(model, f)
    print("SUCCESS: Model saved to 'models/model.pkl'")

if __name__ == "__main__":
    train()