
import numpy as np
from scipy.signal import butter, sosfilt
from scipy.fft import rfft, rfftfreq


class DSPProcessor:
    def __init__(self, sample_rate=1000):
        self.sample_rate = sample_rate

    def filter_signal(self, signal):
        sos = butter(
            4, [10, 400],
            btype="bandpass",
            fs=self.sample_rate,
            output="sos"
        )
        return sosfilt(sos, signal)

    def calculate_fft(self, signal):
        spectrum = np.abs(rfft(signal))
        frequencies = rfftfreq(
            len(signal), d=1 / self.sample_rate
        )
        return frequencies, spectrum

    def analyze(self, signal):
        filtered = self.filter_signal(signal)
        frequencies, spectrum = self.calculate_fft(filtered)

        dominant_index = np.argmax(spectrum)

        anomaly_band = (frequencies >= 200) & (frequencies <= 300)

        band_frequencies = frequencies[anomaly_band]
        band_spectrum = spectrum[anomaly_band]

        anomaly_index = np.argmax(band_spectrum)

        return {
            "dominant_peak": float(frequencies[dominant_index]),
            "anomaly_peak": float(band_frequencies[anomaly_index]),
            "anomaly_amplitude": float(band_spectrum[anomaly_index])
        }


if __name__ == "__main__":
    processor = DSPProcessor()

    time = np.arange(5000) / processor.sample_rate

    normal_signal = (
        np.sin(2 * np.pi * 50 * time)
        + np.sin(2 * np.pi * 120 * time)
        + np.random.normal(0, 0.2, len(time))
    )

    suspicious_signal = (
        normal_signal + np.sin(2 * np.pi * 250 * time)
    )

    normal = processor.analyze(normal_signal)
    suspicious = processor.analyze(suspicious_signal)

    print("\nAETHERHOUND DSP ANALYSIS")
    print("-" * 40)

    print("Normal dominant peak:", normal["dominant_peak"], "Hz")
    print("Normal anomaly-band peak:", normal["anomaly_peak"], "Hz")

    print("\nSuspicious dominant peak:", suspicious["dominant_peak"], "Hz")
    print("Suspicious anomaly-band peak:", suspicious["anomaly_peak"], "Hz")

    print("\nDSP frequency analysis completed.")
