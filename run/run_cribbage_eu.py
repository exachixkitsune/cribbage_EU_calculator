# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 16:40:49 2023
"""


from card import Card, convert_cardlist_to_str
from time import time
from cribbage_eu import (
    calculate_cribbage_EU,
    present_results
)

start_time = time()

# Test;
card_list   = [Card("5D"), Card("9C"), Card("XS"), Card("JC"), Card("QC"), Card("KS")]

print(f"{time()-start_time:.0f}: start" + "{" + ",".join(convert_cardlist_to_str(card_list, True)) + "}")
time_s1 = time()
results_out = calculate_cribbage_EU(card_list, provide_status=False)
present_results(results_out, 12, True)
print(f"{time()-start_time:.0f}: finished in {time() - time_s1}")