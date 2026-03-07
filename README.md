# BPI-Net
## Sparsh

A deep learning pipeline that estimates **Blood Pressure** from **PPG waveforms** and generates **12-lead ECG** signals conditioned on those BP values.

---

## Pipeline Overview

```
PPG Waveform → [Model 1] → Blood Pressure (SBP/DBP) → [Model 2] → 12-lead ECG
```

| Stage | Input | Output | Architecture |
|-------|-------|--------|--------------|
| Model 1 | PPG (625 samples @ 125 Hz) | SBP, DBP (mmHg) | CNN-BiLSTM + Attention |
| Model 2 | BP (SBP, DBP) | 12-lead ECG (1200 samples @ 100 Hz) | Conditional VAE |
| Pipeline | PPG | BP + 12-lead ECG | Combined + fine-tuned adapter |

---

## Datasets

| Dataset | Used For | Source |
|---------|----------|--------|
| **VitalDB** | PPG → BP training | [PhysioNet](https://doi.org/10.13026/czw8-9p62) |
| **Brugada-HUCA** | BP → ECG training | [PhysioNet](https://doi.org/10.13026/0m2w-dy83) |

---

## Project Structure

```
BPI-Net/
├── notebook1_ppg_to_bp.ipynb          # Model 1: PPG → BP
├── notebook2_bp_to_ecg.ipynb          # Model 2: BP → ECG
├── notebook3_combined_pipeline.ipynb  # End-to-end pipeline + fine-tuning
├── view_ecg.py                        # Utility to visualize Brugada-HUCA ECGs
├── requirements.txt
└── README.md
```

### Saved Artifacts (generated after training)

```
best_ppg_to_bp.pth               # Model 1 weights
best_bp_to_ecg.pth               # Model 2 weights
best_ppg_to_ecg_pipeline.pth     # Full pipeline weights
bp_scaler.pkl                    # BP StandardScaler
bp_bounds.pkl                    # BP normalization bounds
ppg_bp_cache.pkl                 # Cached VitalDB PPG/BP windows
```

---

## Setup

```bash
pip install -r requirements.txt
```

---

## Usage

### Run notebooks in order

1. `notebook1_ppg_to_bp.ipynb` — trains and saves Model 1
2. `notebook2_bp_to_ecg.ipynb` — trains and saves Model 2
3. `notebook3_combined_pipeline.ipynb` — assembles and fine-tunes the full pipeline

### Inference

```python
from pipeline import ppg_to_ecg
import numpy as np

ppg_window = np.load('sample_ppg.npy')   # 625 samples @ 125 Hz
result = ppg_to_ecg(ppg_window)

print(f"SBP: {result['SBP']} mmHg")
print(f"DBP: {result['DBP']} mmHg")
print(f"ECG shape: {result['ECG'].shape}")  # (12, 1200)
```

### Visualize ECG data

```bash
python view_ecg.py
```

---

## Requirements

- Python 3.10+
- PyTorch (CUDA recommended for training)
- See `requirements.txt` for full list

---

## References

- Lee, H., & Jung, C. (2022). VitalDB. *PhysioNet*. https://doi.org/10.13026/czw8-9p62
- Costa Cortez, N., & Garcia Iglesias, D. (2026). Brugada-HUCA. *PhysioNet*. https://doi.org/10.13026/0m2w-dy83
