#!/usr/bin/env bash
# =============================================================
# SALA Project - Full In-Place Structure Expansion
# =============================================================
# This script expands the current project into a professional
# layout WITHOUT moving or deleting existing files.
#
# Run from the project root:
#   bash scripts/expand_structure.sh
# =============================================================

set -euo pipefail

ROOT="$(pwd)"

echo "🚀 SALA structure expansion starting..."
echo "   Root: $ROOT"
echo ""

# ─────────────────────────────────────────────
# 1. Folders
# ─────────────────────────────────────────────
echo "📁 [1/7] Creating folders..."

mkdir -p .github/workflows
mkdir -p configs
mkdir -p data/interim
mkdir -p docs/thesis_chapters
mkdir -p experiments
mkdir -p models
mkdir -p results/reports
mkdir -p scripts
mkdir -p src/features
mkdir -p src/simulation
mkdir -p src/utils
mkdir -p tests

echo "   ✓ folders created"

# ─────────────────────────────────────────────
# 2. __init__.py files
# ─────────────────────────────────────────────
echo "🐍 [2/7] Creating __init__.py files..."

touch src/features/__init__.py
touch src/simulation/__init__.py
touch src/utils/__init__.py
touch tests/__init__.py

echo "   ✓ __init__.py files created"

# ─────────────────────────────────────────────
# 3. .gitkeep placeholders
# ─────────────────────────────────────────────
echo "📌 [3/7] Creating .gitkeep placeholders..."

touch data/interim/.gitkeep
touch experiments/.gitkeep
touch models/.gitkeep
touch results/reports/.gitkeep
touch docs/thesis_chapters/.gitkeep

echo "   ✓ placeholders created"

# ─────────────────────────────────────────────
# 4. configs/v1_baseline.yaml
# ─────────────────────────────────────────────
echo "⚙️  [4/7] Writing configs/v1_baseline.yaml..."

cat > configs/v1_baseline.yaml << 'YAML'
version: "v1_baseline"
description: "Initial prototype with VADER sentiment and Z-score anomaly"
date_created: "2026-11-07"
author: "Saleh Tarkashvand"

data:
  assets: ["BTC-USD"]
  start_date: "2022-01-01"
  end_date: "2025-12-31"

models:
  anomaly:
    type: "z_score"
    window: 20
    threshold: 2.5
  sentiment:
    type: "vader"
    calibration_dataset: "zeroshot/twitter-financial-news-sentiment"

automaton:
  type: "associative_l_r_i"
  actions: ["A1_sentiment", "A2_anomaly"]
  learning_rate: 0.05
  init_prob: 0.5

evaluation:
  metrics: ["reward_rate", "sharpe_ratio", "max_drawdown", "win_rate"]
  split:
    train: "2022-01-01 to 2023-12-31"
    validation: "2024-01-01 to 2024-12-31"
    test: "2025-01-01 to 2025-12-31"
YAML

echo "   ✓ configs/v1_baseline.yaml written"

# ─────────────────────────────────────────────
# 5. experiments/v1_baseline (folder + metadata)
# ─────────────────────────────────────────────
echo "🧪 [5/7] Creating experiments/v1_baseline..."

mkdir -p experiments/v1_baseline/results/figures
mkdir -p experiments/v1_baseline/results/tables
mkdir -p experiments/v1_baseline/logs
mkdir -p experiments/v1_baseline/notebooks

touch experiments/v1_baseline/results/figures/.gitkeep
touch experiments/v1_baseline/results/tables/.gitkeep
touch experiments/v1_baseline/logs/.gitkeep
touch experiments/v1_baseline/notebooks/.gitkeep

cat > experiments/v1_baseline/metadata.json << 'JSON'
{
  "version": "v1_baseline",
  "date_created": "2026-11-07",
  "author": "Saleh Tarkashvand",
  "description": "Initial prototype with VADER sentiment and Z-score anomaly",
  "models": {
    "anomaly": {"type": "z_score", "window": 20, "threshold": 2.5},
    "sentiment": {"type": "vader", "accuracy": 0.481}
  },
  "automaton": {
    "type": "associative_l_r_i",
    "actions": ["A1_sentiment", "A2_anomaly"],
    "learning_rate": 0.05
  },
  "results": {
    "reward_rate_btc": 0.487,
    "baseline_sentiment": 0.499,
    "baseline_anomaly": 0.501
  },
  "notes": "All sanity checks passed. Sentiment is synthetic."
}
JSON

