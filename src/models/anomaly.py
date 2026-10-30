"""
SALA Project - Anomaly Detector
================================
Detects abnormal market days using rolling Z-score on daily returns.

Method:
- Daily return: r_t = (P_t - P_{t-1}) / P_{t-1}
- Rolling mean and std over the last `window` days
- Z-score: z_t = (r_t - mean) / std
- Label 1 (abnormal) if |z_t| > threshold, else 0 (normal)

Inputs : data/raw/{ticker}.csv
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


def add_anomaly_columns(
    df: pd.DataFrame,
    window: int = ANOMALY_WINDOW,
    threshold: float = ANOMALY_Z_THRESH,
) -> pd.DataFrame:
    """
    Add Return, Rolling_Mean, Rolling_Std, Z_Score, Is_Anomaly to a
    price DataFrame. Returns a copy.
    """
    out = df.copy()
    close = out["Close"].astype(float)

    # Daily return
    out["Return"] = close.pct_change(fill_method=None)

    # Rolling statistics
    roll = out["Return"].rolling(window=window, min_periods=window)
    out["Rolling_Mean"] = roll.mean()
    out["Rolling_Std"] = roll.std()

    # Z-score (epsilon avoids division by zero)
    eps = 1e-12
    out["Z_Score"] = (out["Return"] - out["Rolling_Mean"]) / (out["Rolling_Std"] + eps)

    # Label
    out["Is_Anomaly"] = (out["Z_Score"].abs() > threshold).astype(int)
    out.loc[out["Z_Score"].isna(), "Is_Anomaly"] = 0

    return out


def process_asset(ticker: str) -> pd.DataFrame | None:
    """
    Load raw CSV for one ticker, add anomaly columns, save to processed/.
    """
    safe = _safe_filename(ticker)
    raw_path = RAW_DIR / f"{safe}.csv"
    if not raw_path.exists():
        print(f"  [{ticker}] raw file missing")
        return None

    df = pd.read_csv(raw_path, index_col="Date", parse_dates=True)
    if "Close" not in df.columns:
        print(f"  [{ticker}] no 'Close' column")
        return None

    df = add_anomaly_columns(df)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out_path = PROCESSED_DIR / f"{safe}.csv"
    df.to_csv(out_path)

    n_anom = int(df["Is_Anomaly"].sum())
    print(f"  [{ticker}] {len(df)} rows, {n_anom} anomalies -> {out_path.name}")
    return df


def process_all_assets() -> dict[str, pd.DataFrame]:
    """
    Process every ticker in src.config.TICKERS.
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


def build_summary(results: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Summary table across all assets.
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
    """Save summary to results/tables/anomaly_summary.csv."""
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    path = TABLES_DIR / "anomaly_summary.csv"
    summary.to_csv(path, index=False)
    print(f"Saved: {path.name}")


def load_processed(ticker: str) -> pd.DataFrame:
    """Load processed CSV for later stages."""
    safe = _safe_filename(ticker)
    path = PROCESSED_DIR / f"{safe}.csv"
    return pd.read_csv(path, index_col="Date", parse_dates=True)