# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 16:20:35 2023
"""

from __future__ import annotations

from copy import copy
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
    set_lists = [
        *[list(i) for i in combinations(full_set_points, 2)],
        *[list(i) for i in combinations(full_set_points, 3)],
        *[list(i) for i in combinations(full_set_points, 4)],
        full_set_points,
    ]

    # list of points: list(map(check_15_score, set_lists))
    # So to give total points:
    return sum(list(map(check_15_score, set_lists)))


def check_15_score(set_points: list[int]) -> int:
    """
    Checking: do the contents of set_points add up to 15 exactly.
    """
    score = sum(set_points)
    if score == 15:
        return 2

    return 0


def calculate_score_2_runs(full_set_vals: list[CardVal]) -> int:
    """
    Look for Runs
    Basically, want to find every instance of runs within the set of values
    the danger here is double-counting a run of 3 which is part of a run of 4, and so on.
    """

    # First, check if all 5 items are a run
    #   If this is the case, no other set can be scored (as any set of 4 will be part of this)
    if is_a_run(full_set_vals):
        return 5

    # Second, check if any combination of 4 is a run
    valid_runs = []
    combination_indicies = list(combinations(range(5), 4))
    for i_combination_set in combination_indicies:
        if is_a_run([full_set_vals[i] for i in i_combination_set]):
            valid_runs.append(copy(i_combination_set))

    # Third, check is any combination of 3 is a run
    # but if the combination is in the combination, reject
    valid_runs_2 = []
    combination_indicies_2 = list(combinations(range(5), 3))
    for i_combination_set_2 in combination_indicies_2:
        if any(is_a_subset_b(i_combination_set_2, j) for j in valid_runs):
            continue
        if is_a_run(full_set_vals[i] for i in i_combination_set_2):
            valid_runs_2.append(copy(i_combination_set_2))

    # Score
    return sum(len(i) for i in valid_runs) + sum(len(i) for i in valid_runs_2)


def is_a_run(test: Iterable[CardVal]) -> bool:
    """
    Is this list of numbers a run
    """
    this_test = list(test)
    this_test.sort()

    # Are all numbers sequential?
    # delta:
    delta = [this_test[i + 1] - this_test[i] for i in range(len(this_test) - 1)]

    # if all sequential, delta is always 1
    return all(i == 1 for i in delta)


def is_a_subset_b(valuesa: tuple[int, ...], valuesb: tuple[int, ...]) -> bool:
    """
    Check if a is a subset of b
    """
    return set(valuesa) <= set(valuesb)


def calculate_score_3_pairs(full_set_vals: list[CardVal]) -> int:
    """
    How many pairs are there in this set?
    Hopefully, trivial?
    Each pair scores 2
    Simple combinatronics
    """

    set_pairs = [list(i) for i in combinations(full_set_vals, 2)]

    return sum(list(map(check_pair_and_score, set_pairs)))


def check_pair_and_score(set_vals: list[CardVal]) -> int:
    """
    Is this a pair? If so, return 2 points
    """
    if set_vals[0] == set_vals[1]:
        return 2
    return 0


def calculate_score_4_flush(hand: set[Card], starter: Card) -> int:
    """
    Check for a flush, and score as appropriate
    I.e. 4 for a flush in hand only, 5 for a flush including the starter
    """
    _, hand_suits = convert_card_array_to_enum_array(hand)

    # Are all the hand suits the same?
    all_hand_same = all(
        hand_suits[0] == hand_suits[i + 1] for i in range(len(hand_suits) - 1)
    )
    if all_hand_same:
        if hand_suits[0] == starter.suit:
            return 5
        return 4

    return 0


def calculate_score_5_nobs(hand: set[Card], starter: Card) -> int:
    """
    Check for "The Nobs"
    I.e. if a card in hand is a jack of the same suit as the starter card
    """
    for i_hand_card in hand:
        if (i_hand_card.val == CardVal.VAL_J) and (i_hand_card.suit == starter.suit):
            return 1
    return 0
