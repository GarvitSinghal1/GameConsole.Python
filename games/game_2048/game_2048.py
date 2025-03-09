#!/usr/bin/env python3
import os
import sys
import time
import random
import colorama
from colorama import Fore, Back, Style

# Import msvcrt only on Windows
if os.name == 'nt':
    import msvcrt
else:
    msvcrt = None

# Initialize colorama
colorama.init(autoreset=True)

# Color mapping for different tile values
COLORS = {
    0: (Fore.WHITE, Back.BLACK),
    2: (Fore.BLACK, Back.WHITE),
    4: (Fore.BLACK, Back.CYAN),
    8: (Fore.WHITE, Back.BLUE),
    16: (Fore.WHITE, Back.MAGENTA),
    32: (Fore.WHITE, Back.RED),
    64: (Fore.WHITE, Back.GREEN),
    128: (Fore.BLACK, Back.YELLOW),
    256: (Fore.WHITE, Back.BLUE),
    512: (Fore.WHITE, Back.MAGENTA),
    1024: (Fore.WHITE, Back.RED),
    2048: (Fore.WHITE, Back.GREEN),
    4096: (Fore.BLACK, Back.YELLOW),
    8192: (Fore.WHITE, Back.BLUE),
}

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the game header."""
    print(f"{Back.YELLOW}{Fore.BLACK}╔═══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Back.YELLOW}{Fore.BLACK}║                         2048                                   ║{Style.RESET_ALL}")
    print(f"{Back.YELLOW}{Fore.BLACK}╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()

def getch():
    """Get a single character from the console (cross-platform)."""
    if os.name == 'nt':  # For Windows
        return msvcrt.getch().decode('utf-8')
    else:  # For Unix/Linux
        import termios
        import tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class Game2048:
    def __init__(self, size=4):
        """Initialize the 2048 game with a given board size."""
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.score = 0
        self.max_tile = 0
        # Add two random tiles to start
        self.add_random_tile()
        self.add_random_tile()
    
    def add_random_tile(self):
        """Add a random tile (2 or 4) to an empty cell."""
        # Find all empty cells
        empty_cells = [(i, j) for i in range(self.size) for j in range(self.size) if self.board[i][j] == 0]
        
        if empty_cells:
            # Choose a random empty cell
            i, j = random.choice(empty_cells)
            
            # Add a 2 (90% chance) or 4 (10% chance)
            self.board[i][j] = 2 if random.random() < 0.9 else 4
            
            # Update max tile
            self.max_tile = max(self.max_tile, self.board[i][j])
    
    def display_board(self):
        """Display the current game board."""
        # Calculate the width needed for each cell based on the highest number
        cell_width = max(len(str(self.max_tile)), 4) + 2
        
        # Print score
        print(f"{Fore.YELLOW}Score: {self.score}{Style.RESET_ALL}")
        print()
        
        # Print top border
        print("┌" + "─" * cell_width + ("┬" + "─" * cell_width) * (self.size - 1) + "┐")
        
        # Print rows
        for i in range(self.size):
            for j in range(self.size):
                value = self.board[i][j]
                if value == 0:
                    # Empty cell
                    print("│" + " " * cell_width, end="")
                else:
                    # Colored cell with value
                    fore, back = COLORS.get(value, (Fore.WHITE, Back.BLACK))
                    centered_value = str(value).center(cell_width)
                    print(f"│{fore}{back}{centered_value}{Style.RESET_ALL}", end="")
            print("│")
            
            # Print row separator
            if i < self.size - 1:
                print("├" + "─" * cell_width + ("┼" + "─" * cell_width) * (self.size - 1) + "┤")
        
        # Print bottom border
        print("└" + "─" * cell_width + ("┴" + "─" * cell_width) * (self.size - 1) + "┘")
        print()
    
    def move_left(self):
        """Move tiles to the left and merge if possible."""
        moved = False
        for i in range(self.size):
            # Compress the row (move all non-zero elements to the left)
            row = [self.board[i][j] for j in range(self.size) if self.board[i][j] != 0]
            row += [0] * (self.size - len(row))
            
            # Merge adjacent identical tiles
            for j in range(self.size - 1):
                if row[j] != 0 and row[j] == row[j + 1]:
                    row[j] *= 2
                    self.score += row[j]  # Add merged value to score
                    self.max_tile = max(self.max_tile, row[j])  # Update max tile
                    row[j + 1] = 0
            
            # Compress again after merging
            row = [row[j] for j in range(self.size) if row[j] != 0]
            row += [0] * (self.size - len(row))
            
            # Check if the move changed the row
            if row != [self.board[i][j] for j in range(self.size)]:
                moved = True
            
            # Update the board
            for j in range(self.size):
                self.board[i][j] = row[j]
        
        return moved
    
    def move_right(self):
        """Move tiles to the right and merge if possible."""
        moved = False
        for i in range(self.size):
            # Compress the row (move all non-zero elements to the right)
            row = [self.board[i][j] for j in range(self.size) if self.board[i][j] != 0]
            row = [0] * (self.size - len(row)) + row
            
            # Merge adjacent identical tiles from right to left
            for j in range(self.size - 1, 0, -1):
                if row[j] != 0 and row[j] == row[j - 1]:
                    row[j] *= 2
                    self.score += row[j]  # Add merged value to score
                    self.max_tile = max(self.max_tile, row[j])  # Update max tile
                    row[j - 1] = 0
            
            # Compress again after merging
            row = [row[j] for j in range(self.size) if row[j] != 0]
            row = [0] * (self.size - len(row)) + row
            
            # Check if the move changed the row
            if row != [self.board[i][j] for j in range(self.size)]:
                moved = True
            
            # Update the board
            for j in range(self.size):
                self.board[i][j] = row[j]
        
        return moved
    
    def move_up(self):
        """Move tiles up and merge if possible."""
        moved = False
        for j in range(self.size):
            # Compress the column (move all non-zero elements up)
            col = [self.board[i][j] for i in range(self.size) if self.board[i][j] != 0]
            col += [0] * (self.size - len(col))
            
            # Merge adjacent identical tiles
            for i in range(self.size - 1):
                if col[i] != 0 and col[i] == col[i + 1]:
                    col[i] *= 2
                    self.score += col[i]  # Add merged value to score
                    self.max_tile = max(self.max_tile, col[i])  # Update max tile
                    col[i + 1] = 0
            
            # Compress again after merging
            col = [col[i] for i in range(self.size) if col[i] != 0]
            col += [0] * (self.size - len(col))
            
            # Check if the move changed the column
            if col != [self.board[i][j] for i in range(self.size)]:
                moved = True
            
            # Update the board
            for i in range(self.size):
                self.board[i][j] = col[i]
        
        return moved
    
    def move_down(self):
        """Move tiles down and merge if possible."""
        moved = False
        for j in range(self.size):
            # Compress the column (move all non-zero elements down)
            col = [self.board[i][j] for i in range(self.size) if self.board[i][j] != 0]
            col = [0] * (self.size - len(col)) + col
            
            # Merge adjacent identical tiles from bottom to top
            for i in range(self.size - 1, 0, -1):
                if col[i] != 0 and col[i] == col[i - 1]:
                    col[i] *= 2
                    self.score += col[i]  # Add merged value to score
                    self.max_tile = max(self.max_tile, col[i])  # Update max tile
                    col[i - 1] = 0
            
            # Compress again after merging
            col = [col[i] for i in range(self.size) if col[i] != 0]
            col = [0] * (self.size - len(col)) + col
            
            # Check if the move changed the column
            if col != [self.board[i][j] for i in range(self.size)]:
                moved = True
            
            # Update the board
            for i in range(self.size):
                self.board[i][j] = col[i]
        
        return moved
    
    def is_game_over(self):
        """Check if the game is over (no more moves possible)."""
        # Check if board is full
        if any(self.board[i][j] == 0 for i in range(self.size) for j in range(self.size)):
            return False
        
        # Check if any adjacent cells have the same value
        for i in range(self.size):
            for j in range(self.size):
                value = self.board[i][j]
                # Check right neighbor
                if j < self.size - 1 and self.board[i][j + 1] == value:
                    return False
                # Check bottom neighbor
                if i < self.size - 1 and self.board[i + 1][j] == value:
                    return False
        
        return True
    
    def is_win(self):
        """Check if the player has won (reached 2048)."""
        return self.max_tile >= 2048

def show_instructions():
    """Display game instructions."""
    print(f"{Fore.CYAN}INSTRUCTIONS:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}2048 is a sliding puzzle game. Combine identical tiles by")
    print(f"moving them in four directions. When two tiles with the same")
    print(f"number touch, they merge into one tile with the sum of their values.{Style.RESET_ALL}")
    print()
    print(f"{Fore.WHITE}The goal is to create a tile with the value 2048.{Style.RESET_ALL}")
    print()
    print(f"{Fore.WHITE}Controls:")
    print(f"  W / UP ARROW    - Move Up")
    print(f"  S / DOWN ARROW  - Move Down")
    print(f"  A / LEFT ARROW  - Move Left")
    print(f"  D / RIGHT ARROW - Move Right")
    print(f"  Q              - Quit the game{Style.RESET_ALL}")
    print()
    input(f"{Fore.GREEN}Press Enter to start the game...{Style.RESET_ALL}")

def get_arrow_key():
    """Get arrow key input (cross-platform)."""
    key = getch().lower()
    
    if key == 'w' or key == '\x1b':  # '\x1b' is Escape, the start of arrow key sequences
        if key == '\x1b':
            # This could be an arrow key sequence
            if getch() == '[':  # Confirm it's an arrow key
                arrow_key = getch()
                if arrow_key == 'A':  # Up arrow
                    return 'w'
        return 'w'
    elif key == 's':
        return 's'
    elif key == 'a':
        return 'a'
    elif key == 'd':
        return 'd'
    elif key == 'q':
        return 'q'
    return None

def main():
    """Main game function."""
    clear_screen()
    print_header()
    show_instructions()
    
    while True:
        # Start a new game
        game = Game2048()
        
        # Game loop
        while not game.is_game_over() and not game.is_win():
            clear_screen()
            print_header()
            game.display_board()
            
            print(f"{Fore.WHITE}Use WASD or arrow keys to move. Q to quit.{Style.RESET_ALL}")
            
            # Get player's move
            moved = False
            while not moved:
                key = get_arrow_key()
                
                if key == 'q':
                    # Quit the game
                    clear_screen()
                    print_header()
                    print(f"{Fore.GREEN}Thanks for playing 2048!{Style.RESET_ALL}")
                    return
                
                # Apply the move if valid
                if key == 'w':
                    moved = game.move_up()
                elif key == 's':
                    moved = game.move_down()
                elif key == 'a':
                    moved = game.move_left()
                elif key == 'd':
                    moved = game.move_right()
                
                if not moved and key in {'w', 's', 'a', 'd'}:
                    print(f"{Fore.RED}Invalid move! Try a different direction.{Style.RESET_ALL}")
                    time.sleep(0.5)
                    clear_screen()
                    print_header()
                    game.display_board()
                    print(f"{Fore.WHITE}Use WASD or arrow keys to move. Q to quit.{Style.RESET_ALL}")
            
            # Add a new random tile after a valid move
            game.add_random_tile()
        
        # Game over or win
        clear_screen()
        print_header()
        game.display_board()
        
        if game.is_win():
            print(f"{Fore.GREEN}Congratulations! You reached 2048! Final score: {game.score}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Game over! No more moves available. Final score: {game.score}{Style.RESET_ALL}")
        
        # Ask to play again
        print()
        play_again = input(f"{Fore.CYAN}Play again? (y/n): {Style.RESET_ALL}").lower()
        if play_again != 'y':
            clear_screen()
            print_header()
            print(f"{Fore.GREEN}Thanks for playing 2048!{Style.RESET_ALL}")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print_header()
        print(f"{Fore.GREEN}Thanks for playing 2048!{Style.RESET_ALL}")
        sys.exit(0) 