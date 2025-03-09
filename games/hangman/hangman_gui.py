#!/usr/bin/env python3
import os
import random
import tkinter as tk
from tkinter import ttk, messagebox

# Import word list from terminal version
from games.hangman import WORDS

class HangmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman")
        self.root.geometry("700x600")
        self.root.configure(bg="#333333")
        self.root.resizable(True, True)
        
        # Set minimum window size
        self.root.minsize(600, 500)
        
        # Game variables
        self.word = ""
        self.word_completion = ""
        self.guessed_letters = []
        self.guessed_words = []
        self.tries = 6
        self.guessed = False
        
        # Create UI elements
        self.create_widgets()
        
        # Start a new game
        self.new_game()
    
    def create_widgets(self):
        """Create the GUI widgets."""
        # Main frame
        main_frame = tk.Frame(self.root, bg="#333333")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title label
        title_label = tk.Label(
            main_frame, 
            text="Hangman", 
            font=("Helvetica", 24, "bold"),
            bg="#333333",
            fg="#66CCFF"  # Cyan
        )
        title_label.pack(pady=(0, 10))
        
        # Game area frame
        game_frame = tk.Frame(main_frame, bg="#222222", relief=tk.RIDGE, bd=2)
        game_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Hangman display
        self.hangman_display = tk.Label(
            game_frame,
            font=("Courier New", 16),
            bg="#222222",
            fg="#FFFFFF",
            justify=tk.LEFT
        )
        self.hangman_display.pack(pady=10)
        
        # Word display
        self.word_display = tk.Label(
            game_frame,
            font=("Courier New", 24, "bold"),
            bg="#222222",
            fg="#FFFFFF"
        )
        self.word_display.pack(pady=10)
        
        # Guessed letters display
        guessed_frame = tk.Frame(game_frame, bg="#222222")
        guessed_frame.pack(fill=tk.X, padx=20, pady=10)
        
        guessed_label = tk.Label(
            guessed_frame,
            text="Guessed Letters:",
            font=("Helvetica", 12),
            bg="#222222",
            fg="#FFFF99"  # Yellow
        )
        guessed_label.pack(side=tk.LEFT, padx=5)
        
        self.guessed_display = tk.Label(
            guessed_frame,
            text="",
            font=("Helvetica", 12),
            bg="#222222",
            fg="#FFFFFF"
        )
        self.guessed_display.pack(side=tk.LEFT, padx=5)
        
        # Tries remaining display
        self.tries_display = tk.Label(
            game_frame,
            text="Tries remaining: 6",
            font=("Helvetica", 12),
            bg="#222222",
            fg="#CCFF99"  # Green
        )
        self.tries_display.pack(pady=5)
        
        # Message display
        self.message_display = tk.Label(
            game_frame,
            text="",
            font=("Helvetica", 14, "bold"),
            bg="#222222",
            fg="#FFFFFF"
        )
        self.message_display.pack(pady=10)
        
        # Input frame
        input_frame = tk.Frame(main_frame, bg="#333333")
        input_frame.pack(fill=tk.X, pady=10)
        
        # Letter input
        letter_label = tk.Label(
            input_frame,
            text="Enter a letter or word:",
            font=("Helvetica", 12),
            bg="#333333",
            fg="#FFFFFF"
        )
        letter_label.pack(side=tk.LEFT, padx=5)
        
        self.letter_entry = tk.Entry(
            input_frame,
            font=("Helvetica", 12),
            width=10,
            bg="#111111",
            fg="#FFFFFF",
            insertbackground="#FFFFFF"
        )
        self.letter_entry.pack(side=tk.LEFT, padx=5)
        self.letter_entry.bind("<Return>", self.make_guess)
        
        # Guess button
        guess_button = tk.Button(
            input_frame,
            text="Guess",
            command=self.make_guess,
            bg="#66CCFF",  # Cyan
            fg="#000000",
            activebackground="#339999",
            activeforeground="#FFFFFF",
            font=("Helvetica", 12, "bold")
        )
        guess_button.pack(side=tk.LEFT, padx=5)
        
        # Virtual keyboard frame
        keyboard_frame = tk.Frame(main_frame, bg="#333333")
        keyboard_frame.pack(fill=tk.X, pady=10)
        
        # Create 3 rows of letter buttons for virtual keyboard
        keyboard_letters = [
            "ABCDEFGHIJ",
            "KLMNOPQRST",
            "UVWXYZ"
        ]
        
        for row_idx, letters in enumerate(keyboard_letters):
            row_frame = tk.Frame(keyboard_frame, bg="#333333")
            row_frame.pack(pady=2)
            
            for letter in letters:
                letter_button = tk.Button(
                    row_frame,
                    text=letter,
                    width=2,
                    font=("Helvetica", 12, "bold"),
                    bg="#444444",
                    fg="#FFFFFF",
                    activebackground="#666666",
                    activeforeground="#FFFFFF",
                    command=lambda l=letter: self.virtual_keyboard_press(l)
                )
                letter_button.pack(side=tk.LEFT, padx=2)
                # Store button reference for disabling when letter is guessed
                setattr(self, f"btn_{letter}", letter_button)
        
        # Control buttons frame
        control_frame = tk.Frame(main_frame, bg="#333333")
        control_frame.pack(fill=tk.X, pady=10)
        
        # New Game button
        new_game_button = tk.Button(
            control_frame,
            text="New Game",
            command=self.new_game,
            bg="#444444",
            fg="#FFFFFF",
            activebackground="#666666",
            activeforeground="#FFFFFF",
            font=("Helvetica", 12)
        )
        new_game_button.pack(side=tk.LEFT, padx=5)
        
        # Quit button
        quit_button = tk.Button(
            control_frame,
            text="Quit",
            command=self.quit_game,
            bg="#663333",
            fg="#FFFFFF",
            activebackground="#993333",
            activeforeground="#FFFFFF",
            font=("Helvetica", 12)
        )
        quit_button.pack(side=tk.RIGHT, padx=5)
    
    def display_hangman(self):
        """Display the hangman based on remaining tries."""
        # ASCII art for hangman at different stages
        hangman_stages = [
            # 6 tries left (empty gallows)
            """
  +---+
  |   |
      |
      |
      |
      |
=========""",
            # 5 tries left (head)
            """
  +---+
  |   |
  O   |
      |
      |
      |
=========""",
            # 4 tries left (head and torso)
            """
  +---+
  |   |
  O   |
  |   |
      |
      |
=========""",
            # 3 tries left (head, torso, and one arm)
            """
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========""",
            # 2 tries left (head, torso, and both arms)
            """
  +---+
  |   |
  O   |
 /|\\  |
      |
      |
=========""",
            # 1 try left (head, torso, both arms, and one leg)
            """
  +---+
  |   |
  O   |
 /|\\  |
 /    |
      |
=========""",
            # 0 tries left (full hangman)
            """
  +---+
  |   |
  O   |
 /|\\  |
 / \\  |
      |
========="""
        ]
        
        # Determine which stage to display
        stage = 6 - self.tries
        
        # Set color based on remaining tries
        if self.tries >= 4:
            fg_color = "#CCFF99"  # Green
        elif self.tries >= 2:
            fg_color = "#FFFF99"  # Yellow
        else:
            fg_color = "#FF6666"  # Red
        
        self.hangman_display.config(text=hangman_stages[stage], fg=fg_color)
    
    def update_word_display(self):
        """Update the display of the word being guessed."""
        # Display the word with spaces between letters
        display_word = " ".join(self.word_completion)
        self.word_display.config(text=display_word)
    
    def update_guessed_display(self):
        """Update the display of guessed letters."""
        guessed_text = ", ".join(sorted(self.guessed_letters))
        self.guessed_display.config(text=guessed_text)
        self.tries_display.config(text=f"Tries remaining: {self.tries}")
        
        # Update color of tries remaining based on number left
        if self.tries >= 4:
            self.tries_display.config(fg="#CCFF99")  # Green
        elif self.tries >= 2:
            self.tries_display.config(fg="#FFFF99")  # Yellow
        else:
            self.tries_display.config(fg="#FF6666")  # Red
    
    def disable_guessed_letters(self):
        """Disable buttons for letters that have been guessed."""
        for letter in self.guessed_letters:
            button = getattr(self, f"btn_{letter}", None)
            if button:
                button.config(state=tk.DISABLED, bg="#222222")
    
    def reset_keyboard(self):
        """Re-enable all keyboard buttons."""
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            button = getattr(self, f"btn_{letter}", None)
            if button:
                button.config(state=tk.NORMAL, bg="#444444")
    
    def virtual_keyboard_press(self, letter):
        """Handle virtual keyboard button press."""
        if letter not in self.guessed_letters and not self.guessed:
            self.letter_entry.delete(0, tk.END)
            self.letter_entry.insert(0, letter)
            self.make_guess()
    
    def make_guess(self, event=None):
        """Process the player's guess."""
        if self.guessed:
            return
        
        guess = self.letter_entry.get().upper().strip()
        self.letter_entry.delete(0, tk.END)
        
        if not guess:
            self.message_display.config(text="Please enter a letter or word.", fg="#FF6666")
            return
        
        # Handle single letter guess
        if len(guess) == 1 and guess.isalpha():
            if guess in self.guessed_letters:
                self.message_display.config(text=f"You already guessed the letter {guess}.", fg="#FFFF99")
                return
            
            self.guessed_letters.append(guess)
            button = getattr(self, f"btn_{guess}", None)
            if button:
                button.config(state=tk.DISABLED, bg="#222222")
            
            if guess in self.word:
                # Correct letter guess
                self.message_display.config(text=f"Good job! {guess} is in the word.", fg="#CCFF99")
                
                # Update word completion
                for i in range(len(self.word)):
                    if self.word[i] == guess:
                        self.word_completion = self.word_completion[:i] + guess + self.word_completion[i+1:]
                
                # Check if the word is complete
                if "_" not in self.word_completion:
                    self.guessed = True
                    self.message_display.config(text=f"Congratulations! You guessed the word: {self.word}", fg="#CCFF99")
            else:
                # Incorrect letter guess
                self.tries -= 1
                self.message_display.config(text=f"Sorry, {guess} is not in the word.", fg="#FF6666")
        
        # Handle full word guess
        elif len(guess) == len(self.word) and guess.isalpha():
            if guess in self.guessed_words:
                self.message_display.config(text=f"You already guessed the word {guess}.", fg="#FFFF99")
                return
            
            self.guessed_words.append(guess)
            
            if guess == self.word:
                # Correct word guess
                self.word_completion = self.word
                self.guessed = True
                self.message_display.config(text=f"Congratulations! You guessed the word: {self.word}", fg="#CCFF99")
            else:
                # Incorrect word guess
                self.tries -= 1
                self.message_display.config(text=f"Sorry, {guess} is not the word.", fg="#FF6666")
        
        else:
            self.message_display.config(text="Not a valid guess.", fg="#FF6666")
        
        # Update displays
        self.display_hangman()
        self.update_word_display()
        self.update_guessed_display()
        
        # Check for game over (out of tries)
        if self.tries <= 0:
            self.guessed = True
            self.message_display.config(text=f"Game over! The word was: {self.word}", fg="#FF6666")
    
    def new_game(self):
        """Start a new game."""
        # Select a random word
        self.word = random.choice(WORDS).upper()
        self.word_completion = "_" * len(self.word)
        self.guessed_letters = []
        self.guessed_words = []
        self.tries = 6
        self.guessed = False
        
        # Reset displays
        self.display_hangman()
        self.update_word_display()
        self.update_guessed_display()
        self.reset_keyboard()
        
        # Reset focus and message
        self.letter_entry.focus_set()
        self.message_display.config(text=f"The word has {len(self.word)} letters. Good luck!", fg="#FFFFFF")
    
    def quit_game(self):
        """Quit the game."""
        if messagebox.askyesno("Quit Game", "Are you sure you want to quit?"):
            self.root.destroy()

def main():
    """Main function to start the GUI game."""
    root = tk.Tk()
    app = HangmanGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 