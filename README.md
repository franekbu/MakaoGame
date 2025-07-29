# Makao Game
The project aims to create a simple macao game to play in the terminal 
and collect data from the game to enable the creation various statistics.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Running the Game](#running-the-game)
- [Project Structure](#project-structure)
- [Makao Game Mechanics](#makao-game-mechanics)
- [Data Logging](#data-logging)
- [Future Improvements](#future-improvements)
- [Contact](#contact)

## Introduction
This project is a console version of the card game Makao, the goal of which was to create a functional gameplay 
and implement the basic principles of object-oriented programming and modular code structure. 
Additionally, the game automatically logs key data from each turn, which allows for analysis of game progress. 
Ideal for quick gameplay without a GUI and for educational/analytical purposes.

## Features
* Macao gameplay in a console environment.
* Multiplayer support (human and bots) - from 2 to 6 players.
* Implementation of basic card functions (2, 3, 4, Jack, Queen, King, Ace).
* Game state management (suit/number requests, freezes, card drawing).
* Automatic logging of data from each turn to CSV files.
* Card deck dynamically replenished from played cards.
* "Macao" and "After Macao" announcement system.
* Scoreboard after the game ends.
* Coloured warnings in terminal.

## Installation
1.  **Cloning repository:**
    ```bash
    git clone git@github.com:franekbu/MakaoGame.git
    cd MakaoGame
    ```

2.  **Requirements:**
    * Python 3.12 (version used)
    * Pandas 2.2.2 (for CSV saving)

3.  **Install Dependencies:**
    ```bash
    pip install pandas
    ```

## Running the Game

```bash
  python main.py
```
After running the game, it can ask some questions about e.g. how many human or bot players

---

## Project Structure
```
.
├── main.py                     # Main file to run a game
└── makao_game/                    # Directory containing class definitions
    ├── __init__.py             # Python package initialization
    ├── game.py                 # Core game logic (mechanics, turns, data management)
    ├── player.py               # Player definition (human and bot)
    ├── cards.py                # Card definition
    ├── dictionaries.py         # Dictionaries with card data, functions and .csv headers
    └── utils.py                # Functions that can be used among many makao_game
└── game_data/                  # Directory for game logs (automatically generated)
    └── [timestamp].csv         # Example CSV files with data from each game turn
```

## Makao Game Mechanics
Makao is a popular card game, in which each player aims to get rid of their cards asap.
* Dealing cards: Each player gets their start deck of cards (5 or 7 depending on how many players play).
* Game: Players take turns in laying down cards matching colour or value to the one on the table. 
* Functional cards:
    * 2,3: Make next player pull 2/3 cards, 
    * 4: freezes next player (skip their turn),
    * Jack: Demands cards with number from 5 to 10,
    * Queen: Block every effect, can be played on any card and any card can be played on it,
    * King:
      * ♥: Next player pull 5 cards,
      * ♠: Previous player pull 5 cards, order of the players is reversed,
      * ♣, ♦: These are non-functional,
    * Ace: Demands specified colour.
* Players are required to announce "Makao" after playing their second-to-last card, 
and "After Makao" after playing their last card. Failure to do so results in drawing 5 penalty cards

## Data Logging

The game automatically saves data from each turn to CSV files. 
These files are stored in the `game_data/` directory and named with the game timestamp (e.g. `YYYY-MM-DD_HH.MM.SS.csv`).

Logged data includes:
* Game_move: The number of moves in the entire game.
* Player_name: The player's name.
* Is_bot: Whether the player is a bot (True/False).
* Player_turn: The turn number for the player.
* Is_finished: Whether the player finished playing this turn.
* Final_place: The place the player occupied (if they finished).
* Is_frozen: Whether the player was frozen this turn.
* Player_deck_size: The number of cards in the player's deck at the start of the turn.
* Played_cards_count: The number of cards played.
* Played_cards_names: The names of the cards played.
* Pulled_cards_count: The number of cards drawn.
* Pulled_cards_names: The names of the cards drawn.
* Top_card_met: The card on the pile before the player's move.
* Is_card_functional: Whether the played card is functional.
* Card_function: Name of the played card's function (e.g. 'add', 'pause').
* Demanded_num: Demanded number (if active).
* Demanded_colour: Demanded colour (if active).

## Future Improvements

* Add GUI.
* Enable the player to play the first drawn card immediately if it's valid.
* Create class for analyzing .csv game data.
* Discord bot


## Contact
If you have any questions or suggestions, please contact: https://github.com/franekbu
