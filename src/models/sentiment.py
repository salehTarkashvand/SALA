"""
SALA Project - Sentiment Analyzer
==================================
Scores text (tweets, news) using VADER, then aggregates to a daily score.

Two modes:
1. `score_text(text)` - VADER compound score for a single text
2. `aggregate_daily(df)` - mean score per day

Output:
- data/processed/sentiment_daily.csv
  Columns: Date, Sentiment_Score, Sentiment_Label, N_Texts

Labels:
- positive: score > 0.05
- negative: score < -0.05
- neutral : otherwise
"""

from __future__ import annotations

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from src.config import PROCESSED_DIR, TABLES_DIR


# ----------------------------------------------------------------------
# VADER scoring
# ----------------------------------------------------------------------
_analyzer = SentimentIntensityAnalyzer()


def score_text(text: str) -> float:
    """
    Return VADER compound score for one text.
    Range: [-1, +1]. Returns 0.0 for empty/invalid text.
    """
    if not isinstance(text, str) or not text.strip():
        return 0.0
    return _analyzer.polarity_scores(text)["compound"]


def label_from_score(score: float) -> str:
    """Convert numeric score to a human-readable label."""
    if score > 0.05:
        return "positive"
    if score < -0.05:
        return "negative"
    return "neutral"


# ----------------------------------------------------------------------
# Aggregate to daily
# ----------------------------------------------------------------------
def aggregate_daily(
    df: pd.DataFrame,
    date_col: str = "Date",
    text_col: str = "Text",
) -> pd.DataFrame:
    """
    Given a DataFrame with columns [Date, Text], compute daily mean sentiment.
    Returns DataFrame with columns [Date, Sentiment_Score, Sentiment_Label, N_Texts].
    """
    out = df.copy()
    out["Sentiment_Score"] = out[text_col].apply(score_text)

    daily = (
        out.groupby(date_col)
        .agg(
            Sentiment_Score=("Sentiment_Score", "mean"),
            N_Texts=("Sentiment_Score", "count"),
        )
        .reset_index()
    )
    daily["Sentiment_Label"] = daily["Sentiment_Score"].apply(label_from_score)
    daily = daily.sort_values(date_col).reset_index(drop=True)
    return daily


def save_daily_sentiment(daily: pd.DataFrame) -> None:
    """Save daily sentiment to data/processed/sentiment_daily.csv."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    path = PROCESSED_DIR / "sentiment_daily.csv"
    daily.to_csv(path, index=False)
    print(f"Saved: {path.name}  ({len(daily)} rows)")


def save_summary(daily: pd.DataFrame) -> None:
    """Save summary counts to results/tables/sentiment_summary.csv."""
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    summary = daily["Sentiment_Label"].value_counts().rename_axis("Label").reset_index(name="Days")
    path = TABLES_DIR / "sentiment_summary.csv"
    summary.to_csv(path, index=False)
    print(f"Saved: {path.name}")
    print(summary.to_string(index=False))


# ----------------------------------------------------------------------
# Calibration against Twitter Financial News Sentiment
# ----------------------------------------------------------------------
def calibrate_on_phrasebank(max_rows: int | None = None) -> pd.DataFrame:
    """
    Load Twitter Financial News Sentiment, score each text with VADER,
    and report accuracy against the gold labels.

    Labels: 0=Bearish (negative), 1=Bullish (positive), 2=Neutral
    """
    from datasets import load_dataset

    ds = load_dataset("zeroshot/twitter-financial-news-sentiment")
    df = ds["train"].to_pandas()

    if max_rows is not None:
        df = df.head(max_rows)

    # Gold labels: 0=negative, 1=positive, 2=neutral
    label_map = {0: "negative", 1: "positive", 2: "neutral"}
    df["gold_label"] = df["label"].map(label_map)
    df["vader_score"] = df["text"].apply(score_text)
    df["pred_label"] = df["vader_score"].apply(label_from_score)

    acc = (df["gold_label"] == df["pred_label"]).mean()
    print(f"Calibration on {len(df)} texts")
    print(f"Accuracy: {acc:.3f}")
    print()
    print("Confusion (gold vs predicted):")
    print(pd.crosstab(df["gold_label"], df["pred_label"]))

    return df