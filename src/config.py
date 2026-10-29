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
# Target assets
# ─────────────────────────────────────────────
TICKERS = {
    "BTC-USD":  "Bitcoin",
    "ETH-USD":  "Ethereum",
    "GC=F":     "Gold Futures",
    "AAPL":     "Apple Stock",
    "^GSPC":    "S&P 500",
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