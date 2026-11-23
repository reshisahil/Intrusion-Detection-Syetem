
import csv
from collections import Counter


def inspect_dataset(file_path):

    with open(file_path, "r", encoding="utf-8-sig", newline="") as file:

        reader = csv.DictReader(file)

        columns = reader.fieldnames

        if not columns:
            raise ValueError("CSV file has no headers")

        total_records = 0
        label_counts = Counter()
        invalid_rows = 0

        for row in reader:

            if not any(value and value.strip() for value in row.values()):
                continue

            total_records += 1

            if None in row:
                invalid_rows += 1
                continue

            label = row.get("Label")

            if label:
                label_counts[label.strip()] += 1

    return {
        "total_records": total_records,
        "total_columns": len(columns),
        "columns": columns,
        "label_distribution": dict(label_counts),
        "invalid_rows": invalid_rows
    }
