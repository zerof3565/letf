#!/usr/bin/env python3
"""Display current active map and allocation, then refresh signal CSV."""

import argparse
import subprocess
import pandas as pd
import numpy as np

# --- Parse arguments ---
parser = argparse.ArgumentParser(description="Current Status: Active Map & Allocation")
parser.add_argument("--start-date", type=str, default=None,
                    help="Start date for data refresh in YYYY-MM-DD format (default: today)")
args = parser.parse_args()

def get_weights_map_a(pct):
    if pct <= -10:
        return 100, 0, 0
    elif pct <= -5:
        return 75, 25, 0
    elif pct <= 0:
        return 50, 50, 0
    elif pct <= 1:
        return 50, 50, 0
    elif pct <= 5:
        return 50, 50, 0
    elif pct <= 10:
        return 25, 75, 0
    else:
        return 25, 75, 0

def get_weights_map_b(pct):
    if pct <= -10:
        return 100, 0, 0
    elif pct <= -5:
        return 50, 50, 0
    elif pct <= 0:
        return 50, 50, 0
    elif pct <= 1:
        return 50, 0, 50
    elif pct <= 5:
        return 0, 50, 50
    elif pct <= 10:
        return 0, 50, 50
    else:
        return 25, 75, 0

def compute_current_allocation(csv_file):
    df = pd.read_csv(csv_file)
    df["date"] = pd.to_datetime(df["date"])

    pct = df["signal_pct_from_sma"].values

    mode_in_map_b = False
    smh_w, vgt_w, tecl_w = 0, 0, 0
    current_map = "A"

    for i in range(len(pct)):
        if pd.isna(pct[i]):
            continue

        if mode_in_map_b:
            if pct[i] >= 10:
                mode_in_map_b = False
                smh_w, vgt_w, tecl_w = get_weights_map_a(pct[i])
                current_map = "A"
            else:
                smh_w, vgt_w, tecl_w = get_weights_map_b(pct[i])
                current_map = "B"
        else:
            if pct[i] <= -10:
                mode_in_map_b = True
                smh_w, vgt_w, tecl_w = get_weights_map_b(pct[i])
                current_map = "B"
            else:
                smh_w, vgt_w, tecl_w = get_weights_map_a(pct[i])
                current_map = "A"

    return df, smh_w, vgt_w, tecl_w, current_map

# --- Refresh signal CSV ---
print("Refreshing signal data...")
print("-" * 50)
cmd = ["python", "two_maps_signal.py"]
if args.start_date:
    # two_maps_signal.py prompts for start date; we pipe it in
    input_text = args.start_date
else:
    input_text = ""
result = subprocess.run(cmd, capture_output=True, text=True, input=input_text)
print(result.stdout)
if result.returncode != 0:
    print("Error refreshing data:")
    print(result.stderr)
    exit(1)
print("-" * 50)
print()

# --- Load data and compute current allocation ---
csv_file = "two_maps_signal.csv"
df, smh_w, vgt_w, tecl_w, current_map = compute_current_allocation(csv_file)

# Get the last valid signal
last_row = df.dropna(subset=["signal_pct_from_sma"]).iloc[-1]
signal_pct = last_row["signal_pct_from_sma"]
spy_close = last_row["spy_close"]
sma200 = last_row["sma200"]
last_date = last_row["date"]

print("=" * 50)
print("  Current Status")
print("=" * 50)
print(f"  Date:           {last_date.strftime('%Y-%m-%d')}")
print(f"  SPY Close:      ${spy_close:,.2f}")
print(f"  SMA 200:        ${sma200:,.2f}")
print(f"  Signal (% from SMA): {signal_pct:+.2f}%")
print()
print(f"  Active Map:     Map {'B (CRASH MODE)' if current_map == 'B' else 'A (NORMAL)'}")
print()
print("  Allocation:")
print(f"    SMH:  {smh_w:>5.1f}%")
print(f"    VGT:  {vgt_w:>5.1f}%")
print(f"    TECL: {tecl_w:>5.1f}%")
print("=" * 50)
