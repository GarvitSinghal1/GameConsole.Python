#!/usr/bin/env python3
import os
import random
import tkinter as tk
from tkinter import ttk, messagebox

# Import word lists from terminal version
from games.word_scramble import (
    EASY_WORDS,
    MEDIUM_WORDS,
    HARD_WORDS,
    VERY_HARD_WORDS,
    scramble_word,
    get_word_list,
    get_hint
)

class WordScrambleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Scramble")
        self.root.geometry("600x550")
        self.root.configure(bg="#333333")
        self.root.resizable(True, True)
        
        # Set minimum window size
        self.root.minsize(500, 400)
        
        # Game variables
        self.level = 1
        self.score = 0
        self.num_words = 0
        self.words_played = 0
        self.current_word = ""
        self.scrambled_word = ""
        self.hint_level = 0
        self.attempts = 0
        self.max_attempts = 3
        self.words_to_play = []
        
        # Create UI elements
        self.create_widgets()
        
        # Show welcome screen
        self.show_welcome()
    
    def create_widgets(self):
        """Create the GUI widgets."""
        # Main frame
        main_frame = tk.Frame(self.root, bg="#333333")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title label
        self.title_label = tk.Label(
            main_frame, 
            text="Word Scramble", 
            font=("Helvetica", 24, "bold"),
            bg="#333333",
            fg="#FF99FF"  # Magenta
        )
        self.title_label.pack(pady=(0, 10))
        
        # Game area frame
        self.game_frame = tk.Frame(main_frame, bg="#222222", relief=tk.RIDGE, bd=2)
        self.game_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrambled word display
        self.scrambled_label = tk.Label(
            self.game_frame,
            text="",
            font=("Courier New", 28, "bold"),
            bg="#222222",
            fg="#FFFFFF"
        )
        self.scrambled_label.pack(pady=20)
        
        # Hint display
        self.hint_label = tk.Label(
            self.game_frame,
            text="",
            font=("Helvetica", 14),
            bg="#222222",
            fg="#FFFF99"  # Yellow
        )
        self.hint_label.pack(pady=10)
        
        # Answer entry frame
        answer_frame = tk.Frame(self.game_frame, bg="#222222")
        answer_frame.pack(pady=10)
        
        answer_label = tk.Label(
            answer_frame,
            text="Your answer:",
            font=("Helvetica", 14),
            bg="#222222",
            fg="#FFFFFF"
        )
        answer_label.pack(side=tk.LEFT, padx=5)
        
        self.answer_entry = tk.Entry(
            answer_frame,
            font=("Helvetica", 14, "bold"),
            width=20,
            bg="#111111",
            fg="#FFFFFF",
            insertbackground="#FFFFFF"
        )
        self.answer_entry.pack(side=tk.LEFT, padx=5)
        self.answer_entry.bind("<Return>", self.check_answer)
        
        # Button frame
        button_frame = tk.Frame(self.game_frame, bg="#222222")
        button_frame.pack(pady=10)
        
        # Submit button
        self.submit_button = tk.Button(
            button_frame,
            text="Submit",
            command=self.check_answer,
            bg="#FF99FF",  # Magenta
            fg="#000000",
            activebackground="#CC66CC",
            activeforeground="#FFFFFF",
            font=("Helvetica", 12, "bold"),
            width=10
        )
        self.submit_button.pack(side=tk.LEFT, padx=5)
        
        # Hint button
        self.hint_button = tk.Button(
            button_frame,
            text="Get Hint",
            command=self.request_hint,
            bg="#FFFF99",  # Yellow
            fg="#000000",
            activebackground="#CCCC66",
            activeforeground="#000000",
            font=("Helvetica", 12),
            width=10
        )
        self.hint_button.pack(side=tk.LEFT, padx=5)
        
        # Skip button
        self.skip_button = tk.Button(
            button_frame,
            text="Skip Word",
            command=self.skip_word,
            bg="#FF6666",  # Red
            fg="#FFFFFF",
            activebackground="#CC3333",
            activeforeground="#FFFFFF",
            font=("Helvetica", 12),
            width=10
        )
        self.skip_button.pack(side=tk.LEFT, padx=5)
        
        # Feedback display
        self.feedback_label = tk.Label(
            self.game_frame,
            text="",
            font=("Helvetica", 14, "bold"),
            bg="#222222",
            fg="#FFFFFF",
            wraplength=500
        )
        self.feedback_label.pack(pady=10)
        
        # Progress and attempts frame
        progress_frame = tk.Frame(self.game_frame, bg="#222222")
        progress_frame.pack(fill=tk.X, padx=20, pady=5)
        
        # Word progress
        self.progress_label = tk.Label(
            progress_frame,
            text="",
            font=("Helvetica", 12),
            bg="#222222",
            fg="#66CCFF"  # Blue
        )
        self.progress_label.pack(side=tk.LEFT)
        
        # Attempts remaining
        self.attempts_label = tk.Label(
            progress_frame,
            text="",
            font=("Helvetica", 12),
            bg="#222222",
            fg="#CCFF99"  # Green
        )
        self.attempts_label.pack(side=tk.RIGHT)
        
        # Score display
        self.score_label = tk.Label(
            self.game_frame,
            text="Score: 0",
            font=("Helvetica", 14, "bold"),
            bg="#222222",
            fg="#CCFF99"  # Green
        )
        self.score_label.pack(pady=5)
        
        # Setup frame (for welcome screen)
        self.setup_frame = tk.Frame(self.game_frame, bg="#222222")
        
        # Control buttons frame
        control_frame = tk.Frame(main_frame, bg="#333333")
        control_frame.pack(fill=tk.X, pady=10)
        
        # New Game button
        self.new_game_button = tk.Button(
            control_frame,
            text="New Game",
            command=self.show_welcome,
            bg="#444444",
            fg="#FFFFFF",
            activebackground="#666666",
            activeforeground="#FFFFFF",
            font=("Helvetica", 12),
            width=10
        )
        self.new_game_button.pack(side=tk.LEFT, padx=5)
        
        # Quit button
        quit_button = tk.Button(
            control_frame,
            text="Quit",
            command=self.quit_game,
            bg="#663333",
            fg="#FFFFFF",
            activebackground="#993333",
            activeforeground="#FFFFFF",
            font=("Helvetica", 12),
            width=10
        )
        quit_button.pack(side=tk.RIGHT, padx=5)
    
    def show_welcome(self):
        """Show the welcome screen with difficulty selection."""
        # Clear game display
        self.scrambled_label.config(text="")
        self.hint_label.config(text="")
        self.feedback_label.config(text="")
        self.progress_label.config(text="")
        self.attempts_label.config(text="")
        self.score_label.config(text="Score: 0")
        
        # Clear answer entry
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.config(state=tk.DISABLED)
        
        # Disable game buttons
        self.submit_button.config(state=tk.DISABLED)
        self.hint_button.config(state=tk.DISABLED)
        self.skip_button.config(state=tk.DISABLED)
        
        # Reset game variables
        self.score = 0
        self.words_played = 0
        
        # Clear previous setup widgets
        for widget in self.setup_frame.winfo_children():
            widget.destroy()
        
        # Show setup frame
        self.setup_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Welcome message
        welcome_label = tk.Label(
            self.setup_frame,
            text="Welcome to Word Scramble!",
            font=("Helvetica", 18, "bold"),
            bg="#222222",
            fg="#FFFFFF"
        )
        welcome_label.pack(pady=10)
        
        instructions = tk.Label(
            self.setup_frame,
            text="Unscramble the letters to form valid words.\nYou can use hints if you get stuck, but they will reduce your score.",
            font=("Helvetica", 12),
            bg="#222222",
            fg="#FFFFFF",
            justify=tk.CENTER
        )
        instructions.pack(pady=5)
        
        # Level selection
        level_frame = tk.Frame(self.setup_frame, bg="#222222")
        level_frame.pack(pady=15)
        
        level_label = tk.Label(
            level_frame,
            text="Choose difficulty level:",
            font=("Helvetica", 14),
            bg="#222222",
            fg="#FFFFFF"
        )
        level_label.pack(anchor=tk.W, padx=10, pady=5)
        
        self.level_var = tk.IntVar(value=1)
        
        # Create radio buttons for levels
        level_descriptions = [
            "Easy (3-4 letter words)",
            "Medium (5-6 letter words)",
            "Hard (7-10 letter words)",
            "Very Hard (11+ letter words)"
        ]
        
        level_colors = ["#CCFF99", "#FFFF99", "#FF6666", "#FF99FF"]  # Green, Yellow, Red, Magenta
        
        for i, (desc, color) in enumerate(zip(level_descriptions, level_colors), 1):
            level_button = tk.Radiobutton(
                self.setup_frame,
                text=f"{i}. {desc}",
                variable=self.level_var,
                value=i,
                font=("Helvetica", 12),
                bg="#222222",
                fg=color,
                selectcolor="#333333",
                activebackground="#222222",
                activeforeground=color
            )
            level_button.pack(anchor=tk.W, padx=30, pady=3)
        
        # Number of words selection
        words_frame = tk.Frame(self.setup_frame, bg="#222222")
        words_frame.pack(pady=15)
        
        words_label = tk.Label(
            words_frame,
            text="How many words?",
            font=("Helvetica", 14),
            bg="#222222",
            fg="#FFFFFF"
        )
        words_label.pack(side=tk.LEFT, padx=10)
        
        self.words_var = tk.IntVar(value=10)
        words_slider = ttk.Scale(
            words_frame,
            from_=5,
            to=15,
            orient=tk.HORIZONTAL,
            variable=self.words_var,
            length=200,
            command=self.update_words_label
        )
        words_slider.pack(side=tk.LEFT, padx=10)
        
        self.words_value_label = tk.Label(
            words_frame,
            text="10",
            font=("Helvetica", 14),
            bg="#222222",
            fg="#FFFFFF",
            width=2
        )
        self.words_value_label.pack(side=tk.LEFT, padx=5)
        
        # Start game button
        start_button = tk.Button(
            self.setup_frame,
            text="Start Game",
            command=self.start_game,
            bg="#FF99FF",  # Magenta
            fg="#000000",
            activebackground="#CC66CC",
            activeforeground="#FFFFFF",
            font=("Helvetica", 14, "bold"),
            width=15,
            height=2
        )
        start_button.pack(pady=20)
    
    def update_words_label(self, *args):
        """Update the label showing number of words."""
        value = int(float(self.words_var.get()))
        self.words_value_label.config(text=str(value))
    
    def start_game(self):
        """Start the game with selected settings."""
        # Get selected level and number of words
        self.level = self.level_var.get()
        self.num_words = int(self.words_var.get())
        
        # Get word list based on level
        word_list = get_word_list(self.level)
        
        # Select random words to play
        self.words_to_play = random.sample(word_list, min(self.num_words, len(word_list)))
        self.words_played = 0
        self.score = 0
        
        # Hide setup frame
        self.setup_frame.pack_forget()
        
        # Enable game controls
        self.answer_entry.config(state=tk.NORMAL)
        self.submit_button.config(state=tk.NORMAL)
        self.hint_button.config(state=tk.NORMAL)
        self.skip_button.config(state=tk.NORMAL)
        
        # Update score display
        self.score_label.config(text="Score: 0")
        
        # Start with the first word
        self.next_word()
    
    def next_word(self):
        """Present the next scrambled word."""
        if self.words_played >= len(self.words_to_play):
            # End of game
            self.show_results()
            return
        
        # Get the next word
        self.current_word = self.words_to_play[self.words_played].upper()
        self.scrambled_word = scramble_word(self.current_word)
        
        # Reset word state
        self.hint_level = 0
        self.attempts = 0
        
        # Calculate base points
        self.base_points = len(self.current_word) * self.level * 10
        
        # Update UI
        self.scrambled_label.config(text=self.scrambled_word)
        self.hint_label.config(text="")
        self.feedback_label.config(text="")
        self.progress_label.config(text=f"Word {self.words_played + 1} of {len(self.words_to_play)}")
        self.attempts_label.config(text=f"Attempts: 0/{self.max_attempts}")
        
        # Clear answer entry and set focus
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.focus_set()
        
        # Increment words played counter
        self.words_played += 1
    
    def request_hint(self):
        """Provide a hint for the current word."""
        if self.hint_level < 3:
            self.hint_level += 1
            
            # Provide a hint
            hint_text = get_hint(self.current_word, self.hint_level)
            self.hint_label.config(text=hint_text)
            
            # Reduce points for using a hint
            self.base_points = max(self.base_points // 2, 5)
            
            # Update feedback
            self.feedback_label.config(
                text="Hint provided. Points have been reduced.",
                fg="#FFFF99"  # Yellow
            )
        else:
            self.feedback_label.config(
                text="You've used all available hints for this word.",
                fg="#FF6666"  # Red
            )
    
    def check_answer(self, event=None):
        """Check the player's answer."""
        answer = self.answer_entry.get().upper().strip()
        
        if not answer:
            self.feedback_label.config(
                text="Please enter an answer.",
                fg="#FF6666"  # Red
            )
            return
        
        # Increment attempts
        self.attempts += 1
        self.attempts_label.config(text=f"Attempts: {self.attempts}/{self.max_attempts}")
        
        # Check if answer is correct
        if answer == self.current_word:
            # Calculate points (reduced for each attempt and hint)
            points = max(self.base_points - ((self.attempts - 1) * (self.base_points // 4)), 5)
            self.score += points
            
            # Update score display
            self.score_label.config(text=f"Score: {self.score}")
            
            # Show success feedback
            self.feedback_label.config(
                text=f"Correct! You earned {points} points.",
                fg="#CCFF99"  # Green
            )
            
            # Disable inputs temporarily 
            self.answer_entry.config(state=tk.DISABLED)
            self.submit_button.config(state=tk.DISABLED)
            self.hint_button.config(state=tk.DISABLED)
            self.skip_button.config(state=tk.DISABLED)
            
            # Move to next word after a delay
            self.root.after(2000, self.enable_controls_and_next_word)
        else:
            if self.attempts >= self.max_attempts:
                # Failed all attempts
                self.feedback_label.config(
                    text=f"Out of attempts! The correct word was: {self.current_word}",
                    fg="#FF6666"  # Red
                )
                
                # Disable inputs temporarily
                self.answer_entry.config(state=tk.DISABLED)
                self.submit_button.config(state=tk.DISABLED)
                self.hint_button.config(state=tk.DISABLED)
                self.skip_button.config(state=tk.DISABLED)
                
                # Move to next word after a delay
                self.root.after(2000, self.enable_controls_and_next_word)
            else:
                # Still have attempts left
                self.feedback_label.config(
                    text=f"Incorrect. Try again! {self.max_attempts - self.attempts} attempts remaining.",
                    fg="#FF6666"  # Red
                )
                
                # Clear answer entry and set focus
                self.answer_entry.delete(0, tk.END)
                self.answer_entry.focus_set()
    
    def enable_controls_and_next_word(self):
        """Enable controls and move to the next word."""
        self.answer_entry.config(state=tk.NORMAL)
        self.submit_button.config(state=tk.NORMAL)
        self.hint_button.config(state=tk.NORMAL)
        self.skip_button.config(state=tk.NORMAL)
        self.next_word()
    
    def skip_word(self):
        """Skip the current word."""
        # Show the correct word
        self.feedback_label.config(
            text=f"Word skipped. The correct word was: {self.current_word}",
            fg="#FFFF99"  # Yellow
        )
        
        # Disable inputs temporarily
        self.answer_entry.config(state=tk.DISABLED)
        self.submit_button.config(state=tk.DISABLED)
        self.hint_button.config(state=tk.DISABLED)
        self.skip_button.config(state=tk.DISABLED)
        
        # Move to next word after a delay
        self.root.after(2000, self.enable_controls_and_next_word)
    
    def show_results(self):
        """Show the final results."""
        # Hide game elements
        self.scrambled_label.config(text="")
        self.hint_label.config(text="")
        self.progress_label.config(text="")
        self.attempts_label.config(text="")
        
        # Disable controls
        self.answer_entry.config(state=tk.DISABLED)
        self.submit_button.config(state=tk.DISABLED)
        self.hint_button.config(state=tk.DISABLED)
        self.skip_button.config(state=tk.DISABLED)
        
        # Calculate percentage score
        max_possible = sum(len(w) * self.level * 10 for w in self.words_to_play)
        percentage = (self.score / max_possible) * 100 if max_possible > 0 else 0
        
        # Determine feedback based on score
        if percentage >= 90:
            feedback = "Outstanding! You're a word wizard!"
            color = "#FF99FF"  # Magenta
        elif percentage >= 70:
            feedback = "Great job! You have exceptional vocabulary skills!"
            color = "#CCFF99"  # Green
        elif percentage >= 50:
            feedback = "Good effort! Your word skills are solid."
            color = "#FFFF99"  # Yellow
        elif percentage >= 30:
            feedback = "Not bad, keep practicing to improve your vocabulary."
            color = "#FFFF99"  # Yellow
        else:
            feedback = "Better luck next time! Try an easier level or use hints."
            color = "#FF6666"  # Red
        
        # Show results
        self.title_label.config(text="Game Complete!")
        result_text = f"Final Score: {self.score} points ({percentage:.1f}%)\n\n{feedback}"
        self.feedback_label.config(text=result_text, fg=color)
    
    def quit_game(self):
        """Quit the game."""
        if messagebox.askyesno("Quit Game", "Are you sure you want to quit?"):
            self.root.destroy()

def main():
    """Main function to start the GUI game."""
    root = tk.Tk()
    
    # Configure style for slider
    style = ttk.Style()
    style.theme_use('default')
    style.configure("TScale", background="#222222", troughcolor="#111111")
    
    app = WordScrambleGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 