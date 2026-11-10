# AetherHound: Air-Gapped RF & Acoustic Covert Channel Detector

**Infotact Solutions Internship – Project 1**

## Overview

AetherHound is a simulation-based cybersecurity project designed to demonstrate the detection of potential covert communication channels in air-gapped systems using Radio Frequency (RF) and acoustic signal analysis.

The project simulates virtual RF and acoustic sensor data, processes signals using Digital Signal Processing (DSP) techniques, and identifies suspicious frequency patterns that may indicate covert data transmission.

This project focuses on building a software-based prototype without requiring physical SDR devices, microphones, or other hardware components.

## Objectives

- Simulate RF signals and acoustic emissions from virtual air-gapped servers.
- Generate normal and suspicious RF and audio datasets.
- Analyze signals using FFT and spectrogram visualization.
- Detect anomalous RF frequency spikes.
- Identify suspicious acoustic frequency patterns.
- Combine RF and acoustic detection results into a unified threat report.
- Develop a simulation-based foundation for future ML anomaly detection.

## System Architecture

Virtual Air-Gapped Server  
↓  
Virtual SDR & Virtual Microphone  
↓  
RF and Acoustic Signal Generation  
↓  
Digital Signal Processing  
↓  
Anomaly Detection  
↓  
Combined Threat Monitoring  
↓  
Detection Reports & Visualizations

## Technologies Used

- Python
- NumPy
- SciPy
- Matplotlib
- SoundFile
- Rich
- CSV
- JSON
- WAV

## Project Structure

```text
AetherHound/
│
├── backend/
│   ├── rf_detector.py
│   └── rf_test.py
│
├── simulation/
│   ├── virtual_sdr.py
│   ├── virtual_microphone.py
│   ├── visualize_signals.py
│   ├── rf_anomaly_detector.py
│   ├── acoustic_anomaly_detector.py
│   └── combined_monitor.py
│
├── dataset/
│   ├── rf/
│   │   ├── normal_rf.csv
│   │   └── suspicious_rf.csv
│   └── acoustic/
│       ├── normal_audio.wav
│       └── suspicious_audio.wav
│
├── reports/
│   ├── rf_fft_comparison.png
│   ├── normal_audio_spectrogram.png
│   ├── suspicious_audio_spectrogram.png
│   ├── rf_detection_report.json
│   ├── acoustic_detection_report.json
│   └── combined_detection_report.json
│
├── documentation/
│   └── Week1_Progress.md
│
├── logs/
├── models/
├── .venv/
└── README.md
```

## Week 1 – Implementation Progress

### Completed Modules

- Virtual SDR signal simulation
- Virtual microphone acoustic simulation
- Normal and suspicious signal generation
- RF FFT visualization
- Acoustic spectrogram visualization
- RF anomaly detection
- Acoustic anomaly detection
- Combined threat monitoring
- JSON-based detection reports

### Sample Detection Results

| Signal | Detection |
|---|---|
| Normal RF | NORMAL |
| Suspicious RF | SUSPICIOUS |
| Normal Acoustic | NORMAL |
| Suspicious Acoustic | SUSPICIOUS |

## Simulation Details

The RF simulation generates synthetic signals containing normal frequency components and introduces an additional suspicious frequency component to represent a potential covert RF channel.

The acoustic simulation generates virtual server fan noise and introduces pulse-based frequency patterns representing a simulated acoustic covert channel.

The detection modules analyze these synthetic signals and classify them using predefined frequency and energy thresholds.

**Note:** These results are generated from controlled simulation datasets and do not represent measurements from real air-gapped systems.

## Project Development Roadmap

- [x] Week 1 – Virtual Sensor Simulation & Basic Anomaly Detection
- [ ] Week 2 – Digital Signal Processing & RF Waterfall Visualization
- [ ] Week 3 – ML-Based Anomaly Detection using Autoencoder
- [ ] Week 4 – Integration, Optimization & Final Demonstration

## Internship

**Organization:** Infotact Solutions  
**Project:** AetherHound – Project 1  
**Domain:** Cybersecurity | Hardware Security | Signal Intelligence (SIGINT)

## Disclaimer

AetherHound is an educational and internship project developed for cybersecurity research and demonstration purposes. It uses simulated RF and acoustic signals and does not require physical hardware for its current implementation.

---

Developed as part of the Infotact Solutions Internship Program.
