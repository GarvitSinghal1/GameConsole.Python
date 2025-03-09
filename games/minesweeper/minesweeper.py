#!/usr/bin/env python3
import os
import sys
import time
import random
import colorama
from colorama import Fore, Back, Style

# Initialize colorama
colorama.init(autoreset=True)

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the game header."""
    print(f"{Back.BLUE}{Fore.WHITE}╔═══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Back.BLUE}{Fore.WHITE}║                     MINESWEEPER                              ║{Style.RESET_ALL}")
    print(f"{Back.BLUE}{Fore.WHITE}╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()

# Colors for numbers 1-8 (adjacent mines)
NUMBER_COLORS = {
    1: Fore.BLUE,
    2: Fore.GREEN,
    3: Fore.RED,
    4: Fore.MAGENTA,
    5: Fore.YELLOW,
    6: Fore.CYAN,
    7: Fore.WHITE,
    8: Fore.BLACK
}

class Minesweeper:
    def __init__(self, rows, cols, num_mines):
        """Initialize the Minesweeper game."""
        self.rows = rows
        self.cols = cols
        self.num_mines = min(num_mines, rows * cols - 1)  # Ensure mines don't exceed board size - 1
        
        # Create the board
        self.board = [['0' for _ in range(cols)] for _ in range(rows)]
        self.revealed = [[False for _ in range(cols)] for _ in range(rows)]
        self.flagged = [[False for _ in range(cols)] for _ in range(rows)]
        
        # Place mines randomly
        self.place_mines()
        
        # Calculate numbers for adjacent cells
        self.calculate_numbers()
        
        # Game state
        self.game_over = False
        self.win = False
    
    def place_mines(self):
        """Place mines randomly on the board."""
        mines_placed = 0
        while mines_placed < self.num_mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            
            if self.board[row][col] != 'M':
                self.board[row][col] = 'M'
                mines_placed += 1
    
    def calculate_numbers(self):
        """Calculate numbers for cells adjacent to mines."""
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == 'M':
                    continue
                
                # Count adjacent mines
                mines = 0
                for r in range(max(0, row-1), min(self.rows, row+2)):
                    for c in range(max(0, col-1), min(self.cols, col+2)):
                        if self.board[r][c] == 'M':
                            mines += 1
                
                self.board[row][col] = str(mines)
    
    def display_board(self, reveal_all=False):
        """Display the current game board."""
        # Print column numbers
        print('    ', end='')
        for col in range(self.cols):
            print(f"{col+1:2d} ", end='')
        print('\n')
        
        # Print the board
        for row in range(self.rows):
            print(f"{row+1:2d} | ", end='')
            for col in range(self.cols):
                if reveal_all and self.board[row][col] == 'M':
                    # Show all mines when game is over
                    print(f"{Fore.RED}M{Style.RESET_ALL} ", end='')
                elif self.flagged[row][col]:
                    # Flagged cell
                    print(f"{Fore.RED}F{Style.RESET_ALL} ", end='')
                elif not self.revealed[row][col]:
                    # Unrevealed cell
                    print(f"■ ", end='')
                elif self.board[row][col] == '0':
                    # Empty cell
                    print(f"  ", end='')
                elif self.board[row][col] == 'M':
                    # Mine (only shown when game is over)
                    print(f"{Fore.RED}M{Style.RESET_ALL} ", end='')
                else:
                    # Number cell
                    number = int(self.board[row][col])
                    color = NUMBER_COLORS.get(number, Fore.WHITE)
                    print(f"{color}{number}{Style.RESET_ALL} ", end='')
            print()
        print()
    
    def is_valid_cell(self, row, col):
        """Check if a cell is within the board boundaries."""
        return 0 <= row < self.rows and 0 <= col < self.cols
    
    def reveal_cell(self, row, col):
        """Reveal a cell and its adjacent cells if it's empty."""
        if not self.is_valid_cell(row, col) or self.revealed[row][col] or self.flagged[row][col]:
            return
        
        # Reveal the cell
        self.revealed[row][col] = True
        
        # If it's a mine, game over
        if self.board[row][col] == 'M':
            self.game_over = True
            return
        
        # If it's an empty cell, reveal adjacent cells recursively
        if self.board[row][col] == '0':
            for r in range(max(0, row-1), min(self.rows, row+2)):
                for c in range(max(0, col-1), min(self.cols, col+2)):
                    if (r, c) != (row, col):
                        self.reveal_cell(r, c)
    
    def toggle_flag(self, row, col):
        """Toggle a flag on or off at the specified cell."""
        if not self.is_valid_cell(row, col) or self.revealed[row][col]:
            return
        
        self.flagged[row][col] = not self.flagged[row][col]
    
    def check_win(self):
        """Check if the player has won."""
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] != 'M' and not self.revealed[row][col]:
                    return False
        
        self.win = True
        self.game_over = True
        return True
    
    def get_unrevealed_count(self):
        """Get the number of unrevealed cells."""
        count = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.revealed[row][col]:
                    count += 1
        return count
    
    def get_flags_count(self):
        """Get the number of flagged cells."""
        count = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if self.flagged[row][col]:
                    count += 1
        return count

