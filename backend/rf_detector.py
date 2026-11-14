
import numpy as np
from scipy.fft import fft, fftfreq


def generate_rf_signal(sampling_rate=1000, duration=1):
    t = np.linspace(
        0, duration, sampling_rate * duration,
        endpoint=False
    )

    noise = np.random.normal(0, 0.1, len(t))

    normal_signal = np.sin(2 * np.pi * 50 * t) + noise

    suspicious_signal = (
        np.sin(2 * np.pi * 50 * t)
        + 0.8 * np.sin(2 * np.pi * 200 * t)
        + noise
    )

    return normal_signal, suspicious_signal


def analyze_signal(signal, sampling_rate=1000):
    signal = np.asarray(signal)

    energy = np.mean(signal ** 2)

    spectrum = np.abs(fft(signal))
    frequencies = fftfreq(len(signal), 1 / sampling_rate)

    positive = frequencies > 0
    frequencies = frequencies[positive]
    spectrum = spectrum[positive]

    dominant_frequency = frequencies[np.argmax(spectrum)]

    # Detect significant frequency components
    threshold = np.max(spectrum) * 0.30

    significant = spectrum > threshold
    detected_frequencies = frequencies[significant]

    unusual_frequencies = detected_frequencies[
        detected_frequencies > 100
    ]

    return {
        "energy": round(float(energy), 4),
        "dominant_frequency": round(float(dominant_frequency), 2),
        "significant_frequencies": np.round(
            detected_frequencies, 2
        ).tolist(),
        "unusual_frequency_count": len(unusual_frequencies)
    }


def detect_anomaly(signal, sampling_rate=1000):
    result = analyze_signal(signal, sampling_rate)

    if result["unusual_frequency_count"] > 0:
        result["status"] = "SUSPICIOUS"
        result["risk_score"] = 80
    else:
        result["status"] = "NORMAL"
        result["risk_score"] = 10

    return result


if __name__ == "__main__":
    normal, suspicious = generate_rf_signal()

    print("\n--- NORMAL SIGNAL ---")
    print(detect_anomaly(normal))

    print("\n--- SUSPICIOUS SIGNAL ---")
    print(detect_anomaly(suspicious))
