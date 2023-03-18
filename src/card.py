# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 14:26:56 2023
"""

from __future__ import annotations
from typing import Tuple, List

from cardenums import CardVal, str_to_cardval, CardSuit, str_to_cardsuit


class Card:
    """
    A class to contain the "Card" object.
    two items: a value, and a suit.
    Definable via a single string containing both elements (e.g. "AS" for the Ace of Spades).
    """

    val: CardVal
    suit: CardSuit

    def __init__(self, str_card: str) -> None:
        """
        Card constructor
        """
        self.set_viastr(str_card)

    def set_viastr(self, str_card: str) -> None:
        """
        Set the value from a string
            - first char is value
            - second char is suit.
            Other characters ignored
        """
        self.val = str_to_cardval(str_card[0])
        self.suit = str_to_cardsuit(str_card[1])

    def set_viapair(self, val: CardVal, suit: CardSuit) -> None:
        """
        Set the value directly
        """
        self.val = val
        self.suit = suit


def convert_card_array_to_enum_array(
    cards: List[Card],
) -> Tuple[List[CardVal], List[CardSuit]]:
    """
    Function to turn an array of cards into it's components parts.
    I.e. a list of values, and a list of suits.
    """
    list_val = []
    list_suit = []
    for i_card in cards:
        list_val.append(i_card.val)
        list_suit.append(i_card.suit)

    return list_val, list_suit
