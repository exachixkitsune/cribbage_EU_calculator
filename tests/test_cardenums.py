"""
Test of the cardenums file, and associated functions.
"""

import pytest

from cardenums import (
    CardVal,
    str_to_cardval,
    CardSuit,
    str_to_cardsuit,
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
        Test setting via str_to_cardval works
        """
        assert str_to_cardval("A") == CardVal.VAL_A
        assert str_to_cardval("2") == CardVal.VAL_2
        assert str_to_cardval("3") == CardVal.VAL_3
        assert str_to_cardval("4") == CardVal.VAL_4
        assert str_to_cardval("5") == CardVal.VAL_5
        assert str_to_cardval("6") == CardVal.VAL_6
        assert str_to_cardval("7") == CardVal.VAL_7
        assert str_to_cardval("8") == CardVal.VAL_8
        assert str_to_cardval("9") == CardVal.VAL_9
        assert str_to_cardval("X") == CardVal.VAL_X
        assert str_to_cardval("J") == CardVal.VAL_J
        assert str_to_cardval("Q") == CardVal.VAL_Q
        assert str_to_cardval("K") == CardVal.VAL_K

    @staticmethod
    def test_cardenums_cardsuit_setto_name() -> None:
        """
        Test making the CardSuit from the name
        """
        assert str_to_cardsuit("Club") == CardSuit.CLUB
        assert str_to_cardsuit("Spade") == CardSuit.SPADE
        assert str_to_cardsuit("Diamond") == CardSuit.DIAMOND
        assert str_to_cardsuit("Heart") == CardSuit.HEART

    @staticmethod
    def test_cardenums_cardsuit_setto_short() -> None:
        """
        Test using a single value to make the name
        """
        assert str_to_cardsuit("C") == CardSuit.CLUB
        assert str_to_cardsuit("S") == CardSuit.SPADE
        assert str_to_cardsuit("D") == CardSuit.DIAMOND
        assert str_to_cardsuit("H") == CardSuit.HEART

    @staticmethod
    def test_cardenums_cardsuit_setto_emoji() -> None:
        """
        Test using an Emoji to make the name
        """
        assert str_to_cardsuit("♣") == CardSuit.CLUB
        assert str_to_cardsuit("♠") == CardSuit.SPADE
        assert str_to_cardsuit("♦") == CardSuit.DIAMOND
        assert str_to_cardsuit("♥") == CardSuit.HEART

    @staticmethod
    def test_cardenums_cardsuit_failure() -> None:
        """
        Test using an Emoji to make the name
        """
        with pytest.raises(KeyError):  # @UndefinedVariable
            str_to_cardsuit("jeff")

    @staticmethod
    def test_cardenums_cardsuit_return_emoji() -> None:
        """
        Test correct emoji returns
        """
        assert cardsuit_to_symbol(CardSuit.CLUB) == "♣"
        assert cardsuit_to_symbol(CardSuit.SPADE) == "♠"
        assert cardsuit_to_symbol(CardSuit.DIAMOND) == "♦"
        assert cardsuit_to_symbol(CardSuit.HEART) == "♥"
