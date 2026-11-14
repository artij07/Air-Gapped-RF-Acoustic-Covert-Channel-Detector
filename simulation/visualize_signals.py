
import csv
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
from scipy.signal import spectrogram


ROOT = Path(__file__).resolve().parent.parent
RF_DIR = ROOT / "dataset" / "rf"
AUDIO_DIR = ROOT / "dataset" / "acoustic"
REPORT_DIR = ROOT / "reports"

REPORT_DIR.mkdir(exist_ok=True)


def load_rf(filename):
    with open(RF_DIR / filename, newline="") as file:
        reader = csv.DictReader(file)
        return np.array([float(row["sample"]) for row in reader])


def plot_rf_fft():
    normal = load_rf("normal_rf.csv")
    suspicious = load_rf("suspicious_rf.csv")

    sample_rate = 1000

    normal_fft = np.abs(np.fft.rfft(normal))
    suspicious_fft = np.abs(np.fft.rfft(suspicious))

    frequencies = np.fft.rfftfreq(len(normal), 1 / sample_rate)

    plt.figure(figsize=(12, 5))
    plt.plot(frequencies, normal_fft, label="Normal RF")
    plt.plot(frequencies, suspicious_fft, label="Suspicious RF")

    plt.title("Virtual SDR - RF Frequency Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("FFT Amplitude")
    plt.xlim(0, 400)
    plt.legend()
    plt.grid(True)

    plt.savefig(REPORT_DIR / "rf_fft_comparison.png", dpi=150)
    plt.close()

    print("[+] RF FFT graph saved")


def plot_audio_spectrogram(filename, output_name):
    audio, sample_rate = sf.read(AUDIO_DIR / filename)

    frequencies, times, power = spectrogram(
        audio,
        fs=sample_rate,
        nperseg=1024,
        noverlap=512
    )

    plt.figure(figsize=(12, 5))

    plt.pcolormesh(
        times,
        frequencies,
        10 * np.log10(power + 1e-12),
        shading="auto",
        cmap="inferno"
    )

    plt.title(filename.replace("_", " ").title())
    plt.xlabel("Time (seconds)")
    plt.ylabel("Frequency (Hz)")
    plt.ylim(0, 3000)
    plt.colorbar(label="Power (dB)")

    plt.savefig(REPORT_DIR / output_name, dpi=150)
    plt.close()

    print(f"[+] Spectrogram saved: {output_name}")


if __name__ == "__main__":
    plot_rf_fft()

    plot_audio_spectrogram(
        "normal_audio.wav",
        "normal_audio_spectrogram.png"
    )

    plot_audio_spectrogram(
        "suspicious_audio.wav",
        "suspicious_audio_spectrogram.png"
    )

    print("\nAll signal visualizations completed!")
