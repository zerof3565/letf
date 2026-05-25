#!/usr/bin/env python3
"""Backtest of the SPY 200SMA Two-Map Strategy using pre-computed signal data, refreshing CSV first."""

import argparse
import subprocess
import pandas as pd

# --- Parse arguments ---
parser = argparse.ArgumentParser(description="SPY 200SMA Two-Map Strategy Backtest")
parser.add_argument("--start-date", type=str, default=None,
                    help="Start date for backtest in YYYY-MM-DD format (e.g. 2020-01-01)")
args = parser.parse_args()

# --- Refresh signal CSV ---
print("Refreshing signal data...")
print("-" * 50)
cmd = ["python", "two_maps_signal.py"]
if args.start_date:
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

# --- Load data ---
csv_file = "two_maps_signal.csv"
df = pd.read_csv(csv_file)
df["date"] = pd.to_datetime(df["date"])

if args.start_date:
    start_dt = pd.to_datetime(args.start_date)
    df = df[df["date"] >= start_dt]
    print(f"Filtered to start date: {start_dt.date()}")

print(f"Loaded {len(df)} rows from {csv_file}")
print(f"Date range: {df['date'].iloc[0].date()} to {df['date'].iloc[-1].date()}")
print()

# --- Map A: Normal mode (no TECL) ---
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

# --- Map B: Crash mode (includes TECL) ---
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

# --- Run strategy: Map A default, switch to Map B on crash, back to A on recovery ---
pct = df["signal_pct_from_sma"].values
spy_ret = df["spy_ret"].values
smh_ret = df["smh_ret"].values
vgt_ret = df["vgt_ret"].values
tecl_ret = df["tecl_ret"].values

w_smh = []
w_vgt = []
w_tecl = []
in_map_b = []
mode_in_map_b = False

for i in range(len(pct)):
    if pd.isna(pct[i]):
        w_smh.append(0)
        w_vgt.append(0)
        w_tecl.append(0)
        in_map_b.append(False)
        continue

    if mode_in_map_b:
        if pct[i] >= 10:
            mode_in_map_b = False
            smh_w, vgt_w, tecl_w = get_weights_map_a(pct[i])
        else:
            smh_w, vgt_w, tecl_w = get_weights_map_b(pct[i])
    else:
        if pct[i] <= -10:
            mode_in_map_b = True
            smh_w, vgt_w, tecl_w = get_weights_map_b(pct[i])
        else:
            smh_w, vgt_w, tecl_w = get_weights_map_a(pct[i])

    w_smh.append(smh_w)
    w_vgt.append(vgt_w)
    w_tecl.append(tecl_w)
    in_map_b.append(mode_in_map_b)

df["allocation_SMH"] = w_smh
df["allocation_VGT"] = w_vgt
df["allocation_TECL"] = w_tecl
df["in_map_b"] = in_map_b

# --- Compute strategy returns (1-day lag) ---
strategy_ret = (
    pd.Series(df["allocation_SMH"].shift(1).values, index=df["date"]) / 100 * pd.Series(smh_ret, index=df["date"]) +
    pd.Series(df["allocation_VGT"].shift(1).values, index=df["date"]) / 100 * pd.Series(vgt_ret, index=df["date"]) +
    pd.Series(df["allocation_TECL"].shift(1).values, index=df["date"]) / 100 * pd.Series(tecl_ret, index=df["date"])
)

# Equity curves
spy_equity = pd.Series((1 + pd.Series(spy_ret, index=df["date"])).cumprod(), index=df["date"])
smh_equity = pd.Series((1 + pd.Series(smh_ret, index=df["date"])).cumprod(), index=df["date"])
vgt_equity = pd.Series((1 + pd.Series(vgt_ret, index=df["date"])).cumprod(), index=df["date"])
tecl_equity = pd.Series((1 + pd.Series(tecl_ret, index=df["date"])).cumprod(), index=df["date"])
strategy_equity = pd.Series((1 + strategy_ret.fillna(0)).cumprod(), index=df["date"])