def show_instructions():
    """Display game instructions."""
    print(f"{Fore.CYAN}INSTRUCTIONS:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Minesweeper is a puzzle game where you need to clear a board")
    print(f"containing hidden mines without detonating any of them.{Style.RESET_ALL}")
    print()
    print(f"{Fore.WHITE}Each cell you reveal will either be empty, have a number")
    print(f"indicating how many mines are adjacent to it, or contain a mine.")
    print(f"Use this information to deduce where mines are located.{Style.RESET_ALL}")
    print()
    print(f"{Fore.WHITE}Commands:")
    print(f" - 'r' followed by row,col (e.g., 'r 1,2') to reveal a cell")
    print(f" - 'f' followed by row,col (e.g., 'f 1,2') to flag/unflag a cell")
    print(f" - 'q' to quit the game{Style.RESET_ALL}")
    print()
    input(f"{Fore.GREEN}Press Enter to start the game...{Style.RESET_ALL}")

def main():
    """Main game function."""
    clear_screen()
    print_header()
    show_instructions()
    
    while True:
        clear_screen()
        print_header()
        
        # Choose difficulty
        print(f"{Fore.CYAN}Choose difficulty:{Style.RESET_ALL}")
        print(f"1. Easy (9x9 grid, 10 mines)")
        print(f"2. Medium (16x16 grid, 40 mines)")
        print(f"3. Hard (16x30 grid, 99 mines)")
        print(f"4. Custom")
        print()
        
        while True:
            try:
                choice = int(input(f"{Fore.YELLOW}Enter your choice (1-4): {Style.RESET_ALL}"))
                if 1 <= choice <= 4:
                    break
                else:
                    print(f"{Fore.RED}Please enter a number between 1 and 4.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
        
        # Set board dimensions and number of mines based on difficulty
        if choice == 1:  # Easy
            rows, cols, mines = 9, 9, 10
        elif choice == 2:  # Medium
            rows, cols, mines = 16, 16, 40
        elif choice == 3:  # Hard
            rows, cols, mines = 16, 30, 99
        else:  # Custom
            try:
                print(f"{Fore.CYAN}Custom difficulty:{Style.RESET_ALL}")
                rows = int(input(f"{Fore.YELLOW}Enter number of rows (5-24): {Style.RESET_ALL}"))
                cols = int(input(f"{Fore.YELLOW}Enter number of columns (5-30): {Style.RESET_ALL}"))
                max_mines = rows * cols - 1
                mines = int(input(f"{Fore.YELLOW}Enter number of mines (1-{max_mines}): {Style.RESET_ALL}"))
                
                # Validate input
                if rows < 5 or rows > 24 or cols < 5 or cols > 30 or mines < 1 or mines > max_mines:
                    print(f"{Fore.RED}Invalid input. Using Easy difficulty.{Style.RESET_ALL}")
                    rows, cols, mines = 9, 9, 10
                    time.sleep(1.5)
            except ValueError:
                print(f"{Fore.RED}Invalid input. Using Easy difficulty.{Style.RESET_ALL}")
                rows, cols, mines = 9, 9, 10
                time.sleep(1.5)
        
        # Create and play the game
        game = Minesweeper(rows, cols, mines)
        
        while not game.game_over:
            clear_screen()
            print_header()
            print(f"{Fore.CYAN}Mines: {mines} | Flags: {game.get_flags_count()} | Unrevealed cells: {game.get_unrevealed_count()}{Style.RESET_ALL}")
            print()
            game.display_board()
            print(f"{Fore.YELLOW}Commands: 'r row,col' to reveal | 'f row,col' to flag | 'q' to quit{Style.RESET_ALL}")
            
            cmd = input(f"{Fore.GREEN}Enter command: {Style.RESET_ALL}").strip().lower()
            
            if cmd == 'q':
                print(f"{Fore.YELLOW}Game aborted.{Style.RESET_ALL}")
                time.sleep(1)
                break
            
            try:
                # Parse command and coordinates
                parts = cmd.split()
                if len(parts) != 2:
                    print(f"{Fore.RED}Invalid command format. Use 'r row,col' or 'f row,col'.{Style.RESET_ALL}")
                    time.sleep(1)
                    continue
                
                action, coords = parts
                row, col = map(int, coords.split(','))
                
                # Convert to 0-indexed
                row -= 1
                col -= 1
                
                if action == 'r':
                    # Reveal cell
                    game.reveal_cell(row, col)
                    # Check if player has won
                    game.check_win()
                elif action == 'f':
                    # Toggle flag
                    game.toggle_flag(row, col)
                else:
                    print(f"{Fore.RED}Invalid command. Use 'r' to reveal or 'f' to flag.{Style.RESET_ALL}")
                    time.sleep(1)
            except (ValueError, IndexError):
                print(f"{Fore.RED}Invalid coordinates. Use format 'row,col' (e.g., '1,2').{Style.RESET_ALL}")
                time.sleep(1)
        
        # Display final board and result
        if game.game_over:
            clear_screen()
            print_header()
            print(f"{Fore.CYAN}Mines: {mines} | Flags: {game.get_flags_count()} | Unrevealed cells: {game.get_unrevealed_count()}{Style.RESET_ALL}")
            print()
            game.display_board(reveal_all=True)
            
            if game.win:
                print(f"{Fore.GREEN}Congratulations! You found all the mines!{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Game over! You hit a mine!{Style.RESET_ALL}")
        
        # Ask to play again
        print()
        play_again = input(f"{Fore.CYAN}Play again? (y/n): {Style.RESET_ALL}").lower()
        if play_again != 'y':
            clear_screen()
            print_header()
            print(f"{Fore.GREEN}Thanks for playing Minesweeper!{Style.RESET_ALL}")
            time.sleep(1.5)
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print_header()
        print(f"{Fore.GREEN}Thanks for playing Minesweeper!{Style.RESET_ALL}")
        sys.exit(0) 