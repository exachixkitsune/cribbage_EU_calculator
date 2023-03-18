# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 16:11:32 2023
"""

from __future__ import annotations

from enum import Enum, IntEnum

# from cardenums import cardval, str_to_cardval, cardsuit, str_to_cardsuit, cardsuit_to_symbol


class CardVal(IntEnum):
    """
    Enumeration of the different card types and their associated values
    """

    VAL_A = 1
    VAL_2 = 2
    VAL_3 = 3
    VAL_4 = 4
    VAL_5 = 5
    VAL_6 = 6
    VAL_7 = 7
    VAL_8 = 8
    VAL_9 = 9
    VAL_X = 10
    VAL_J = 11
    VAL_Q = 12
    VAL_K = 13

    def __str__(self) -> str:
        print("__STR__")
        return self.name[-1:]


def str_to_cardval(in_name: str) -> CardVal:
    """
    Turns a string value into the cardval enum.
    Essentially, the last character in the enumeration.
    This exists because numbers cannot be the enum name.
    I.e. CardVal.2 couldn't exist
    """
    test_name = f"VAL_{in_name}"
    return CardVal[test_name]


class CardSuit(str, Enum):
    """
    Enumeration of the different card suits
    """

    CLUB = "Club"
    SPADE = "Spade"
    DIAMOND = "Diamond"
    HEART = "Heart"


suits_symbols = {
    CardSuit.CLUB: "♣",
    CardSuit.SPADE: "♠",
    CardSuit.DIAMOND: "♦",
    CardSuit.HEART: "♥",
}


def str_to_cardsuit(in_name: str) -> CardSuit:
    """
    Converts a string to the appropriate CardSuit
    3 ways:
        1. using the first character of the suit (E.g. C for Clubs)
        2. using the emoji (♣, ♠, ♦, ♥)
        3. using the normal method from the CardSuit Enum
    """

    # First character Matches:
    for i_suit in list(CardSuit):
        if i_suit.name[0] == in_name[0]:
            return i_suit

    # Emoji Matches:
    # Failed; try different way
    if in_name in suits_symbols.values():
        for (
            i_suits_symbol
        ) in suits_symbols.keys():  # pragma pylint: disable=C0201,C0206
            # Pylint wants me to iterate the dictionary directly or using .items() instead of
            # calling keys; but I will want to return the key, so I'm doing it this way
            if suits_symbols[i_suits_symbol] == in_name:
                return i_suits_symbol

    # Try just using the normal method
    return CardSuit[in_name]


def cardsuit_to_symbol(in_suit: CardSuit) -> str:
    """
    Return the appropriate emoji symbol for the suit.
    """
    return suits_symbols[in_suit]
