"""
SALA Project - Central Configuration
=====================================
All paths and parameters for the project are defined in this file.
Any module that needs a path or a setting imports it from here.
"""

from pathlib import Path

# ─────────────────────────────────────────────
# Main project paths
# ─────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR       = PROJECT_ROOT / "data"
RAW_DIR        = DATA_DIR / "raw"
PROCESSED_DIR  = DATA_DIR / "processed"
EXTERNAL_DIR   = DATA_DIR / "external"

RESULTS_DIR    = PROJECT_ROOT / "results"
FIGURES_DIR    = RESULTS_DIR / "figures"
TABLES_DIR     = RESULTS_DIR / "tables"
MODELS_DIR     = RESULTS_DIR / "models"

DOCS_DIR       = PROJECT_ROOT / "docs"

# Automatically create folders if they do not exist
for d in [RAW_DIR, PROCESSED_DIR, EXTERNAL_DIR,
          FIGURES_DIR, TABLES_DIR, MODELS_DIR, DOCS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ─────────────────────────────────────────────
# Target assets (grouped by category)
# ─────────────────────────────────────────────
TICKERS = {
    # ── Cryptocurrencies ──
    "BTC-USD":   "Bitcoin",
    "ETH-USD":   "Ethereum",
    "BNB-USD":   "BNB",
    "SOL-USD":   "Solana",
    "XRP-USD":   "XRP",
    "ADA-USD":   "Cardano",
    "DOGE-USD":  "Dogecoin",
    "TRX-USD":   "TRON",
    "DOT-USD":   "Polkadot",
    "POL28321-USD": "Polygon (prev. MATIC)",
    "AVAX-USD":  "Avalanche",
    "LINK-USD":  "Chainlink",
    "USDT-USD":  "Tether",

    # ── Forex & Dollar Index ──
    "DX-Y.NYB":  "U.S. Dollar Index",
    "EURUSD=X":  "EUR/USD",
    "JPY=X":     "USD/JPY",
    "GBPUSD=X":  "GBP/USD",
    "CAD=X":     "USD/CAD",
    "AUDUSD=X":  "AUD/USD",
    "CHF=X":     "USD/CHF",
    "CNY=X":     "USD/CNY",

    # ── Commodities ──
    "GC=F":      "Gold Futures",
    "SI=F":      "Silver Futures",
    "CL=F":      "WTI Crude Oil",
    "BZ=F":      "Brent Crude Oil",
    "NG=F":      "Natural Gas",
    "HG=F":      "Copper Futures",
    "PL=F":      "Platinum Futures",
    "ZC=F":      "Corn Futures",

    # ── Global Stock Indices ──
    "^GSPC":     "S&P 500",
    "^IXIC":     "NASDAQ Composite",
    "^DJI":      "Dow Jones",
    "^GDAXI":    "DAX",
    "^FTSE":     "FTSE 100",
    "^N225":     "Nikkei 225",
    "^HSI":      "Hang Seng",
    "^STOXX50E": "Euro Stoxx 50",
    "^GSPTSE":   "S&P/TSX Composite",
    "^BVSP":     "IBOVESPA",
}

# ─────────────────────────────────────────────
# Data time range
# ─────────────────────────────────────────────
START_DATE = "2022-01-01"
END_DATE   = "2025-12-31"

# ─────────────────────────────────────────────
# Anomaly detector parameters
# ─────────────────────────────────────────────
ANOMALY_WINDOW   = 20       # moving average window (days)
ANOMALY_Z_THRESH = 2.5      # Z-Score threshold for "abnormal"

# ─────────────────────────────────────────────
# Learning Automaton (SALA) parameters
# ─────────────────────────────────────────────
LA_LEARNING_RATE = 0.05     # learning rate (a in L_R-I)
LA_INIT_PROB     = 0.5      # initial probability for each action (50/50)

# ─────────────────────────────────────────────
# Storage settings
# ─────────────────────────────────────────────
FIGURE_DPI    = 120
RANDOM_SEED   = 42