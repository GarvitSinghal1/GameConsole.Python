#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox, Label, Button, Frame, StringVar, IntVar, Radiobutton
import random
import time
import sys
import os

class MinesweeperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")
        self.root.geometry("800x650")
        self.root.configure(bg="#333333")
        self.root.resizable(True, True)
        
        # Game parameters
        self.difficulty = "medium"  # Default difficulty
        self.rows = 16
        self.cols = 16
        self.num_mines = 40
        
        # Colors
        self.colors = {
            "background": "#333333",
            "cell_bg": "#666666",
            "revealed_bg": "#999999",
            "text": "#FFFFFF",
            "mine": "#FF0000",
            "flag": "#FF9900",
            "numbers": ["#0000FF", "#008000", "#FF0000", "#000080", 
                        "#800000", "#008080", "#000000", "#808080"]
        }
        
        # Game state
        self.board = []  # Will hold cell values (mines, numbers)
        self.buttons = []  # Will hold Button widgets
        self.revealed = []  # Cells that have been revealed
        self.flagged = []  # Cells that have been flagged
        self.game_over = False
        self.first_click = True
        
        # Create widgets
        self.create_widgets()
        
        # Show welcome screen
        self.show_welcome()
    
    def create_widgets(self):
        """Create the GUI widgets."""
        # Main frame
        self.main_frame = Frame(self.root, bg=self.colors["background"])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title label
        self.title_label = Label(
            self.main_frame,
            text="Minesweeper",
            font=("Helvetica", 24, "bold"),
            bg=self.colors["background"],
            fg=self.colors["text"]
        )
        self.title_label.pack(pady=(0, 10))
        
        # Game info frame
        self.info_frame = Frame(self.main_frame, bg=self.colors["background"])
        self.info_frame.pack(fill=tk.X, pady=5)
        
        # Mines counter
        self.mines_var = StringVar(value=f"Mines: {self.num_mines}")
        self.mines_label = Label(
            self.info_frame,
            textvariable=self.mines_var,
            font=("Helvetica", 12),
            bg=self.colors["background"],
            fg=self.colors["text"]
        )
        self.mines_label.pack(side=tk.LEFT, padx=10)
        
        # Flags counter
        self.flags_var = StringVar(value="Flags: 0")
        self.flags_label = Label(
            self.info_frame,
            textvariable=self.flags_var,
            font=("Helvetica", 12),
            bg=self.colors["background"],
            fg=self.colors["text"]
        )
        self.flags_label.pack(side=tk.RIGHT, padx=10)
        
        # Game board frame with scrollbars
        self.board_container = Frame(self.main_frame, bg=self.colors["background"])
        self.board_container.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Add scrollbars
        self.h_scrollbar = tk.Scrollbar(self.board_container, orient=tk.HORIZONTAL)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.v_scrollbar = tk.Scrollbar(self.board_container)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Canvas for scrollable board
        self.canvas = tk.Canvas(
            self.board_container,
            bg=self.colors["background"],
            xscrollcommand=self.h_scrollbar.set,
            yscrollcommand=self.v_scrollbar.set
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure scrollbars
        self.h_scrollbar.config(command=self.canvas.xview)
        self.v_scrollbar.config(command=self.canvas.yview)
        
        # Frame inside canvas for the board
        self.board_frame = Frame(self.canvas, bg=self.colors["background"])
        self.canvas.create_window((0, 0), window=self.board_frame, anchor=tk.NW)
        
        # Difficulty selection frame
        self.difficulty_frame = Frame(self.main_frame, bg=self.colors["background"])
        self.difficulty_frame.pack(fill=tk.X, pady=10)
        
        # Difficulty label
        self.difficulty_label = Label(
            self.difficulty_frame,
            text="Difficulty:",
            font=("Helvetica", 12),
            bg=self.colors["background"],
            fg=self.colors["text"]
        )
        self.difficulty_label.pack(side=tk.LEFT, padx=10)
        
        # Difficulty radio buttons
        self.difficulty_var = StringVar(value=self.difficulty)
        
        self.easy_radio = Radiobutton(
            self.difficulty_frame,
            text="Easy",
            variable=self.difficulty_var,
            value="easy",
            command=self.change_difficulty,
            bg=self.colors["background"],
            fg=self.colors["text"],
            selectcolor="#444444",
            activebackground=self.colors["background"],
            activeforeground=self.colors["text"]
        )
        self.easy_radio.pack(side=tk.LEFT, padx=5)
        
        self.medium_radio = Radiobutton(
            self.difficulty_frame,
            text="Medium",
            variable=self.difficulty_var,
            value="medium",
            command=self.change_difficulty,
            bg=self.colors["background"],
            fg=self.colors["text"],
            selectcolor="#444444",
            activebackground=self.colors["background"],
            activeforeground=self.colors["text"]
        )
        self.medium_radio.pack(side=tk.LEFT, padx=5)
        
        self.hard_radio = Radiobutton(
            self.difficulty_frame,
            text="Hard",
            variable=self.difficulty_var,
            value="hard",
            command=self.change_difficulty,
            bg=self.colors["background"],
            fg=self.colors["text"],
            selectcolor="#444444",
            activebackground=self.colors["background"],
            activeforeground=self.colors["text"]
        )
        self.hard_radio.pack(side=tk.LEFT, padx=5)
        
        # Control buttons at the bottom
        self.control_frame = Frame(self.main_frame, bg=self.colors["background"])
        self.control_frame.pack(fill=tk.X, pady=10)
        
        # New Game button
        self.new_game_button = Button(
            self.control_frame,
            text="New Game",
            font=("Helvetica", 12),
            bg="#4CAF50",
            fg="white",
            command=self.new_game
        )
        self.new_game_button.pack(side=tk.LEFT, padx=10)
        
        # Quit button
        self.quit_button = Button(
            self.control_frame,
            text="Quit",
            font=("Helvetica", 12),
            bg="#F44336",
            fg="white",
            command=self.quit_game
        )
        self.quit_button.pack(side=tk.RIGHT, padx=10)
        
        # Initialize the game board
        self.initialize_board()
    
    def show_welcome(self):
        """Show welcome screen and instructions."""
        welcome_window = tk.Toplevel(self.root)
        welcome_window.title("Welcome to Minesweeper")
        welcome_window.geometry("500x400")
        welcome_window.configure(bg=self.colors["background"])
        welcome_window.transient(self.root)
        welcome_window.grab_set()
        welcome_window.resizable(True, True)
        
        # Welcome title
        welcome_label = Label(
            welcome_window,
            text="Welcome to Minesweeper",
            font=("Helvetica", 18, "bold"),
            bg=self.colors["background"],
            fg=self.colors["text"]
        )
        welcome_label.pack(pady=20)
        
        # Instructions
        instructions_frame = Frame(welcome_window, bg=self.colors["background"], padx=20)
        instructions_frame.pack(fill=tk.BOTH, expand=True)
        
        instructions = [
            "Minesweeper is a puzzle game where you need to clear a",
            "board containing hidden mines without detonating any of them.",
            "",
            "• Left-click on a cell to reveal it",
            "• Right-click on a cell to flag it as a potential mine",
            "• Numbers indicate how many mines are adjacent to that cell",
            "• Use logic to deduce where mines are located",
            "",
            "Difficulty levels:",
            "• Easy: 9x9 grid with 10 mines",
            "• Medium: 16x16 grid with 40 mines",
            "• Hard: 16x30 grid with 99 mines",
            "",
            "Your first click is always safe!"
        ]
        
        for line in instructions:
            Label(
                instructions_frame,
                text=line,
                font=("Helvetica", 12),
                bg=self.colors["background"],
                fg=self.colors["text"],
                justify=tk.LEFT
            ).pack(anchor=tk.W, pady=1)
        
        # Start button
        start_button = Button(
            welcome_window,
            text="Start Game",
            font=("Helvetica", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            command=welcome_window.destroy
        )
        start_button.pack(pady=20)
    
    def change_difficulty(self):
        """Change the game difficulty and restart."""
        self.difficulty = self.difficulty_var.get()
        self.new_game()
    
    def initialize_board(self):
        """Initialize the game board with the selected difficulty."""
        # Set board dimensions and number of mines based on difficulty
        if self.difficulty == "easy":
            self.rows, self.cols, self.num_mines = 9, 9, 10
        elif self.difficulty == "medium":
            self.rows, self.cols, self.num_mines = 16, 16, 40
        else:  # hard
            self.rows, self.cols, self.num_mines = 16, 30, 99
        
        # Update mines counter
        self.mines_var.set(f"Mines: {self.num_mines}")
        self.flags_var.set("Flags: 0")
        
        # Clear existing board
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        
        # Reset game state
        self.board = [['0' for _ in range(self.cols)] for _ in range(self.rows)]
        self.buttons = []
        self.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.flagged = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.game_over = False
        self.first_click = True
        
        # Create buttons for each cell
        for row in range(self.rows):
            button_row = []
            for col in range(self.cols):
                button = Button(
                    self.board_frame,
                    width=2,
                    height=1,
                    bg=self.colors["cell_bg"],
                    relief=tk.RAISED,
                    borderwidth=2
                )
                button.grid(row=row, column=col, padx=1, pady=1)
                button.bind("<Button-1>", lambda event, r=row, c=col: self.left_click(r, c))
                button.bind("<Button-3>", lambda event, r=row, c=col: self.right_click(r, c))
                button_row.append(button)
            self.buttons.append(button_row)
        
        # Update canvas scroll region
        self.board_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
    
    def place_mines(self, first_row, first_col):
        """Place mines randomly on the board, avoiding the first clicked cell."""
        mines_placed = 0
        while mines_placed < self.num_mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            
            # Avoid placing mines at or around the first click
            if abs(row - first_row) <= 1 and abs(col - first_col) <= 1:
                continue
            
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
    
    def left_click(self, row, col):
        """Handle left click on a cell (reveal)."""
        if self.game_over or self.flagged[row][col]:
            return
        
        # First click is always safe
        if self.first_click:
            self.place_mines(row, col)
            self.calculate_numbers()
            self.first_click = False
        
        self.reveal_cell(row, col)
        
        # Check if game is over
        if self.check_win():
            self.game_over = True
            self.show_all_mines()
            messagebox.showinfo("Congratulations", "You found all the mines!")
    
    def right_click(self, event, row, col):
        """Handle right click on a cell (flag)."""
        if self.game_over or self.revealed[row][col]:
            return
        
        # Toggle flag
        self.flagged[row][col] = not self.flagged[row][col]
        
        if self.flagged[row][col]:
            self.buttons[row][col].config(text="🚩", fg=self.colors["flag"])
        else:
            self.buttons[row][col].config(text="")
        
        # Update flag counter
        flag_count = sum(sum(row) for row in self.flagged)
        self.flags_var.set(f"Flags: {flag_count}")
        
        # Check if game is won
        if self.check_win():
            self.game_over = True
            self.show_all_mines()
            messagebox.showinfo("Congratulations", "You found all the mines!")
    
    def reveal_cell(self, row, col):
        """Reveal a cell and its adjacent cells if it's empty."""
        if not self.is_valid_cell(row, col) or self.revealed[row][col] or self.flagged[row][col]:
            return
        
        # Reveal the cell
        self.revealed[row][col] = True
        
        # Update button appearance
        button = self.buttons[row][col]
        button.config(relief=tk.SUNKEN, bg=self.colors["revealed_bg"])
        
        # If it's a mine, game over
        if self.board[row][col] == 'M':
            button.config(text="💣", fg=self.colors["mine"])
            self.game_over = True
            self.show_all_mines()
            messagebox.showinfo("Game Over", "You hit a mine!")
            return
        
        # If it's a number, show it
        if self.board[row][col] != '0':
            number = int(self.board[row][col])
            color_idx = min(number - 1, len(self.colors["numbers"]) - 1)
            button.config(text=str(number), fg=self.colors["numbers"][color_idx])
        
        # If it's an empty cell, reveal adjacent cells recursively
        if self.board[row][col] == '0':
            for r in range(max(0, row-1), min(self.rows, row+2)):
                for c in range(max(0, col-1), min(self.cols, col+2)):
                    if (r, c) != (row, col):
                        self.reveal_cell(r, c)
    
    def is_valid_cell(self, row, col):
        """Check if a cell is within the board boundaries."""
        return 0 <= row < self.rows and 0 <= col < self.cols
    
    def check_win(self):
        """Check if the player has won."""
        for row in range(self.rows):
            for col in range(self.cols):
                # If a non-mine cell is still hidden, game is not won
                if self.board[row][col] != 'M' and not self.revealed[row][col]:
                    return False
                
                # If a mine is not flagged, game is not won
                if self.board[row][col] == 'M' and not self.flagged[row][col]:
                    return False
        
        return True
    
    def show_all_mines(self):
        """Reveal all mines on the board."""
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == 'M':
                    if not self.flagged[row][col]:
                        # Show unflagged mines
                        self.buttons[row][col].config(text="💣", fg=self.colors["mine"])
                elif self.flagged[row][col]:
                    # Show incorrectly flagged cells
                    self.buttons[row][col].config(text="❌", fg=self.colors["mine"])
    
    def new_game(self):
        """Start a new game with the current difficulty."""
        self.initialize_board()
    
    def quit_game(self):
        """Quit the game."""
        if messagebox.askyesno("Quit", "Are you sure you want to quit the game?"):
            self.root.destroy()

def main():
    """Main function to start the GUI game."""
    root = tk.Tk()
    app = MinesweeperGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 