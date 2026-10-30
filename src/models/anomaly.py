"""
SALA Project - Anomaly Detector
================================
Detects abnormal market days using rolling Z-score on daily returns.

The core idea (from Learning Automata theory, Section 2):
- An "abnormal" day is one where the return is far from the recent norm.
- We use a rolling window (default 20 days) to estimate the local mean/std.
- |Z-score| > threshold  ->  abnormal.

Inputs : data/raw/{ticker}.csv  (Date, Open, High, Low, Close, Volume)
Outputs: data/processed/{ticker}.csv  (+ Return, Z_Score, Is_Anomaly)
"""

from __future__ import annotations

import pandas as pd

from src.config import (
    TICKERS,
    RAW_DIR,
    PROCESSED_DIR,
    TABLES_DIR,
    ANOMALY_WINDOW,
    ANOMALY_Z_THRESH,
)
from src.data.loader import _safe_filename


# ----------------------------------------------------------------------
# Core calculations
# ----------------------------------------------------------------------
def add_anomaly_columns(
    df: pd.DataFrame,
    window: int = ANOMALY_WINDOW,
    threshold: float = ANOMALY_Z_THRESH,
) -> pd.DataFrame:
    """
    Add Return, Rolling_Mean, Rolling_Std, Z_Score, Is_Anomaly to a
    price DataFrame. Modifies a copy, not the original.
    """
    out = df.copy()
    close = out["Close"].astype(float)

    # Daily return: r_t = (P_t - P_{t-1}) / P_{t-1}
    out["Return"] = close.pct_change(fill_method=None)

    # Rolling statistics over the last `window` days
    roll = out["Return"].rolling(window=window, min_periods=window)
    out["Rolling_Mean"] = roll.mean()
    out["Rolling_Std"] = roll.std()

    # Z-score: how many std-devs is today's return from the local mean?
    # eps avoids division-by-zero on perfectly flat windows (rare).
    eps = 1e-12
    out["Z_Score"] = (out["Return"] - out["Rolling_Mean"]) / (out["Rolling_Std"] + eps)

    # Label: 1 if |Z| > threshold, else 0. NaN (warm-up) becomes 0.
    out["Is_Anomaly"] = (out["Z_Score"].abs() > threshold).astype(int)
    out.loc[out["Z_Score"].isna(), "Is_Anomaly"] = 0

    return out


# ----------------------------------------------------------------------
# Single asset
# ----------------------------------------------------------------------
def process_asset(ticker: str) -> pd.DataFrame | None:
    """
    Load raw CSV for one ticker, add anomaly columns, save to processed/.
    Returns the processed DataFrame, or None if raw file is missing.
    """
    safe = _safe_filename(ticker)
    raw_path = RAW_DIR / f"{safe}.csv"
    if not raw_path.exists():
        print(f"  [{ticker}] raw file missing: {raw_path.name}")
        return None

    df = pd.read_csv(raw_path, index_col="Date", parse_dates=True)
    if "Close" not in df.columns:
        print(f"  [{ticker}] no 'Close' column, skipping")
        return None

    df = add_anomaly_columns(df)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out_path = PROCESSED_DIR / f"{safe}.csv"
    df.to_csv(out_path)

    n_anom = int(df["Is_Anomaly"].sum())
    print(f"  [{ticker}] {len(df)} rows, {n_anom} anomalies -> {out_path.name}")
    return df


# ----------------------------------------------------------------------
# All assets
# ----------------------------------------------------------------------
def process_all_assets() -> dict[str, pd.DataFrame]:
    """
    Process every ticker in src.config.TICKERS.
    Returns {ticker: processed DataFrame}.
    """
    print(f"Processing {len(TICKERS)} assets "
          f"(window={ANOMALY_WINDOW}, threshold={ANOMALY_Z_THRESH})")
    print("-" * 65)

    results: dict[str, pd.DataFrame] = {}
    for ticker in TICKERS:
        df = process_asset(ticker)
        if df is not None:
            results[ticker] = df

    print("-" * 65)
    print(f"Processed {len(results)}/{len(TICKERS)} assets.")
    return results


# ----------------------------------------------------------------------
# Summary
# ----------------------------------------------------------------------
def build_summary(results: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Build a summary table across all assets.
    """
    rows = []
    for ticker, df in results.items():
        n = len(df)
        n_anom = int(df["Is_Anomaly"].sum())
        rows.append({
            "Ticker": ticker,
            "Days": n,
            "Anomalies": n_anom,
            "Anomaly_Rate_%": round(100 * n_anom / n, 2) if n else 0.0,
            "Max_|Z|": round(float(df["Z_Score"].abs().max(skipna=True)), 2)
                       if df["Z_Score"].notna().any() else 0.0,
        })
    summary = pd.DataFrame(rows).sort_values("Anomaly_Rate_%", ascending=False)
    summary.reset_index(drop=True, inplace=True)
    return summary


def save_summary(summary: pd.DataFrame) -> None:
    """Save summary table to results/tables/anomaly_summary.csv."""
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    path = TABLES_DIR / "anomaly_summary.csv"
    summary.to_csv(path, index=False)
    print(f"Saved: {path.name}")


# ----------------------------------------------------------------------
# Loader for later stages
# ----------------------------------------------------------------------
def load_processed(ticker: str) -> pd.DataFrame:
    """Load the processed CSV (with Return, Z_Score, Is_Anomaly)."""
    safe = _safe_filename(ticker)
    path = PROCESSED_DIR / f"{safe}.csv"
    return pd.read_csv(path, index_col="Date", parse_dates=True)