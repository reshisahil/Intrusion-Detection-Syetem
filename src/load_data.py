
from pathlib import Path
import pandas as pd
import numpy as np

# Project folder
PROJECT_DIR = Path(__file__).resolve().parents[1]

# Dataset location
DATASET_PATH = (
    PROJECT_DIR / "data" / "raw" /
    "Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"
)

print("=" * 55)
print(" AI-ASSISTED INTRUSION DETECTION SYSTEM")
print(" MEMBER 1 - DATASET INSPECTION")
print("=" * 55)

# Check whether dataset exists
if not DATASET_PATH.exists():
    raise FileNotFoundError(f"Dataset not found: {DATASET_PATH}")

# Load dataset
print("\nLoading dataset...")

df = pd.read_csv(DATASET_PATH, encoding="utf-8-sig", low_memory=False)

# Clean column names
df.columns = df.columns.str.strip()

# Display basic information
print("\n1. DATASET DIMENSIONS")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\n2. FIRST FIVE RECORDS")
print(df.head())

print("\n3. COLUMN NAMES")
print(df.columns.tolist())

# Check attack labels
print("\n4. ATTACK LABEL DISTRIBUTION")

if "Label" in df.columns:
    print(df["Label"].value_counts(dropna=False))
else:
    print("Label column not found!")

# Check missing values
print("\n5. MISSING VALUES")
print(df.isnull().sum().sum())

# Check duplicate records
print("\n6. DUPLICATE RECORDS")
print(df.duplicated().sum())

# Check infinite values
print("\n7. INFINITE VALUES")
print(np.isinf(df.select_dtypes(include="number")).sum().sum())

print("\n" + "=" * 55)
print(" DATASET INSPECTION COMPLETED!")
print("=" * 55)
