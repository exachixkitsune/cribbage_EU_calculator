# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 17:41:40 2023
"""

from typing import List

from card import Card, convert_card_array_to_enum_array
from cardenums import CardVal, CardSuit

# pragma pylint: disable=R0903
#  Disable "too few public methods" for test cases - most test files will be classes used for
#  grouping and then individual tests alongside these


class TestCard:
    """
    Test the card class
    Setup tests are validating the elements are set correctly for each suit;
    followed by testing the other setup method.
    Note, the constructor tests the "from string" setup method.
    """

    @staticmethod
    def test_card_setup_init_1() -> None:
        """
        Test card is made correctly
        """
        test_card = Card("AC")
        assert test_card.val == CardVal.VAL_A
        assert test_card.suit == CardSuit.CLUB

    @staticmethod
    def test_card_setup_init_2() -> None:
        """
        Test card is made correctly
        """
        test_card = Card("6S")
        assert test_card.val == CardVal.VAL_6
        assert test_card.suit == CardSuit.SPADE

    @staticmethod
    def test_card_setup_init_3() -> None:
        """
        Test card is made correctly
        """
        test_card = Card("4D")
        assert test_card.val == CardVal.VAL_4
        assert test_card.suit == CardSuit.DIAMOND

    @staticmethod
    def test_card_setup_init_4() -> None:
        """
        Test card is made correctly
        """
        test_card = Card("QH")
        assert test_card.val == CardVal.VAL_Q
        assert test_card.suit == CardSuit.HEART

    @staticmethod
    def test_card_setup_pair_1() -> None:
        """
        Test card is made correctly, using the direct function rather than the constructor
        """
        test_card = Card("QH")
        test_card.set_viapair(CardVal.VAL_J, CardSuit.DIAMOND)
        assert test_card.val == CardVal.VAL_J
        assert test_card.suit == CardSuit.DIAMOND


class TestCardToArray:
    """
    Test converting a single card to an array
    """

    @staticmethod
    def test_card_toarray_set_empty() -> None:
        """
        Empty array testing
        """
        test_card_array: List[Card] = []
        test_card_vals, test_card_suits = convert_card_array_to_enum_array(
            test_card_array
        )

        #  Specifically not simplified here, as the values should be empty sets
        assert test_card_vals == []  # pragma pylint: disable=C1803
        assert test_card_suits == []  # pragma pylint: disable=C1803

    @staticmethod
    def test_card_toarray_set_4() -> None:
        """
        Normal array of 4
        """
        test_card_array = [Card("4D"), Card("6D"), Card("8S"), Card("XH")]
        test_card_vals, test_card_suits = convert_card_array_to_enum_array(
            test_card_array
        )
        assert test_card_vals == [
            CardVal.VAL_4,
            CardVal.VAL_6,
            CardVal.VAL_8,
            CardVal.VAL_X,
        ]
        assert test_card_suits == [
            CardSuit.DIAMOND,
            CardSuit.DIAMOND,
            CardSuit.SPADE,
            CardSuit.HEART,
        ]

    @staticmethod
    def test_card_toarray_set_5() -> None:
        """
        Normal array of 5
        """
        test_card_array = [Card("2C"), Card("5S"), Card("5D"), Card("JH"), Card("KS")]
        test_card_vals, test_card_suits = convert_card_array_to_enum_array(
            test_card_array
        )
        assert test_card_vals == [
            CardVal.VAL_2,
            CardVal.VAL_5,
            CardVal.VAL_5,
            CardVal.VAL_J,
            CardVal.VAL_K,
        ]
        assert test_card_suits == [
            CardSuit.CLUB,
            CardSuit.SPADE,
            CardSuit.DIAMOND,
            CardSuit.HEART,
            CardSuit.SPADE,
        ]
