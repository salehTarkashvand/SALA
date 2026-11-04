"""
SALA Project - Associative Learning Automaton
==============================================
An associative version of the Learning Automaton: it keeps one
L_R-I automaton per context (market state), so the policy can
differ between normal, anomalous, bullish, and bearish states.

Context key (for SALA):
    (sentiment_label, anomaly_flag)
    e.g. ("positive", 0), ("negative", 1), ...
"""

from __future__ import annotations

from collections import defaultdict
from typing import Hashable

from src.automaton.learning_automaton import LearningAutomaton


class AssociativeLearningAutomaton:
    """
    Associative LA: one L_R-I automaton per context key.

    Parameters
    ----------
    learning_rate : float
        Passed to each per-context LearningAutomaton.
    init_prob : float
        Initial probability of A1 for each new context.
    seed : int or None
        Base seed; each context gets a distinct sub-seed.
    """

    def __init__(self, learning_rate: float = 0.05, init_prob: float = 0.5,
                 seed: int | None = None):
        self.a = learning_rate
        self.init_prob = init_prob
        self.seed = seed
        self.automata: dict[Hashable, LearningAutomaton] = {}

    # ------------------------------------------------------------------
    # Internal: lazy creation of per-context automaton
    # ------------------------------------------------------------------
    def _get(self, context: Hashable) -> LearningAutomaton:
        if context not in self.automata:
            sub_seed = None if self.seed is None else hash(context) % (2**32) + self.seed
            self.automata[context] = LearningAutomaton(
                learning_rate=self.a,
                init_prob=self.init_prob,
                seed=sub_seed,
            )
        return self.automata[context]

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def choose_action(self, context: Hashable) -> int:
        return self._get(context).choose_action()

    def update(self, context: Hashable, action: int, reward: bool) -> None:
        self._get(context).update(action, reward)

    def get_probabilities(self, context: Hashable) -> list[float]:
        return self._get(context).get_probabilities().tolist()

    def known_contexts(self) -> list[Hashable]:
        return sorted(self.automata.keys(), key=str)

    def summary(self) -> dict[Hashable, list[float]]:
        return {ctx: self.get_probabilities(ctx) for ctx in self.automata}

    def __repr__(self) -> str:
        return (f"AssociativeLearningAutomaton("
                f"n_contexts={len(self.automata)}, a={self.a})")