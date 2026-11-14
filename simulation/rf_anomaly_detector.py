
import csv
import json
from pathlib import Path

import numpy as np
from scipy.signal import find_peaks


ROOT = Path(__file__).resolve().parent.parent
RF_DIR = ROOT / "dataset" / "rf"
REPORT_DIR = ROOT / "reports"


class RFAnomalyDetector:

    def __init__(self, sample_rate=1000):
        self.sample_rate = sample_rate

    def load_signal(self, filename):
        with open(RF_DIR / filename, newline="") as file:
            reader = csv.DictReader(file)
            return np.array(
                [float(row["sample"]) for row in reader]
            )

    def analyze(self, signal):
        signal = signal - np.mean(signal)

        fft_values = np.abs(np.fft.rfft(signal))
        fft_values = fft_values / len(signal) * 2

        frequencies = np.fft.rfftfreq(
            len(signal),
            1 / self.sample_rate
        )

        peaks, _ = find_peaks(fft_values, height=0.1)

        detected_peaks = []

        for peak in peaks:
            frequency = float(frequencies[peak])
            amplitude = float(fft_values[peak])

            detected_peaks.append({
                "frequency_hz": round(frequency, 2),
                "amplitude": round(amplitude, 3)
            })

        suspicious_spike = any(
            abs(item["frequency_hz"] - 250) <= 2
            and item["amplitude"] > 0.5
            for item in detected_peaks
        )

        status = "SUSPICIOUS" if suspicious_spike else "NORMAL"

        return {
            "status": status,
            "suspicious_frequency_detected": suspicious_spike,
            "detected_peaks": detected_peaks
        }


if __name__ == "__main__":
    detector = RFAnomalyDetector()

    results = {}

    for filename in [
        "normal_rf.csv",
        "suspicious_rf.csv"
    ]:
        signal = detector.load_signal(filename)
        result = detector.analyze(signal)

        results[filename] = result

        print(f"\nFile: {filename}")
        print(f"Status: {result['status']}")
        print(f"Detected Peaks: {result['detected_peaks']}")

    REPORT_DIR.mkdir(exist_ok=True)

    report_path = REPORT_DIR / "rf_detection_report.json"

    with open(report_path, "w") as file:
        json.dump(results, file, indent=4)

    print(f"\n[+] Detection report saved: {report_path}")
