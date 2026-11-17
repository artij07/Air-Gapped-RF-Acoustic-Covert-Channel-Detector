
import time
import numpy as np
from rich.live import Live
from rich.table import Table
from rich.text import Text


SAMPLE_RATE = 1000
FFT_SIZE = 512
FRAMES = 30


def generate_rf_frame(frame_number):
    time_axis = np.arange(FFT_SIZE) / SAMPLE_RATE

    normal_signal = (
        np.sin(2 * np.pi * 50 * time_axis)
        + np.sin(2 * np.pi * 120 * time_axis)
        + np.random.normal(0, 0.15, FFT_SIZE)
    )

    suspicious_signal = np.sin(
        2 * np.pi * 250 * time_axis
    ) * (0.8 if frame_number >= 15 else 0)

    return normal_signal + suspicious_signal


def analyze_frame(signal):
    window = np.hanning(len(signal))
    spectrum = np.abs(np.fft.rfft(signal * window))
    frequencies = np.fft.rfftfreq(
        len(signal), d=1 / SAMPLE_RATE
    )

    band = (frequencies >= 200) & (frequencies <= 300)

    band_frequencies = frequencies[band]
    band_amplitudes = spectrum[band]

    peak_index = np.argmax(band_amplitudes)

    return (
        float(band_frequencies[peak_index]),
        float(band_amplitudes[peak_index])
    )


def build_display(history, frame_number):
    table = Table(title="AETHERHOUND - LIVE RF WATERFALL")
    table.add_column("Frame", justify="right")
    table.add_column("Frequency", justify="right")
    table.add_column("Band Activity")
    table.add_column("Status")

    for number, frequency, amplitude in history:
        bar_length = min(int(amplitude * 5), 30)
        bar = "█" * bar_length

        if amplitude > 10:
            status = Text("SUSPICIOUS", style="bold red")
        else:
            status = Text("NORMAL", style="green")

        table.add_row(
            str(number),
            f"{frequency:.1f} Hz",
            bar,
            status
        )

    table.caption = (
        f"Frame {frame_number}/{FRAMES} | "
        "Simulated data only - no physical SDR"
    )

    return table


def run_waterfall():
    history = []

    with Live(refresh_per_second=8) as live:
        for frame in range(1, FRAMES + 1):
            signal = generate_rf_frame(frame)

            frequency, amplitude = analyze_frame(signal)

            history.append((frame, frequency, amplitude))
            history = history[-10:]

            live.update(build_display(history, frame))

            time.sleep(0.3)

    print("\nRF waterfall simulation completed.")


if __name__ == "__main__":
    run_waterfall()
