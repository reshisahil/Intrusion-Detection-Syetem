
from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = PROJECT_DIR / "data" / "processed" / "processed_data.csv"
FEATURE_PATH = PROJECT_DIR / "data" / "processed" / "feature_columns.txt"

print("=" * 50)
print("MEMBER 1 - FINAL DATA VALIDATION")
print("=" * 50)

df = pd.read_csv(DATA_PATH, low_memory=False)

features = [c for c in df.columns if c != "Label"]
saved_features = FEATURE_PATH.read_text(encoding="utf-8").splitlines()

checks = {
    "Dataset exists": DATA_PATH.exists(),
    "Label column exists": "Label" in df.columns,
    "Feature list matches CSV": features == saved_features,
    "All features are numeric": all(
        pd.api.types.is_numeric_dtype(df[c]) for c in features
    ),
    "No missing values": not df.isnull().any().any(),
    "No infinite values": not np.isinf(
        df[features].to_numpy(dtype=float)
    ).any(),
    "No duplicate records": not df.duplicated().any(),
    "Expected labels present": set(df["Label"].unique()) == {"BENIGN", "DDoS"},
}

print("\nDATASET SUMMARY")
print("Records:", len(df))
print("Features:", len(features))
print("Total columns:", len(df.columns))

print("\nCLASS DISTRIBUTION")
print(df["Label"].value_counts())

print("\nVALIDATION CHECKS")
for name, passed in checks.items():
    print(f"{'PASS' if passed else 'FAIL'} - {name}")

print("\nCONSTANT FEATURES")
constant = [c for c in features if df[c].nunique() <= 1]
print(constant if constant else "None")

print("\nOVERALL RESULT:",
      "READY FOR HANDOVER" if all(checks.values())
      else "REVIEW REQUIRED")

print("=" * 50)
