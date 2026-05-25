## Getting Daily Status for Allocation and Signal Line
cd ~/Documents/letf && uv run current_status.py --start-date 2025-02-18


## Run Backtest

Generate signal data and run the Two-Map Strategy backtest:

```bash
cd ~/Documents/letf && uv run two_maps_strategy.py --start-date 2025-02-19
```

This will:
1. Fetch market data (SPY, SMH, VGT, TECL) and compute the signal line
2. Run the backtest with Map A / Map B allocation logic
3. Output performance metrics, year-by-year returns, and distribution stats
4. Export `daily_verification.csv` with row-by-row audit trail (date, signal, mode, allocations, returns, equity curve)

### Output Files

| File | Description |
|------|-------------|
| `two_maps_signal.csv` | Raw signal data: dates, SPY close, SMA200, signal %, daily returns for all tickers |
| `daily_verification.csv` | Full backtest audit trail: allocations, mode (A/B), strategy returns, equity curves |
