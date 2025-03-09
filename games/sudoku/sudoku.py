#!/usr/bin/env python3
import os
import sys
import time
import random
import colorama
from colorama import Fore, Back, Style
import copy

# Initialize colorama
colorama.init(autoreset=True)

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the game header."""
    print(f"{Back.CYAN}{Fore.WHITE}╔═══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Back.CYAN}{Fore.WHITE}║                        SUDOKU                                ║{Style.RESET_ALL}")
    print(f"{Back.CYAN}{Fore.WHITE}╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()

class Sudoku:
    def __init__(self, difficulty="medium"):
        """Initialize the Sudoku game."""
        self.difficulty = difficulty
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.original_board = None
        self.solution = None
        self.generate_puzzle()
    
    def generate_puzzle(self):
        """Generate a new Sudoku puzzle."""
        # Start with a solved board
        self.generate_solved_board()
        
        # Make a copy of the solved board as the solution
        self.solution = copy.deepcopy(self.board)
        
        # Remove numbers to create the puzzle
        self.remove_numbers()
        
        # Make a copy of the puzzle as the original board
        self.original_board = copy.deepcopy(self.board)
    
    def generate_solved_board(self):
        """Generate a solved Sudoku board."""
        # Start with an empty board
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        
        # Fill the diagonal 3x3 boxes first (these can be filled independently)
        for i in range(0, 9, 3):
            self.fill_box(i, i)
        
        # Fill the rest of the board using backtracking
        self.solve_board()
    
    def fill_box(self, row, col):
        """Fill a 3x3 box with random numbers."""
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        
        for i in range(3):
            for j in range(3):
                self.board[row + i][col + j] = numbers.pop()
    
    def solve_board(self):
        """Solve the Sudoku board using backtracking."""
        empty_cell = self.find_empty()
        if not empty_cell:
            return True  # Board is solved
        
        row, col = empty_cell
        
        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                
                if self.solve_board():
                    return True
                
                self.board[row][col] = 0  # Backtrack
        
        return False
    
    def find_empty(self):
        """Find an empty cell in the board."""
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j)
        return None
    
    def is_valid(self, row, col, num):
        """Check if a number can be placed in a cell."""
        # Check row
        for j in range(9):
            if self.board[row][j] == num:
                return False
        
        # Check column
        for i in range(9):
            if self.board[i][col] == num:
                return False
        
        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.board[i][j] == num:
                    return False
        
        return True
    
    def remove_numbers(self):
        """Remove numbers from the solved board to create a puzzle."""
        # Number of cells to remove based on difficulty
        if self.difficulty == "easy":
            cells_to_remove = 40
        elif self.difficulty == "medium":
            cells_to_remove = 50
        else:  # hard
            cells_to_remove = 60
        
        # Create a list of all cell positions
        positions = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(positions)
        
        # Remove numbers one by one, ensuring the puzzle still has a unique solution
        for i, j in positions:
            if cells_to_remove <= 0:
                break
            
            temp = self.board[i][j]
            self.board[i][j] = 0
            
            # Check if the puzzle still has a unique solution
            # For simplicity, we'll just check if it's solvable
            # A more thorough check would ensure uniqueness
            board_copy = copy.deepcopy(self.board)
            if self.count_solutions(board_copy) == 1:
                cells_to_remove -= 1
            else:
                self.board[i][j] = temp  # Restore the number
    
    def count_solutions(self, board, limit=2):
        """Count the number of solutions to the puzzle, up to a limit."""
        empty_cell = self.find_empty_in_board(board)
        if not empty_cell:
            return 1  # Found a solution
        
        row, col = empty_cell
        count = 0
        
        for num in range(1, 10):
            if self.is_valid_in_board(board, row, col, num):
                board[row][col] = num
                
                count += self.count_solutions(board, limit - count)
                
                if count >= limit:
                    break
                
                board[row][col] = 0  # Backtrack
        
        return count
    
    def find_empty_in_board(self, board):
        """Find an empty cell in a given board."""
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None
    
    def is_valid_in_board(self, board, row, col, num):
        """Check if a number can be placed in a cell of a given board."""
        # Check row
        for j in range(9):
            if board[row][j] == num:
                return False
        
        # Check column
        for i in range(9):
            if board[i][col] == num:
                return False
        
        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] == num:
                    return False
        
        return True
    
    def is_complete(self):
        """Check if the board is complete and correct."""
        # Check if there are any empty cells
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return False
        
        # Check if the board is valid
        for i in range(9):
            for j in range(9):
                num = self.board[i][j]
                self.board[i][j] = 0
                if not self.is_valid(i, j, num):
                    self.board[i][j] = num
                    return False
                self.board[i][j] = num
        
        return True
    
    def is_original(self, row, col):
        """Check if a cell is part of the original puzzle."""
        return self.original_board[row][col] != 0
    
    def place_number(self, row, col, num):
        """Place a number in a cell if it's valid."""
        if self.is_original(row, col):
            return False, "Cannot modify original numbers."
        
        if num == 0:
            # Erasing a cell is always allowed
            self.board[row][col] = 0
            return True, "Cell cleared."
        
        if not self.is_valid(row, col, num):
            return False, "Invalid move. Number conflicts with row, column, or box."
        
        self.board[row][col] = num
        return True, "Number placed successfully."
    
    def get_hint(self):
        """Get a hint by revealing a random cell."""
        # Find all empty cells
        empty_cells = []
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    empty_cells.append((i, j))
        
        if not empty_cells:
            return False, "No empty cells left."
        
        # Choose a random empty cell
        row, col = random.choice(empty_cells)
        
        # Reveal the correct number
        self.board[row][col] = self.solution[row][col]
        
        return True, f"Hint: Placed {self.solution[row][col]} at position ({row+1}, {col+1})."
    
    def print_board(self):
        """Print the Sudoku board."""
        print(f"{Fore.CYAN}   1 2 3   4 5 6   7 8 9{Style.RESET_ALL}")
        print(f"{Fore.CYAN}  ╔═══════╦═══════╦═══════╗{Style.RESET_ALL}")
        
        for i in range(9):
            print(f"{Fore.CYAN}{i+1} ║{Style.RESET_ALL}", end="")
            
            for j in range(9):
                if j % 3 == 0 and j > 0:
                    print(f"{Fore.CYAN}║{Style.RESET_ALL}", end="")
                
                if self.board[i][j] == 0:
                    print(f" ·", end="")
                else:
                    if self.is_original(i, j):
                        print(f"{Fore.GREEN} {self.board[i][j]}{Style.RESET_ALL}", end="")
                    else:
                        print(f"{Fore.WHITE} {self.board[i][j]}{Style.RESET_ALL}", end="")
            
            print(f"{Fore.CYAN} ║{Style.RESET_ALL}")
            
            if i % 3 == 2 and i < 8:
                print(f"{Fore.CYAN}  ╠═══════╬═══════╬═══════╣{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}  ╚═══════╩═══════╩═══════╝{Style.RESET_ALL}")
        print()

