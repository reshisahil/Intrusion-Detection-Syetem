
from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_DIR = Path(__file__).resolve().parents[1]

INPUT_PATH = PROJECT_DIR / "data" / "processed" / "cleaned_data.csv"
OUTPUT_PATH = PROJECT_DIR / "data" / "processed" / "processed_data.csv"

print("=" * 50)
print("MEMBER 1 - FEATURE SELECTION")
print("=" * 50)

# Load cleaned dataset
df = pd.read_csv(INPUT_PATH, low_memory=False)
df.columns = df.columns.str.strip()

# Clean labels
df["Label"] = df["Label"].astype(str).str.strip()

# Remove identification fields
unwanted_columns = [
    "Flow ID",
    "Source IP",
    "Destination IP",
    "Timestamp"
]

removed = [c for c in unwanted_columns if c in df.columns]
df.drop(columns=removed, inplace=True)

print("\nIdentification columns removed:", removed)

# Separate label from features
labels = df["Label"]
features = df.drop(columns=["Label"])

# Convert features to numeric
features = features.apply(pd.to_numeric, errors="coerce")

# Remove columns that contain non-numeric values
invalid_columns = features.columns[
    features.isnull().any()
].tolist()

features.drop(columns=invalid_columns, inplace=True)

print("Non-numeric columns removed:", invalid_columns)

# Replace infinite values
features.replace([np.inf, -np.inf], np.nan, inplace=True)

# Remove rows with invalid feature values
valid_rows = features.notna().all(axis=1)

features = features.loc[valid_rows]
labels = labels.loc[valid_rows]

# Remove constant features
constant_columns = [
    col for col in features.columns
    if features[col].nunique() <= 1
]

features.drop(columns=constant_columns, inplace=True)

print("Constant features removed:", constant_columns)

# Recombine features and labels

final_df = features.copy()
final_df["Label"] = labels

# Save final dataset
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
final_df.to_csv(OUTPUT_PATH, index=False)

# Save feature names for Member 2
feature_list = list(features.columns)

feature_file = PROJECT_DIR / "data" / "processed" / "feature_columns.txt"
feature_file.write_text("\n".join(feature_list), encoding="utf-8")

print("\nFINAL DATASET REPORT")
print("-" * 40)
print("Total records:", len(final_df))
print("Total ML features:", len(feature_list))
print("Total columns including label:", len(final_df.columns))
print("\nTraffic distribution:")
print(final_df["Label"].value_counts())
print("\nRemaining missing values:", final_df.isnull().sum().sum())
print("\nRemaining infinite values:",
      np.isinf(final_df.select_dtypes(include="number")).sum().sum())

print("\nProcessed dataset saved at:", OUTPUT_PATH)
print("Feature list saved at:", feature_file)
print("\nFEATURE SELECTION COMPLETED!")
