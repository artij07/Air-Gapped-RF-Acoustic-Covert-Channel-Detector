
import numpy as np
from scipy.signal import butter, sosfilt
from scipy.fft import rfft, rfftfreq


class DSPProcessor:
    """Digital signal processing for simulated RF signals."""

    def __init__(self, sample_rate=1000):
        self.sample_rate = sample_rate

    def filter_signal(self, signal, low=10, high=400):
        """Apply Butterworth bandpass filtering."""
        sos = butter(
            4,
            [low, high],
            btype="bandpass",
            fs=self.sample_rate,
            output="sos"
        )
        return sosfilt(sos, signal)

    def calculate_fft(self, signal):
        """Calculate frequency spectrum using FFT."""
        spectrum = np.abs(rfft(signal))
        frequencies = rfftfreq(
            len(signal),
            d=1 / self.sample_rate
        )
        return frequencies, spectrum

    def analyze(self, signal):
        """Filter and analyze an RF signal."""
        filtered = self.filter_signal(signal)
        frequencies, spectrum = self.calculate_fft(filtered)

        peak_index = np.argmax(spectrum)

        return {
            "filtered_signal": filtered,
            "peak_frequency": float(frequencies[peak_index]),
            "peak_amplitude": float(spectrum[peak_index]),
            "frequencies": frequencies,
            "spectrum": spectrum
        }


if __name__ == "__main__":
    processor = DSPProcessor()

    time = np.arange(5000) / processor.sample_rate

    normal_signal = (
        np.sin(2 * np.pi * 50 * time)
        + np.sin(2 * np.pi * 120 * time)
        + np.random.normal(0, 0.2, len(time))
    )

    suspicious_signal = normal_signal + np.sin(
        2 * np.pi * 250 * time
    )

    normal_result = processor.analyze(normal_signal)
    suspicious_result = processor.analyze(suspicious_signal)

    print("\nAETHERHOUND DSP ANALYSIS")
    print("-" * 35)
    print("Normal RF peak:",
          normal_result["peak_frequency"], "Hz")
    print("Suspicious RF peak:",
          suspicious_result["peak_frequency"], "Hz")
    print("DSP processing completed successfully.")
