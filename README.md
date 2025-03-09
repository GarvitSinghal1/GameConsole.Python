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

## Adding Your Own Games

The Python Game Console is designed to be easily extensible. You can add your own games by following these steps:

### 1. Create Game Files

You'll need to create at least one file for your game, and optionally a second file for a GUI version:

#### Terminal Version (Required)
Create a file in the `games` directory with a name describing your game (e.g., `my_game.py`).

Your game file must include:
- A `main()` function that serves as the entry point
- Appropriate terminal UI elements (using colorama for colors)
- Clean exit behavior that returns to the console when complete

#### GUI Version (Optional)
Create a file in the `games` directory with "_gui" appended to the name (e.g., `my_game_gui.py`).

Your GUI game file must include:
- A `main()` function that serves as the entry point
- Tkinter-based user interface
- Proper window management (closing windows should return to the console)

### 2. Update the Catalog

Add your game to the catalog file at `games/catalog.json`:

```json
{
    "name": "My Game",
    "description": "A brief description of what your game does.",
    "module": "my_game",
    "difficulty": "Medium",
    "players": 1
}
```

Fields:
- `name`: Display name of your game
- `description`: Brief description shown in the menu
- `module`: The filename without the `.py` extension
- `difficulty`: One of "Easy", "Medium", "Hard"
- `players`: Number of players (typically 1 or 2)

### 3. Example: Minimal Terminal Game

Here's a minimal example of a terminal game:

```python
#!/usr/bin/env python3
import os
import time
import colorama
from colorama import Fore, Back, Style

# Initialize colorama
colorama.init()

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the game header."""
    print(f"{Back.RED}{Fore.WHITE}╔═══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Back.RED}{Fore.WHITE}║                       MY GAME                                 ║{Style.RESET_ALL}")
    print(f"{Back.RED}{Fore.WHITE}╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()

def main():
    """Main game function."""
    clear_screen()
    print_header()
    
    print(f"{Fore.CYAN}Welcome to My Game!{Style.RESET_ALL}")
    print(f"{Fore.WHITE}This is a simple example game.{Style.RESET_ALL}")
    print()
    
    # Game loop
    playing = True
    while playing:
        choice = input(f"{Fore.GREEN}Enter a command (q to quit): {Style.RESET_ALL}")
        
        if choice.lower() == 'q':
            playing = False
        else:
            print(f"{Fore.YELLOW}You entered: {choice}{Style.RESET_ALL}")
    
    print(f"{Fore.CYAN}Thanks for playing!{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
```

### 4. Example: Minimal GUI Game

Here's a minimal example of a GUI game:

```python
#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox

class MyGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("My Game")
        self.root.geometry("500x400")
        self.root.configure(bg="#333333")
        
        # Create UI elements
        self.create_widgets()
    
    def create_widgets(self):
        """Create the GUI widgets."""
        # Main frame
        main_frame = tk.Frame(self.root, bg="#333333")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title label
        title_label = tk.Label(
            main_frame, 
            text="My Game", 
            font=("Helvetica", 24, "bold"),
            bg="#333333",
            fg="#66CCFF"  # Blue
        )
        title_label.pack(pady=10)
        
        # Game instructions
        instructions = tk.Label(
            main_frame,
            text="This is a simple example game.",
            font=("Helvetica", 12),
            bg="#333333",
            fg="#FFFFFF"
        )
        instructions.pack(pady=20)
        
        # Action button
        action_button = tk.Button(
            main_frame,
            text="Do Something",
            command=self.do_action,
            bg="#66CCFF",  # Blue
            fg="#000000",
            font=("Helvetica", 14, "bold"),
            width=15
        )
        action_button.pack(pady=20)
        
        # Quit button
        quit_button = tk.Button(
            main_frame,
            text="Quit",
            command=self.quit_game,
            bg="#FF6666",  # Red
            fg="#FFFFFF",
            font=("Helvetica", 12),
            width=10
        )
        quit_button.pack(pady=20)
    
    def do_action(self):
        """Perform some action in the game."""
        messagebox.showinfo("Action", "You did something!")
    
    def quit_game(self):
        """Quit the game."""
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            self.root.destroy()

def main():
    """Main function to start the GUI game."""
    root = tk.Tk()
    app = MyGameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

### 5. Best Practices

When adding games to the console, follow these best practices:

- **User Experience**: Match the visual style of the existing games (dark theme, colorful elements)
- **Error Handling**: Include proper error handling to prevent crashes
- **Documentation**: Add clear instructions and help text within your game
- **Performance**: Keep resource usage reasonable for smooth operation
- **Exit Handling**: Ensure your game returns cleanly to the console when completed
- **Cross-Platform**: Test on different operating systems if possible
- **Code Quality**: Write clean, well-documented code for easier maintenance

### 6. Testing Your Game

To test your game:

1. Add it to the `games/catalog.json` file
2. Run the console (`python main.py`)
3. Select your game from the menu
4. Test all features and edge cases
5. Ensure it returns cleanly to the console when exiting

If you encounter issues, check the console output for error messages.

## License

MIT License - Feel free to modify and distribute! 