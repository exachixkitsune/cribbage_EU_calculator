# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 16:20:35 2023
"""

from __future__ import annotations

import itertools
from collections.abc import Iterable
from itertools import combinations

from card import Card, convert_card_array_to_enum_array
from cardenums import CardVal


def calculate_score(hand: set[Card], starter: Card) -> int:
    """
    Calculates the score of a hand of cards.
    https://en.wikipedia.org/wiki/Rules_of_cribbage#The_show
    Scoring routes:
        1. Separate combination of cards totaling 15, 2 points
        2. Runs - run of 3-5; 3:3, 4:4, 5:5
        3. Pairs - each pair scores 2;
            This does scale; 3 cards score 6 (AB,AC,BC = 3x2 = 6)
            4 cards score 12 (AB,AC,AD,BC,BD,CD = 6x2 = 12)
            Thus, just check each pair.
        4. Flush - 2 mutually exclusive options
            4 card flush 4 points
            5 card flush 5 points
        5. "His Nobs" - holding a jack in hand, same suit as starter.
    """

    # ASSERT:
    assert len(hand) == 4

    # Generate set of all cards
    # Copy here to avoid ruining hand
    full_set = set(hand)
    full_set.add(starter)

    full_set_vals, _ = convert_card_array_to_enum_array(full_set)

    this_score = {
        "fifteen": calculate_score_1_15s(full_set_vals),
        "runs": calculate_score_2_runs(full_set_vals),
        "pairs": calculate_score_3_pairs(full_set_vals),
        "flush": calculate_score_4_flush(hand, starter),
        "nobs": calculate_score_5_nobs(hand, starter),
    }

    return sum(this_score.values())


def calculate_score_1_15s(full_set_vals: list[CardVal]) -> int:
    """
    Calculate 15s
    """
    # Convert each score to a value
    # Values cap at 10 points
    full_set_points = [min(int(x), 10) for x in full_set_vals]

    # Evaluate each combination
    return sum(
        2 * (sum(potential_set) == 15)
        for potential_set
        in itertools.chain(
            combinations(full_set_points, 2),
            combinations(full_set_points, 3),
            combinations(full_set_points, 4),
            [full_set_points],
        )
    )


def calculate_score_2_runs(full_set_vals: list[CardVal]) -> int:
    """
    Look for Runs
    Basically, want to find every instance of runs within the set of values
    the danger here is double-counting a run of 3 which is part of a run of 4, and so on.
    """

    # Ensure the values are sorted, otherwise combinations may not give correctly ordered combos.
    full_set_vals = sorted(full_set_vals)

    # First, check if all 5 items are a run
    #   If this is the case, no other set can be scored (as any set of 4 will be part of this)
    if is_a_run(full_set_vals):
        return 5

    # Second, check if any combination of 4 is a run
    valid_runs = sum(len(cards) for cards in combinations(full_set_vals, 4) if is_a_run(cards))

    if valid_runs:
        return valid_runs

    return sum(len(cards) for cards in combinations(full_set_vals, 3) if is_a_run(cards))


def is_a_run(test: Iterable[CardVal]) -> bool:
    """
    Is this list of numbers a run
    """
    test_iter = test.__iter__()
    lowest = test_iter.__next__() + 1

    return all(lowest + idx == value for idx, value in enumerate(test_iter))


def calculate_score_3_pairs(full_set_vals: list[CardVal]) -> int:
    """
    How many pairs are there in this set?
    Hopefully, trivial?
    Each pair scores 2
    Simple combinatronics
    """
    return sum(2 * (i[0] == i[1]) for i in combinations(full_set_vals, 2))


def calculate_score_4_flush(hand: set[Card], starter: Card) -> int:
    """
    Check for a flush, and score as appropriate
    I.e. 4 for a flush in hand only, 5 for a flush including the starter
    """

    # Are all the hand suits the same?
    all_hand_same = set(card.suit for card in hand)

    if len(all_hand_same) != 1:
        return 0

    return 5 if all_hand_same.pop() == starter.suit else 4


def calculate_score_5_nobs(hand: set[Card], starter: Card) -> int:
    """
    Check for "The Nobs"
    I.e. if a card in hand is a jack of the same suit as the starter card
    """
    for i_hand_card in hand:
        if (i_hand_card.val == CardVal.VAL_J) and (i_hand_card.suit == starter.suit):
            return 1
    return 0
