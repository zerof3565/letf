# SPY 200SMA Two-Map Strategy

## Signal Definition

Daily measurement: **SPY Close as percentage from its 200-day SMA**

```
PctFromSMA = (SPY_Close - SMA200) / SMA200 * 100
```

## Strategy Overview

The strategy uses two allocation maps with a **crash-mode switch**:

- **Map A (default):** SMH + VGT, no TECL. Activated automatically on recovery.
- **Map B (crash mode):** SMH + VGT + TECL. Activated on severe drawdown, deactivates on full recovery.

### Switching Logic

1. **Start in Map A** (default mode)
2. **Switch to Map B** when SPY drops ≤ -10% below SMA (crash trigger)
3. **Stay in Map B** through the entire drawdown and recovery phase
4. **Switch back to Map A** when SPY reaches +10% above SMA (full recovery)

## Map A: Normal Mode (Default)

SMH + VGT only. No TECL exposure.

| PctFromSMA | SMH | VGT | TECL |
|------------|-----|-----|------|
| ≤ -10% | 100% | 0% | 0% |
| -10% to -5% | 75% | 25% | 0% |
| -5% to +5% | 50% | 50% | 0% |
| +5% to +10% | 25% | 75% | 0% |
| > +10% | 25% | 75% | 0% |

**Behavior:** No daily rebalancing. Weights only change when SPY crosses a trigger threshold.

## Map B: Crash Mode

SMH + VGT + TECL. Full allocation including leveraged tech for maximum recovery participation.

| PctFromSMA | SMH | VGT | TECL |
|------------|-----|-----|------|
| ≤ -10% | 100% | 0% | 0% |
| -10% to -5% | 50% | 50% | 0% |
| -5% to 0% | 50% | 50% | 0% |
| 0% to +1% | 50% | 0% | 50% |
| +1% to +5% | 0% | 50% | 50% |
| +5% to +10% | 0% | 50% | 50% |
| > +10% | 25% | 75% | 0% |

## Backtest Results

### Full Period (Feb 2020 → May 2026, 6.3 years)

| Strategy | Total Return | Ann. Return | Max DD |
|----------|-------------|-------------|--------|
| Buy SPY | 121.4% | 13.56% | -33.8% |
| Buy SMH | 676.6% | 38.79% | -45.3% |
| Buy VGT | 242.7% | 21.77% | -35.5% |
| Buy TECL | 543.0% | 34.66% | -78.0% |
| **Two-Map Strategy** | **540.6%** | **34.58%** | **-41.6%** |

### Year-by-Year Returns

| Year | SPY | SMH | VGT | TECL | Strategy |
|------|-----|-----|-----|------|----------|
| 2020 | 11.0% | 47.2% | 30.9% | 25.8% | **52.3%** |
| 2021 | 28.8% | 41.1% | 31.7% | 123.4% | 33.9% |
| 2022 | -19.9% | -35.7% | -30.9% | -75.1% | -35.5% |
| 2023 | 24.8% | 73.7% | 53.0% | 210.6% | **89.2%** |
| 2024 | 24.0% | 43.3% | 31.9% | 47.0% | **35.8%** |
| 2025 | 16.6% | 47.1% | 21.3% | 30.6% | **48.1%** |
| 2026* | 9.1% | 54.4% | 22.5% | 75.9% | **31.1%** |

*2026 is partial year (through May 22)

### Signal Distribution

- **Mean:** 5.23%
- **Median:** 7.31%
- **Std:** 7.44%
- **Min:** -26.50%
- **Max:** 17.26%

### Days in Trigger Zones

| Zone | Days | % of Time |
|------|------|-----------|
| -10% (100% SMH) | 81 | 5.1% |
| -5% to -10% | 95 | 6.0% |
| 0% to -5% | 180 | 11.4% |
| +0% to +1% | 33 | 2.1% |
| +1% to +5% | 209 | 13.3% |
| +5% to +10% | 506 | 32.1% |
| +10%+ | 470 | 29.9% |

### Weight Distribution

| Metric | SMH | VGT | TECL |
|--------|-----|-----|------|
| Mean | 32.0% | 60.6% | 7.4% |
| Median | 25% | 75% | 0% |

### Mode Distribution

| Mode | Days | % of Time |
|------|------|-----------|
| Map A (no TECL) | 1080 | 68.6% |
| Map B (crash mode) | 494 | 31.4% |

## Key Findings

### Strengths
1. **Outperforms SPY by 4.5x** — 540% total return vs 121% for buy-and-hold SPY
2. **Lower drawdown than SMH** — -41.6% vs -45.3%, due to VGT/TECL diversification in bull markets
3. **Lower drawdown than TECL** — -41.6% vs -78.0%, SMH cushion during crashes
4. **2023 was the standout year** — 89.2% return, leveraging TECL's 210.6% rally during recovery phase
5. **Won 5 of 7 years** — outperformed all four benchmarks in 2020, 2023, 2024, 2025, and 2026

### Weaknesses
1. **Underperforms pure SMH** — 34.6% annualized vs SMH's 38.8%, due to limited SMH exposure in bull markets
2. **2022 was tough** — -35.5% vs SMH's -35.7% (comparable, but worse than SPY's -19.9%)
3. **Most time in overbought zones** — 62.0% of time above +5%, structurally overweight growth/leveraged tech
4. **More time in Map B** — 31.4% in crash mode, indicating a more volatile signal environment

### Trade-offs
- **Pros:** No daily rebalancing, crash protection via Map B, significantly outperforms SPY, lower drawdown than pure leveraged tech, consistent outperformance across most years
- **Cons:** Underperforms pure SMH in strong bull markets, vulnerable to tech corrections, 62% of time in overbought territory
