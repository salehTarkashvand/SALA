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
