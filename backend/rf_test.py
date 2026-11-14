
from rf_detector import generate_rf_signal, detect_anomaly

normal, suspicious = generate_rf_signal()

print("Normal Signal Result:")
print(detect_anomaly(normal))

print("\nSuspicious Signal Result:")
print(detect_anomaly(suspicious))
