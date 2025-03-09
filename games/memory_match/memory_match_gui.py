#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox, Label, Button, Frame
import random
import time
import sys
import os
from PIL import Image, ImageTk

# Import card symbols from terminal version if possible
try:
    from games.memory_match import CARD_SYMBOLS
except ImportError:
    # Fallback symbols if import fails
    CARD_SYMBOLS = {
        "easy": ['♥', '♦', '♠', '♣', '★', '●', '■', '▲'],
        "medium": ['♥', '♦', '♠', '♣', '★', '●', '■', '▲', '◆', '□', '△', '○'],
        "hard": ['♥', '♦', '♠', '♣', '★', '●', '■', '▲', '◆', '□', '△', '○', '♪', '♫', '☼', '☀', '☁', '☂']
    }

class MemoryMatchGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Match")
        self.root.geometry("800x650")
        self.root.configure(bg="#34495e")
        self.root.resizable(True, True)
        
        # Game parameters
        self.difficulty = "medium"  # Default difficulty
        self.symbols = CARD_SYMBOLS[self.difficulty]
        self.num_pairs = len(self.symbols)
        self.rows = 4
        self.cols = 6  # Default grid size for medium difficulty
        
        # Colors
        self.colors = {
            "background": "#34495e",
            "card_back": "#2c3e50",
            "card_face": "#3498db",
            "text": "#ecf0f1",
            "matched": "#2ecc71"
        }
        
        # Game state
        self.card_symbols = []
        self.cards = []  # Will hold Button widgets
        self.card_values = []  # Will hold symbol values
        self.revealed = []  # Cards currently face up
        self.matched_pairs = []  # Pairs that have been matched
        self.moves = 0
        self.matches = 0
        self.first_card = None
        self.can_click = True
        
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
            text="Memory Match",
            font=("Helvetica", 24, "bold"),
            bg=self.colors["background"],
            fg=self.colors["text"]
        )
        self.title_label.pack(pady=(0, 10))
        
        # Game info frame
        self.info_frame = Frame(self.main_frame, bg=self.colors["background"])
        self.info_frame.pack(fill=tk.X, pady=5)
        
        # Moves counter
        self.moves_var = tk.StringVar(value="Moves: 0")
        self.moves_label = Label(
            self.info_frame,
            textvariable=self.moves_var,
            font=("Helvetica", 12),
            bg=self.colors["background"],
            fg=self.colors["text"]
        )
        self.moves_label.pack(side=tk.LEFT, padx=10)
        
        # Matches counter
        self.matches_var = tk.StringVar(value=f"Matches: 0/{self.num_pairs}")
        self.matches_label = Label(
            self.info_frame,
            textvariable=self.matches_var,
            font=("Helvetica", 12),
            bg=self.colors["background"],
            fg=self.colors["text"]
        )
        self.matches_label.pack(side=tk.RIGHT, padx=10)
        
        # Game board frame
        self.board_frame = Frame(self.main_frame, bg=self.colors["background"])
        self.board_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
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
        
        # Easy button
        self.easy_button = Button(
            self.difficulty_frame,
            text="Easy",
            font=("Helvetica", 10),
            bg="#3498db",
            fg=self.colors["text"],
            command=lambda: self.set_difficulty("easy")
        )
        self.easy_button.pack(side=tk.LEFT, padx=5)
        
        # Medium button
        self.medium_button = Button(
            self.difficulty_frame,
            text="Medium",
            font=("Helvetica", 10),
            bg="#9b59b6",
            fg=self.colors["text"],
            command=lambda: self.set_difficulty("medium")
        )
        self.medium_button.pack(side=tk.LEFT, padx=5)
        
        # Hard button
        self.hard_button = Button(
            self.difficulty_frame,
            text="Hard",
            font=("Helvetica", 10),
            bg="#e74c3c",
            fg=self.colors["text"],
            command=lambda: self.set_difficulty("hard")
        )
        self.hard_button.pack(side=tk.LEFT, padx=5)
        
        # Control buttons at the bottom
        self.control_frame = Frame(self.main_frame, bg=self.colors["background"])
        self.control_frame.pack(fill=tk.X, pady=10)
        
        # New Game button
        self.new_game_button = Button(
            self.control_frame,
            text="New Game",
            font=("Helvetica", 12),
            bg="#2ecc71",
            fg=self.colors["text"],
            command=self.new_game
        )
        self.new_game_button.pack(side=tk.LEFT, padx=10)
        
        # Quit button
        self.quit_button = Button(
            self.control_frame,
            text="Quit",
            font=("Helvetica", 12),
            bg="#e74c3c",
            fg=self.colors["text"],
            command=self.quit_game
        )
        self.quit_button.pack(side=tk.RIGHT, padx=10)
        
        # Initialize the game board
        self.initialize_board()
    
    def show_welcome(self):
        """Show welcome screen and instructions."""
        welcome_window = tk.Toplevel(self.root)
        welcome_window.title("Welcome to Memory Match")
        welcome_window.geometry("500x400")
        welcome_window.configure(bg=self.colors["background"])
        welcome_window.transient(self.root)
        welcome_window.grab_set()
        welcome_window.resizable(True, True)
        
        # Welcome title
        welcome_label = Label(
            welcome_window,
            text="Welcome to Memory Match",
            font=("Helvetica", 18, "bold"),
            bg=self.colors["background"],
            fg=self.colors["text"]
        )
        welcome_label.pack(pady=20)
        
        # Instructions
        instructions_frame = Frame(welcome_window, bg=self.colors["background"], padx=20)
        instructions_frame.pack(fill=tk.BOTH, expand=True)
        
        instructions = [
            "Memory Match is a card-matching game where you need",
            "to find all matching pairs of symbols.",
            "",
            "• Click on any card to reveal its symbol",
            "• Then click on another card to find its match",
            "• If the two cards match, they remain face up",
            "• If they don't match, they'll flip back over",
            "• The game is complete when all pairs are found",
            "",
            "Choose your difficulty level:",
            "• Easy: 4x4 grid (8 pairs)",
            "• Medium: 4x6 grid (12 pairs)",
            "• Hard: 6x6 grid (18 pairs)",
            "",
            "Try to complete the game in as few moves as possible!"
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
            bg="#2ecc71",
            fg=self.colors["text"],
            command=welcome_window.destroy
        )
        start_button.pack(pady=20)
    
    def initialize_board(self):
        """Initialize the game board with the selected difficulty."""
        # Clear existing cards
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        
        # Set grid dimensions based on difficulty
        if self.difficulty == "easy":
            self.rows, self.cols = 4, 4
        elif self.difficulty == "medium":
            self.rows, self.cols = 4, 6
        else:  # hard
            self.rows, self.cols = 6, 6
        
        # Reset game state
        self.symbols = CARD_SYMBOLS[self.difficulty]
        self.num_pairs = len(self.symbols)
        self.matches_var.set(f"Matches: 0/{self.num_pairs}")
        self.moves = 0
        self.moves_var.set("Moves: 0")
        self.matches = 0
        self.first_card = None
        self.can_click = True
        self.cards = []
        self.card_values = []
        self.revealed = []
        self.matched_pairs = []
        
        # Create the deck with pairs of symbols
        self.card_symbols = self.symbols * 2
        random.shuffle(self.card_symbols)
        
        # Calculate card dimensions
        card_width = min(90, 700 // self.cols)
        card_height = min(90, 500 // self.rows)
        
        # Create card grid
        for i in range(self.rows):
            row_frame = Frame(self.board_frame, bg=self.colors["background"])
            row_frame.pack(pady=2)
            row_cards = []
            row_values = []
            
            for j in range(self.cols):
                idx = i * self.cols + j
                if idx < len(self.card_symbols):
                    symbol = self.card_symbols[idx]
                    
                    # Create card button
                    card = Button(
                        row_frame,
                        text="?",
                        font=("Helvetica", 16, "bold"),
                        width=3,
                        height=1,
                        bg=self.colors["card_back"],
                        fg=self.colors["text"],
                        relief=tk.RAISED,
                        bd=3,
                        command=lambda row=i, col=j: self.card_click(row, col)
                    )
                    card.grid(row=0, column=j, padx=2, pady=2)
                    row_cards.append(card)
                    row_values.append(symbol)
                else:
                    # For odd-sized grids, fill with empty frames
                    empty = Frame(
                        row_frame,
                        width=card_width,
                        height=card_height,
                        bg=self.colors["background"]
                    )
                    empty.grid(row=0, column=j, padx=2, pady=2)
                    row_cards.append(None)
                    row_values.append(None)
                    
            self.cards.append(row_cards)
            self.card_values.append(row_values)
    
    def set_difficulty(self, difficulty):
        """Set the game difficulty and restart."""
        self.difficulty = difficulty
        self.new_game()
    
    def card_click(self, row, col):
        """Handle card click events."""
        # Ignore clicks if the game is waiting or card is already revealed/matched
        if not self.can_click or (row, col) in self.revealed or (row, col) in self.matched_pairs:
            return
        
        # Get the card value and update display
        card = self.cards[row][col]
        value = self.card_values[row][col]
        self.flip_card(card, value)
        self.revealed.append((row, col))
        
        # First card of the pair
        if self.first_card is None:
            self.first_card = (row, col)
            return
        
        # Second card of the pair
        self.moves += 1
        self.moves_var.set(f"Moves: {self.moves}")
        
        first_row, first_col = self.first_card
        first_value = self.card_values[first_row][first_col]
        
        # Check for match
        if value == first_value:
            # Match found
            self.matched_pairs.append((first_row, first_col))
            self.matched_pairs.append((row, col))
            self.revealed = []
            self.first_card = None
            self.matches += 1
            self.matches_var.set(f"Matches: {self.matches}/{self.num_pairs}")
            
            # Update card appearance for matched pairs
            self.cards[first_row][first_col].config(bg=self.colors["matched"])
            card.config(bg=self.colors["matched"])
            
            # Check if game is over
            if self.matches == self.num_pairs:
                self.game_over()
        else:
            # No match, flip cards back after a delay
            self.can_click = False
            self.root.after(1000, lambda: self.flip_back(first_row, first_col, row, col))
    
    def flip_card(self, card, value):
        """Flip a card to show its value."""
        card.config(text=value, bg=self.colors["card_face"])
    
    def flip_back(self, row1, col1, row2, col2):
        """Flip two cards back to hidden state."""
        self.cards[row1][col1].config(text="?", bg=self.colors["card_back"])
        self.cards[row2][col2].config(text="?", bg=self.colors["card_back"])
        self.revealed = []
        self.first_card = None
        self.can_click = True
    
    def game_over(self):
        """Show game over message and statistics."""
        # Calculate performance rating
        perfect_score = self.num_pairs
        if self.moves <= perfect_score * 2:
            rating = "Perfect Memory! Incredible performance!"
        elif self.moves <= perfect_score * 3:
            rating = "Excellent! You have a great memory!"
        elif self.moves <= perfect_score * 4:
            rating = "Very good! You have a good memory!"
        else:
            rating = "Good job! Keep practicing to improve your memory!"
        
        messagebox.showinfo(
            "Game Complete",
            f"Congratulations! You found all {self.num_pairs} pairs in {self.moves} moves!\n\n{rating}"
        )
    
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
    app = MemoryMatchGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 