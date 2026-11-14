
import numpy as np
import csv
from pathlib import Path


class VirtualSDR:
    def __init__(self, sample_rate=1000, duration=5):
        self.sample_rate = sample_rate
        self.duration = duration
        self.samples = sample_rate * duration
        self.time = np.arange(self.samples) / sample_rate

    def generate_normal_signal(self):
        """Simulate normal RF background noise."""
        noise = np.random.normal(0, 0.2, self.samples)

        background = (
            0.5 * np.sin(2 * np.pi * 50 * self.time)
            + 0.2 * np.sin(2 * np.pi * 120 * self.time)
        )

        return background + noise

    def generate_suspicious_signal(self):
        """Simulate an artificial RF frequency spike."""
        noise = np.random.normal(0, 0.2, self.samples)

        background = (
            0.5 * np.sin(2 * np.pi * 50 * self.time)
            + 0.2 * np.sin(2 * np.pi * 120 * self.time)
        )

        suspicious_spike = (
            1.5 * np.sin(2 * np.pi * 250 * self.time)
        )

        return background + noise + suspicious_spike

    def save_signal(self, signal, filename):
        output_path = Path("dataset/rf") / filename

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["sample"])

            for value in signal:
                writer.writerow([value])

        print(f"[+] Signal saved: {output_path}")


if __name__ == "__main__":
    sdr = VirtualSDR()

    normal_signal = sdr.generate_normal_signal()
    suspicious_signal = sdr.generate_suspicious_signal()

    sdr.save_signal(normal_signal, "normal_rf.csv")
    sdr.save_signal(suspicious_signal, "suspicious_rf.csv")

    print("\nVirtual SDR Simulation Completed!")
    print(f"Sample Rate: {sdr.sample_rate} Hz")
    print(f"Duration: {sdr.duration} seconds")
    print(f"Total Samples: {sdr.samples}")
