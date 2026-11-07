# SALA Changelog

All notable changes to this project are documented here.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)

## [v1.0.0] - 2026-11-07

### Added
- Data downloader for 39 assets (crypto, forex, commodities, indices).
- Anomaly detector (rolling Z-score, window=20, threshold=2.5).
- Sentiment analyzer (VADER) with calibration on Twitter Financial News.
- Learning Automaton (L_R-I) with associative extension.

### Results
- Sanity checks passed (p(A1) → 1.0 on synthetic data).
- BTC-USD backtest: reward rate 48.7% (vs. 49.9% and 50.1% baselines).

### Known limitations
- Sentiment data is synthetic; VADER accuracy only 48.1%.
- Single asset only (BTC-USD).

## [Unreleased] - Planned for v2.0.0

### To be added
- Real sentiment data (Kaggle + GDELT).
- Train/Validation/Test split.
- Multi-asset evaluation (oil, gold, dollar, BTC, S&P 500).
- FinBERT as a sentiment backend.
- Walk-forward validation.
