"""
Test of the cardenums file, and associated functions.
"""

import pytest

from cardenums import (
    CardVal,
    CardSuit,
    cardsuit_to_symbol,
)

# pragma pylint: disable=R0903
#  Disable "too few public methods" for test cases - most test files will be classes used for
#  grouping and then individual tests alongside these


class TestCardenums:
    """
    Test of the cardenums file, and associated functions.
    """

    @staticmethod
    def test_cardenums_cardval_sets() -> None:
        """
        Test each of the values are expected
        """
        assert CardVal.VAL_A == 1
        assert CardVal.VAL_2 == 2
        assert CardVal.VAL_3 == 3
        assert CardVal.VAL_4 == 4
        assert CardVal.VAL_5 == 5
        assert CardVal.VAL_6 == 6
        assert CardVal.VAL_7 == 7
        assert CardVal.VAL_8 == 8
        assert CardVal.VAL_9 == 9
        assert CardVal.VAL_X == 10
        assert CardVal.VAL_J == 11
        assert CardVal.VAL_Q == 12
        assert CardVal.VAL_K == 13

    @staticmethod
    def test_cardenums_cardval_strings() -> None:
        """
        Test each of the string outputs are valid
        """
        assert str(CardVal.VAL_A) == "A"
        assert str(CardVal.VAL_2) == "2"
        assert str(CardVal.VAL_3) == "3"
        assert str(CardVal.VAL_4) == "4"
        assert str(CardVal.VAL_5) == "5"
        assert str(CardVal.VAL_6) == "6"
        assert str(CardVal.VAL_7) == "7"
        assert str(CardVal.VAL_8) == "8"
        assert str(CardVal.VAL_9) == "9"
        assert str(CardVal.VAL_X) == "X"
        assert str(CardVal.VAL_J) == "J"
        assert str(CardVal.VAL_Q) == "Q"
        assert str(CardVal.VAL_K) == "K"

    @staticmethod
    def test_cardenums_cardval_setfromstring() -> None:
        """
        Test setting via CardVal.from_str works
        """
        assert CardVal.from_str("A") == CardVal.VAL_A
        assert CardVal.from_str("2") == CardVal.VAL_2
        assert CardVal.from_str("3") == CardVal.VAL_3
        assert CardVal.from_str("4") == CardVal.VAL_4
        assert CardVal.from_str("5") == CardVal.VAL_5
        assert CardVal.from_str("6") == CardVal.VAL_6
        assert CardVal.from_str("7") == CardVal.VAL_7
        assert CardVal.from_str("8") == CardVal.VAL_8
        assert CardVal.from_str("9") == CardVal.VAL_9
        assert CardVal.from_str("X") == CardVal.VAL_X
        assert CardVal.from_str("J") == CardVal.VAL_J
        assert CardVal.from_str("Q") == CardVal.VAL_Q
        assert CardVal.from_str("K") == CardVal.VAL_K

    @staticmethod
    def test_cardenums_cardsuit_setto_name() -> None:
        """
        Test making the CardSuit from the name
        """
        assert CardSuit.from_str("Club") == CardSuit.CLUB
        assert CardSuit.from_str("Spade") == CardSuit.SPADE
        assert CardSuit.from_str("Diamond") == CardSuit.DIAMOND
        assert CardSuit.from_str("Heart") == CardSuit.HEART

    @staticmethod
    def test_cardenums_cardsuit_setto_short() -> None:
        """
        Test using a single value to make the name
        """
        assert CardSuit.from_str("C") == CardSuit.CLUB
        assert CardSuit.from_str("S") == CardSuit.SPADE
        assert CardSuit.from_str("D") == CardSuit.DIAMOND
        assert CardSuit.from_str("H") == CardSuit.HEART

    @staticmethod
    def test_cardenums_cardsuit_setto_emoji() -> None:
        """
        Test using an Emoji to make the name
        """
        assert CardSuit.from_str("♣") == CardSuit.CLUB
        assert CardSuit.from_str("♠") == CardSuit.SPADE
        assert CardSuit.from_str("♦") == CardSuit.DIAMOND
        assert CardSuit.from_str("♥") == CardSuit.HEART

    @staticmethod
    def test_cardenums_cardsuit_failure() -> None:
        """
        Test using an Emoji to make the name
        """
        with pytest.raises(KeyError):  # @UndefinedVariable
            CardSuit.from_str("jeff")

    @staticmethod
    def test_cardenums_cardsuit_return_emoji() -> None:
        """
        Test correct emoji returns
        """
        assert cardsuit_to_symbol(CardSuit.CLUB) == "♣"
        assert cardsuit_to_symbol(CardSuit.SPADE) == "♠"
        assert cardsuit_to_symbol(CardSuit.DIAMOND) == "♦"
        assert cardsuit_to_symbol(CardSuit.HEART) == "♥"
