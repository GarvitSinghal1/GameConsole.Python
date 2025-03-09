#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import random
import time
import sys
import os

class AnagramsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Anagrams")
        self.root.geometry("800x600")
        self.root.configure(bg="#1E3F66")  # Dark blue background
        self.root.resizable(True, True)

        # Game parameters
        self.difficulty = "medium"
        self.time_limit = 60  # seconds
        self.time_remaining = self.time_limit
        self.score = 0
        self.game_active = False
        self.timer_id = None
        self.found_words = []
        self.current_word = ""
        self.scrambled_word = ""
        self.valid_words = []
        self.all_words = []
        
        # Try to load words from dictionary file
        try:
            word_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                    "assets", "word_lists", "english_words.txt")
            with open(word_file, "r") as f:
                self.all_words = [word.strip().lower() for word in f if 3 <= len(word.strip()) <= 8]
        except FileNotFoundError:
            # Fallback word list if file not found
            self.all_words = [
                "python", "computer", "program", "code", "algorithm", "function", "variable",
                "keyboard", "mouse", "screen", "software", "hardware", "network", "database",
                "language", "syntax", "memory", "processor", "graphics", "internet", "website",
                "browser", "server", "client", "system", "file", "folder", "script", "loop",
                "array", "class", "object", "method", "string", "integer", "boolean", "error"
            ]
        
        # Create widgets
        self.create_widgets()
        
        # Show welcome screen
        self.show_welcome()
    
    def create_widgets(self):
        """Create the GUI widgets."""
        # Main frame
        self.main_frame = tk.Frame(self.root, bg="#1E3F66")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title label
        self.title_label = tk.Label(
            self.main_frame,
            text="ANAGRAMS",
            font=("Helvetica", 24, "bold"),
            bg="#1E3F66",
            fg="#FFFFFF"
        )
        self.title_label.pack(pady=(0, 20))
        
        # Game info frame
        self.info_frame = tk.Frame(self.main_frame, bg="#1E3F66")
        self.info_frame.pack(fill=tk.X, pady=5)
        
        # Score display
        self.score_var = tk.StringVar(value="Score: 0")
        self.score_label = tk.Label(
            self.info_frame,
            textvariable=self.score_var,
            font=("Helvetica", 16, "bold"),
            bg="#1E3F66",
            fg="#FFFFFF"
        )
        self.score_label.pack(side=tk.LEFT, padx=10)
        
        # Timer display
        self.timer_var = tk.StringVar(value=f"Time: {self.time_limit}")
        self.timer_label = tk.Label(
            self.info_frame,
            textvariable=self.timer_var,
            font=("Helvetica", 16, "bold"),
            bg="#1E3F66",
            fg="#FFFFFF"
        )
        self.timer_label.pack(side=tk.RIGHT, padx=10)
        
        # Word display frame
        self.word_frame = tk.Frame(self.main_frame, bg="#1E3F66")
        self.word_frame.pack(fill=tk.X, pady=20)
        
        # Scrambled word label
        self.word_var = tk.StringVar(value="")
        self.word_label = tk.Label(
            self.word_frame,
            textvariable=self.word_var,
            font=("Courier", 24, "bold"),
            bg="#2A4E6E",  # Slightly lighter blue
            fg="#FFFFFF",
            width=20,
            height=2
        )
        self.word_label.pack(pady=10)
        
        # User input frame
        self.input_frame = tk.Frame(self.main_frame, bg="#1E3F66")
        self.input_frame.pack(fill=tk.X, pady=10)
        
        # Word entry
        self.entry_var = tk.StringVar()
        self.word_entry = tk.Entry(
            self.input_frame,
            textvariable=self.entry_var,
            font=("Helvetica", 16),
            width=20,
            bg="#FFFFFF",
            fg="#000000"
        )
        self.word_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        self.word_entry.bind("<Return>", lambda e: self.check_word())
        
        # Submit button
        self.submit_button = tk.Button(
            self.input_frame,
            text="Submit",
            font=("Helvetica", 12),
            bg="#4CAF50",  # Green
            fg="white",
            command=self.check_word
        )
        self.submit_button.pack(side=tk.RIGHT, padx=10)
        
        # Found words frame
        self.found_frame = tk.Frame(self.main_frame, bg="#1E3F66")
        self.found_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Found words label
        tk.Label(
            self.found_frame,
            text="Found Words:",
            font=("Helvetica", 14, "bold"),
            bg="#1E3F66",
            fg="#FFFFFF"
        ).pack(anchor=tk.W, pady=(0, 5))
        
        # Found words text area
        self.found_text = scrolledtext.ScrolledText(
            self.found_frame,
            wrap=tk.WORD,
            width=40,
            height=8,
            font=("Helvetica", 12),
            bg="#2A4E6E",
            fg="#FFFFFF"
        )
        self.found_text.pack(fill=tk.BOTH, expand=True)
        self.found_text.config(state=tk.DISABLED)
        
        # Difficulty selection frame
        self.difficulty_frame = tk.Frame(self.main_frame, bg="#1E3F66")
        self.difficulty_frame.pack(fill=tk.X, pady=10)
        
        # Difficulty label
        tk.Label(
            self.difficulty_frame,
            text="Difficulty:",
            font=("Helvetica", 12),
            bg="#1E3F66",
            fg="#FFFFFF"
        ).pack(side=tk.LEFT, padx=10)
        
        # Difficulty radio buttons
        self.difficulty_var = tk.StringVar(value=self.difficulty)
        
        tk.Radiobutton(
            self.difficulty_frame,
            text="Easy",
            variable=self.difficulty_var,
            value="easy",
            command=self.change_difficulty,
            bg="#1E3F66",
            fg="#FFFFFF",
            selectcolor="#2A4E6E",
            activebackground="#1E3F66",
            activeforeground="#FFFFFF"
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Radiobutton(
            self.difficulty_frame,
            text="Medium",
            variable=self.difficulty_var,
            value="medium",
            command=self.change_difficulty,
            bg="#1E3F66",
            fg="#FFFFFF",
            selectcolor="#2A4E6E",
            activebackground="#1E3F66",
            activeforeground="#FFFFFF"
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Radiobutton(
            self.difficulty_frame,
            text="Hard",
            variable=self.difficulty_var,
            value="hard",
            command=self.change_difficulty,
            bg="#1E3F66",
            fg="#FFFFFF",
            selectcolor="#2A4E6E",
            activebackground="#1E3F66",
            activeforeground="#FFFFFF"
        ).pack(side=tk.LEFT, padx=5)
        
        # Control buttons frame
        self.control_frame = tk.Frame(self.main_frame, bg="#1E3F66")
        self.control_frame.pack(fill=tk.X, pady=10)
        
        # Start button
        self.start_button = tk.Button(
            self.control_frame,
            text="Start Game",
            font=("Helvetica", 12),
            bg="#4CAF50",  # Green
            fg="white",
            command=self.start_game
        )
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        # New word button
        self.new_word_button = tk.Button(
            self.control_frame,
            text="New Word",
            font=("Helvetica", 12),
            bg="#2196F3",  # Blue
            fg="white",
            command=self.new_word,
            state=tk.DISABLED
        )
        self.new_word_button.pack(side=tk.LEFT, padx=10)
        
        # Quit button
        self.quit_button = tk.Button(
            self.control_frame,
            text="Quit",
            font=("Helvetica", 12),
            bg="#F44336",  # Red
            fg="white",
            command=self.quit_game
        )
        self.quit_button.pack(side=tk.RIGHT, padx=10)
    
    def show_welcome(self):
        """Show welcome screen and instructions."""
        welcome_window = tk.Toplevel(self.root)
        welcome_window.title("Welcome to Anagrams")
        welcome_window.geometry("500x400")
        welcome_window.configure(bg="#1E3F66")
        welcome_window.transient(self.root)
        welcome_window.grab_set()
        welcome_window.resizable(True, True)
        
        # Welcome title
        tk.Label(
            welcome_window,
            text="Welcome to Anagrams",
            font=("Helvetica", 18, "bold"),
            bg="#1E3F66",
            fg="#FFFFFF"
        ).pack(pady=20)
        
        # Instructions
        instructions_frame = tk.Frame(welcome_window, bg="#1E3F66", padx=20)
        instructions_frame.pack(fill=tk.BOTH, expand=True)
        
        instructions = [
            "Anagrams is a word game where you form words using the",
            "letters from a scrambled word.",
            "",
            "How to Play:",
            "• Use the letters shown to form as many valid words as possible",
            "• Each valid word earns points based on word length",
            "• Words must be at least 3 letters long",
            "• Try to find as many words as you can before time runs out!",
            "",
            "Difficulty Levels:",
            "• Easy: 90 seconds, shorter words",
            "• Medium: 60 seconds, medium length words",
            "• Hard: 45 seconds, longer words"
        ]
        
        for line in instructions:
            tk.Label(
                instructions_frame,
                text=line,
                font=("Helvetica", 12),
                bg="#1E3F66",
                fg="#FFFFFF",
                justify=tk.LEFT
            ).pack(anchor=tk.W, pady=1)
        
        # Start button
        tk.Button(
            welcome_window,
            text="Let's Play!",
            font=("Helvetica", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            command=welcome_window.destroy
        ).pack(pady=20)
    
    def change_difficulty(self):
        """Change the game difficulty."""
        self.difficulty = self.difficulty_var.get()
        
        if self.difficulty == "easy":
            self.time_limit = 90
        elif self.difficulty == "medium":
            self.time_limit = 60
        else:  # hard
            self.time_limit = 45
        
        self.time_remaining = self.time_limit
        self.timer_var.set(f"Time: {self.time_remaining}")
    
    def start_game(self):
        """Start a new game."""
        # If a game is already in progress, confirm restart
        if self.game_active:
            if not messagebox.askyesno("New Game", "Are you sure you want to start a new game?"):
                return
        
        # Reset game state
        self.score = 0
        self.score_var.set("Score: 0")
        self.time_remaining = self.time_limit
        self.timer_var.set(f"Time: {self.time_remaining}")
        self.found_words = []
        self.found_text.config(state=tk.NORMAL)
        self.found_text.delete("1.0", tk.END)
        self.found_text.config(state=tk.DISABLED)
        
        # Enable game controls
        self.word_entry.config(state=tk.NORMAL)
        self.submit_button.config(state=tk.NORMAL)
        self.new_word_button.config(state=tk.NORMAL)
        
        # Get a new word
        self.new_word()
        
        # Start the timer
        self.game_active = True
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.update_timer()
    
    def new_word(self):
        """Generate a new word for the game."""
        if not self.game_active:
            return
        
        # Select word based on difficulty
        if self.difficulty == "easy":
            word_length_range = (4, 6)
        elif self.difficulty == "medium":
            word_length_range = (5, 7)
        else:  # hard
            word_length_range = (6, 8)
        
        # Filter words by length
        filtered_words = [word for word in self.all_words 
                         if word_length_range[0] <= len(word) <= word_length_range[1]]
        
        if not filtered_words:
            filtered_words = self.all_words
        
        # Select a random word
        self.current_word = random.choice(filtered_words).lower()
        
        # Generate anagrams
        self.valid_words = self.find_all_words(self.current_word)
        
        # Scramble the word
        self.scramble_word()
        
        # Clear entry
        self.entry_var.set("")
        self.word_entry.focus()
    
    def scramble_word(self):
        """Scramble the current word."""
        word_chars = list(self.current_word)
        random.shuffle(word_chars)
        
        # Make sure the scrambled word is different from the original
        while ''.join(word_chars) == self.current_word and len(self.current_word) > 1:
            random.shuffle(word_chars)
        
        self.scrambled_word = ''.join(word_chars)
        self.word_var.set(self.scrambled_word.upper())
    
    def find_all_words(self, word):
        """Find all valid words that can be formed from the letters of the given word."""
        # Count the frequency of each letter in the word
        letter_counts = {}
        for letter in word:
            if letter in letter_counts:
                letter_counts[letter] += 1
            else:
                letter_counts[letter] = 1
        
        valid_words = []
        
        # Check each word in our dictionary
        for dict_word in self.all_words:
            if len(dict_word) >= 3 and self.can_form_word(dict_word, letter_counts.copy()):
                valid_words.append(dict_word)
        
        return valid_words
    
    def can_form_word(self, word, letter_counts):
        """Check if a word can be formed using the available letters."""
        for letter in word:
            if letter not in letter_counts or letter_counts[letter] == 0:
                return False
            letter_counts[letter] -= 1
        return True
    
    def check_word(self):
        """Check if the entered word is valid."""
        if not self.game_active:
            return
        
        # Get the entered word
        entered_word = self.entry_var.get().strip().lower()
        
        # Clear the entry
        self.entry_var.set("")
        
        # Check if the word is valid
        if (len(entered_word) >= 3 and 
            entered_word in self.valid_words and 
            entered_word not in self.found_words):
            
            # Add to found words
            self.found_words.append(entered_word)
            
            # Update score based on word length
            word_score = len(entered_word) ** 2
            self.score += word_score
            self.score_var.set(f"Score: {self.score}")
            
            # Update found words display
            self.found_text.config(state=tk.NORMAL)
            self.found_text.insert(tk.END, f"{entered_word} (+{word_score})\n")
            self.found_text.see(tk.END)
            self.found_text.config(state=tk.DISABLED)
            
            # Check if all words are found
            if len(self.found_words) == len(self.valid_words):
                messagebox.showinfo("Congratulations!", "You found all possible words!")
                self.new_word()
        elif entered_word in self.found_words:
            messagebox.showinfo("Already Found", "You've already found this word!")
        elif entered_word:
            messagebox.showinfo("Invalid Word", "Not a valid word from the current letters!")
    
    def update_timer(self):
        """Update the game timer."""
        if not self.game_active:
            return
        
        self.time_remaining -= 1
        self.timer_var.set(f"Time: {self.time_remaining}")
        
        if self.time_remaining <= 0:
            self.game_over()
        else:
            self.timer_id = self.root.after(1000, self.update_timer)
    
    def game_over(self):
        """Handle game over."""
        self.game_active = False
        
        # Disable game controls
        self.word_entry.config(state=tk.DISABLED)
        self.submit_button.config(state=tk.DISABLED)
        self.new_word_button.config(state=tk.DISABLED)
        
        # Show game over message
        missed_words = [word for word in self.valid_words if word not in self.found_words]
        
        message = f"Time's up! Your score: {self.score}\n\n"
        if missed_words:
            message += "Words you missed:\n" + ", ".join(missed_words)
        
        messagebox.showinfo("Game Over", message)
    
    def quit_game(self):
        """Quit the game."""
        if messagebox.askyesno("Quit", "Are you sure you want to quit the game?"):
            self.root.destroy()

def main():
    """Main function to start the GUI game."""
    root = tk.Tk()
    app = AnagramsGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 