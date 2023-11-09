# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 20:51:47 2023
"""

from cribbage.card import Card
from cribbage.cardenums import CardVal
from cribbage.scorecalc import (
    calculate_score,
    calculate_score_1_15s,
    calculate_score_2_runs,
    calculate_score_3_pairs,
    calculate_score_4_flush,
    calculate_score_5_nobs,
)

# pragma pylint: disable=R0903
#  Disable "too few public methods" for test cases - most test files will be classes used for
#  grouping and then individual tests alongside these


class TestScoreOverall:
    """
    Overall test of the score calculator
    """

    @staticmethod
    def test_score_noscore() -> None:
        """
        Test successfully counts 0 points
        """
        assert (
            calculate_score(
                {
                    Card.from_str("JH"),
                    Card.from_str("3C"),
                    Card.from_str("KS"),
                    Card.from_str("7D"),
                },
                Card.from_str("9C"),
            )
            == 0
        )

    @staticmethod
    def test_score_1() -> None:
        """
        Test hand: 4 15s, 1 pair, nobs.
        4*2 + 2 + 1 = 11 points
        """
        assert (
            calculate_score(
                {
                    Card.from_str("JS"),
                    Card.from_str("5H"),
                    Card.from_str("XC"),
                    Card.from_str("5S"),
                },
                Card.from_str("4S"),
            )
            == 11
        )

    @staticmethod
    def test_score_2() -> None:
        """
        Test hand: 2 15s, 1 pair, 2 runs of 4
        2*2 + 2 + 2*4 = 14
        """
        assert (
            calculate_score(
                {
                    Card.from_str("5D"),
                    Card.from_str("6S"),
                    Card.from_str("5C"),
                    Card.from_str("7C"),
                },
                Card.from_str("4S"),
            )
            == 14
        )

    @staticmethod
    def test_score_3() -> None:
        """
        Test hand: 1 15
        2
        """
        assert (
            calculate_score(
                {
                    Card.from_str("AH"),
                    Card.from_str("KS"),
                    Card.from_str("2S"),
                    Card.from_str("6H"),
                },
                Card.from_str("4S"),
            )
            == 2
        )


class TestScore1:
    """
    Tests for calculating score 1
    """

    @staticmethod
    def test_score1_noscore() -> None:
        """
        No 15s, no points
        """
        assert (
            calculate_score_1_15s(
                [
                    CardVal.from_str("X"),
                    CardVal.from_str("X"),
                    CardVal.from_str("J"),
                    CardVal.from_str("J"),
                    CardVal.from_str("Q"),
                ]
            )
            == 0
        )

    @staticmethod
    def test_score1_1() -> None:
        """
        one 15
        """
        assert (
            calculate_score_1_15s(
                [
                    CardVal.from_str("6"),
                    CardVal.from_str("7"),
                    CardVal.from_str("8"),
                    CardVal.from_str("X"),
                    CardVal.from_str("Q"),
                ]
            )
            == 2
        )

    @staticmethod
    def test_score1_2() -> None:
        """
        one 15
        """
        assert (
            calculate_score_1_15s(
                [
                    CardVal.from_str("6"),
                    CardVal.from_str("7"),
                    CardVal.from_str("8"),
                    CardVal.from_str("9"),
                    CardVal.from_str("Q"),
                ]
            )
            == 4
        )

    @staticmethod
    def test_score1_3() -> None:
        """
        one 15
        """
        assert (
            calculate_score_1_15s(
                [
                    CardVal.from_str("5"),
                    CardVal.from_str("5"),
                    CardVal.from_str("5"),
                    CardVal.from_str("X"),
                    CardVal.from_str("X"),
                ]
            )
            == 14
        )

    @staticmethod
    def test_score1_4() -> None:
        """
        one 15
        """
        assert (
            calculate_score_1_15s(
                [
                    CardVal.from_str("5"),
                    CardVal.from_str("Q"),
                    CardVal.from_str("K"),
                    CardVal.from_str("X"),
                    CardVal.from_str("X"),
                ]
            )
            == 8
        )


class TestScore2:
    """
    Test for calculating score 2
    """

    @staticmethod
    def test_score2_simple() -> None:
        """
        No runs, no points
        """
        assert (
            calculate_score_2_runs(
                [
                    CardVal.from_str("2"),
                    CardVal.from_str("4"),
                    CardVal.from_str("6"),
                    CardVal.from_str("8"),
                    CardVal.from_str("X"),
                ]
            )
            == 0
        )

    @staticmethod
    def test_score2_1run_5() -> None:
        """
        One big run
        """
        assert (
            calculate_score_2_runs(
                [
                    CardVal.from_str("2"),
                    CardVal.from_str("3"),
                    CardVal.from_str("4"),
                    CardVal.from_str("5"),
                    CardVal.from_str("6"),
                ]
            )
            == 5
        )

    @staticmethod
    def test_score2_1run_3() -> None:
        """
        one runs of 3
        """
        assert (
            calculate_score_2_runs(
                [
                    CardVal.from_str("A"),
                    CardVal.from_str("2"),
                    CardVal.from_str("3"),
                    CardVal.from_str("6"),
                    CardVal.from_str("7"),
                ]
            )
            == 3
        )

    @staticmethod
    def test_score2_1run_3_unordered() -> None:
        """
        one runs of 3
        """
        assert (
            calculate_score_2_runs(
                [
                    CardVal.from_str("X"),
                    CardVal.from_str("Q"),
                    CardVal.from_str("3"),
                    CardVal.from_str("J"),
                    CardVal.from_str("7"),
                ]
            )
            == 3
        )

    @staticmethod
    def test_score2_pair() -> None:
        """
        two runs of 3, with a pair
        """
        assert (
            calculate_score_2_runs(
                [
                    CardVal.from_str("2"),
                    CardVal.from_str("3"),
                    CardVal.from_str("3"),
                    CardVal.from_str("4"),
                    CardVal.from_str("6"),
                ]
            )
            == 6
        )

    @staticmethod
    def test_score2_pair_unordered() -> None:
        """
        Two runs of 3, with a pair, out of order
        """
        assert (
            calculate_score_2_runs(
                [
                    CardVal.from_str("6"),
                    CardVal.from_str("2"),
                    CardVal.from_str("3"),
                    CardVal.from_str("3"),
                    CardVal.from_str("4"),
                ]
            )
            == 6
        )

    @staticmethod
    def test_score2_1run_4() -> None:
        """
        Run of 4, check no 3-dupling
        """
        assert (
            calculate_score_2_runs(
                [
                    CardVal.from_str("2"),
                    CardVal.from_str("3"),
                    CardVal.from_str("4"),
                    CardVal.from_str("5"),
                    CardVal.from_str("8"),
                ]
            )
            == 4
        )

    @staticmethod
    def test_score2_1run_4_unordered() -> None:
        """
        Run of 4, check no 3-dupling, out of order
        """
        assert (
            calculate_score_2_runs(
                [
                    CardVal.from_str("5"),
                    CardVal.from_str("2"),
                    CardVal.from_str("8"),
                    CardVal.from_str("3"),
                    CardVal.from_str("4"),
                ]
            )
            == 4
        )

    @staticmethod
    def test_score2_pair_4() -> None:
        """
        Run of 4, check no 3-dupling, out of order
        also a pair
        """
        assert (
            calculate_score_2_runs(
                [
                    CardVal.from_str("5"),
                    CardVal.from_str("2"),
                    CardVal.from_str("4"),
                    CardVal.from_str("3"),
                    CardVal.from_str("4"),
                ]
            )
            == 8
        )

    @staticmethod
    def test_score2_run3_2pair() -> None:
        """
        2 pairs:
            135,145,235,245 = 4x3 = 12
        """
        assert (
            calculate_score_2_runs(
                [
                    CardVal.from_str("X"),
                    CardVal.from_str("X"),
                    CardVal.from_str("J"),
                    CardVal.from_str("J"),
                    CardVal.from_str("Q"),
                ]
            )
            == 12
        )

    @staticmethod
    def test_score2_run3_trip() -> None:
        """
        trips:
            125,135,145 = 3x3 = 9
        """
        assert (
            calculate_score_2_runs(
                [
                    CardVal.from_str("9"),
                    CardVal.from_str("X"),
                    CardVal.from_str("X"),
                    CardVal.from_str("X"),
                    CardVal.from_str("J"),
                ]
            )
            == 9
        )


class TestScore3:
    """
    Test for the pairs checker
    """

    @staticmethod
    def test_score3_zero1() -> None:
        """
        No pairs - 0 points
        """
        assert (
            calculate_score_3_pairs(
                [
                    CardVal.from_str("2"),
                    CardVal.from_str("4"),
                    CardVal.from_str("6"),
                    CardVal.from_str("8"),
                    CardVal.from_str("X"),
                ]
            )
            == 0
        )

    @staticmethod
    def test_score3_zero2() -> None:
        """
        No pairs - 0 points
        """
        assert (
            calculate_score_3_pairs(
                [
                    CardVal.from_str("2"),
                    CardVal.from_str("9"),
                    CardVal.from_str("6"),
                    CardVal.from_str("8"),
                    CardVal.from_str("X"),
                ]
            )
            == 0
        )

    @staticmethod
    def test_score3_zero3() -> None:
        """
        No pairs - 0 points
        """
        assert (
            calculate_score_3_pairs(
                [
                    CardVal.from_str("2"),
                    CardVal.from_str("9"),
                    CardVal.from_str("6"),
                    CardVal.from_str("J"),
                    CardVal.from_str("X"),
                ]
            )
            == 0
        )

    @staticmethod
    def test_score3_1pair_1() -> None:
        """
        One pair - 2 points
        """
        assert (
            calculate_score_3_pairs(
                [
                    CardVal.from_str("2"),
                    CardVal.from_str("9"),
                    CardVal.from_str("6"),
                    CardVal.from_str("9"),
                    CardVal.from_str("X"),
                ]
            )
            == 2
        )

    @staticmethod
    def test_score3_1pair_2() -> None:
        """
        One pair - 2 points
        """
        assert (
            calculate_score_3_pairs(
                [
                    CardVal.from_str("J"),
                    CardVal.from_str("Q"),
                    CardVal.from_str("9"),
                    CardVal.from_str("J"),
                    CardVal.from_str("K"),
                ]
            )
            == 2
        )

    @staticmethod
    def test_score3_2pair_1() -> None:
        """
        Two pairs - 4 points
        """
        assert (
            calculate_score_3_pairs(
                [
                    CardVal.from_str("2"),
                    CardVal.from_str("9"),
                    CardVal.from_str("X"),
                    CardVal.from_str("9"),
                    CardVal.from_str("X"),
                ]
            )
            == 4
        )

    @staticmethod
    def test_score3_2pair_2() -> None:
        """
        Two pairs - 4 points
        """
        assert (
            calculate_score_3_pairs(
                [
                    CardVal.from_str("J"),
                    CardVal.from_str("Q"),
                    CardVal.from_str("9"),
                    CardVal.from_str("J"),
                    CardVal.from_str("Q"),
                ]
            )
            == 4
        )

    @staticmethod
    def test_score3_3pair_1() -> None:
        """
        Three pairs - 6 points
        """
        assert (
            calculate_score_3_pairs(
                [
                    CardVal.from_str("2"),
                    CardVal.from_str("9"),
                    CardVal.from_str("9"),
                    CardVal.from_str("9"),
                    CardVal.from_str("X"),
                ]
            )
            == 6
        )

    @staticmethod
    def test_score3_3pair_2() -> None:
        """
        Three pairs - 6 points
        """
        assert (
            calculate_score_3_pairs(
                [
                    CardVal.from_str("J"),
                    CardVal.from_str("9"),
                    CardVal.from_str("2"),
                    CardVal.from_str("J"),
                    CardVal.from_str("J"),
                ]
            )
            == 6
        )

    @staticmethod
    def test_score3_manypair() -> None:
        """
        Four pairs - 8 points
        """
        assert (
            calculate_score_3_pairs(
                [
                    CardVal.from_str("2"),
                    CardVal.from_str("9"),
                    CardVal.from_str("9"),
                    CardVal.from_str("9"),
                    CardVal.from_str("2"),
                ]
            )
            == 8
        )

    @staticmethod
    def test_score3_manypair_2() -> None:
        """
        Six pairs - 12 points
        """
        assert (
            calculate_score_3_pairs(
                [
                    CardVal.from_str("2"),
                    CardVal.from_str("9"),
                    CardVal.from_str("9"),
                    CardVal.from_str("9"),
                    CardVal.from_str("9"),
                ]
            )
            == 12
        )


class TestScore4:
    """
    Test for the flush checker
    """

    @staticmethod
    def test_score4_fail1() -> None:
        """
        No flush
        """
        assert (
            calculate_score_4_flush(
                {
                    Card.from_str("AH"),
                    Card.from_str("3C"),
                    Card.from_str("5S"),
                    Card.from_str("7D"),
                },
                Card.from_str("9C"),
            )
            == 0
        )

    @staticmethod
    def test_score4_fail2() -> None:
        """
        No Flush - specifically, card 1 is also the same suit as the starter.
        """
        assert (
            calculate_score_4_flush(
                {
                    Card.from_str("5H"),
                    Card.from_str("8D"),
                    Card.from_str("9D"),
                    Card.from_str("XD"),
                },
                Card.from_str("2H"),
            )
            == 0
        )

    @staticmethod
    def test_score4_flush1() -> None:
        """
        Yes Flush, but only in hand
        """
        assert (
            calculate_score_4_flush(
                {
                    Card.from_str("AH"),
                    Card.from_str("3H"),
                    Card.from_str("5H"),
                    Card.from_str("7H"),
                },
                Card.from_str("9C"),
            )
            == 4
        )

    @staticmethod
    def test_score4_fullflush() -> None:
        """
        Yes Flush, full flush
        """
        assert (
            calculate_score_4_flush(
                {
                    Card.from_str("AH"),
                    Card.from_str("3H"),
                    Card.from_str("5H"),
                    Card.from_str("7H"),
                },
                Card.from_str("9H"),
            )
            == 5
        )

    @staticmethod
    def test_score4_flush2() -> None:
        """
        Yes Flush, but only in hand
        """
        assert (
            calculate_score_4_flush(
                {
                    Card.from_str("5D"),
                    Card.from_str("8D"),
                    Card.from_str("9D"),
                    Card.from_str("XD"),
                },
                Card.from_str("2H"),
            )
            == 4
        )


class TestScore5:
    """
    Test for the nobs scoring
    """

    @staticmethod
    def test_score5_fail1() -> None:
        """
        No jack - no points
        """
        assert (
            calculate_score_5_nobs(
                {
                    Card.from_str("AH"),
                    Card.from_str("3C"),
                    Card.from_str("5S"),
                    Card.from_str("7D"),
                },
                Card.from_str("9C"),
            )
            == 0
        )

    @staticmethod
    def test_score5_fail2() -> None:
        """
        Yes jack, but no match - no points
        """
        assert (
            calculate_score_5_nobs(
                {
                    Card.from_str("JH"),
                    Card.from_str("3C"),
                    Card.from_str("JS"),
                    Card.from_str("7D"),
                },
                Card.from_str("9C"),
            )
            == 0
        )

    @staticmethod
    def test_score5_fail3() -> None:
        """
        Yes Jack, no match - no points
        """
        assert (
            calculate_score_5_nobs(
                {
                    Card.from_str("JH"),
                    Card.from_str("5C"),
                    Card.from_str("JC"),
                    Card.from_str("JD"),
                },
                Card.from_str("3S"),
            )
            == 0
        )

    @staticmethod
    def test_score5_success1() -> None:
        """
        Yes Jack, yes match - points
        """
        assert (
            calculate_score_5_nobs(
                {
                    Card.from_str("JH"),
                    Card.from_str("3C"),
                    Card.from_str("JS"),
                    Card.from_str("JD"),
                },
                Card.from_str("3D"),
            )
            == 1
        )

    @staticmethod
    def test_score5_success2() -> None:
        """
        Yes Jack, yes match - points
        """
        assert (
            calculate_score_5_nobs(
                {
                    Card.from_str("JH"),
                    Card.from_str("3C"),
                    Card.from_str("JS"),
                    Card.from_str("JD"),
                },
                Card.from_str("3H"),
            )
            == 1
        )
