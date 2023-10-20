# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 14:26:56 2023
"""

from __future__ import annotations
from typing import Any, Tuple, List, Iterable

from cardenums import (
    CardVal,
    str_to_cardval,
    CardSuit,
    str_to_cardsuit,
    cardsuit_to_symbol,
)


class Card:
    """
    A class to contain the "Card" object.
    two items: a value, and a suit.
    Definable via a single string containing both elements (e.g. "AS" for the Ace of Spades).
    """

    val: CardVal
    suit: CardSuit

    def __init__(self, str_card: str = "") -> None:
        """
        Card constructor
        """
        if str_card:
            self.set_viastr(str_card)
        else:
            self.val = []
            self.suit = []

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

    def to_str(self, use_symbol: bool = False) -> str:
        """
        Function to generate the relevant string
        Called by all other stringmaking functions
        """
        first = str(self.val)
        if use_symbol:
            second = cardsuit_to_symbol(self.suit)
        else:
            second = str(self.suit)
        return f"{first}{second}"

    def to_str_emoji(self) -> str:
        """
        Return string of card, but with emoji as the suit
        """
        return self.to_str(True)

    def __str__(self) -> str:
        """
        Default string creation
        No emoji
        """
        return self.to_str(False)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Card):
            return False
        return (self.val == other.val) and (self.suit == other.suit)

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)


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


def convert_cardlist_to_str(
    cardlist_in: List[Card], use_symbol: bool = False
) -> List[str]:
    """
    Function to convert a list of cards into a string
    """
    list_out = []
    for i_card in cardlist_in:
        list_out.append(i_card.to_str(use_symbol))
    return list_out


def all_possible_cards() -> Iterable[Card]:
    """
    Generator listing all possible cards
    Cycle the CardVal and CardSuit enums
    """
    for i_cardval in CardVal:
        for i_cardsuit in CardSuit:
            i_card = Card("AC")
            i_card.set_viapair(i_cardval, i_cardsuit)
            yield i_card


total_possible_cards = len(list(all_possible_cards()))
