Hi!

This is code to automatically calculate the expected utility of a hand for cribbage as played on Board Game Arena (BGA).

How run?
--------

- Install dependancies

```shell
pip install . 
cribbage [cards]
```

Each 'Card' is 2 characters, a Number and a Suit.

Use:
* 'A' for Ace,
* 'X' for 10,
* 'J' for Jack,
* 'Q' for Queen,
* 'K' for King, and
* Any other number is it's own number.

Use:
* 'C' or ♣ for clubs,
* 'S' or ♠ for spades,
* 'D' or ♦ for diamonds, and
* 'H' or ♥ for hearts.

So `AC` is an Ace of Clubs, but `KD` is a King of Diamonds.

- Run?

```shell
python -m run.run_cribbage_eu
```

How Dev?
--------

I reccomend a venv but I can't tell you what to do

Install the dev requirements.

Proceed to look at src.

There are lint and test commands with:
```shell
pip install -r requirements-dev.txt
mewbot-lint
mewbot-test
```

No guarantee that the existing code passess the lints though.