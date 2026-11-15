
import argparse
from pathlib import Path

import joblib
import pandas as pd


ML_DIR = Path(__file__).resolve().parent
MODEL_PATH = ML_DIR / "model.pkl"


def predict_attacks(input_file):

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Trained model not found. Run train_model.py first."
        )

    print("[+] Loading trained IDS model...")

    bundle = joblib.load(MODEL_PATH)

    model = bundle["model"]
    feature_columns = bundle["feature_columns"]

    print("[+] Loading new network data...")

    data = pd.read_csv(input_file)

    # Check that all expected features are available
    missing_columns = [
        col for col in feature_columns
        if col not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required features: {missing_columns}"
        )

    # Keep the same feature order used during training
    data = data[feature_columns]

    predictions = model.predict(data)

    results = data.copy()
    results["prediction"] = predictions

    # Add prediction probabilities when supported
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(data)

        results["confidence"] = probabilities.max(axis=1)

    output_file = Path(input_file).with_name(
        "prediction_results.csv"
    )

    results.to_csv(output_file, index=False)

    print("\n========== PREDICTION RESULTS ==========")

    for index, prediction in enumerate(predictions):
        print(f"Record {index + 1}: {prediction}")

    print(f"\n[+] Results saved to: {output_file}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Predict suspicious network activity"
    )

    parser.add_argument(
        "--input",
        required=True,
        help="CSV file containing network features"
    )

    args = parser.parse_args()

    predict_attacks(args.input)
