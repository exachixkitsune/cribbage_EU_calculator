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

from typing import List, Dict, Tuple, Callable
from itertools import combinations
from time import time
from statistics import mean, stdev, median

from card import Card, convert_cardlist_to_str, all_possible_cards
from scorecalc import calculate_score


def present_results(
    results_in: List[Dict],
    num_make: int = 3,
    emoji_mode: bool = False,
) -> None:
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
    provide_results(results_in, lambda x: x["hand_eu"]["mean"], num_make, emoji_mode)

    # 2.
    print(f"Top {num_make} highest EU options (median)")
    provide_results(results_in, lambda x: x["hand_eu"]["median"], num_make, emoji_mode)

    # 3.
    print(f"Top {num_make} highest min hand score")
    provide_results(results_in, lambda x: x["hand_eu"]["min"], num_make, emoji_mode)

    # 4.
    print(f"Top {num_make} best overall EU (hand + crib)")
    provide_results(
        results_in,
        lambda x: x["hand_eu"]["mean"] + x["crib_eu"]["mean"],
        num_make,
        emoji_mode,
    )

    # 5.
    print(f"Top {num_make} best overall EU (hand - crib)")
    provide_results(
        results_in,
        lambda x: x["hand_eu"]["mean"] - x["crib_eu"]["mean"],
        num_make,
        emoji_mode,
    )

    # 6
    print(f"Top {num_make} LEAST crib EU")
    provide_results(results_in, lambda x: -x["crib_eu"]["mean"], num_make, emoji_mode)

    # 6
    print(f"Top {num_make} MOST crib EU (mean)")
    provide_results(results_in, lambda x: x["crib_eu"]["mean"], num_make, emoji_mode)


def provide_results(
    results_in: List[Dict],
    keyfunc: Callable,
    num_make: int = 3,
    emoji_mode: bool = False,
) -> None:
    """
    Function taking the card list,
    sorting,
    printing the top n rows
    and any rows matching the last value
    """
    results_in.sort(reverse=True, key=keyfunc)
    for i_row in range(num_make):
        this_val = keyfunc(results_in[i_row])
        print(
            f"  {i_row:2.0f}:discard:"
            + "{"
            + ",".join(
                convert_cardlist_to_str(results_in[i_row]["discard"], emoji_mode)
            )
            + "}"
            + f": EU:{this_val:.2f}"
            + " (keep: {"
            + ",".join(convert_cardlist_to_str(results_in[i_row]["hand"], emoji_mode))
            + "})"
        )

    last_val = keyfunc(results_in[i_row])
    for i_row in range(num_make, len(results_in)):
        if keyfunc(results_in[i_row]) != last_val:
            break
        this_val = keyfunc(results_in[i_row])
        print(
            f"  {i_row:2.0f}:discard:"
            + "{"
            + ",".join(
                convert_cardlist_to_str(results_in[i_row]["discard"], emoji_mode)
            )
            + "}"
            + f": EU:{this_val:.2f}"
            + " (keep: {"
            + ",".join(convert_cardlist_to_str(results_in[i_row]["hand"], emoji_mode))
            + "})"
        )


