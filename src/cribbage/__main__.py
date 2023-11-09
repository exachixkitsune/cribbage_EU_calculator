# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 16:40:49 2023
"""

import sys
from time import time

from cribbage import card
from cribbage.cribbage_eu import calculate_cribbage_eu, present_results


def main() -> None:
    """Get cards from command line and run the analysis."""
    start_time = time()

    print(sys.argv[1:])
    cards = set(map(card.Card.from_str, sys.argv[1:]))

    print(f"{time()-start_time:.0f}: Analysing " + card.convert_cardlist_to_str(cards))
    results_out = calculate_cribbage_eu(cards)
    present_results(list(results_out), 4)
    print(f"{time()-start_time:.0f}: finished in {time() - start_time}")


if __name__ == "__main__":
    main()
