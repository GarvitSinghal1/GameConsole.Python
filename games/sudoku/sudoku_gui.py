#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox, ttk
import random
import copy
import sys
import os

# Try to import Sudoku class from terminal version
try:
    from games.sudoku import Sudoku
except ImportError:
    # Define Sudoku class if import fails
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
            
            return True, (row, col, self.solution[row][col])

class SudokuCell(tk.Frame):
    """A single cell in the Sudoku grid."""
    def __init__(self, master, row, col, value=0, is_original=False, **kwargs):
        super().__init__(master, **kwargs)
        
        self.row = row
        self.col = col
        self.value = value
        self.is_original = is_original
        
        # Create the cell button
        self.button = tk.Button(
            self,
            text="" if value == 0 else str(value),
            width=3,
            height=1,
            font=("Helvetica", 14, "bold" if is_original else "normal"),
            bg="#F0F0F0" if not is_original else "#E0E0E0",
            fg="black" if not is_original else "blue",
            relief=tk.RAISED if not is_original else tk.SUNKEN,
            command=self.on_click
        )
        self.button.pack(fill=tk.BOTH, expand=True)
        
        # Configure border based on position
        self.configure(
            borderwidth=2,
            relief=tk.RAISED
        )
    
    def on_click(self):
        """Handle cell click event."""
        if not self.is_original:
            self.master.master.select_cell(self.row, self.col)
    
    def update_value(self, value):
        """Update the cell's value."""
        self.value = value
        self.button.config(text="" if value == 0 else str(value))
    
    def highlight(self, highlight=True):
        """Highlight or unhighlight the cell."""
        if highlight:
            self.button.config(bg="#FFFF99")
        else:
            self.button.config(bg="#F0F0F0" if not self.is_original else "#E0E0E0")

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        self.root.geometry("700x750")
        self.root.configure(bg="#F5F5F5")
        self.root.resizable(True, True)
        
        # Game parameters
        self.difficulty = "medium"  # Default difficulty
        self.game = None
        self.selected_cell = None
        self.cells = []
        
        # Create widgets
        self.create_widgets()
        
        # Show welcome screen
        self.show_welcome()
        
        # Start a new game
        self.new_game()
    
    def create_widgets(self):
        """Create the GUI widgets."""
        # Main frame
        self.main_frame = tk.Frame(self.root, bg="#F5F5F5")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title label
        self.title_label = tk.Label(
            self.main_frame,
            text="SUDOKU",
            font=("Helvetica", 24, "bold"),
            bg="#F5F5F5"
        )
        self.title_label.pack(pady=(0, 10))
        
        # Game info frame
        self.info_frame = tk.Frame(self.main_frame, bg="#F5F5F5")
        self.info_frame.pack(fill=tk.X, pady=5)
        
        # Difficulty label
        self.difficulty_var = tk.StringVar(value=f"Difficulty: {self.difficulty.capitalize()}")
        self.difficulty_label = tk.Label(
            self.info_frame,
            textvariable=self.difficulty_var,
            font=("Helvetica", 12),
            bg="#F5F5F5"
        )
        self.difficulty_label.pack(side=tk.LEFT, padx=10)
        
        # Status label
        self.status_var = tk.StringVar(value="Select a cell to begin")
        self.status_label = tk.Label(
            self.info_frame,
            textvariable=self.status_var,
            font=("Helvetica", 12),
            bg="#F5F5F5"
        )
        self.status_label.pack(side=tk.RIGHT, padx=10)
        
        # Game board frame
        self.board_frame = tk.Frame(self.main_frame, bg="black")
        self.board_frame.pack(pady=10)
        
        # Create the 9x9 grid of cells
        for i in range(9):
            row_cells = []
            for j in range(9):
                cell = SudokuCell(
                    self.board_frame,
                    row=i,
                    col=j,
                    width=50,
                    height=50,
                    padx=1,
                    pady=1,
                    bg="black"
                )
                cell.grid(row=i, column=j, padx=1 if j % 3 != 2 else 3, pady=1 if i % 3 != 2 else 3)
                row_cells.append(cell)
            self.cells.append(row_cells)
        
        # Number buttons frame
        self.numbers_frame = tk.Frame(self.main_frame, bg="#F5F5F5")
        self.numbers_frame.pack(pady=10)
        
        # Create number buttons (1-9 and erase)
        for i in range(1, 10):
            button = tk.Button(
                self.numbers_frame,
                text=str(i),
                width=3,
                height=2,
                font=("Helvetica", 12, "bold"),
                command=lambda num=i: self.place_number(num)
            )
            button.grid(row=0, column=i-1, padx=5, pady=5)
        
        # Erase button
        erase_button = tk.Button(
            self.numbers_frame,
            text="X",
            width=3,
            height=2,
            font=("Helvetica", 12, "bold"),
            bg="#FF9999",
            command=lambda: self.place_number(0)
        )
        erase_button.grid(row=0, column=9, padx=5, pady=5)
        
        # Control buttons frame
        self.control_frame = tk.Frame(self.main_frame, bg="#F5F5F5")
        self.control_frame.pack(fill=tk.X, pady=10)
        
        # Hint button
        self.hint_button = tk.Button(
            self.control_frame,
            text="Hint",
            font=("Helvetica", 12),
            bg="#4CAF50",
            fg="white",
            command=self.get_hint
        )
        self.hint_button.pack(side=tk.LEFT, padx=10)
        
        # Check button
        self.check_button = tk.Button(
            self.control_frame,
            text="Check Solution",
            font=("Helvetica", 12),
            bg="#2196F3",
            fg="white",
            command=self.check_solution
        )
        self.check_button.pack(side=tk.LEFT, padx=10)
        
        # Solve button
        self.solve_button = tk.Button(
            self.control_frame,
            text="Solve Puzzle",
            font=("Helvetica", 12),
            bg="#FF9800",
            fg="white",
            command=self.solve_puzzle
        )
        self.solve_button.pack(side=tk.LEFT, padx=10)
        
        # Difficulty selection frame
        self.difficulty_frame = tk.Frame(self.main_frame, bg="#F5F5F5")
        self.difficulty_frame.pack(fill=tk.X, pady=10)
        
        # Difficulty label
        self.difficulty_select_label = tk.Label(
            self.difficulty_frame,
            text="Difficulty:",
            font=("Helvetica", 12),
            bg="#F5F5F5"
        )
        self.difficulty_select_label.pack(side=tk.LEFT, padx=10)
        
        # Difficulty radio buttons
        self.difficulty_var = tk.StringVar(value=self.difficulty)
        
        self.easy_radio = tk.Radiobutton(
            self.difficulty_frame,
            text="Easy",
            variable=self.difficulty_var,
            value="easy",
            command=self.change_difficulty,
            bg="#F5F5F5"
        )
        self.easy_radio.pack(side=tk.LEFT, padx=5)
        
        self.medium_radio = tk.Radiobutton(
            self.difficulty_frame,
            text="Medium",
            variable=self.difficulty_var,
            value="medium",
            command=self.change_difficulty,
            bg="#F5F5F5"
        )
        self.medium_radio.pack(side=tk.LEFT, padx=5)
        
        self.hard_radio = tk.Radiobutton(
            self.difficulty_frame,
            text="Hard",
            variable=self.difficulty_var,
            value="hard",
            command=self.change_difficulty,
            bg="#F5F5F5"
        )
        self.hard_radio.pack(side=tk.LEFT, padx=5)
        
        # New Game button
        self.new_game_button = tk.Button(
            self.difficulty_frame,
            text="New Game",
            font=("Helvetica", 12),
            bg="#673AB7",
            fg="white",
            command=self.new_game
        )
        self.new_game_button.pack(side=tk.RIGHT, padx=10)
        
        # Quit button
        self.quit_button = tk.Button(
            self.difficulty_frame,
            text="Quit",
            font=("Helvetica", 12),
            bg="#F44336",
            fg="white",
            command=self.quit_game
        )
        self.quit_button.pack(side=tk.RIGHT, padx=10)
    
    def show_welcome(self):
        """Show welcome screen and instructions."""
        welcome_window = tk.Toplevel(self.root)
        welcome_window.title("Welcome to Sudoku")
        welcome_window.geometry("500x400")
        welcome_window.transient(self.root)
        welcome_window.grab_set()
        welcome_window.resizable(True, True)
        
        # Welcome title
        welcome_label = tk.Label(
            welcome_window,
            text="Welcome to Sudoku",
            font=("Helvetica", 18, "bold")
        )
        welcome_label.pack(pady=20)
        
        # Instructions
        instructions_frame = tk.Frame(welcome_window, padx=20)
        instructions_frame.pack(fill=tk.BOTH, expand=True)
        
        instructions = [
            "Sudoku is a logic-based number placement puzzle.",
            "The objective is to fill a 9×9 grid with digits so that",
            "each column, each row, and each of the nine 3×3 subgrids",
            "contain all of the digits from 1 to 9.",
            "",
            "How to play:",
            "1. Click on an empty cell to select it",
            "2. Click a number button (1-9) to place that number",
            "3. Click 'X' to erase a number",
            "4. Original numbers (in blue) cannot be modified",
            "",
            "Features:",
            "• Hint: Reveals a random cell with the correct number",
            "• Check Solution: Verifies if your solution is correct",
            "• Solve Puzzle: Shows the complete solution",
            "• New Game: Starts a new game with selected difficulty",
            "",
            "Difficulty levels affect how many numbers are initially revealed."
        ]
        
        for line in instructions:
            tk.Label(
                instructions_frame,
                text=line,
                justify=tk.LEFT
            ).pack(anchor=tk.W, pady=1)
        
        # Start button
        start_button = tk.Button(
            welcome_window,
            text="Start Game",
            font=("Helvetica", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            command=welcome_window.destroy
        )
        start_button.pack(pady=20)
    
    def change_difficulty(self):
        """Change the game difficulty."""
        new_difficulty = self.difficulty_var.get()
        if new_difficulty != self.difficulty:
            self.difficulty = new_difficulty
            self.difficulty_var.set(f"Difficulty: {self.difficulty.capitalize()}")
            
            # Ask if the user wants to start a new game
            if messagebox.askyesno("New Game", "Start a new game with the selected difficulty?"):
                self.new_game()
    
    def new_game(self):
        """Start a new game."""
        # Show loading message
        self.status_var.set("Generating puzzle...")
        self.root.update()
        
        # Create a new Sudoku game
        self.game = Sudoku(self.difficulty)
        
        # Update the board display
        self.update_board()
        
        # Clear selection
        self.selected_cell = None
        
        # Update status
        self.status_var.set("Select a cell to begin")
    
    def update_board(self):
        """Update the board display from the game state."""
        for i in range(9):
            for j in range(9):
                value = self.game.board[i][j]
                is_original = self.game.is_original(i, j)
                
                # Update cell properties
                self.cells[i][j].value = value
                self.cells[i][j].is_original = is_original
                
                # Update button appearance
                self.cells[i][j].button.config(
                    text="" if value == 0 else str(value),
                    font=("Helvetica", 14, "bold" if is_original else "normal"),
                    bg="#F0F0F0" if not is_original else "#E0E0E0",
                    fg="black" if not is_original else "blue",
                    relief=tk.RAISED if not is_original else tk.SUNKEN
                )
    
    def select_cell(self, row, col):
        """Select a cell in the grid."""
        # Unhighlight previously selected cell
        if self.selected_cell:
            prev_row, prev_col = self.selected_cell
            self.cells[prev_row][prev_col].highlight(False)
        
        # Highlight the new selected cell
        self.cells[row][col].highlight(True)
        
        # Update selected cell
        self.selected_cell = (row, col)
        
        # Update status
        self.status_var.set(f"Selected cell: ({row+1}, {col+1})")
    
    def place_number(self, num):
        """Place a number in the selected cell."""
        if not self.selected_cell:
            self.status_var.set("Please select a cell first")
            return
        
        row, col = self.selected_cell
        
        # Try to place the number
        success, message = self.game.place_number(row, col, num)
        
        if success:
            # Update the cell display
            self.cells[row][col].update_value(num)
            
            # Check if the puzzle is complete
            if self.game.is_complete():
                messagebox.showinfo("Congratulations", "You solved the puzzle!")
                self.status_var.set("Puzzle solved!")
            else:
                self.status_var.set(message)
        else:
            self.status_var.set(message)
    
    def get_hint(self):
        """Get a hint by revealing a random cell."""
        success, result = self.game.get_hint()
        
        if success:
            row, col, value = result
            
            # Update the cell display
            self.cells[row][col].update_value(value)
            
            # Flash the cell to highlight it
            self.flash_cell(row, col)
            
            # Update status
            self.status_var.set(f"Hint: {value} at position ({row+1}, {col+1})")
            
            # Check if the puzzle is complete
            if self.game.is_complete():
                messagebox.showinfo("Congratulations", "You solved the puzzle!")
                self.status_var.set("Puzzle solved!")
        else:
            self.status_var.set(result)
    
    def flash_cell(self, row, col):
        """Flash a cell to highlight it."""
        cell = self.cells[row][col]
        
        # Flash sequence: highlight -> normal -> highlight -> normal
        cell.highlight(True)
        self.root.after(200, lambda: cell.highlight(False))
        self.root.after(400, lambda: cell.highlight(True))
        self.root.after(600, lambda: cell.highlight(False))
    
    def check_solution(self):
        """Check if the current board state is a valid solution."""
        if self.game.is_complete():
            messagebox.showinfo("Correct", "Congratulations! Your solution is correct.")
            self.status_var.set("Puzzle solved!")
        else:
            messagebox.showinfo("Incomplete", "The puzzle is not complete or has errors.")
            self.status_var.set("Puzzle incomplete or has errors")
    
    def solve_puzzle(self):
        """Show the solution to the puzzle."""
        if messagebox.askyesno("Solve Puzzle", "Are you sure you want to see the solution?"):
            # Update the board with the solution
            self.game.board = copy.deepcopy(self.game.solution)
            
            # Update the display
            self.update_board()
            
            # Update status
            self.status_var.set("Puzzle solved")
    
    def quit_game(self):
        """Quit the game."""
        if messagebox.askyesno("Quit", "Are you sure you want to quit the game?"):
            self.root.destroy()

def main():
    """Main function to start the GUI game."""
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 