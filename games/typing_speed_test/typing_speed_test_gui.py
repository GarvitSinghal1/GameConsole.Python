#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import time
import random
import sys
import os

# Import word lists and paragraphs from terminal version
try:
    from games.typing_speed_test import EASY_WORDS, MEDIUM_WORDS, HARD_WORDS, PARAGRAPHS
except ImportError:
    # Fallback word lists if import fails
    EASY_WORDS = ["the", "and", "for", "are", "but", "not", "you", "all", "any", "can"]
    MEDIUM_WORDS = ["about", "after", "again", "along", "began", "below", "between", "thing"]
    HARD_WORDS = ["necessary", "according", "especially", "technology", "relationship"]
    PARAGRAPHS = ["The quick brown fox jumps over the lazy dog."]

class TypingSpeedTestGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("800x600")
        self.root.configure(bg="#2c3e50")
        self.root.resizable(True, True)
        
        # Test variables
        self.test_type = "word"  # "word" or "paragraph"
        self.difficulty = "medium"  # "easy", "medium", or "hard"
        self.test_text = ""
        self.start_time = 0
        self.is_test_running = False
        self.test_complete = False
        
        # Colors
        self.colors = {
            "bg": "#2c3e50",
            "text": "#ecf0f1",
            "accent": "#3498db",
            "correct": "#2ecc71",
            "incorrect": "#e74c3c",
            "button": "#2980b9",
            "button_text": "#ffffff"
        }
        
        # Create widgets
        self.create_widgets()
        
        # Show welcome screen
        self.show_welcome()
    
    def create_widgets(self):
        """Create the GUI widgets."""
        # Main frame
        self.main_frame = tk.Frame(self.root, bg=self.colors["bg"])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title label
        self.title_label = tk.Label(
            self.main_frame,
            text="Typing Speed Test",
            font=("Helvetica", 24, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["text"]
        )
        self.title_label.pack(pady=(0, 20))
        
        # Settings frame for test configuration
        self.settings_frame = tk.Frame(self.main_frame, bg=self.colors["bg"])
        self.settings_frame.pack(fill=tk.X, pady=10)
        
        # Test type selection
        self.test_type_label = tk.Label(
            self.settings_frame,
            text="Test Type:",
            font=("Helvetica", 12),
            bg=self.colors["bg"],
            fg=self.colors["text"]
        )
        self.test_type_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        
        self.test_type_var = tk.StringVar(value="word")
        self.word_test_radio = tk.Radiobutton(
            self.settings_frame,
            text="Word Test",
            variable=self.test_type_var,
            value="word",
            command=self.update_settings,
            bg=self.colors["bg"],
            fg=self.colors["text"],
            selectcolor=self.colors["accent"],
            activebackground=self.colors["bg"],
            activeforeground=self.colors["text"]
        )
        self.word_test_radio.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        
        self.paragraph_test_radio = tk.Radiobutton(
            self.settings_frame,
            text="Paragraph Test",
            variable=self.test_type_var,
            value="paragraph",
            command=self.update_settings,
            bg=self.colors["bg"],
            fg=self.colors["text"],
            selectcolor=self.colors["accent"],
            activebackground=self.colors["bg"],
            activeforeground=self.colors["text"]
        )
        self.paragraph_test_radio.grid(row=0, column=2, padx=10, pady=5, sticky=tk.W)
        
        # Difficulty selection (enabled only for word test)
        self.difficulty_label = tk.Label(
            self.settings_frame,
            text="Difficulty:",
            font=("Helvetica", 12),
            bg=self.colors["bg"],
            fg=self.colors["text"]
        )
        self.difficulty_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        
        self.difficulty_var = tk.StringVar(value="medium")
        self.easy_radio = tk.Radiobutton(
            self.settings_frame,
            text="Easy",
            variable=self.difficulty_var,
            value="easy",
            bg=self.colors["bg"],
            fg=self.colors["text"],
            selectcolor=self.colors["accent"],
            activebackground=self.colors["bg"],
            activeforeground=self.colors["text"]
        )
        self.easy_radio.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)
        
        self.medium_radio = tk.Radiobutton(
            self.settings_frame,
            text="Medium",
            variable=self.difficulty_var,
            value="medium",
            bg=self.colors["bg"],
            fg=self.colors["text"],
            selectcolor=self.colors["accent"],
            activebackground=self.colors["bg"],
            activeforeground=self.colors["text"]
        )
        self.medium_radio.grid(row=1, column=2, padx=10, pady=5, sticky=tk.W)
        
        self.hard_radio = tk.Radiobutton(
            self.settings_frame,
            text="Hard",
            variable=self.difficulty_var,
            value="hard",
            bg=self.colors["bg"],
            fg=self.colors["text"],
            selectcolor=self.colors["accent"],
            activebackground=self.colors["bg"],
            activeforeground=self.colors["text"]
        )
        self.hard_radio.grid(row=1, column=3, padx=10, pady=5, sticky=tk.W)
        
        # Start button
        self.start_button = tk.Button(
            self.settings_frame,
            text="Start Test",
            font=("Helvetica", 12, "bold"),
            bg=self.colors["button"],
            fg=self.colors["button_text"],
            command=self.start_test,
            padx=20,
            pady=5
        )
        self.start_button.grid(row=2, column=0, columnspan=4, pady=15)
        
        # Text display frame
        self.text_frame = tk.Frame(self.main_frame, bg=self.colors["bg"])
        self.text_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Test text display
        self.text_display = scrolledtext.ScrolledText(
            self.text_frame,
            font=("Courier", 14),
            wrap=tk.WORD,
            bg="#34495e",
            fg=self.colors["text"],
            height=5,
            state=tk.DISABLED
        )
        self.text_display.pack(fill=tk.X, expand=True, padx=5, pady=5)
        
        # User input text box
        self.input_text = scrolledtext.ScrolledText(
            self.text_frame,
            font=("Courier", 14),
            wrap=tk.WORD,
            bg="#34495e",
            fg=self.colors["correct"],
            height=5,
            state=tk.DISABLED
        )
        self.input_text.pack(fill=tk.X, expand=True, padx=5, pady=5)
        
        # Timer label
        self.timer_label = tk.Label(
            self.text_frame,
            text="Time: 0.0 seconds",
            font=("Helvetica", 12),
            bg=self.colors["bg"],
            fg=self.colors["text"]
        )
        self.timer_label.pack(pady=5)
        
        # Results frame
        self.results_frame = tk.Frame(self.main_frame, bg=self.colors["bg"])
        self.results_frame.pack(fill=tk.X, pady=10)
        
        # Create results labels
        self.wpm_label = tk.Label(
            self.results_frame,
            text="WPM: 0",
            font=("Helvetica", 16, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["text"]
        )
        self.wpm_label.pack(side=tk.LEFT, padx=20)
        
        self.accuracy_label = tk.Label(
            self.results_frame,
            text="Accuracy: 0%",
            font=("Helvetica", 16, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["text"]
        )
        self.accuracy_label.pack(side=tk.RIGHT, padx=20)
        
        # Feedback label
        self.feedback_label = tk.Label(
            self.main_frame,
            text="",
            font=("Helvetica", 14, "italic"),
            bg=self.colors["bg"],
            fg=self.colors["accent"]
        )
        self.feedback_label.pack(pady=10)
        
        # Control buttons at the bottom
        self.control_frame = tk.Frame(self.main_frame, bg=self.colors["bg"])
        self.control_frame.pack(fill=tk.X, pady=10)
        
        # New test button
        self.new_test_button = tk.Button(
            self.control_frame,
            text="New Test",
            font=("Helvetica", 12),
            bg=self.colors["button"],
            fg=self.colors["button_text"],
            command=self.reset_test,
            state=tk.DISABLED
        )
        self.new_test_button.pack(side=tk.LEFT, padx=10)
        
        # Quit button
        self.quit_button = tk.Button(
            self.control_frame,
            text="Quit",
            font=("Helvetica", 12),
            bg="#e74c3c",
            fg=self.colors["button_text"],
            command=self.quit_game
        )
        self.quit_button.pack(side=tk.RIGHT, padx=10)
        
        # Set up timer update
        self.update_timer_id = None
    
    def show_welcome(self):
        """Show welcome screen and instructions."""
        welcome_window = tk.Toplevel(self.root)
        welcome_window.title("Welcome to Typing Speed Test")
        welcome_window.geometry("500x400")
        welcome_window.configure(bg=self.colors["bg"])
        welcome_window.transient(self.root)
        welcome_window.grab_set()
        welcome_window.resizable(True, True)
        
        # Welcome title
        welcome_label = tk.Label(
            welcome_window,
            text="Welcome to Typing Speed Test",
            font=("Helvetica", 18, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["text"]
        )
        welcome_label.pack(pady=20)
        
        # Instructions
        instructions_frame = tk.Frame(welcome_window, bg=self.colors["bg"], padx=20)
        instructions_frame.pack(fill=tk.BOTH, expand=True)
        
        instructions = [
            "This is a typing speed test to measure your typing",
            "speed and accuracy. You can choose between:",
            "",
            "1. Word Test - Type a series of random words",
            "   (Easy, Medium, or Hard difficulty)",
            "",
            "2. Paragraph Test - Type a complete paragraph",
            "",
            "Your results will be measured in:",
            "• WPM (Words Per Minute)",
            "• Accuracy Percentage",
            "",
            "When you're ready to start, click the Start Test button."
        ]
        
        for line in instructions:
            tk.Label(
                instructions_frame,
                text=line,
                font=("Helvetica", 12),
                bg=self.colors["bg"],
                fg=self.colors["text"],
                justify=tk.LEFT
            ).pack(anchor=tk.W, pady=1)
        
        # Start button
        start_button = tk.Button(
            welcome_window,
            text="Continue",
            font=("Helvetica", 14, "bold"),
            bg=self.colors["button"],
            fg=self.colors["button_text"],
            command=welcome_window.destroy,
            padx=20,
            pady=5
        )
        start_button.pack(pady=20)
    
    def update_settings(self):
        """Update UI based on selected test type."""
        test_type = self.test_type_var.get()
        
        # Enable/disable difficulty selection based on test type
        if test_type == "word":
            self.difficulty_label.config(state=tk.NORMAL)
            self.easy_radio.config(state=tk.NORMAL)
            self.medium_radio.config(state=tk.NORMAL)
            self.hard_radio.config(state=tk.NORMAL)
        else:
            self.difficulty_label.config(state=tk.DISABLED)
            self.easy_radio.config(state=tk.DISABLED)
            self.medium_radio.config(state=tk.DISABLED)
            self.hard_radio.config(state=tk.DISABLED)
    
    def generate_word_test(self, difficulty, num_words=20):
        """Generate a list of random words based on difficulty."""
        if difficulty == "easy":
            return random.sample(EASY_WORDS * 3, num_words)
        elif difficulty == "medium":
            return random.sample(MEDIUM_WORDS * 2, num_words)
        else:  # hard
            return random.sample(HARD_WORDS + MEDIUM_WORDS, num_words)
    
    def start_test(self):
        """Start the typing test."""
        self.test_type = self.test_type_var.get()
        self.difficulty = self.difficulty_var.get()
        
        # Generate test text
        if self.test_type == "word":
            words = self.generate_word_test(self.difficulty, 20)
            self.test_text = " ".join(words)
        else:  # paragraph
            self.test_text = random.choice(PARAGRAPHS)
        
        # Display the test text
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(tk.END, self.test_text)
        self.text_display.config(state=tk.DISABLED)
        
        # Enable input and set focus
        self.input_text.config(state=tk.NORMAL)
        self.input_text.delete(1.0, tk.END)
        self.input_text.focus_set()
        
        # Start the timer
        self.start_time = time.time()
        self.is_test_running = True
        self.test_complete = False
        self.update_timer()
        
        # Update UI
        self.start_button.config(state=tk.DISABLED)
        self.word_test_radio.config(state=tk.DISABLED)
        self.paragraph_test_radio.config(state=tk.DISABLED)
        
        # Bind to key events to detect completion
        self.input_text.bind("<KeyRelease>", self.check_completion)
    
    def update_timer(self):
        """Update the timer display."""
        if self.is_test_running:
            elapsed_time = time.time() - self.start_time
            self.timer_label.config(text=f"Time: {elapsed_time:.1f} seconds")
            
            # Update timer every 100ms
            self.update_timer_id = self.root.after(100, self.update_timer)
    
    def check_completion(self, event=None):
        """Check if the test is complete based on user input."""
        if not self.is_test_running or self.test_complete:
            return
        
        # Get user input
        user_text = self.input_text.get(1.0, tk.END).strip()
        
        # Check if the user has typed the full test text (or pressed Enter on the last line)
        if event and event.keysym == "Return" and len(user_text) >= len(self.test_text):
            self.complete_test()
        
        # Highlight correct/incorrect characters as they type
        self.highlight_text()
    
    def highlight_text(self):
        """Highlight text as correct or incorrect while typing."""
        user_text = self.input_text.get(1.0, tk.END).strip()
        test_text = self.test_text
        
        # Reset all formatting
        self.input_text.tag_remove("correct", "1.0", tk.END)
        self.input_text.tag_remove("incorrect", "1.0", tk.END)
        
        # Configure tags
        self.input_text.tag_configure("correct", foreground=self.colors["correct"])
        self.input_text.tag_configure("incorrect", foreground=self.colors["incorrect"])
        
        # Apply formatting to each character
        for i in range(min(len(user_text), len(test_text))):
            if user_text[i] == test_text[i]:
                self.input_text.tag_add("correct", f"1.{i}", f"1.{i+1}")
            else:
                self.input_text.tag_add("incorrect", f"1.{i}", f"1.{i+1}")
    
    def complete_test(self):
        """Complete the test and calculate results."""
        # Stop the timer
        self.is_test_running = False
        self.test_complete = True
        elapsed_time = time.time() - self.start_time
        
        if self.update_timer_id:
            self.root.after_cancel(self.update_timer_id)
        
        # Get user input
        user_text = self.input_text.get(1.0, tk.END).strip()
        
        # Calculate results
        wpm = self.calculate_wpm(len(user_text), elapsed_time)
        accuracy = self.calculate_accuracy(self.test_text, user_text)
        
        # Update results display
        self.wpm_label.config(text=f"WPM: {wpm}")
        self.accuracy_label.config(text=f"Accuracy: {accuracy}%")
        
        # Provide feedback
        if wpm < 20:
            feedback = "Keep practicing! You're building a good foundation."
        elif wpm < 40:
            feedback = "Good job! You're approaching average typing speed."
        elif wpm < 60:
            feedback = "Nice work! You have a solid typing speed."
        elif wpm < 80:
            feedback = "Excellent! You're well above average typing speed."
        else:
            feedback = "Amazing! You're at professional typing level!"
        
        self.feedback_label.config(text=feedback)
        
        # Update UI
        self.input_text.config(state=tk.DISABLED)
        self.new_test_button.config(state=tk.NORMAL)
    
    def calculate_wpm(self, typed_chars, elapsed_time_sec):
        """Calculate words per minute (WPM) based on the standard 5 chars per word."""
        # Standard: 5 characters = 1 word
        words = typed_chars / 5
        minutes = elapsed_time_sec / 60
        return round(words / minutes) if minutes > 0 else 0
    
    def calculate_accuracy(self, original_text, typed_text):
        """Calculate accuracy percentage based on character-by-character comparison."""
        # Trim typed_text to the length of original_text to avoid penalizing for missing chars
        typed_text = typed_text[:len(original_text)]
        
        # Count correct characters
        correct_chars = sum(1 for a, b in zip(original_text, typed_text) if a == b)
        
        # Calculate accuracy
        accuracy = (correct_chars / len(original_text)) * 100 if original_text else 0
        return round(accuracy, 1)
    
    def reset_test(self):
        """Reset the test for a new attempt."""
        # Reset UI
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)
        self.text_display.config(state=tk.DISABLED)
        
        self.input_text.config(state=tk.NORMAL)
        self.input_text.delete(1.0, tk.END)
        self.input_text.config(state=tk.DISABLED)
        
        self.timer_label.config(text="Time: 0.0 seconds")
        self.wpm_label.config(text="WPM: 0")
        self.accuracy_label.config(text="Accuracy: 0%")
        self.feedback_label.config(text="")
        
        # Reset test state
        self.is_test_running = False
        self.test_complete = False
        
        # Re-enable test controls
        self.start_button.config(state=tk.NORMAL)
        self.word_test_radio.config(state=tk.NORMAL)
        self.paragraph_test_radio.config(state=tk.NORMAL)
        self.update_settings()  # Update UI based on current settings
        
        # Disable new test button
        self.new_test_button.config(state=tk.DISABLED)
    
    def quit_game(self):
        """Quit the game."""
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            # Cancel timer if running
            if self.update_timer_id:
                self.root.after_cancel(self.update_timer_id)
            self.root.destroy()

def main():
    """Main function to start the GUI game."""
    root = tk.Tk()
    app = TypingSpeedTestGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 