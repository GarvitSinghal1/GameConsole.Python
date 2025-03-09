# Python Game Console

A versatile gaming console application featuring a collection of fun mini-games written in Python. Available with both terminal-based and graphical user interfaces!

## Features

- Choose between dark-themed terminal interface or modern GUI
- Easy-to-use game selection menu
- Currently includes 10 mini-games
- Expandable architecture for adding more games

## Screenshots

*Terminal Interface:*
```
╔═══════════════════════════════════════════════════════════════╗
║                     PYTHON GAME CONSOLE                       ║
╚═══════════════════════════════════════════════════════════════╝

Current Mode: TERMINAL

Available Games:

1. Number Guesser
   Try to guess a random number between 1 and 100.

2. Hangman
   Classic word guessing game. Try to guess the word before the hangman is complete.

...

╔═══════════════════════════════════════════════════════════════╗
║ [Q]uit  [R]efresh  [I] Change Interface                       ║
╚═══════════════════════════════════════════════════════════════╝
```

*GUI Interface (varies by game):*
Each game features a modern graphical interface with interactive elements.

## Requirements

- Python 3.6+
- Colorama library for terminal color support
- Pillow (PIL) library for GUI image handling
- Tkinter (included with Python) for GUI interfaces

## Installation

1. Clone the repository
2. Install requirements:
   ```
   pip install -r requirements.txt
   ```
3. Run the console:
   ```
   python console.py
   ```

## Quick Start

The simplest way to start the Python Game Console is to run:

```
python main.py
```

This will prompt you to choose between the terminal or GUI interface. Simply enter your choice and the appropriate interface will launch.

### Launch Options

You can bypass the interface selection prompt by specifying which interface you want:

```
# Ask for interface choice (default)
python main.py

# Force terminal interface without asking
python main.py --mode terminal
# or
python main.py -m terminal

# Force GUI interface without asking
python main.py --mode gui
# or
python main.py -m gui
```

### For Windows Users

Windows users can simply double-click `play_games.bat` to start the game console.

### For Linux/Mac Users

Linux/Mac users can run the shell script to start the game console:

```
chmod +x play_games.sh  # Make it executable (first time only)
./play_games.sh
```

## Games

The console includes the following games, all available in both terminal and GUI modes:
1. Number Guesser - Guess a random number
2. Hangman - Classic word guessing game
3. Rock Paper Scissors - Play against the computer
4. Quiz Game - Test your knowledge
5. Tic Tac Toe - Play against a friend
6. Math Challenge - Solve math problems
7. Word Scramble - Unscramble the words
8. Blackjack - Card game to reach 21
9. Snake - Classic snake game
10. Text Adventure - Short interactive adventure

## Interface Options

When you start the console, you'll be prompted to choose your preferred interface:
- Terminal Mode: Text-based interface with colorful ASCII art and text
- GUI Mode: Graphical windows with visual elements and interactive components

You can switch between interfaces at any time from the main menu by pressing 'I'.

## Adding Games

You can add your own games by:
1. Creating a new Python file in the `games` directory (e.g., `my_game.py` for terminal version)
2. Creating a matching GUI version (e.g., `my_game_gui.py`) if desired
3. Implementing a `main()` function as the entry point for each version
4. Adding the game information to the `games/catalog.json` file

## License

MIT License - Feel free to modify and distribute! 