#!/usr/bin/env python3
"""Fetch market data, compute signal line and allocations, export to CSV."""

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
future_end = pd.Timestamp(datetime.now().date()).strftime("%Y-%m-%d")

print(f"Fetching data from {warmup_start} to {future_end}...")
# Download SPY raw (unadjusted) for signal line
spy_raw = yf.download("SPY", start=warmup_start, end=future_end, progress=False, auto_adjust=False, actions=True, group_by="ticker")
# Download all 4 tickers with adjusted close for returns
all_adj = yf.download(["SPY", "SMH", "VGT", "TECL"], start=warmup_start, end=future_end, progress=False, auto_adjust=True, actions=True, group_by="ticker")

# Use adjusted close prices for returns (includes dividends via backward scaling)
def get_adjusted_close(data, ticker):
    if isinstance(data.columns, pd.MultiIndex):
        frame = data[ticker]
    else:
        frame = data.copy()
    frame.columns = [str(c).strip().lower().replace(" ", "_") for c in frame.columns]
    return frame["close"].copy()

# Use raw close prices for signal line (matches TradingView)
def get_raw_close(data, ticker):
    if isinstance(data.columns, pd.MultiIndex):
        frame = data[ticker]
    else:
        frame = data.copy()
    frame.columns = [str(c).strip().lower().replace(" ", "_") for c in frame.columns]
    return frame["close"].copy()

spy_close_raw = get_raw_close(spy_raw, "SPY")
spy_close_adj = get_adjusted_close(all_adj, "SPY")
smh_close_adj = get_adjusted_close(all_adj, "SMH")
vgt_close_adj = get_adjusted_close(all_adj, "VGT")
tecl_close_adj = get_adjusted_close(all_adj, "TECL")

# Normalize index (remove tz, normalize to midnight)
def normalize_index(idx):
    ni = pd.DatetimeIndex(pd.to_datetime(idx))
    if ni.tz is not None:
        ni = ni.tz_localize(None)
    return ni.normalize()

for frame, name in [(spy_close_raw, "spy_close_raw"),
                      (spy_close_adj, "spy_close_adj"), (smh_close_adj, "smh_close_adj"),
                      (vgt_close_adj, "vgt_close_adj"), (tecl_close_adj, "tecl_close_adj")]:
    globals()[name].index = normalize_index(frame.index)

# Align to common index (all series share the same download period)
common_idx = spy_close_raw.index.intersection(smh_close_adj.index).intersection(vgt_close_adj.index).intersection(tecl_close_adj.index)
for name in ["spy_close_raw", "spy_close_adj", "smh_close_adj", "vgt_close_adj", "tecl_close_adj"]:
    globals()[name] = globals()[name][common_idx]

# Compute SMA on full raw data first (before trimming) so warmup is correct
sma200_full = spy_close_raw.rolling(window=200).mean()

# Trim to user's desired range
spy_close_raw = spy_close_raw[spy_close_raw.index >= start_date]
spy_close_adj = spy_close_adj[spy_close_adj.index >= start_date]
smh_close_adj = smh_close_adj[smh_close_adj.index >= start_date]
vgt_close_adj = vgt_close_adj[vgt_close_adj.index >= start_date]
tecl_close_adj = tecl_close_adj[tecl_close_adj.index >= start_date]
sma200 = sma200_full[sma200_full.index >= start_date]

if len(spy_close_raw) == 0:
    print(f"No data available from {start_date.date()} onwards.")
    print(f"Latest available date: {common_idx[-1].date()}")
    exit(1)

print(f"Date range: {spy_close_raw.index[0].date()} to {spy_close_raw.index[-1].date()}")
print(f"Total trading days: {len(spy_close_raw)}")
print()

# --- Compute signal (raw close) ---
spy_close_price = spy_close_raw
pct_from_sma = (spy_close_price - sma200) / sma200 * 100

# --- Compute daily returns (adjusted close) ---
spy_ret = spy_close_adj.pct_change()
smh_ret = smh_close_adj.pct_change()
vgt_ret = vgt_close_adj.pct_change()
tecl_ret = tecl_close_adj.pct_change()

# --- Build DataFrame and export ---
df = pd.DataFrame({
    "date": pct_from_sma.index,
    "spy_close": spy_close_price.values,
    "sma200": sma200.values,
    "signal_pct_from_sma": pct_from_sma.values,
    "spy_ret": spy_ret.values,
    "smh_ret": smh_ret.values,
    "vgt_ret": vgt_ret.values,
    "tecl_ret": tecl_ret.values,
})

output_file = "two_maps_signal.csv"
df.to_csv(output_file, index=False)
print(f"Exported to {output_file} ({len(df)} rows)")
print(f"Signal rows with valid data: {df['signal_pct_from_sma'].notna().sum()}")
print(f"Signal rows with NaN: {df['signal_pct_from_sma'].isna().sum()}")
