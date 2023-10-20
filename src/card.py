# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 14:26:56 2023
"""

from __future__ import annotations

from typing import Any, Iterable

from cardenums import (
    CardVal,
    CardSuit,
    cardsuit_to_symbol,
)


class Card:
    """
    A class to contain the "Card" object.
    two items: a value, and a suit.
    Definable via a single string containing both elements (e.g. "AS" for the Ace of Spades).
    """

    @classmethod
    def from_str(cls, str_card: str) -> Card:
        """
        Set the value from a string
            - first char is value
            - second char is suit.
            Other characters ignored
        """

        return cls(CardVal.from_str(str_card[0]), CardSuit.from_str(str_card[1]))

    val: CardVal
    suit: CardSuit

    def __init__(self, val: CardVal, suit: CardSuit) -> None:
        """
        Card constructor
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

    def __repr__(self) -> str:
        """
        Default string creation
        No emoji
        """
        return "card.Card<" + self.to_str(False) + ">"

    def __hash__(self) -> int:
        return hash(self.__str__())

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Card):
            return False
        return (self.val == other.val) and (self.suit == other.suit)

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Card):
            raise TypeError(
                f"'<' not supported between instance of 'Card' and '{type(other)}'"
            )

        if self.val == other.val:
            return self.suit < other.suit

        return self.val < other.val

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)


def convert_card_array_to_enum_array(
    cards: set[Card],
) -> tuple[list[CardVal], list[CardSuit]]:
    """
    Function to turn an array of cards into it's components parts.
    I.e. a list of values, and a list of suits.
    """
    list_val = []
    list_suit = []
    for i_card in cards:
        list_val.append(i_card.val)
        list_suit.append(i_card.suit)

    return sorted(list_val), sorted(list_suit)


def convert_cardlist_to_str(cardlist_in: set[Card], emoji: bool = False) -> str:
    """
    Function to convert a list of cards into a string
    """
    return ", ".join(x.to_str(emoji) for x in sorted(cardlist_in))


def all_possible_cards() -> Iterable[Card]:
    """
    Generator listing all possible cards
    Cycle the CardVal and CardSuit enums
    """
    for i_cardval in CardVal:
        for i_cardsuit in CardSuit:
            yield Card(i_cardval, i_cardsuit)
