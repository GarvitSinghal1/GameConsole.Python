#!/usr/bin/env python3
import random
import tkinter as tk
from tkinter import ttk, messagebox

class NumberGuesserGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guesser")
        self.root.geometry("500x400")
        self.root.configure(bg="#333333")
        self.root.resizable(True, True)
        
        # Set minimum window size
        self.root.minsize(400, 300)
        
        # Game variables
        self.secret_number = random.randint(1, 100)
        self.guesses_taken = 0
        self.max_guesses = 10
        self.game_over = False
        
        # Create UI elements
        self.create_widgets()
        
        # Start with game instructions
        self.show_instructions()
    
    def create_widgets(self):
        """Create the GUI widgets."""
        # Main frame
        main_frame = tk.Frame(self.root, bg="#333333")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title label
        title_label = tk.Label(
            main_frame, 
            text="Number Guesser", 
            font=("Helvetica", 24, "bold"),
            bg="#333333",
            fg="#FF99FF"  # Magenta
        )
        title_label.pack(pady=(0, 10))
        
        # Instructions/feedback text
        self.feedback_text = tk.Text(
            main_frame, 
            wrap=tk.WORD, 
            font=("Helvetica", 12),
            width=40,
            height=8,
            bg="#111111",
            fg="#FFFFFF",
            relief=tk.RIDGE,
            padx=10,
            pady=10
        )
        self.feedback_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.feedback_text.config(state=tk.DISABLED)  # Make read-only initially
        
        # Guess input frame
        guess_frame = tk.Frame(main_frame, bg="#333333")
        guess_frame.pack(fill=tk.X, pady=10)
        
        # Guess label
        guess_label = tk.Label(
            guess_frame, 
            text="Enter your guess (1-100):", 
            font=("Helvetica", 12),
            bg="#333333",
            fg="#FFFFFF"
        )
        guess_label.pack(side=tk.LEFT, padx=5)
        
        # Guess entry
        vcmd = (self.root.register(self.validate_input), '%P')
        self.guess_entry = tk.Entry(
            guess_frame,
            font=("Helvetica", 12),
            width=5,
            bg="#111111",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
            validate="key",
            validatecommand=vcmd
        )
        self.guess_entry.pack(side=tk.LEFT, padx=5)
        self.guess_entry.bind("<Return>", self.check_guess)
        self.guess_entry.focus_set()  # Set focus to entry
        
        # Guess button
        self.guess_button = tk.Button(
            guess_frame, 
            text="Guess", 
            command=self.check_guess,
            bg="#FF99FF",  # Magenta
            fg="#000000",
            activebackground="#CC66CC",
            activeforeground="#FFFFFF",
            font=("Helvetica", 12, "bold"),
            width=10
        )
        self.guess_button.pack(side=tk.LEFT, padx=5)
        
        # Progress frame
        progress_frame = tk.Frame(main_frame, bg="#333333")
        progress_frame.pack(fill=tk.X, pady=5)
        
        # Attempts label
        self.attempts_label = tk.Label(
            progress_frame, 
            text=f"Guesses: 0/{self.max_guesses}", 
            font=("Helvetica", 12),
            bg="#333333",
            fg="#FFFFFF"
        )
        self.attempts_label.pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress_var = tk.IntVar(value=0)
        self.progress_bar = ttk.Progressbar(
            progress_frame, 
            orient=tk.HORIZONTAL, 
            length=200, 
            mode='determinate',
            variable=self.progress_var,
            maximum=self.max_guesses
        )
        self.progress_bar.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg="#333333")
        buttons_frame.pack(fill=tk.X, pady=10)
        
        # New Game button
        self.new_game_button = tk.Button(
            buttons_frame, 
            text="New Game", 
            command=self.new_game,
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
            buttons_frame, 
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
        
        # Configure tag colors for text highlighting
        self.feedback_text.tag_configure("normal", foreground="#FFFFFF")
        self.feedback_text.tag_configure("success", foreground="#CCFF99")  # Green
        self.feedback_text.tag_configure("info", foreground="#66CCFF")  # Blue
        self.feedback_text.tag_configure("warning", foreground="#FFFF99")  # Yellow
        self.feedback_text.tag_configure("error", foreground="#FF6666")  # Red
        self.feedback_text.tag_configure("bold", font=("Helvetica", 12, "bold"))
        self.feedback_text.tag_configure("title", font=("Helvetica", 14, "bold"), foreground="#FF99FF")  # Magenta
    
    def show_instructions(self):
        """Display the game instructions."""
        self.write_text("Welcome to Number Guesser!", "title")
        self.write_text("\nI'm thinking of a number between 1 and 100.")
        self.write_text("Can you guess it in 10 tries or fewer?")
        self.write_text("\nEnter your guess below and click 'Guess' or press Enter.")
    
    def validate_input(self, text):
        """Validate the input to allow only numbers."""
        if text == "":
            return True
        try:
            num = int(text)
            return 1 <= num <= 100
        except ValueError:
            return False
    
    def write_text(self, text, tag="normal"):
        """Write text to the feedback text area with the specified tag."""
        self.feedback_text.config(state=tk.NORMAL)
        self.feedback_text.insert(tk.END, text + "\n", tag)
        self.feedback_text.see(tk.END)  # Scroll to the end
        self.feedback_text.config(state=tk.DISABLED)
    
    def check_guess(self, event=None):
        """Check the player's guess."""
        if self.game_over:
            return
        
        # Get the guess
        try:
            guess = int(self.guess_entry.get())
        except ValueError:
            self.write_text("Please enter a valid number between 1 and 100.", "error")
            return
        
        # Clear the entry
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus_set()
        
        # Update guesses taken
        self.guesses_taken += 1
        self.progress_var.set(self.guesses_taken)
        self.attempts_label.config(text=f"Guesses: {self.guesses_taken}/{self.max_guesses}")
        
        # Check the guess
        if guess < self.secret_number:
            self.write_text(f"Guess #{self.guesses_taken}: {guess} - Too low! Try a higher number.", "info")
        elif guess > self.secret_number:
            self.write_text(f"Guess #{self.guesses_taken}: {guess} - Too high! Try a lower number.", "warning")
        else:
            # Correct guess!
            self.write_text(f"Guess #{self.guesses_taken}: {guess} - That's correct!", "success")
            self.write_text("\nCongratulations! You guessed the number in " + str(self.guesses_taken) + " tries!", "success")
            
            if self.guesses_taken == 1:
                self.write_text("Incredible! A hole in one!", "success")
            elif self.guesses_taken <= 3:
                self.write_text("Impressive! You're a natural!", "success")
            elif self.guesses_taken <= 6:
                self.write_text("Well done! That was a good game!", "success")
            else:
                self.write_text("You got it just in time!", "success")
            
            self.game_over = True
            self.guess_button.config(state=tk.DISABLED)
            return
        
        # Check if the player has used all guesses
        if self.guesses_taken >= self.max_guesses:
            self.write_text("\nGame over! You've used all your guesses.", "error")
            self.write_text(f"The number I was thinking of was {self.secret_number}.", "info")
            self.game_over = True
            self.guess_button.config(state=tk.DISABLED)
    
    def new_game(self):
        """Start a new game."""
        # Reset game variables
        self.secret_number = random.randint(1, 100)
        self.guesses_taken = 0
        self.game_over = False
        
        # Reset UI
        self.progress_var.set(0)
        self.attempts_label.config(text=f"Guesses: 0/{self.max_guesses}")
        self.guess_button.config(state=tk.NORMAL)
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus_set()
        
        # Clear feedback text
        self.feedback_text.config(state=tk.NORMAL)
        self.feedback_text.delete(1.0, tk.END)
        self.feedback_text.config(state=tk.DISABLED)
        
        # Show instructions
        self.show_instructions()
    
    def quit_game(self):
        """Quit the game."""
        if messagebox.askyesno("Quit Game", "Are you sure you want to quit?"):
            self.root.destroy()

def main():
    """Main function to start the GUI game."""
    root = tk.Tk()
    
    # Set style for the progress bar
    style = ttk.Style()
    style.theme_use('default')
    style.configure("TProgressbar", thickness=20, background='#FF99FF')  # Magenta
    
    app = NumberGuesserGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 