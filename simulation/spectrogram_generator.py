
import csv
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt

from pathlib import Path
from scipy.signal import spectrogram


# ==========================================
# AETHERHOUND - SPECTROGRAM GENERATOR
# ==========================================

ROOT = Path(__file__).resolve().parent.parent

RF_DIR = ROOT / "dataset" / "rf"
AUDIO_DIR = ROOT / "dataset" / "acoustic"

OUTPUT_DIR = ROOT / "reports" / "spectrograms"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RF_SAMPLE_RATE = 1000


def load_rf_signal(csv_path):
    """Load RF samples from a CSV file."""

    samples = []

    with open(csv_path, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            samples.append(float(row["sample"]))

    return np.array(samples, dtype=float)


def generate_spectrogram(signal, sample_rate, label, signal_type):
    """Generate spectrogram matrix, axes and PNG plot."""

    if len(signal) == 0:
        raise ValueError(f"{label} {signal_type} signal is empty.")

    nperseg = 256 if signal_type == "RF" else 1024
    nperseg = min(nperseg, len(signal))

    frequencies, times, power = spectrogram(
        signal,
        fs=sample_rate,
        window="hann",
        nperseg=nperseg,
        noverlap=nperseg // 2,
        scaling="density",
        mode="psd"
    )

    # Convert power into decibels
    power_db = 10 * np.log10(power + 1e-12)

    # Save spectrogram matrix
    matrix_path = (
        OUTPUT_DIR /
        f"{label}_{signal_type.lower()}_matrix.npy"
    )

    np.save(matrix_path, power_db)

    # Save frequency and time axes
    axes_path = (
        OUTPUT_DIR /
        f"{label}_{signal_type.lower()}_axes.npz"
    )

    np.savez(
        axes_path,
        frequencies=frequencies,
        times=times
    )

    # Generate spectrogram visualization
    plt.figure(figsize=(10, 5))

    plt.pcolormesh(
        times,
        frequencies,
        power_db,
        shading="auto",
        cmap="viridis"
    )

    plt.title(f"{label.title()} {signal_type} Spectrogram")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Frequency (Hz)")

    plt.colorbar(label="Power (dB)")

    plt.tight_layout()

    image_path = (
        OUTPUT_DIR /
        f"{label}_{signal_type.lower()}_spectrogram.png"
    )

    plt.savefig(image_path, dpi=150)
    plt.close()

    print(f"\n{label.upper()} {signal_type}")
    print("-" * 35)
    print(f"Samples: {len(signal)}")
    print(f"Sample Rate: {sample_rate} Hz")
    print(f"Matrix Shape: {power_db.shape}")
    print(f"Matrix: {matrix_path.name}")
    print(f"Plot: {image_path.name}")

    return power_db


def process_rf_signals():
    """Process normal and suspicious RF datasets."""

    print("\nPROCESSING RF SIGNALS")

    for label in ["normal", "suspicious"]:

        csv_path = RF_DIR / f"{label}_rf.csv"

        signal = load_rf_signal(csv_path)

        generate_spectrogram(
            signal=signal,
            sample_rate=RF_SAMPLE_RATE,
            label=label,
            signal_type="RF"
        )


def process_acoustic_signals():
    """Process normal and suspicious acoustic datasets."""

    print("\nPROCESSING ACOUSTIC SIGNALS")

    for label in ["normal", "suspicious"]:

        wav_path = AUDIO_DIR / f"{label}_audio.wav"

        signal, sample_rate = sf.read(wav_path)

        # Convert stereo audio to mono if necessary
        if signal.ndim > 1:
            signal = np.mean(signal, axis=1)

        generate_spectrogram(
            signal=signal,
            sample_rate=sample_rate,
            label=label,
            signal_type="Acoustic"
        )


def main():

    print("\n" + "=" * 50)
    print("AETHERHOUND - SPECTROGRAM GENERATION")
    print("=" * 50)

    process_rf_signals()
    process_acoustic_signals()

    print("\n" + "=" * 50)
    print("ALL SPECTROGRAMS GENERATED SUCCESSFULLY")
    print("=" * 50)

    print(f"\nOutput Directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
