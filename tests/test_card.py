# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 17:41:40 2023
"""

from cribbage.card import (
    Card,
    all_possible_cards,
    convert_card_array_to_enum_array,
    convert_cardlist_to_str,
)
from cribbage.cardenums import CardSuit, CardVal

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
        test_card = Card.from_str("AC")
        assert test_card.val == CardVal.VAL_A
        assert test_card.suit == CardSuit.CLUB
        # Fully test resolution.
        assert str(test_card) == "AC"
        assert test_card.to_str() == "AC"
        assert test_card.to_str(False) == "AC"
        assert test_card.to_str(True) == "A♣"
        assert test_card.to_str_emoji() == "A♣"

    @staticmethod
    def test_card_setup_init_2() -> None:
        """
        Test card is made correctly
        """
        test_card = Card.from_str("6S")
        assert test_card.val == CardVal.VAL_6
        assert test_card.suit == CardSuit.SPADE
        assert str(test_card) == "6S"
        assert test_card.to_str_emoji() == "6♠"

    @staticmethod
    def test_card_setup_init_3() -> None:
        """
        Test card is made correctly
        """
        test_card = Card.from_str("4D")
        assert test_card.val == CardVal.VAL_4
        assert test_card.suit == CardSuit.DIAMOND
        assert str(test_card) == "4D"
        assert test_card.to_str_emoji() == "4♦"

    @staticmethod
    def test_card_setup_init_4() -> None:
        """
        Test card is made correctly
        """
        test_card = Card.from_str("QH")
        assert test_card.val == CardVal.VAL_Q
        assert test_card.suit == CardSuit.HEART
        assert str(test_card) == "QH"
        assert test_card.to_str_emoji() == "Q♥"

    @staticmethod
    def test_card_setup_pair_1() -> None:
        """
        Test card is made correctly, using the direct function rather than the constructor
        """
        test_card = Card(CardVal.VAL_J, CardSuit.DIAMOND)
        assert test_card.val == CardVal.VAL_J
        assert test_card.suit == CardSuit.DIAMOND
        assert str(test_card) == "JD"
        assert test_card.to_str_emoji() == "J♦"

    @staticmethod
    def test_card_eq_check_1() -> None:
        """
        Test equivilency works
        Test that type mismatch is fine
        """
        test_card_1 = Card.from_str("QH")
        assert (test_card_1 == 5) is False

    @staticmethod
    def test_card_eq_check_2() -> None:
        """
        Test equivilency works
        Actual equivilency
        """
        test_card_1 = Card.from_str("QH")
        test_card_2 = Card.from_str("QH")
        assert (test_card_1 == test_card_2) is True
        assert (test_card_1 != test_card_2) is False

    @staticmethod
    def test_card_eq_check_3() -> None:
        """
        Test equivilency works
        Actual equivilency
        """
        test_card_1 = Card.from_str("QH")
        test_card_2 = Card.from_str("KH")
        assert (test_card_1 == test_card_2) is False
        assert (test_card_1 != test_card_2) is True

    @staticmethod
    def test_card_eq_check_4() -> None:
        """
        Test equivilency works
        Actual equivilency
        """
        test_card_1 = Card.from_str("QH")
        test_card_2 = Card.from_str("QS")
        assert (test_card_1 == test_card_2) is False
        assert (test_card_1 != test_card_2) is True


class TestCardToArray:
    """
    Test converting a single card to an array
    """

    @staticmethod
    def test_card_toarray_set_empty() -> None:
        """
        Empty array testing
        """
        test_card_array: set[Card] = set()
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
        test_card_array = {
            Card.from_str("4D"),
            Card.from_str("6D"),
            Card.from_str("8S"),
            Card.from_str("XH"),
        }
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
            CardSuit.HEART,
            CardSuit.SPADE,
        ]

    @staticmethod
    def test_card_toarray_set_5() -> None:
        """
        Normal array of 5
        """
        test_card_array = {
            Card.from_str("2C"),
            Card.from_str("5D"),
            Card.from_str("5S"),
            Card.from_str("JH"),
            Card.from_str("KS"),
        }
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
            CardSuit.DIAMOND,
            CardSuit.HEART,
            CardSuit.SPADE,
            CardSuit.SPADE,
        ]


class TestCardListToString:
    """
    testing for the convert_cardlist_to_str function
    """

    @staticmethod
    def test_cardlist_to_str_empty() -> None:
        """
        Test that empty in gives empty out
        """
        assert convert_cardlist_to_str(set()) == ""  # pragma pylint: disable=C1803

    @staticmethod
    def test_cardlist_to_str_test1() -> None:
        """
        basic test - 1 item
        """
        assert convert_cardlist_to_str({Card.from_str("2C")}) == "2C"

    @staticmethod
    def test_cardlist_to_str_test5() -> None:
        """
        basic test - many items
        """
        assert (
            convert_cardlist_to_str(
                {
                    Card.from_str("2C"),
                    Card.from_str("5S"),
                    Card.from_str("5D"),
                    Card.from_str("JH"),
                }
            )
            == "2C, 5D, 5S, JH"
        )

    @staticmethod
    def test_cardlist_to_str_test5_symbols() -> None:
        """
        basic test - many items
        """
        cards = {
            Card.from_str("2C"),
            Card.from_str("5S"),
            Card.from_str("JH"),
            Card.from_str("5D"),
        }
        print(sorted(cards))

        assert convert_cardlist_to_str(cards, True) == "2♣, 5♦, 5♠, J♥"


class TestAllPossibleCards:
    """
    Testing for the all_possible_cards function
    Test it makes each card sequentially.
    """

    @staticmethod
    def test_all_possible_cards_generator() -> None:
        """
        Testing for the all_possible_cards function
        Test it makes each card sequentially.
        """
        eachcard = [
            "AC",
            "AS",
            "AD",
            "AH",
            "2C",
            "2S",
            "2D",
            "2H",
            "3C",
            "3S",
            "3D",
            "3H",
            "4C",
            "4S",
            "4D",
            "4H",
            "5C",
            "5S",
            "5D",
            "5H",
            "6C",
            "6S",
            "6D",
            "6H",
            "7C",
            "7S",
            "7D",
            "7H",
            "8C",
            "8S",
            "8D",
            "8H",
            "9C",
            "9S",
            "9D",
            "9H",
            "XC",
            "XS",
            "XD",
            "XH",
            "JC",
            "JS",
            "JD",
            "JH",
            "QC",
            "QS",
            "QD",
            "QH",
            "KC",
            "KS",
            "KD",
            "KH",
        ]
        i_counter = -1
        for i_card in all_possible_cards():
            i_counter += 1
            assert str(i_card) == eachcard[i_counter]
