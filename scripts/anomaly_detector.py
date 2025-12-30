import pandas as pd
from sklearn.ensemble import IsolationForest
import os

# ==========================================
# CONFIGURATION
# ==========================================
# We define paths relative to the project root for portability.
INPUT_PATH = "data/raw/procurement_data.csv"
OUTPUT_PATH = "data/processed/procurement_data_audited.csv"

def run_anomaly_detection():
    """
    Reads raw procurement data, trains an unsupervised ML model (Isolation Forest),
    and tags records that statistically deviate from the norm.
    """
    
    # 1. INGESTION
    # Check if data exists first (Error Handling)
    if not os.path.exists(INPUT_PATH):
        print(f"❌ Error: Input file not found at {INPUT_PATH}. Run data_generator.py first.")
        return

    print("Loading data...")
    df = pd.read_csv(INPUT_PATH)

    # 2. FEATURE ENGINEERING
    # The model needs numerical input. We select the financial columns.
    # LOGIC: Anomalies in procurement usually manifest in the relationship between 
    # what was planned (Budget) and what happened (ActualSpend).
    features = df[['Budget', 'ActualSpend']]

    # 3. MODEL INITIALIZATION
    # ALGORITHM: Isolation Forest.
    # MECHANICS: It isolates observations by randomly selecting a feature and 
    # then randomly selecting a split value between the max and min values of the selected feature.
    # REASONING: Highly efficient for high-dimensional datasets and does not assume a normal distribution 
    # (unlike Z-Score/Standard Deviation methods).
    model = IsolationForest(
        n_estimators=100,     # Number of trees in the forest
        contamination=0.05,   # Sensitivity: We expect ~5% of contracts to be anomalous
        random_state=42       # Reproducibility: Ensures the same outliers are flagged every time
    )

    print("Training Isolation Forest model...")
    # The model "learns" the shape of the data here.
    model.fit(features)

    # 4. PREDICTION
    # The model returns -1 for outliers and 1 for inliers.
    predictions = model.predict(features)

    # 5. POST-PROCESSING
    # Translate model output (-1/1) into Business Terminology (True/False).
    # This makes the data strictly typed for Power BI (Boolean).
    df['IsAnomaly'] = [True if x == -1 else False for x in predictions]

    # OPTIONAL: Scoring
    # 'decision_function' gives the raw anomaly score. Lower = more abnormal.
    # Useful for sorting by "Severity" in the dashboard.
    df['AnomalyScore'] = model.decision_function(features)

    # 6. EXPORT
    # We save to 'processed' because this data is now enriched.
    # Ensure directory exists
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    
    df.to_csv(OUTPUT_PATH, index=False)
    
    # Summary Metrics for the Console
    anomaly_count = df['IsAnomaly'].sum()
    print(f"✅ Audit Complete. {len(df)} records processed.")
    print(f"⚠️  Flagged {anomaly_count} anomalies based on financial patterns.")
    print(f"📂 Enriched data saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    run_anomaly_detection()