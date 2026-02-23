import os
import pandas as pd
import wfdb
import matplotlib.pyplot as plt

# =============================================================================
# Configuration – adapt these paths to match your folder structure
# =============================================================================
# The root folder that contains both 'files' and 'metadata.csv'
base_dir = r"D:\BPI-Net\brugada-huca-12-lead-ecg-recordings-for-the-study-of-brugada-syndrome-1.0.0\brugada-huca-12-lead-ecg-recordings-for-the-study-of-brugada-syndrome-1.0.0"
data_dir = os.path.join(base_dir, "files")
metadata_path = os.path.join(base_dir, "metadata.csv")

# =============================================================================
# Load metadata
# =============================================================================
try:
    metadata = pd.read_csv(metadata_path)
    print("Metadata loaded successfully.")
except FileNotFoundError:
    print(f"ERROR: metadata.csv not found at {metadata_path}")
    exit(1)

# =============================================================================
# Get list of available patient IDs (folder names)
# =============================================================================
if not os.path.isdir(data_dir):
    print(f"ERROR: data directory not found at {data_dir}")
    exit(1)

patient_ids = [d for d in os.listdir(data_dir) 
               if os.path.isdir(os.path.join(data_dir, d)) and d.isdigit()]
patient_ids.sort()

print(f"\nFound {len(patient_ids)} patient folders.")

# =============================================================================
# Interactive selection
# =============================================================================
while True:
    print("\n--- Available patient IDs (first 20 shown) ---")
    print(patient_ids[:20])   # show only first 20 to avoid clutter
    if len(patient_ids) > 20:
        print("(list truncated)")

    chosen = input("\nEnter a patient ID (or 'q' to quit): ").strip()
    if chosen.lower() == 'q':
        break

    if chosen not in patient_ids:
        print(f"Patient ID '{chosen}' not found. Please try again.")
        continue

    # =========================================================================
    # Load the ECG record
    # =========================================================================
    record_path = os.path.join(data_dir, chosen, chosen)
    try:
        record = wfdb.rdrecord(record_path)
    except Exception as e:
        print(f"Error reading record: {e}")
        continue

    # =========================================================================
    # Display metadata for this patient
    # =========================================================================
    patient_meta = metadata[metadata['patient_id'] == int(chosen)]
    if patient_meta.empty:
        print(f"No metadata found for patient {chosen}.")
    else:
        print("\n--- Metadata ---")
        print(patient_meta.to_string(index=False))

    # =========================================================================
    # Plot all 12 leads
    # =========================================================================
    signals = record.p_signal          # shape (samples, 12)
    lead_names = record.sig_name        # list of 12 lead names
    fs = record.fs                      # sampling frequency (100 Hz)

    time = [i / fs for i in range(signals.shape[0])]   # time in seconds

    fig, axes = plt.subplots(4, 3, figsize=(15, 10))
    fig.suptitle(f'Patient {chosen} – 12‑lead ECG', fontsize=16)

    for i, ax in enumerate(axes.flat):
        ax.plot(time, signals[:, i], linewidth=0.8)
        ax.set_title(lead_names[i])
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('mV')
        ax.grid(True, linestyle=':', alpha=0.6)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()