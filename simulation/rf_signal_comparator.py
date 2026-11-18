
import json
from pathlib import Path

import numpy as np


SAMPLE_RATE = 1000
DURATION = 5
ANOMALY_LOW = 200
ANOMALY_HIGH = 300
ANOMALY_THRESHOLD = 0.05


def generate_signals():
    rng = np.random.default_rng(42)

    sample_count = SAMPLE_RATE * DURATION
    time_axis = np.arange(sample_count) / SAMPLE_RATE

    normal_signal = (
        np.sin(2 * np.pi * 50 * time_axis)
        + np.sin(2 * np.pi * 120 * time_axis)
        + rng.normal(0, 0.2, sample_count)
    )

    suspicious_signal = (
        normal_signal
        + np.sin(2 * np.pi * 250 * time_axis)
    )

    return normal_signal, suspicious_signal


def measure_anomaly_band(signal):
    window = np.hanning(len(signal))

    spectrum = np.abs(
        np.fft.rfft(signal * window)
    ) * 2 / np.sum(window)

    frequencies = np.fft.rfftfreq(
        len(signal), d=1 / SAMPLE_RATE
    )

    band_mask = (
        (frequencies >= ANOMALY_LOW)
        & (frequencies <= ANOMALY_HIGH)
    )

    band_frequencies = frequencies[band_mask]
    band_amplitudes = spectrum[band_mask]

    peak_index = np.argmax(band_amplitudes)

    return {
        "peak_frequency_hz": float(band_frequencies[peak_index]),
        "peak_amplitude": float(band_amplitudes[peak_index]),
        "status": (
            "SUSPICIOUS"
            if band_amplitudes[peak_index] > ANOMALY_THRESHOLD
            else "NORMAL"
        )
    }


def main():
    normal_signal, suspicious_signal = generate_signals()

    normal_result = measure_anomaly_band(normal_signal)
    suspicious_result = measure_anomaly_band(suspicious_signal)

    report = {
        "project": "AetherHound",
        "analysis_band_hz": [
            ANOMALY_LOW,
            ANOMALY_HIGH
        ],
        "threshold": ANOMALY_THRESHOLD,
        "normal_signal": normal_result,
        "suspicious_signal": suspicious_result
    }

    print("\nAETHERHOUND RF SIGNAL COMPARATOR")
    print("=" * 42)

    for name, result in [
        ("NORMAL SIGNAL", normal_result),
        ("SUSPICIOUS SIGNAL", suspicious_result)
    ]:
        print(f"\n{name}")
        print("Peak frequency:", result["peak_frequency_hz"], "Hz")
        print("Peak amplitude:", round(result["peak_amplitude"], 5))
        print("Detection status:", result["status"])

    Path("reports").mkdir(exist_ok=True)

    report_path = Path("reports/rf_comparison_report.json")
    report_path.write_text(
        json.dumps(report, indent=4),
        encoding="utf-8"
    )

    print("\nReport saved:", report_path)
    print("RF comparison completed.")


if __name__ == "__main__":
    main()
