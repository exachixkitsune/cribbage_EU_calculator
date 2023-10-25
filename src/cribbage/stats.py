"""Stats"""

import statistics

from .card import Card


class ScoringStats:
    """Stats for a specific scenario"""

    possible_scores: list[int]
    mean: float
    stdev: float
    median: float
    min: int
    max: int

    def __init__(self, scores: list[int]) -> None:
        self.possible_scores = scores
        self.mean = statistics.mean(scores)
        self.stdev = statistics.stdev(scores)
        self.median = statistics.median(scores)
        self.min = min(scores)
        self.max = max(scores)

    def __str__(self) -> str:
        return f"{self.mean:.2f}±{self.stdev:.2f}"

    def __hash__(self) -> int:
        return hash(self.possible_scores)


class DiscardOption:
    """Stats for a hand+discard combo."""

    hand: set[Card]
    discard: set[Card]

    hand_scores: ScoringStats
    crib_scores: ScoringStats

    def __init__(
        self,
        hand: set[Card],
        discard: set[Card],
        hand_scores: ScoringStats,
        crib_scores: ScoringStats,
    ) -> None:
        self.hand = hand
        self.discard = discard

        self.hand_scores = hand_scores
        self.crib_scores = crib_scores

    def __str__(self) -> str:
        return f"keep {self.hand}, discard {self.discard}"

    def __hash__(self) -> int:
        return hash((self.hand, self.discard))