# Fill initial NaN (first row has no return)
spy_equity.iloc[0] = 1.0
smh_equity.iloc[0] = 1.0
vgt_equity.iloc[0] = 1.0
tecl_equity.iloc[0] = 1.0

# --- Compute metrics ---
def calc_metrics(equity, name):
    total_return = (equity.iloc[-1] - 1) * 100
    n_years = (equity.index[-1] - equity.index[0]).days / 365.25
    ann_return = (equity.iloc[-1] ** (1 / n_years) - 1) * 100 if n_years > 0 else 0

    running_max = equity.cummax()
    drawdown = (equity - running_max) / running_max * 100
    max_dd = drawdown.min()

    return {
        "name": name,
        "total_return": total_return,
        "ann_return": ann_return,
        "max_dd": max_dd,
        "n_years": n_years,
    }

metrics = []
for eq, nm in [(spy_equity, "Buy SPY"), (smh_equity, "Buy SMH"),
               (vgt_equity, "Buy VGT"), (tecl_equity, "Buy TECL"),
               (strategy_equity, "Two-Map Strategy (A default, B on crash)")]:
    metrics.append(calc_metrics(eq, nm))

print("=" * 80)
print(f"{'Strategy':<40} {'Total Return':>14} {'Ann. Return':>13} {'Max DD':>11}")
print("=" * 80)
for m in metrics:
    print(f"{m['name']:<40} {m['total_return']:>13.2f}% {m['ann_return']:>12.2f}% {m['max_dd']:>10.2f}%")
print("=" * 80)
print()

# --- Map B transition stats ---
b_periods = 0
b_total_days = 0
b_max_days = 0
b_current_days = 0
for i in range(len(df)):
    if pd.isna(df["signal_pct_from_sma"].iloc[i]):
        continue
    if df["in_map_b"].iloc[i]:
        b_current_days += 1
        if b_current_days == 1:
            b_periods += 1
        if b_current_days > b_max_days:
            b_max_days = b_current_days
        b_total_days += 1
    else:
        b_current_days = 0

print(f"Map B (crash mode) stats:")
print(f"  Number of crash periods entered: {b_periods}")
print(f"  Total days in Map B: {b_total_days} ({b_total_days/len(df)*100:.2f}%)")
print(f"  Max consecutive days in Map B: {b_max_days}")
print()

# --- Year-by-year ---
print("=" * 75)
print("Year-by-Year Returns:")
print("=" * 75)
strat_yearly = {}
spy_yearly = {}
smh_yearly = {}
vgt_yearly = {}
tecl_yearly = {}

for yr in range(spy_equity.index.year.min(), spy_equity.index.year.max() + 1):
    spy_y = spy_equity[spy_equity.index.year == yr]
    smh_y = smh_equity[smh_equity.index.year == yr]
    vgt_y = vgt_equity[vgt_equity.index.year == yr]
    tecl_y = tecl_equity[tecl_equity.index.year == yr]
    strat_y = strategy_equity[strategy_equity.index.year == yr]

    if len(spy_y) < 2 or len(strat_y) < 2:
        continue

    spy_ret_y = (spy_y.iloc[-1] / spy_y.iloc[0] - 1) * 100
    smh_ret_y = (smh_y.iloc[-1] / smh_y.iloc[0] - 1) * 100
    vgt_ret_y = (vgt_y.iloc[-1] / vgt_y.iloc[0] - 1) * 100
    tecl_ret_y = (tecl_y.iloc[-1] / tecl_y.iloc[0] - 1) * 100
    strat_ret_y = (strat_y.iloc[-1] / strat_y.iloc[0] - 1) * 100

    spy_yearly[yr] = spy_ret_y
    smh_yearly[yr] = smh_ret_y
    vgt_yearly[yr] = vgt_ret_y
    tecl_yearly[yr] = tecl_ret_y
    strat_yearly[yr] = strat_ret_y

