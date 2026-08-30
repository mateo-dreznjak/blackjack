# Blackjack

A console-based Blackjack game written in Python.

## Features

- One player per game
- Hit and stand
- Blackjack pays 3:2
- Bust and push
- Normal wins pay 1:1
- Six-deck shoe with automatic reshuffling
- The game ends when the player cannot place the minimum bet
- The player acts before the dealer
- Insurance
- Two different side bets
- Double and surrender
- Split and up to two resplits for a maximum of four hands
- Dealer hits on soft 17

### Side bets

Side bets are evaluated using the player's first two cards and the dealer's visible card.

- The poker side bet wins with a flush, straight, three of a kind, or straight flush
- The special side bet wins with combinations such as three 7s, 6-7-8, or totals of 19, 20, and 21

## Requirements

- Tested with Python 3.14.4
- No third-party packages required

## Running the game

1. Install Python.
2. Clone or download the repository.
3. Open a terminal in the project folder.
4. Run the game:

```powershell
python main.py
```

## Game flow

When the program starts, the player enters a name and starting balance. The name must contain only letters and be between 4 and 12 characters long. The starting balance must be a multiple of 25 between 500 and 10,000.

The main loop asks whether the player wants to play a round. Entering `y` starts a round, while `n` ends the program. The game also ends when the player's bankroll falls below 25 euros.

At the start of each round, the player places a main bet and can choose to place one or two side bets. The player and dealer then receive their cards, and the player chooses from the available actions. If the player surrenders, half of the main bet is returned and the round ends.

After the player finishes, the dealer plays their hand if at least one player hand still needs to be resolved. The game evaluates every hand and handles wins, losses, pushes, and payouts before returning to the main loop.

## Project structure

- `main.py`: Entry point that creates the game, runs the setup, and starts the game handler
- `blackjack_game.py`: Contains the game loop, coordinates the other modules, and handles most output
- `bankroll.py`: Stores the player's balance and handles deposits, withdrawals, and balance checks
- `card.py`: Stores the suit, rank, and value of a card
- `dealer.py`: Stores the dealer and their hand
- `deck.py`: Creates the six-deck shoe, draws cards, and handles reshuffling
- `hand.py`: Stores a hand, adds cards, calculates its total, and tracks aces and busts
- `outcome_eval.py`: Evaluates normal hands, blackjack, side bets, and insurance
- `payout.py`: Applies payouts for wins, pushes, surrender, blackjack, side bets, and insurance
- `player.py`: Stores the player's hands, bankroll, side bets, and insurance state
- `player_actions.py`: Handles player actions, bets, side bets, and insurance
- `player_options.py`: Determines which actions are available for the current hand
- `side_bet.py`: Stores the type, amount, result, and multiplier of a side bet
- `test_input_feed.py`: Supplies repeated input for longer test runs

## Testing

I initially tested the game manually by playing through different situations and fixing errors as I found them.

I later added `test_input_feed.py` to supply repeated input for longer runs. It helps reproduce bugs more efficiently, but the program output is still checked manually.

## Current status

The core game is finished. I may still adjust some output and delays.

## What I learned

This was my first full Python project after building smaller calculators and mini-games. My main focus was object-oriented programming. I learned how classes and objects work, how to structure a project, and how to decide which class should hold each responsibility.

Before writing the code, I planned which classes and methods I needed and where they belonged. I also improved my understanding of probability by designing a weighted card and deck system.
