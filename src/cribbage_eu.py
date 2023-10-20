# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 13:50:09 2023

Functions here to calculate the EU from a single hand

A player will have a hand of 6 cards, they can downselect from that 4 cards;
which 4 cards gives the best EU?

Calculations for EU:
    1. Score from the hand remaining
    2. Score from the crib; either if the crib is yours or the crib is your Opps.

OP's hand's score is not dependant on your actions.

3 levels of stats outputs:
    Just the Mean
    "Minimum","Maximum","Mean","Standard Deviation","Median"
    Full list of potential values
"""

import concurrent.futures
from typing import Callable, Iterable
from itertools import combinations

from card import Card, all_possible_cards, convert_cardlist_to_str
from stats import DiscardOption, ScoringStats
from scorecalc import calculate_score


def present_results(results_in: list[DiscardOption], num_make: int = 3) -> None:
    """
    Describe the results

    Describe the following:
        1. Top n most hand EU (mean)
        2. Top n most hand EU (median)
        3. Top n garunteed hand score
        4. What gives the best overall EU (if own crib)
        5. What gives the best delta EU (if own crib)
        6. What gives LEAST crib EU
    """

    # Limits
    num_make = min(num_make, len(results_in))

    # 1.
    print(f"Top {num_make} highest EU options (mean)")
    provide_results(results_in, lambda x: x.hand_scores.mean, num_make)
    print()

    # 2.
    print(f"Top {num_make} highest EU options (median)")
    provide_results(results_in, lambda x: x.hand_scores.median, num_make)
    print()

    # 3.
    print(f"Top {num_make} highest min hand score")
    provide_results(results_in, lambda x: x.hand_scores.min, num_make)
    print()

    # 4.
    print(f"Top {num_make} best overall EU (hand + crib)")
    provide_results(
        results_in,
        lambda x: x.hand_scores.mean + x.crib_scores.mean,
        num_make,
    )
    print()

    # 5.
    print(f"Top {num_make} best overall EU (hand - crib)")
    provide_results(
        results_in,
        lambda x: x.hand_scores.mean - x.crib_scores.mean,
        num_make,
    )
    print()

    # 6.
    print(f"Top {num_make} LEAST crib EU")
    provide_results(results_in, lambda x: -x.crib_scores.mean, num_make)
    print()

    # 7.
    print(f"Top {num_make} MOST crib EU (mean)")
    provide_results(results_in, lambda x: x.crib_scores.mean, num_make)


def provide_results(
    results_in: list[DiscardOption],
    keyfunc: Callable[[DiscardOption], float],
    num_make: int = 3,
) -> None:
    """
    Function taking the card list,
    sorting,
    printing the top n rows
    and any rows matching the last value
    """

    if num_make < 1:
        return

    results_in.sort(reverse=True, key=keyfunc)

    # Get the value for the nth place,
    # we will display all records that are at least this value.
    final_val = keyfunc(results_in[num_make - 1])
    last_val = -100.123

    for i_row, result in enumerate(results_in):
        score = keyfunc(results_in[i_row])

        if score < final_val:
            break

        print(
            (
                f"Discard {{{convert_cardlist_to_str(result.discard, True)}}}, "
                f"keep {{{convert_cardlist_to_str(result.hand, True)}}}: {score:.2f}"
                f"{'=' if score == last_val else ''}"
            )
        )

        last_val = score


def calculate_cribbage_eu(
    initial_hand: set[Card],
    num_discard: int = 2,
) -> Iterable[DiscardOption]:
    """
    Calculate the EU for each option of discard to crib.


    Process:
        A. Select one of the combinations of 4 cards to keep and 2 to discard
            1. Score from the hand:
                a. Set a list of "Excluded" cards (2 discarded cards)
                b. Iterate over a list of all potential cards, except the ones in hand or excluded
                c. determine potential handscore from each option (Multi) -> store.
            2. Score from the crib:
                a. Generate a list of possible cards in hand.
                b. Generate combinations iterator
                c. Score each combinations (Multi) -> store.
        B. Interpret each score

    """

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Validation
    # assert(len(initial_hand) == 6)

    # Generate each combination of potential cards to discard to crib
    # Use indicies, as this enables
    discards = [set(discard) for discard in combinations(initial_hand, num_discard)]

    # Iterate over each option
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(calculate_score_for_option, initial_hand - discard, discard)
            for discard in discards
        ]
        for result in concurrent.futures.as_completed(futures):
            yield result.result()


def calculate_score_for_option(hand: set[Card], discard: set[Card]) -> DiscardOption:
    # What cards remain in hand
    i_discard = discard
    i_hand = hand

    # Calculate potential scores from hand
    hand_scores = calculate_scores_from_hand(i_hand, i_discard)
    crib_scores = calculate_scores_from_crib(i_hand, i_discard)

    # Calculate Stats
    discard_stats = DiscardOption(
        i_hand, i_discard, ScoringStats(hand_scores), ScoringStats(crib_scores)
    )

    return discard_stats


def calculate_scores_from_hand(
    hand_cards: set[Card], excluded_cards: set[Card]
) -> list[int]:
    """
    Calculate the scores for the hand

    as above;
        a. Set a list of "Excluded" cards (2 discarded cards) (input as excluded_cards)
        b. Iterate over a list of all potential cards, except the ones in hand or excluded
        c. determine potential handscore from each option (Multi) -> store.

        When providing status, need to inject in the middle of the loop system, so manually define
        the loop. Otherwise, can just use the map.
    """

    all_excluded_cards = hand_cards.union(excluded_cards)

    results_list = [
        calculate_score(hand_cards, starter_card)
        for starter_card in all_possible_cards()
        if (starter_card not in all_excluded_cards)
    ]

    return results_list


def calculate_scores_from_crib(
    hand_cards: set[Card], discarded_cards: set[Card]
) -> list[int]:
    """
    Calculate the scores for the crib

    as above;
        a. Generate a list of possible cards in hand.
        b. Generate combinations iterator
        c. Score each combination (Multi) -> store.
    """

    # Possible cards in hand
    all_excluded_cards = hand_cards.union(discarded_cards)
    possible_cards = [
        starter_card
        for starter_card in all_possible_cards()
        if (starter_card not in all_excluded_cards)
    ]

    # Crib is at least the two discarded cards + 2 cards discarded by op + 1 card starter
    # Thus, 2 discarded_cards + combination of 3 other cards; of which each 1 is taken as the
    # starter once. This covers the entire possibility space.
    # Alternative is to extract one possible card, and then combination across the rest of the space
    # And that seems too complicated.
    results_list = []
    for i_cards_tuple in combinations(possible_cards, 3):
        i_cards = set(i_cards_tuple)
        for i_starter in i_cards:
            # Calculate score
            results_list.append(
                calculate_score(discarded_cards.union(i_cards) - {i_starter}, i_starter)
            )

    return results_list
