
import json
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import spectrogram


ROOT = Path(__file__).resolve().parent.parent
AUDIO_DIR = ROOT / "dataset" / "acoustic"
REPORT_DIR = ROOT / "reports"


class AcousticAnomalyDetector:

    def analyze(self, filename):
        audio, sample_rate = sf.read(AUDIO_DIR / filename)

        frequencies, times, power = spectrogram(
            audio,
            fs=sample_rate,
            nperseg=1024,
            noverlap=512
        )

        # Analyze energy near artificial 1000 Hz frequency
        target_band = (frequencies >= 950) & (frequencies <= 1050)
        target_power = power[target_band, :]

        # Calculate energy in each time window
        window_energy = np.sum(target_power, axis=0)

        threshold = 0.0005

        active_windows = window_energy > threshold

        # Find consecutive active windows
        pulse_count = np.sum(
            active_windows[1:] & ~active_windows[:-1]
        )

        suspicious = pulse_count >= 3

        return {
            "status": "SUSPICIOUS" if suspicious else "NORMAL",
            "pulse_count": int(pulse_count),
            "target_frequency_hz": 1000,
            "active_windows": int(np.sum(active_windows))
        }


if __name__ == "__main__":
    detector = AcousticAnomalyDetector()

    results = {}

    for filename in [
        "normal_audio.wav",
        "suspicious_audio.wav"
    ]:
        result = detector.analyze(filename)
        results[filename] = result

        print(f"\nFile: {filename}")
        print(f"Status: {result['status']}")
        print(f"Pulse Count: {result['pulse_count']}")

    REPORT_DIR.mkdir(exist_ok=True)

    report_path = REPORT_DIR / "acoustic_detection_report.json"

    with open(report_path, "w") as file:
        json.dump(results, file, indent=4)

    print(f"\n[+] Acoustic report saved: {report_path}")
