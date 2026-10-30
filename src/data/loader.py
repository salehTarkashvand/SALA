"""
SALA Project - Data Loader
===========================
Functions for downloading and loading financial data.
"""

from __future__ import annotations

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

import pandas as pd
import yfinance as yf

from src.config import TICKERS, START_DATE, END_DATE, RAW_DIR


# ----------------------------------------------------------------------
# Download
# ----------------------------------------------------------------------
def download_asset(
    ticker: str,
    start: str,
    end: str,
    max_retries: int = 3,
    retry_delay: float = 2.0,
) -> pd.DataFrame:
    """
    Download daily data for a single ticker with retry logic.
    """
    for attempt in range(1, max_retries + 1):
        try:
            df = yf.download(
                ticker,
                start=start,
                end=end,
                progress=False,
                auto_adjust=True,
                threads=False,
            )
            if df is not None and len(df) > 0:
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)
                df.index.name = "Date"
                return df
        except Exception as e:
            print(f"  attempt {attempt} failed: {e}")

        if attempt < max_retries:
            time.sleep(retry_delay)

    return pd.DataFrame()


def download_all_assets() -> Dict[str, pd.DataFrame]:
    """
    Download all assets defined in `src.config.TICKERS`.
    Continues even if some tickers fail.
    """
    result: Dict[str, pd.DataFrame] = {}
    failed = []

    total = len(TICKERS)
    for i, ticker in enumerate(TICKERS, start=1):
        print(f"[{i:>2}/{total}] {ticker:<12}", end=" ")
        df = download_asset(ticker, START_DATE, END_DATE)

        if len(df) == 0:
            print("FAILED")
            failed.append(ticker)
            continue

        print(f"OK ({len(df)} rows)")
        result[ticker] = df

    print()
    print(f"Downloaded: {len(result)}/{total}")
    if failed:
        print(f"Failed: {failed}")

    return result


# ----------------------------------------------------------------------
# Save / Load
# ----------------------------------------------------------------------
def _safe_filename(ticker: str) -> str:
    """Convert a ticker symbol into a safe filename."""
    return (
        ticker.replace("^", "")
        .replace("=", "_")
        .replace(".", "_")
    )


def save_raw(data: Dict[str, pd.DataFrame]) -> None:
    """Save each DataFrame to `data/raw/{ticker}.csv`."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    for ticker, df in data.items():
        path = RAW_DIR / f"{_safe_filename(ticker)}.csv"
        df.to_csv(path)
        print(f"Saved: {path.name}")


def save_metadata(data: Dict[str, pd.DataFrame]) -> None:
    """Save download metadata to `data/raw/metadata.json`."""
    metadata = {
        "project": "SALA",
        "download_time": datetime.now().isoformat(),
        "start_date": START_DATE,
        "end_date": END_DATE,
        "tickers": {t: TICKERS[t] for t in data.keys()},
        "rows_per_ticker": {t: len(df) for t, df in data.items()},
    }
    path = RAW_DIR / "metadata.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"Saved: {path.name}")


def load_raw(ticker: str) -> pd.DataFrame:
    """Load a previously saved raw CSV back into a DataFrame."""
    path = RAW_DIR / f"{_safe_filename(ticker)}.csv"
    return pd.read_csv(path, index_col="Date", parse_dates=True)