print(f"{'Year':<8} {'SPY':>10} {'SMH':>10} {'VGT':>10} {'TECL':>10} {'Strategy':>12}")
print("-" * 70)
for yr in sorted(strat_yearly.keys()):
    marker = " **" if abs(strat_yearly[yr]) > abs(spy_yearly[yr]) else ""
    print(f"{yr:<8} {spy_yearly[yr]:>9.2f}% {smh_yearly[yr]:>9.2f}% {vgt_yearly[yr]:>9.2f}% {tecl_yearly[yr]:>9.2f}% {strat_yearly[yr]:>11.2f}%{marker}")
print("=" * 75)
print()

# --- Weight distribution ---
print("=" * 75)
print("Weight Distribution:")
print("=" * 75)
print(f"{'Metric':<15} {'SMH':>10} {'VGT':>10} {'TECL':>10}")
print("-" * 45)
print(f"{'Mean':<15} {df['allocation_SMH'].mean():>9.2f}% {df['allocation_VGT'].mean():>9.2f}% {df['allocation_TECL'].mean():>9.2f}%")
print(f"{'Median':<15} {df['allocation_SMH'].median():>9.0f}% {df['allocation_VGT'].median():>9.0f}% {df['allocation_TECL'].median():>9.0f}%")
print()

# --- Signal stats ---
valid_pct = df["signal_pct_from_sma"].dropna()
print("=" * 75)
print("Signal Distribution:")
print("=" * 75)
print(f"{'Mean':<15} {valid_pct.mean():>10.2f}%")
print(f"{'Median':<15} {valid_pct.median():>10.2f}%")
print(f"{'Std':<15} {valid_pct.std():>10.2f}%")
print(f"{'Min':<15} {valid_pct.min():>10.2f}%")
print(f"{'Max':<15} {valid_pct.max():>10.2f}%")
print()

# Count days in each trigger zone
zone_names = ["-10% (100% SMH)", "-5% to -10%", "0% to -5%", "+0% to +1%", "+1% to +5%", "+5% to +10%", "+10%+"]
zone_ranges = [(-100, -10), (-10, -5), (-5, 0), (0, 1), (1, 5), (5, 10), (10, 100)]

print("Days in Trigger Zones:")
print("-" * 50)
for name, (lo, hi) in zip(zone_names, zone_ranges):
    count = ((valid_pct >= lo) & (valid_pct < hi)).sum()
    pct_val = count / len(valid_pct) * 100
    print(f"  {name:<25} {count:>6} days  ({pct_val:5.2f}%)")
print("-" * 50)
print()

# --- Days in each mode ---
print("Days in Each Mode:")
print("-" * 50)
map_a_days = (~df["in_map_b"]).sum()
map_b_days = df["in_map_b"].sum()
print(f"  Map A (no TECL):  {map_a_days:>6} days  ({map_a_days/len(df)*100:.2f}%)")
print(f"  Map B (crash):    {map_b_days:>6} days  ({map_b_days/len(df)*100:.2f}%)")
print("-" * 50)
print()

# --- Export daily verification CSV ---
verification_df = pd.DataFrame({
    "date": df["date"].values,
    "signal_pct_from_sma": df["signal_pct_from_sma"].values,
    "mode": ["B" if b else "A" for b in df["in_map_b"].values],
    "allocation_SMH": df["allocation_SMH"].values,
    "allocation_VGT": df["allocation_VGT"].values,
    "allocation_TECL": df["allocation_TECL"].values,
    "spy_ret": df["spy_ret"].values,
    "smh_ret": df["smh_ret"].values,
    "vgt_ret": df["vgt_ret"].values,
    "tecl_ret": df["tecl_ret"].values,
    "strategy_ret": strategy_ret.fillna(0).values,
    "strategy_equity": strategy_equity.values,
    "spy_equity": spy_equity.values,
})
verification_df.to_csv("daily_verification.csv", index=False)
print(f"Daily verification exported to daily_verification.csv ({len(verification_df)} rows)")
