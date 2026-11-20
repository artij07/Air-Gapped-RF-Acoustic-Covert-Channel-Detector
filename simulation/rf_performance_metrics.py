
import json
from pathlib import Path

import numpy as np

from rf_signal_comparator import measure_anomaly_band

SAMPLE_RATE = 1000
DURATION = 5
TEST_SAMPLES = 20


def generate_evaluation_dataset():
    rng = np.random.default_rng(42)
    time_axis = np.arange(SAMPLE_RATE * DURATION) / SAMPLE_RATE

    signals = []
    actual_labels = []

    for index in range(TEST_SAMPLES):
        signal = (
            np.sin(2 * np.pi * 50 * time_axis)
            + np.sin(2 * np.pi * 120 * time_axis)
            + rng.normal(0, 0.2, len(time_axis))
        )

        if index >= TEST_SAMPLES // 2:
            signal += np.sin(2 * np.pi * 250 * time_axis)

        signals.append(signal)
        actual_labels.append(1 if index >= TEST_SAMPLES // 2 else 0)

    return signals, actual_labels


def calculate_metrics(actual, predicted):
    tp = sum(a == 1 and p == 1 for a, p in zip(actual, predicted))
    tn = sum(a == 0 and p == 0 for a, p in zip(actual, predicted))
    fp = sum(a == 0 and p == 1 for a, p in zip(actual, predicted))
    fn = sum(a == 1 and p == 0 for a, p in zip(actual, predicted))

    total = len(actual)

    accuracy = (tp + tn) / total if total else 0
    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0

    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) else 0
    )

    return {
        "total_samples": total,
        "true_positive": tp,
        "true_negative": tn,
        "false_positive": fp,
        "false_negative": fn,
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4)
    }


def main():
    signals, actual_labels = generate_evaluation_dataset()

    predicted_labels = []

    for signal in signals:
        result = measure_anomaly_band(signal)
        predicted_labels.append(
            1 if result["status"] == "SUSPICIOUS" else 0
        )

    metrics = calculate_metrics(actual_labels, predicted_labels)

    report = {
        "project": "AetherHound",
        "evaluation_type": "Synthetic RF signal evaluation",
        "metrics": metrics
    }

    Path("reports").mkdir(exist_ok=True)

    output_path = Path("reports/rf_performance_report.json")
    output_path.write_text(
        json.dumps(report, indent=4),
        encoding="utf-8"
    )

    print("\nAETHERHOUND - RF PERFORMANCE EVALUATION")
    print("=" * 45)

    for key, value in metrics.items():
        print(f"{key.replace('_', ' ').title()}: {value}")

    print("\nReport saved:", output_path)
    print("Performance evaluation completed.")


if __name__ == "__main__":
    main()