echo "   ✓ experiments/v1_baseline created"

# ─────────────────────────────────────────────
# 6. src/utils/experiment_logger.py
# ─────────────────────────────────────────────
echo "📝 [6/7] Writing src/utils/experiment_logger.py..."

cat > src/utils/experiment_logger.py << 'PY'
"""
SALA Project - Experiment Logger
================================
Automatically creates versioned experiment folders and metadata files.

Usage
-----
from src.utils.experiment_logger import create_experiment, update_results

create_experiment(
    version_name="v2_real_data",
    description="Added Kaggle + GDELT real sentiment data.",
    models={...},
    automaton={...},
    data={...},
)

# After running the model:
update_results("v2_real_data", {"reward_rate": 0.512})
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

EXPERIMENTS_DIR = Path(__file__).resolve().parent.parent.parent / "experiments"


def create_experiment(
    version_name: str,
    description: str,
    models: dict,
    automaton: dict,
    data: dict,
) -> Path:
    """
    Create a new experiment folder with a metadata.json file.
    Returns the path to the experiment folder.
    """
    exp_dir = EXPERIMENTS_DIR / version_name
    exp_dir.mkdir(parents=True, exist_ok=True)

    # Subfolders
    for sub in ["results/figures", "results/tables", "logs", "notebooks"]:
        (exp_dir / sub).mkdir(parents=True, exist_ok=True)
        (exp_dir / sub / ".gitkeep").touch()

    timestamp = datetime.now().isoformat(timespec="seconds")
    metadata = {
        "version": version_name,
        "date_created": timestamp,
        "description": description,
        "models": models,
        "automaton": automaton,
        "data": data,
        "results": {},
    }

    metadata_path = exp_dir / f"{timestamp[:10]}_metadata.json"
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print(f"✅ Created experiment: {exp_dir}")
    print(f"   Metadata: {metadata_path}")
    return exp_dir


def update_results(version_name: str, results: dict) -> None:
    """
    Update the results section of the latest metadata.json for a version.
    """
    exp_dir = EXPERIMENTS_DIR / version_name
    metadata_files = sorted(exp_dir.glob("*_metadata.json"))
    if not metadata_files:
        raise FileNotFoundError(f"No metadata found in {exp_dir}")

    metadata_path = metadata_files[-1]
    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    metadata["results"] = results
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print(f"✅ Updated results in: {metadata_path}")
PY

echo "   ✓ experiment_logger.py written"

# ─────────────────────────────────────────────
# 7. CHANGELOG.md, Makefile, README (append note)
# ─────────────────────────────────────────────
echo "📚 [7/7] Writing CHANGELOG.md and Makefile..."

cat > CHANGELOG.md << 'MD'
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
MD

cat > Makefile << 'MK'
.PHONY: setup test download train report clean tree

setup:
	@echo "Creating conda environment from environment.yml..."
	conda env create -f environment.yml || echo "Environment exists."

test:
	pytest tests/ -v

download:
	python scripts/download_data.py

train:
	python scripts/run_experiment.py --config configs/v1_baseline.yaml

report:
	python scripts/generate_report.py --config configs/v1_baseline.yaml

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

tree:
	find . -type d -not -path './.git*' -not -path './.venv*' \
		-not -path '*/__pycache__*' -not -path './.vscode*' \
		| sort | sed -e 's;[^/]*/;|____;g;s;____|; |;g'
MK

echo "   ✓ CHANGELOG.md and Makefile written"

# ─────────────────────────────────────────────
# Done
# ─────────────────────────────────────────────
echo ""
echo "✅ Structure expansion complete."
echo ""
echo "Next steps:"
echo "  1. Review the new layout:  make tree"
echo "  2. Stage and commit:       git add ."
echo "  3. Commit:                 git commit -m 'chore: expand project to professional layout'"
echo ""