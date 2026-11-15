
import argparse
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    precision_score,
    recall_score,
    f1_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


# Project paths
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "processed" / "network_features.csv"
ML_DIR = Path(__file__).resolve().parent
MODEL_PATH = ML_DIR / "model.pkl"
EVALUATION_DIR = ML_DIR / "evaluation"


def train_model(data_path, target_column):

    print("[+] Loading processed dataset...")

    df = pd.read_csv(data_path)

    if target_column not in df.columns:
        raise ValueError(
            f"Target column '{target_column}' not found. "
            f"Available columns: {list(df.columns)}"
        )

    # Remove rows without labels
    df = df.dropna(subset=[target_column])

    X = df.drop(columns=[target_column])
    y = df[target_column]

    if X.empty:
        raise ValueError("Dataset contains no feature columns.")

    if y.nunique() < 2:
        raise ValueError("At least two target classes are required.")

    print(f"[+] Dataset shape: {df.shape}")
    print(f"[+] Features: {X.shape[1]}")
    print(f"[+] Classes: {list(y.unique())}")

    # Identify numeric and categorical columns
    numeric_features = X.select_dtypes(
        include=["number"]
    ).columns.tolist()

    categorical_features = X.select_dtypes(
        exclude=["number"]
    ).columns.tolist()

    # Preprocessing pipelines
    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median"))
    ])

    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    transformers = []

    if numeric_features:
        transformers.append(
            ("numeric", numeric_pipeline, numeric_features)
        )

    if categorical_features:
        transformers.append(
            ("categorical", categorical_pipeline, categorical_features)
        )

    preprocessor = ColumnTransformer(transformers=transformers)

    # Split before fitting preprocessing to prevent data leakage
    stratify_labels = y if y.value_counts().min() >= 2 else None

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=stratify_labels
    )

    print("[+] Training Random Forest model...")

    model = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(
            n_estimators=200,
            random_state=42,
            class_weight="balanced",
            n_jobs=-1
        ))
    ])

    model.fit(X_train, y_train)

    print("[+] Evaluating model...")

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(
        y_test, predictions, average="weighted", zero_division=0
    )
    recall = recall_score(
        y_test, predictions, average="weighted", zero_division=0
    )
    f1 = f1_score(
        y_test, predictions, average="weighted", zero_division=0
    )

    print("\n========== MODEL RESULTS ==========")
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-score:  {f1:.4f}")

    report = classification_report(
        y_test, predictions, zero_division=0
    )

    print("\nClassification Report:")
    print(report)

    # Save evaluation results
    EVALUATION_DIR.mkdir(parents=True, exist_ok=True)

    with open(
        EVALUATION_DIR / "classification_report.txt",
        "w",
        encoding="utf-8"
    ) as file:
        file.write("MODEL EVALUATION RESULTS\n\n")
        file.write(f"Accuracy: {accuracy:.4f}\n")
        file.write(f"Precision: {precision:.4f}\n")
        file.write(f"Recall: {recall:.4f}\n")
        file.write(f"F1-score: {f1:.4f}\n\n")
        file.write(report)

    # Generate confusion matrix
    cm = confusion_matrix(y_test, predictions)

    display = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=model.classes_
    )

    display.plot(cmap="Blues", xticks_rotation=45)
    plt.title("IDS - Random Forest Confusion Matrix")
    plt.tight_layout()

    plt.savefig(
        EVALUATION_DIR / "confusion_matrix.png",
        dpi=300
    )
    plt.close()

    # Save the complete preprocessing + model pipeline
    bundle = {
        "model": model,
        "feature_columns": X.columns.tolist(),
        "target_column": target_column,
        "classes": model.classes_.tolist()
    }

    joblib.dump(bundle, MODEL_PATH)

    print(f"\n[+] Model saved to: {MODEL_PATH}")
    print("[+] Evaluation files generated successfully.")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Train the IDS machine learning model"
    )

    parser.add_argument(
        "--data",
        default=str(DATA_PATH),
        help="Path to processed CSV dataset"
    )

    parser.add_argument(
        "--target",
        default="label",
        help="Name of the target/label column"
    )

    args = parser.parse_args()

    train_model(args.data, args.target)
