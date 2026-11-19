
import unittest

from simulation.rf_signal_comparator import (
    generate_signals,
    measure_anomaly_band
)


class TestRFSignalComparator(unittest.TestCase):

    def setUp(self):
        self.normal_signal, self.suspicious_signal = generate_signals()

    def test_normal_signal_detection(self):
        result = measure_anomaly_band(self.normal_signal)

        self.assertEqual(result["status"], "NORMAL")

    def test_suspicious_signal_detection(self):
        result = measure_anomaly_band(self.suspicious_signal)

        self.assertEqual(result["status"], "SUSPICIOUS")

    def test_anomaly_frequency(self):
        result = measure_anomaly_band(self.suspicious_signal)

        self.assertAlmostEqual(
            result["peak_frequency_hz"],
            250.0,
            delta=1.0
        )

    def test_suspicious_signal_has_higher_amplitude(self):
        normal = measure_anomaly_band(self.normal_signal)
        suspicious = measure_anomaly_band(self.suspicious_signal)

        self.assertGreater(
            suspicious["peak_amplitude"],
            normal["peak_amplitude"]
        )

    def test_result_contains_required_fields(self):
        result = measure_anomaly_band(self.normal_signal)

        self.assertIn("peak_frequency_hz", result)
        self.assertIn("peak_amplitude", result)
        self.assertIn("status", result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