def show_instructions():
    """Display game instructions."""
    print(f"{Fore.CYAN}INSTRUCTIONS:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Sudoku is a logic-based number placement puzzle.")
    print(f"The objective is to fill a 9×9 grid with digits so that")
    print(f"each column, each row, and each of the nine 3×3 subgrids")
    print(f"contain all of the digits from 1 to 9.{Style.RESET_ALL}")
    print()
    print(f"{Fore.WHITE}Commands:")
    print(f" - To place a number: enter row, column, and number (e.g., '3 5 7')")
    print(f" - To erase a number: enter row, column, and 0 (e.g., '3 5 0')")
    print(f" - For a hint: enter 'h' or 'hint'")
    print(f" - To quit: enter 'q' or 'quit'")
    print(f" - To check your solution: enter 'c' or 'check'")
    print(f" - To start a new game: enter 'n' or 'new'")
    print(f" - To solve the puzzle: enter 's' or 'solve'{Style.RESET_ALL}")
    print()
    print(f"{Fore.GREEN}Original numbers are shown in green and cannot be modified.{Style.RESET_ALL}")
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
        print(f"1. Easy")
        print(f"2. Medium")
        print(f"3. Hard")
        print()
        
        while True:
            try:
                choice = int(input(f"{Fore.YELLOW}Enter your choice (1-3): {Style.RESET_ALL}"))
                if 1 <= choice <= 3:
                    break
                else:
                    print(f"{Fore.RED}Please enter a number between 1 and 3.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
        
        # Set difficulty based on choice
        if choice == 1:
            difficulty = "easy"
        elif choice == 2:
            difficulty = "medium"
        else:
            difficulty = "hard"
        
        # Create a new Sudoku game
        print(f"{Fore.CYAN}Generating puzzle...{Style.RESET_ALL}")
        game = Sudoku(difficulty)
        
        # Main game loop
        while True:
            clear_screen()
            print_header()
            print(f"{Fore.CYAN}Difficulty: {difficulty.capitalize()}{Style.RESET_ALL}")
            print()
            
            game.print_board()
            
            # Get user input
            user_input = input(f"{Fore.YELLOW}Enter command: {Style.RESET_ALL}").strip().lower()
            
            if user_input in ['q', 'quit']:
                clear_screen()
                print_header()
                print(f"{Fore.GREEN}Thanks for playing Sudoku!{Style.RESET_ALL}")
                time.sleep(1.5)
                return
            
            elif user_input in ['h', 'hint']:
                success, message = game.get_hint()
                print(f"{Fore.CYAN}{message}{Style.RESET_ALL}")
                time.sleep(1.5)
            
            elif user_input in ['c', 'check']:
                if game.is_complete():
                    print(f"{Fore.GREEN}Congratulations! You solved the puzzle!{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}The puzzle is not complete or has errors.{Style.RESET_ALL}")
                time.sleep(1.5)
            
            elif user_input in ['n', 'new']:
                break  # Start a new game
            
            elif user_input in ['s', 'solve']:
                # Confirm before solving
                confirm = input(f"{Fore.YELLOW}Are you sure you want to see the solution? (y/n): {Style.RESET_ALL}").strip().lower()
                if confirm == 'y':
                    game.board = copy.deepcopy(game.solution)
                    clear_screen()
                    print_header()
                    print(f"{Fore.CYAN}Difficulty: {difficulty.capitalize()}{Style.RESET_ALL}")
                    print()
                    game.print_board()
                    print(f"{Fore.CYAN}Here's the solution.{Style.RESET_ALL}")
                    time.sleep(3)
                    break  # Start a new game
            
            else:
                # Try to parse as row, column, number
                try:
                    parts = user_input.split()
                    if len(parts) == 3:
                        row = int(parts[0]) - 1  # Convert to 0-based index
                        col = int(parts[1]) - 1  # Convert to 0-based index
                        num = int(parts[2])
                        
                        if 0 <= row < 9 and 0 <= col < 9 and 0 <= num <= 9:
                            success, message = game.place_number(row, col, num)
                            print(f"{Fore.CYAN}{message}{Style.RESET_ALL}")
                            time.sleep(1)
                            
                            # Check if the puzzle is complete after a successful move
                            if success and game.is_complete():
                                clear_screen()
                                print_header()
                                print(f"{Fore.CYAN}Difficulty: {difficulty.capitalize()}{Style.RESET_ALL}")
                                print()
                                game.print_board()
                                print(f"{Fore.GREEN}Congratulations! You solved the puzzle!{Style.RESET_ALL}")
                                time.sleep(3)
                                break  # Start a new game
                        else:
                            print(f"{Fore.RED}Invalid input. Row and column must be between 1 and 9, number between 0 and 9.{Style.RESET_ALL}")
                            time.sleep(1.5)
                    else:
                        print(f"{Fore.RED}Invalid command. Type 'h' for help.{Style.RESET_ALL}")
                        time.sleep(1.5)
                except ValueError:
                    print(f"{Fore.RED}Invalid input format. Please enter row, column, and number as integers.{Style.RESET_ALL}")
                    time.sleep(1.5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print_header()
        print(f"{Fore.GREEN}Thanks for playing Sudoku!{Style.RESET_ALL}")
        sys.exit(0) 