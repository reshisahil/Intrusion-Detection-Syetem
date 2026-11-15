
from pathlib import Path
import pandas as pd
import numpy as np

# Project directory
PROJECT_DIR = Path(__file__).resolve().parents[1]

INPUT_PATH = (
    PROJECT_DIR / "data" / "raw" /
    "Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"
)

OUTPUT_PATH = (
    PROJECT_DIR / "data" / "processed" /
    "cleaned_data.csv"
)

print("=" * 50)
print(" MEMBER 1 - DATA CLEANING")
print("=" * 50)

# Load original dataset
df = pd.read_csv(INPUT_PATH, encoding="utf-8-sig",
                 low_memory=False)

df.columns = df.columns.str.strip()

original_rows = len(df)

print("\nOriginal records:", original_rows)

# Step 1: Remove duplicate records
duplicates = df.duplicated().sum()
df = df.drop_duplicates()

print("Duplicates removed:", duplicates)

# Step 2: Replace infinite values
numeric_columns = df.select_dtypes(include="number").columns

infinite_count = np.isinf(df[numeric_columns]).sum().sum()

df[numeric_columns] = df[numeric_columns].replace(
    [np.inf, -np.inf], np.nan
)

print("Infinite values replaced:", infinite_count)

# Step 3: Check missing values
missing_before = df.isnull().sum().sum()

print("Missing values before cleaning:", missing_before)

# Step 4: Remove rows containing missing values
df = df.dropna()

print("Rows removed due to missing values:",
      original_rows - duplicates - len(df))

# Step 5: Save cleaned dataset
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_PATH, index=False)

# Final report
print("\nFINAL CLEANING REPORT")
print("-" * 40)

print("Original records:", original_rows)
print("Final records:", len(df))
print("Final columns:", len(df.columns))
print("Remaining missing values:", df.isnull().sum().sum())
print("Remaining duplicates:", df.duplicated().sum())

if "Label" in df.columns:
    print("\nFinal traffic distribution:")
    print(df["Label"].value_counts())

print("\nCleaned dataset saved successfully!")
print("Location:", OUTPUT_PATH)