def calculate_cribbage_EU(
    initial_hand: List[Card],
    provide_status: bool = False,
    update_interval: int = 1,
    emoji_mode: bool = False,
    num_discard: int = 2,
) -> List[Dict]:
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
    discard_options_indicies_iterator = combinations(
        range(len(initial_hand)), num_discard
    )

    hand_count = 0

    overall_results = []

    # Iterate over each option
    start_time = time()
    for i_discard_option_indicies in discard_options_indicies_iterator:
        # What cards remain in hand
        i_hand_cards_indicies = set(range(len(initial_hand))) - set(
            i_discard_option_indicies
        )

        i_discard = [initial_hand[i] for i in i_discard_option_indicies]
        i_hand = [initial_hand[i] for i in i_hand_cards_indicies]

        if provide_status:
            hand_count += 1
            discard_cards = (
                "{" + ",".join(convert_cardlist_to_str(i_discard, emoji_mode)) + "}"
            )
            hand_cards = (
                "{" + ",".join(convert_cardlist_to_str(i_hand, emoji_mode)) + "}"
            )
            curr_time = time() - start_time
            print(
                (
                    f"{curr_time:.0f}:On Hand {hand_count}, "
                    f"with hand:{hand_cards}, discard:{discard_cards}"
                )
            )

        # Calculate potential scores from hand
        hand_scores = calculate_scores_from_hand(i_hand, i_discard)

        crib_scores, _ = calculate_scores_from_crib(i_hand, i_discard)

        # Calculate Stats
        hand_eu = {
            "raw": hand_scores,
            "mean": mean(hand_scores),
            "stdev": stdev(hand_scores),
            "median": median(hand_scores),
            "min": min(hand_scores),
            "max": max(hand_scores),
        }
        crib_eu = {
            "raw": crib_scores,
            "mean": mean(crib_scores),
            "stdev": stdev(crib_scores),
            "median": median(crib_scores),
            "min": min(crib_scores),
            "max": max(crib_scores),
        }
        overall_results.append(
            {
                "hand": i_hand,
                "discard": i_discard,
                "hand_eu": hand_eu,
                "crib_eu": crib_eu,
            }
        )

        if provide_status:
            curr_time = time() - start_time
            print(
                (
                    f"{curr_time:.0f}:  hand score: {hand_eu['mean']:.2f}±{hand_eu['stdev']:.2f}, "
                    f"median:{hand_eu['median']}, range:{hand_eu['min']}-{hand_eu['max']}"
                )
            )
            curr_time = time() - start_time
            print(
                (
                    f"{curr_time:.0f}:  crib score: {crib_eu['mean']:.2f}±{crib_eu['stdev']:.2f}, "
                    f"median:{crib_eu['median']}, range:{crib_eu['min']}-{crib_eu['max']}"
                )
            )

    return overall_results


def calculate_scores_from_hand(
    hand_cards: List[Card], excluded_cards: List[Card]
) -> List[int]:
    """
    Calculate the scores for the hand

    as above;
        a. Set a list of "Excluded" cards (2 discarded cards) (input as excluded_cards)
        b. Iterate over a list of all potential cards, except the ones in hand or excluded
        c. determine potential handscore from each option (Multi) -> store.

        When providing status, need to inject in the middle of the loop system, so manually define
        the loop. Otherwise, can just use the map.
    """

    all_excluded_cards = hand_cards + excluded_cards

    results_list = [
        calculate_score(hand_cards, starter_card)
        for starter_card in all_possible_cards()
        if (starter_card not in all_excluded_cards)
    ]

    return results_list


def calculate_scores_from_crib(
    hand_cards: List[Card], discarded_cards: List[Card]
) -> Tuple[List[int], list[list[object]]]:
    """
    Calculate the scores for the crib

    as above;
        a. Generate a list of possible cards in hand.
        b. Generate combinations iterator
        c. Score each combination (Multi) -> store.
    """

    # Possible cards in hand
    all_excluded_cards = hand_cards + discarded_cards
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
    detailed_list = []
    for i_cards in combinations(possible_cards, 3):
        for i_starter in range(len(i_cards)):
            i_cribcards = list(set(range(3)) - {i_starter})
            # Calculate score
            results_list.append(
                calculate_score(
                    discarded_cards
                    + [i_cards[i_cribcards[0]], i_cards[i_cribcards[1]]],
                    i_cards[i_starter],
                )
            )
            detailed_list.append(
                [
                    [
                        i_cards[i_starter],
                        discarded_cards
                        + [i_cards[i_cribcards[0]], i_cards[i_cribcards[1]]],
                    ],
                    results_list[-1],
                ]
            )

    return (results_list, detailed_list)
