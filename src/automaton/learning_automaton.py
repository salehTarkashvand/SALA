"""
SALA Project - Learning Automaton (L_R-I)
==========================================
A simple Learning Automaton with two actions, using the
Linear Reward-Inaction (L_R-I) update rule.

Theory (from Chapter 2 of the course notes):
- Actions: α = {A1, A2}
- Action probability vector: P = [p1, p2],  p1 + p2 = 1
- When action A_i is rewarded:  p_i += a * (1 - p_i)
                                 p_j -= a * p_j  (j ≠ i)
- When action A_i is penalized: no change (inaction)
"""

from __future__ import annotations

import numpy as np


class LearningAutomaton:
    """
    Two-action Learning Automaton with L_R-I update rule.

    Parameters
    ----------
    learning_rate : float
        Reward parameter `a` in (0, 1). Larger = faster learning but
        more noise. Default 0.05.
    init_prob : float
        Initial probability of action A1. Default 0.5 (uniform).
    seed : int or None
        Random seed for reproducibility.
    """

    def __init__(self, learning_rate: float = 0.05, init_prob: float = 0.5,
                 seed: int | None = None):
        if not (0 < learning_rate < 1):
            raise ValueError("learning_rate must be in (0, 1)")
        if not (0 < init_prob < 1):
            raise ValueError("init_prob must be in (0, 1)")

        self.a = learning_rate
        self.p = np.array([init_prob, 1.0 - init_prob], dtype=float)
        self.rng = np.random.default_rng(seed)

    # ------------------------------------------------------------------
    # Choose an action
    # ------------------------------------------------------------------
    def choose_action(self) -> int:
        """
        Sample an action index from the current probability vector.
        Returns 0 (A1) or 1 (A2).
        """
        return int(self.rng.choice(2, p=self.p))

    # ------------------------------------------------------------------
    # Update probabilities
    # ------------------------------------------------------------------
    def update(self, action: int, reward: bool) -> None:
        """
        Update the probability vector after receiving feedback.

        Parameters
        ----------
        action : int
            The action that was taken (0 or 1).
        reward : bool
            True if the action was rewarded, False if penalized.
            Under L_R-I, penalized actions cause no change.
        """
        if not reward:
            return  # inaction: no update on penalty

        # Reward: increase p[action], decrease the other
        self.p[action] += self.a * (1.0 - self.p[action])
        self.p[1 - action] = 1.0 - self.p[action]

    # ------------------------------------------------------------------
    # Inspect
    # ------------------------------------------------------------------
    def get_probabilities(self) -> np.ndarray:
        return self.p.copy()

    def reset(self, init_prob: float = 0.5) -> None:
        self.p = np.array([init_prob, 1.0 - init_prob], dtype=float)

    def __repr__(self) -> str:
        return f"LearningAutomaton(p=[{self.p[0]:.3f}, {self.p[1]:.3f}], a={self.a})"