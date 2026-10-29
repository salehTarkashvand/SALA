# SALA — Sentiment-Aware Learning Automaton

**Version:** v0.1.0 (Initial design)
**Status:** 🚧 In development
**Author:** Saleh Tarkashvand
**Type:** Master's thesis project

---

## 1. Overview

**SALA** (Sentiment-Aware Learning Automaton) is an adaptive decision-support
system for financial markets. It combines **sentiment analysis**, **anomaly
detection**, and a **learning automaton** to decide, in each market condition,
which source of information to trust more.

The system is designed for assets such as stocks, gold, and cryptocurrencies,
operating in **non-stationary** environments where the optimal decision
strategy changes over time.

---

## 2. Problem Statement

Financial markets are driven by two different forces:

1. **Quantitative behavior** — price movements, volatility, volume, patterns.
2. **Qualitative behavior** — news, social media, investor sentiment, fear and greed.

Most existing models rely on only one of these. However:

- In **normal** market conditions, historical price patterns are usually informative.
- In **abnormal** (shock) conditions, sentiment and news often dominate.

A fixed-weight combination of both sources fails because the market regime keeps
changing. The system must **learn dynamically** which source to trust in each
state.

---

## 3. Learning Model

SALA is formulated as an **Associative Learning Automaton** operating in a
**non-stationary S-model environment**.

| Concept (from Learning Automata theory) | SALA implementation                        |
|-----------------------------------------|--------------------------------------------|
| Context vector `X`                      | (sentiment, anomaly, market features)      |
| Action set `α`                          | {trust sentiment, trust anomaly}           |
| Reinforcement signal `β`                | realized profit/loss after trade           |
| Environment `F`                         | financial market (unknown, non-stationary) |
| Learning algorithm `T`                  | Linear Reward–Inaction (initial version)   |

---

## 4. Assets Under Study

Initial dataset covers **five assets** over a 3-year window (2022–2025):

| Ticker  | Asset        | Type           |
|---------|--------------|----------------|
| BTC-USD | Bitcoin      | Cryptocurrency |
| ETH-USD | Ethereum     | Cryptocurrency |
| GC=F    | Gold Futures | Commodity      |
| AAPL    | Apple Inc.   | Stock          |
| ^GSPC   | S&P 500      | Market index   |

---

## 5. Project Structure

SALA/
├── data/
│ ├── raw/ Raw downloaded data (prices, text)
│ ├── processed/ Cleaned, merged, feature-engineered data
│ └── external/ External datasets (sentiment corpora)
├── notebooks/ Exploration notebooks (numbered, sequential)
├── src/
│ ├── config.py Central configuration (paths, parameters)
│ ├── data/ Data loading and processing
│ ├── models/ Sentiment and anomaly models
│ ├── automaton/ Learning automaton implementation
│ └── evaluation/ Metrics (accuracy, return, Sharpe ratio)
├── results/
│ ├── figures/ Plots
│ ├── tables/ Result tables (CSV / Markdown)
│ └── models/ Saved trained models
├── docs/ Notes and references
├── tests/ Automated tests
├── requirements.txt
├── environment.yml
└── README.md


---

## 7. Installation

### Prerequisites

- macOS (Apple Silicon arm64) or Linux
- Miniforge / conda installed

### Setup

```bash
# Create and activate the environment
conda env create -f environment.yml
conda activate sala

# Verify
python -c "import numpy, pandas, sklearn, yfinance; print('OK')"

# 1. Download data
jupyter lab notebooks/01_data_download.ipynb

# 2. Explore data
jupyter lab notebooks/02_data_exploration.ipynb

# 3. Train anomaly detector
jupyter lab notebooks/03_anomaly_detector.ipynb

# 4. Train sentiment model
jupyter lab notebooks/04_sentiment_analysis.ipynb

# 5. Train the learning automaton
jupyter lab notebooks/05_learning_automaton.ipynb

# 6. End-to-end evaluation
jupyter lab notebooks/06_full_pipeline.ipynb

9. Roadmap
v0.1.0 — Design (current)
☑ Project structure
☑ Central configuration
☑ Scenario definition
☑ Environment setup
v0.2.0 — Data Layer
□ Download price data (yfinance)
□ Download/curate textual data (tweets, news)
□ Data quality checks
v0.3.0 — Individual Models
□ Anomaly detector (Z-score / MAD baseline)
□ Sentiment analyzer (lexicon-based baseline, then DistilBERT)
v0.4.0 — Learning Automaton
□ L_R-I implementation
□ Associative version
□ Integration with both models
v0.5.0 — Evaluation
□ Backtest on held-out period
□ Compare with baselines (Buy & Hold, always-trust-one-model)
□ Metrics: accuracy, return, Sharpe ratio, drawdown
10. References
Narendra, K. S., & Thathachar, M. A. L. (1989).
Learning Automata: An Introduction. Prentice Hall.

Thathachar, M. A. L., & Sastry, P. S. (2004).
Networks of Learning Automata. Springer.

Course notes on Learning Automata, Chapter 2.

11. License
This project is part of a Master's thesis and is currently private.
License will be determined at the time of publication.


---

## What changed

| Before | After |
|---|---|
| Section 3 was split into "Layer 1", "Layer 2", "Layer 3" sub-headings | Section 3 is now **one continuous paragraph** describing all three layers in order, followed by the diagram |

Everything else is identical.

## Next steps

1. Replace the whole content of `README.md` with the block above.
2. Press `Cmd+S` to save.
3. Run in terminal (with `(sala)` active) and send me the output:

```bash
git status