#!/usr/bin/env python3
"""Fetch market data, compute signal line and allocations, export to CSV (TQQQ version)."""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

# --- Prompt for start date ---
raw = input("Enter start date (YYYY-MM-DD), or press Enter for today: ").strip()
if raw:
    start_date = pd.Timestamp(raw)
else:
    start_date = pd.Timestamp(datetime.now().date())

# Fetch with 200-day warmup buffer before the user's start date
warmup_start = (start_date - pd.Timedelta(days=300)).strftime("%Y-%m-%d")
future_end = (pd.Timestamp(datetime.now().date()) + pd.Timedelta(days=7)).strftime("%Y-%m-%d")

print(f"Fetching data from {warmup_start} to {future_end}...")
spy = yf.download("SPY", start=warmup_start, end=future_end, progress=False, auto_adjust=False, actions=True, group_by="ticker")
smh = yf.download("SMH", start=warmup_start, end=future_end, progress=False, auto_adjust=False, actions=True, group_by="ticker")
vgt = yf.download("VGT", start=warmup_start, end=future_end, progress=False, auto_adjust=False, actions=True, group_by="ticker")
tqqq = yf.download("TQQQ", start=warmup_start, end=future_end, progress=False, auto_adjust=False, actions=True, group_by="ticker")

# Use close prices (raw close + dividends for adjusted close)
def get_close(data, ticker):
    if isinstance(data.columns, pd.MultiIndex):
        frame = data[ticker]
    else:
        frame = data.copy()
    frame.columns = [str(c).strip().lower().replace(" ", "_") for c in frame.columns]
    close = frame["close"].copy()
    if "dividends" in frame.columns:
        close = close + frame["dividends"]
    return close

spy_close = get_close(spy, "SPY")
smh_close = get_close(smh, "SMH")
vgt_close = get_close(vgt, "VGT")
tqqq_close = get_close(tqqq, "TQQQ")

# Normalize index (remove tz, normalize to midnight)
def normalize_index(idx):
    ni = pd.DatetimeIndex(pd.to_datetime(idx))
    if ni.tz is not None:
        ni = ni.tz_localize(None)
    return ni.normalize()

spy_close.index = normalize_index(spy_close.index)
smh_close.index = normalize_index(smh_close.index)
vgt_close.index = normalize_index(vgt_close.index)
tqqq_close.index = normalize_index(tqqq_close.index)

# Align to common index
common_idx = spy_close.index.intersection(smh_close.index).intersection(vgt_close.index).intersection(tqqq_close.index)
spy_close = spy_close[common_idx]
smh_close = smh_close[common_idx]
vgt_close = vgt_close[common_idx]
tqqq_close = tqqq_close[common_idx]

# Compute SMA on full data first (before trimming) so warmup is correct
sma200_full = spy_close.rolling(window=200).mean()

# Trim to user's desired range
spy_close = spy_close[spy_close.index >= start_date]
smh_close = smh_close[smh_close.index >= start_date]
vgt_close = vgt_close[vgt_close.index >= start_date]
tqqq_close = tqqq_close[tqqq_close.index >= start_date]
sma200 = sma200_full[sma200_full.index >= start_date]

if len(spy_close) == 0:
    print(f"No data available from {start_date.date()} onwards.")
    print(f"Latest available date: {common_idx[-1].date()}")
    exit(1)

print(f"Date range: {spy_close.index[0].date()} to {spy_close.index[-1].date()}")
print(f"Total trading days: {len(spy_close)}")
print()

# --- Compute signal ---
spy_close_price = spy_close
pct_from_sma = (spy_close_price - sma200) / sma200 * 100

# --- Compute daily returns ---
spy_ret = spy_close.pct_change()
smh_ret = smh_close.pct_change()
vgt_ret = vgt_close.pct_change()
tqqq_ret = tqqq_close.pct_change()

# --- Build DataFrame and export ---
df = pd.DataFrame({
    "date": pct_from_sma.index,
    "spy_close": spy_close_price.values,
    "sma200": sma200.values,
    "signal_pct_from_sma": pct_from_sma.values,
    "spy_ret": spy_ret.values,
    "smh_ret": smh_ret.values,
    "vgt_ret": vgt_ret.values,
    "tqqq_ret": tqqq_ret.values,
})

output_file = "two_maps_signal_tqqq.csv"
df.to_csv(output_file, index=False)
print(f"Exported to {output_file} ({len(df)} rows)")
print(f"Signal rows with valid data: {df['signal_pct_from_sma'].notna().sum()}")
print(f"Signal rows with NaN: {df['signal_pct_from_sma'].isna().sum()}")
