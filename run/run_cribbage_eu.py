# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 16:40:49 2023
"""

from time import time

import card

from cribbage_eu import calculate_cribbage_eu, present_results


if __name__ == "__main__":
    start_time = time()

    cards = set(map(card.Card.from_str, ["2H", "9H", "XS", "JC", "JD", "KC"]))

    print(f"{time()-start_time:.0f}: Analysing " + card.convert_cardlist_to_str(cards))
    results_out = calculate_cribbage_eu(cards, provide_status=False)
    present_results(list(results_out), 4)
    print(f"{time()-start_time:.0f}: finished in {time() - start_time}")
