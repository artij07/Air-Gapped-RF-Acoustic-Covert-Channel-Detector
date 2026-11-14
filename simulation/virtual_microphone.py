
import numpy as np
import soundfile as sf
from pathlib import Path


class VirtualMicrophone:
    def __init__(self, sample_rate=16000, duration=5):
        self.sample_rate = sample_rate
        self.duration = duration
        self.samples = sample_rate * duration
        self.time = np.arange(self.samples) / sample_rate

    def generate_normal_audio(self):
        """Simulate normal server fan noise."""
        fan_noise = (
            0.4 * np.sin(2 * np.pi * 120 * self.time)
            + 0.2 * np.sin(2 * np.pi * 240 * self.time)
        )

        noise = np.random.normal(0, 0.05, self.samples)

        return fan_noise + noise

    def generate_suspicious_audio(self):
        """Simulate fan audio with artificial Morse-like pulses."""
        audio = self.generate_normal_audio()

        # Artificial pulse pattern: ON, OFF, ON, OFF
        pulse_pattern = [1, 0, 1, 0, 1, 1, 1, 0]

        pulse_duration = 0.25
        pulse_samples = int(pulse_duration * self.sample_rate)

        for index, pulse in enumerate(pulse_pattern):
            start = index * pulse_samples
            end = start + pulse_samples

            if end > self.samples:
                break

            if pulse == 1:
                audio[start:end] += (
                    0.8 * np.sin(2 * np.pi * 1000 * self.time[start:end])
                )

        return audio

    def save_audio(self, audio, filename):
        output_path = Path("dataset/acoustic") / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Prevent clipping in the generated audio
        audio = np.clip(audio, -1.0, 1.0)

        sf.write(output_path, audio, self.sample_rate)

        print(f"[+] Audio saved: {output_path}")


if __name__ == "__main__":
    mic = VirtualMicrophone()

    normal_audio = mic.generate_normal_audio()
    suspicious_audio = mic.generate_suspicious_audio()

    mic.save_audio(normal_audio, "normal_audio.wav")
    mic.save_audio(suspicious_audio, "suspicious_audio.wav")

    print("\nVirtual Microphone Simulation Completed!")
    print(f"Sample Rate: {mic.sample_rate} Hz")
    print(f"Duration: {mic.duration} seconds")
    print(f"Total Samples: {mic.samples}")
