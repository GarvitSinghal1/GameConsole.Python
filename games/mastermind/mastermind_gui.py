#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox, Label, Button, Frame, StringVar, Radiobutton
import random
import sys
import os

# Import color definitions from terminal version if possible
try:
    from games.mastermind import COLORS
except ImportError:
    # Fallback colors if import fails
    COLORS = {
        'R': ("#FF0000", "Red"),
        'G': ("#00FF00", "Green"),
        'B': ("#0000FF", "Blue"),
        'Y': ("#FFFF00", "Yellow"),
        'M': ("#FF00FF", "Magenta"),
        'C': ("#00FFFF", "Cyan"),
        'W': ("#FFFFFF", "White")
    }

class MastermindGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mastermind")
        self.root.geometry("700x650")
        self.root.configure(bg="#333333")
        self.root.resizable(True, True)
        
        # Game parameters
        self.difficulty = "medium"  # Default difficulty
        self.code_length = 5
        self.max_attempts = 10
        self.allow_duplicates = True
        
        # Colors for GUI
        self.gui_colors = {
            'R': ("#FF0000", "Red"),
            'G': ("#00FF00", "Green"),
            'B': ("#0000FF", "Blue"),
            'Y': ("#FFFF00", "Yellow"),
            'M': ("#FF00FF", "Magenta"),
            'C': ("#00FFFF", "Cyan"),
            'W': ("#FFFFFF", "White")
        }
        
        # Game state
        self.available_colors = list(self.gui_colors.keys())
        self.secret_code = []
        self.attempts = []
        self.feedbacks = []
        self.current_attempt = 0
        self.current_position = 0
        self.game_over = False
        self.win = False
        
        # UI elements
        self.peg_buttons = []
        self.guess_frames = []
        self.feedback_frames = []
        self.selected_color = StringVar(value='R')  # Default selected color
        
        # Create widgets
        self.create_widgets()
        
        # Show welcome screen
        self.show_welcome()
        
        # Initialize the game
        self.new_game()
    
    def create_widgets(self):
        """Create the GUI widgets."""
        # Main frame
        self.main_frame = Frame(self.root, bg="#333333")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title label
        self.title_label = Label(
            self.main_frame,
            text="Mastermind",
            font=("Helvetica", 24, "bold"),
            bg="#333333",
            fg="#FFFFFF"
        )
        self.title_label.pack(pady=(0, 10))
        
        # Game info frame
        self.info_frame = Frame(self.main_frame, bg="#333333")
        self.info_frame.pack(fill=tk.X, pady=5)
        
        # Attempts counter
        self.attempts_var = StringVar(value="Attempts: 0/10")
        self.attempts_label = Label(
            self.info_frame,
            textvariable=self.attempts_var,
            font=("Helvetica", 12),
            bg="#333333",
            fg="#FFFFFF"
        )
        self.attempts_label.pack(side=tk.LEFT, padx=10)
        
        # Difficulty label
        self.difficulty_var = StringVar(value="Difficulty: Medium")
        self.difficulty_label = Label(
            self.info_frame,
            textvariable=self.difficulty_var,
            font=("Helvetica", 12),
            bg="#333333",
            fg="#FFFFFF"
        )
        self.difficulty_label.pack(side=tk.RIGHT, padx=10)
        
        # Game board frame
        self.board_frame = Frame(self.main_frame, bg="#333333")
        self.board_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Secret code frame (at the top)
        self.secret_frame = Frame(self.board_frame, bg="#333333")
        self.secret_frame.pack(pady=10)
        
        # Secret code label
        self.secret_label = Label(
            self.secret_frame,
            text="Secret Code:",
            font=("Helvetica", 12),
            bg="#333333",
            fg="#FFFFFF"
        )
        self.secret_label.pack(side=tk.LEFT, padx=10)
        
        # Secret code pegs
        self.secret_pegs = []
        self.secret_pegs_frame = Frame(self.secret_frame, bg="#333333")
        self.secret_pegs_frame.pack(side=tk.LEFT)
        
        for i in range(self.code_length):
            peg = Label(
                self.secret_pegs_frame,
                text="?",
                font=("Helvetica", 16, "bold"),
                width=2,
                height=1,
                bg="#666666",
                fg="#FFFFFF",
                relief=tk.RAISED,
                borderwidth=2
            )
            peg.grid(row=0, column=i, padx=2, pady=2)
            self.secret_pegs.append(peg)
        
        # Attempts frame (scrollable)
        self.attempts_canvas = tk.Canvas(self.board_frame, bg="#333333", highlightthickness=0)
        self.attempts_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.attempts_scrollbar = tk.Scrollbar(self.board_frame, orient=tk.VERTICAL, command=self.attempts_canvas.yview)
        self.attempts_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.attempts_canvas.configure(yscrollcommand=self.attempts_scrollbar.set)
        
        self.attempts_frame = Frame(self.attempts_canvas, bg="#333333")
        self.attempts_canvas.create_window((0, 0), window=self.attempts_frame, anchor=tk.NW)
        
        # Color selection frame
        self.color_frame = Frame(self.main_frame, bg="#333333")
        self.color_frame.pack(fill=tk.X, pady=10)
        
        # Color selection label
        self.color_label = Label(
            self.color_frame,
            text="Select Color:",
            font=("Helvetica", 12),
            bg="#333333",
            fg="#FFFFFF"
        )
        self.color_label.pack(side=tk.LEFT, padx=10)
        
        # Color radio buttons
        for color_code, (color_hex, color_name) in self.gui_colors.items():
            color_radio = Radiobutton(
                self.color_frame,
                text="",
                variable=self.selected_color,
                value=color_code,
                bg="#333333",
                selectcolor="#333333",
                indicatoron=0,
                width=2,
                height=1,
                borderwidth=3,
                relief=tk.RAISED
            )
            color_radio.config(bg=color_hex, activebackground=color_hex)
            color_radio.pack(side=tk.LEFT, padx=5)
        
        # Current guess frame
        self.current_guess_frame = Frame(self.main_frame, bg="#333333")
        self.current_guess_frame.pack(fill=tk.X, pady=10)
        
        # Current guess label
        self.current_guess_label = Label(
            self.current_guess_frame,
            text="Current Guess:",
            font=("Helvetica", 12),
            bg="#333333",
            fg="#FFFFFF"
        )
        self.current_guess_label.pack(side=tk.LEFT, padx=10)
        
        # Current guess pegs
        self.current_pegs_frame = Frame(self.current_guess_frame, bg="#333333")
        self.current_pegs_frame.pack(side=tk.LEFT)
        
        self.current_pegs = []
        for i in range(self.code_length):
            peg = Button(
                self.current_pegs_frame,
                text="",
                font=("Helvetica", 12),
                width=2,
                height=1,
                bg="#666666",
                relief=tk.RAISED,
                borderwidth=2,
                command=lambda pos=i: self.set_peg(pos)
            )
            peg.grid(row=0, column=i, padx=2, pady=2)
            self.current_pegs.append(peg)
        
        # Submit button
        self.submit_button = Button(
            self.current_guess_frame,
            text="Submit",
            font=("Helvetica", 12),
            bg="#4CAF50",
            fg="white",
            command=self.submit_guess
        )
        self.submit_button.pack(side=tk.LEFT, padx=20)
        
        # Difficulty selection frame
        self.difficulty_frame = Frame(self.main_frame, bg="#333333")
        self.difficulty_frame.pack(fill=tk.X, pady=10)
        
        # Difficulty selection label
        self.difficulty_select_label = Label(
            self.difficulty_frame,
            text="Difficulty:",
            font=("Helvetica", 12),
            bg="#333333",
            fg="#FFFFFF"
        )
        self.difficulty_select_label.pack(side=tk.LEFT, padx=10)
        
        # Difficulty radio buttons
        self.difficulty_var = StringVar(value=self.difficulty)
        
        self.easy_radio = Radiobutton(
            self.difficulty_frame,
            text="Easy",
            variable=self.difficulty_var,
            value="easy",
            command=self.change_difficulty,
            bg="#333333",
            fg="#FFFFFF",
            selectcolor="#444444",
            activebackground="#333333",
            activeforeground="#FFFFFF"
        )
        self.easy_radio.pack(side=tk.LEFT, padx=5)
        
        self.medium_radio = Radiobutton(
            self.difficulty_frame,
            text="Medium",
            variable=self.difficulty_var,
            value="medium",
            command=self.change_difficulty,
            bg="#333333",
            fg="#FFFFFF",
            selectcolor="#444444",
            activebackground="#333333",
            activeforeground="#FFFFFF"
        )
        self.medium_radio.pack(side=tk.LEFT, padx=5)
        
        self.hard_radio = Radiobutton(
            self.difficulty_frame,
            text="Hard",
            variable=self.difficulty_var,
            value="hard",
            command=self.change_difficulty,
            bg="#333333",
            fg="#FFFFFF",
            selectcolor="#444444",
            activebackground="#333333",
            activeforeground="#FFFFFF"
        )
        self.hard_radio.pack(side=tk.LEFT, padx=5)
        
        self.expert_radio = Radiobutton(
            self.difficulty_frame,
            text="Expert",
            variable=self.difficulty_var,
            value="expert",
            command=self.change_difficulty,
            bg="#333333",
            fg="#FFFFFF",
            selectcolor="#444444",
            activebackground="#333333",
            activeforeground="#FFFFFF"
        )
        self.expert_radio.pack(side=tk.LEFT, padx=5)
        
        # Control buttons at the bottom
        self.control_frame = Frame(self.main_frame, bg="#333333")
        self.control_frame.pack(fill=tk.X, pady=10)
        
        # New Game button
        self.new_game_button = Button(
            self.control_frame,
            text="New Game",
            font=("Helvetica", 12),
            bg="#2196F3",
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
        
        # Update canvas scroll region
        self.attempts_frame.update_idletasks()
        self.attempts_canvas.config(scrollregion=self.attempts_canvas.bbox("all"))
    
    def show_welcome(self):
        """Show welcome screen and instructions."""
        welcome_window = tk.Toplevel(self.root)
        welcome_window.title("Welcome to Mastermind")
        welcome_window.geometry("500x450")
        welcome_window.configure(bg="#333333")
        welcome_window.transient(self.root)
        welcome_window.grab_set()
        welcome_window.resizable(True, True)
        
        # Welcome title
        welcome_label = Label(
            welcome_window,
            text="Welcome to Mastermind",
            font=("Helvetica", 18, "bold"),
            bg="#333333",
            fg="#FFFFFF"
        )
        welcome_label.pack(pady=20)
        
        # Instructions
        instructions_frame = Frame(welcome_window, bg="#333333", padx=20)
        instructions_frame.pack(fill=tk.BOTH, expand=True)
        
        instructions = [
            "Mastermind is a code-breaking game where you need to",
            "guess a secret code of colored pegs.",
            "",
            "How to play:",
            "1. Select a color from the color palette",
            "2. Click on a position in your current guess to place the color",
            "3. Fill all positions and click Submit to make your guess",
            "4. Use the feedback to deduce the secret code:",
            "   • Black pegs: Correct color and position",
            "   • White pegs: Correct color but wrong position",
            "",
            "Difficulty levels:",
            "• Easy: 4 colors, 12 attempts, duplicates allowed",
            "• Medium: 5 colors, 10 attempts, duplicates allowed",
            "• Hard: 6 colors, 8 attempts, duplicates allowed",
            "• Expert: 6 colors, 8 attempts, no duplicates",
            "",
            "Try to crack the code in as few attempts as possible!"
        ]
        
        for line in instructions:
            Label(
                instructions_frame,
                text=line,
                font=("Helvetica", 12),
                bg="#333333",
                fg="#FFFFFF",
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
    
    def new_game(self):
        """Start a new game with the current difficulty."""
        # Set game parameters based on difficulty
        if self.difficulty == "easy":
            self.code_length = 4
            self.max_attempts = 12
            self.allow_duplicates = True
        elif self.difficulty == "medium":
            self.code_length = 5
            self.max_attempts = 10
            self.allow_duplicates = True
        elif self.difficulty == "hard":
            self.code_length = 6
            self.max_attempts = 8
            self.allow_duplicates = True
        else:  # expert
            self.code_length = 6
            self.max_attempts = 8
            self.allow_duplicates = False
        
        # Update difficulty label
        self.difficulty_var.set(f"Difficulty: {self.difficulty.capitalize()}")
        
        # Reset game state
        self.secret_code = self.generate_code()
        self.attempts = []
        self.feedbacks = []
        self.current_attempt = 0
        self.current_position = 0
        self.game_over = False
        self.win = False
        
        # Update attempts counter
        self.attempts_var.set(f"Attempts: {self.current_attempt}/{self.max_attempts}")
        
        # Clear secret code display
        # First, remove existing pegs
        for peg in self.secret_pegs:
            peg.destroy()
        
        # Create new secret pegs with the correct code_length
        self.secret_pegs = []
        for i in range(self.code_length):
            peg = Label(
                self.secret_pegs_frame,
                text="?",
                font=("Helvetica", 16, "bold"),
                width=2,
                height=1,
                bg="#666666",
                fg="#FFFFFF",
                relief=tk.RAISED,
                borderwidth=2
            )
            peg.grid(row=0, column=i, padx=2, pady=2)
            self.secret_pegs.append(peg)
        
        # Clear current guess and recreate with new code_length
        for peg in self.current_pegs:
            peg.destroy()
        
        self.current_pegs = []
        for i in range(self.code_length):
            peg = Button(
                self.current_pegs_frame,
                text="",
                font=("Helvetica", 12),
                width=2,
                height=1,
                bg="#666666",
                relief=tk.RAISED,
                borderwidth=2,
                command=lambda pos=i: self.set_peg(pos)
            )
            peg.grid(row=0, column=i, padx=2, pady=2)
            self.current_pegs.append(peg)
        
        # Clear attempts board
        for widget in self.attempts_frame.winfo_children():
            widget.destroy()
        
        # Create new attempt rows
        self.guess_frames = []
        self.feedback_frames = []
        
        for i in range(self.max_attempts):
            # Create row frame
            row_frame = Frame(self.attempts_frame, bg="#333333")
            row_frame.pack(fill=tk.X, pady=2)
            
            # Row number
            row_label = Label(
                row_frame,
                text=f"{i+1}.",
                font=("Helvetica", 12),
                width=3,
                bg="#333333",
                fg="#FFFFFF"
            )
            row_label.pack(side=tk.LEFT, padx=5)
            
            # Guess pegs frame
            guess_frame = Frame(row_frame, bg="#333333")
            guess_frame.pack(side=tk.LEFT, padx=10)
            
            # Create pegs for this row
            pegs = []
            for j in range(self.code_length):
                peg = Label(
                    guess_frame,
                    text="",
                    font=("Helvetica", 12),
                    width=2,
                    height=1,
                    bg="#666666",
                    relief=tk.RAISED,
                    borderwidth=2
                )
                peg.grid(row=0, column=j, padx=2, pady=2)
                pegs.append(peg)
            
            self.guess_frames.append(pegs)
            
            # Feedback pegs frame
            feedback_frame = Frame(row_frame, bg="#333333")
            feedback_frame.pack(side=tk.LEFT, padx=10)
            
            # Create feedback pegs (arranged in a grid)
            feedback_pegs = []
            for j in range(self.code_length):
                peg = Label(
                    feedback_frame,
                    text="",
                    font=("Helvetica", 8),
                    width=1,
                    height=1,
                    bg="#444444",
                    relief=tk.RAISED,
                    borderwidth=1
                )
                peg.grid(row=j//2, column=j%2, padx=1, pady=1)
                feedback_pegs.append(peg)
            
            self.feedback_frames.append(feedback_pegs)
        
        # Update canvas scroll region
        self.attempts_frame.update_idletasks()
        self.attempts_canvas.config(scrollregion=self.attempts_canvas.bbox("all"))
        
        # Enable submit button
        self.submit_button.config(state=tk.NORMAL)
    
    def generate_code(self):
        """Generate a random secret code."""
        if self.allow_duplicates:
            return [random.choice(self.available_colors) for _ in range(self.code_length)]
        else:
            # Ensure no duplicates
            return random.sample(self.available_colors, self.code_length)
    
    def set_peg(self, position):
        """Set a peg in the current guess to the selected color."""
        if self.game_over:
            return
        
        color_code = self.selected_color.get()
        color_hex, _ = self.gui_colors[color_code]
        
        # Update the peg
        self.current_pegs[position].config(text=color_code, bg=color_hex, fg="#000000")
        
        # Move to next position
        self.current_position = (position + 1) % self.code_length
    
    def submit_guess(self):
        """Submit the current guess."""
        if self.game_over:
            return
        
        # Get the current guess
        guess = []
        for peg in self.current_pegs:
            color_code = peg.cget("text")
            if not color_code:
                messagebox.showinfo("Incomplete Guess", "Please fill all positions in your guess.")
                return
            guess.append(color_code)
        
        # Evaluate the guess
        feedback = self.evaluate_guess(guess)
        
        # Update game state
        self.attempts.append(guess)
        self.feedbacks.append(feedback)
        self.current_attempt += 1
        
        # Update attempts counter
        self.attempts_var.set(f"Attempts: {self.current_attempt}/{self.max_attempts}")
        
        # Update the board
        self.update_board()
        
        # Clear current guess
        for peg in self.current_pegs:
            peg.config(text="", bg="#666666")
        
        # Check if the player has won
        if feedback[0] == self.code_length:
            self.win = True
            self.game_over = True
            self.reveal_secret_code()
            messagebox.showinfo("Congratulations", f"You cracked the code in {self.current_attempt} attempts!")
            self.submit_button.config(state=tk.DISABLED)
            return
        
        # Check if the player has lost
        if self.current_attempt >= self.max_attempts:
            self.game_over = True
            self.reveal_secret_code()
            messagebox.showinfo("Game Over", "You failed to crack the code.")
            self.submit_button.config(state=tk.DISABLED)
            return
    
    def evaluate_guess(self, guess):
        """Evaluate a guess against the secret code."""
        # Count exact matches (correct color in correct position)
        exact_matches = sum(1 for i in range(self.code_length) if guess[i] == self.secret_code[i])
        
        # Count color matches (correct color but wrong position)
        # We need to count each color only once
        guess_colors = {}
        secret_colors = {}
        
        for i in range(self.code_length):
            if guess[i] != self.secret_code[i]:  # Skip exact matches
                guess_colors[guess[i]] = guess_colors.get(guess[i], 0) + 1
                secret_colors[self.secret_code[i]] = secret_colors.get(self.secret_code[i], 0) + 1
        
        color_matches = sum(min(guess_colors.get(color, 0), secret_colors.get(color, 0)) for color in set(guess_colors) | set(secret_colors))
        
        return (exact_matches, color_matches)
    
    def update_board(self):
        """Update the game board with the latest guess and feedback."""
        row = self.current_attempt - 1
        
        # Update guess pegs
        for i, color_code in enumerate(self.attempts[row]):
            color_hex, _ = self.gui_colors[color_code]
            self.guess_frames[row][i].config(text=color_code, bg=color_hex, fg="#000000")
        
        # Update feedback pegs
        exact, color = self.feedbacks[row]
        
        for i in range(self.code_length):
            if i < exact:
                # Exact match
                self.feedback_frames[row][i].config(bg="#000000")  # Black
            elif i < exact + color:
                # Color match
                self.feedback_frames[row][i].config(bg="#FFFFFF")  # White
            else:
                # No match
                self.feedback_frames[row][i].config(bg="#444444")  # Gray
    
    def reveal_secret_code(self):
        """Reveal the secret code."""
        for i, color_code in enumerate(self.secret_code):
            color_hex, _ = self.gui_colors[color_code]
            self.secret_pegs[i].config(text=color_code, bg=color_hex, fg="#000000")
    
    def quit_game(self):
        """Quit the game."""
        if messagebox.askyesno("Quit", "Are you sure you want to quit the game?"):
            self.root.destroy()

def main():
    """Main function to start the GUI game."""
    root = tk.Tk()
    app = MastermindGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 