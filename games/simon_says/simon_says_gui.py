#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
import sys
import os

class SimonSaysGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simon Says")
        self.root.geometry("600x650")
        self.root.configure(bg="#333333")
        self.root.resizable(True, True)
        
        # Game parameters
        self.difficulty = "medium"  # Default difficulty
        self.sequence = []
        self.player_sequence = []
        self.current_index = 0
        self.score = 0
        self.game_active = False
        self.player_turn = False
        self.animation_in_progress = False
        
        # Difficulty settings
        self.difficulty_settings = {
            "easy": {"display_time": 1000, "pause_time": 500, "timeout": 0},  # 0 means no timeout
            "medium": {"display_time": 800, "pause_time": 400, "timeout": 5000},
            "hard": {"display_time": 500, "pause_time": 300, "timeout": 3000}
        }
        
        # Button colors
        self.button_colors = {
            "red": {"bg": "#FF0000", "active_bg": "#FF6666", "flash_bg": "#FF9999"},
            "green": {"bg": "#00FF00", "active_bg": "#66FF66", "flash_bg": "#99FF99"},
            "blue": {"bg": "#0000FF", "active_bg": "#6666FF", "flash_bg": "#9999FF"},
            "yellow": {"bg": "#FFFF00", "active_bg": "#FFFF66", "flash_bg": "#FFFF99"}
        }
        
        # Create widgets
        self.create_widgets()
        
        # Show welcome screen
        self.show_welcome()
    
    def create_widgets(self):
        """Create the GUI widgets."""
        # Main frame
        self.main_frame = tk.Frame(self.root, bg="#333333")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title label
        self.title_label = tk.Label(
            self.main_frame,
            text="SIMON SAYS",
            font=("Helvetica", 24, "bold"),
            bg="#333333",
            fg="#FFFFFF"
        )
        self.title_label.pack(pady=(0, 20))
        
        # Game info frame
        self.info_frame = tk.Frame(self.main_frame, bg="#333333")
        self.info_frame.pack(fill=tk.X, pady=10)
        
        # Score label
        self.score_var = tk.StringVar(value="Score: 0")
        self.score_label = tk.Label(
            self.info_frame,
            textvariable=self.score_var,
            font=("Helvetica", 14),
            bg="#333333",
            fg="#FFFFFF"
        )
        self.score_label.pack(side=tk.LEFT, padx=10)
        
        # Status label
        self.status_var = tk.StringVar(value="Press Start to begin")
        self.status_label = tk.Label(
            self.info_frame,
            textvariable=self.status_var,
            font=("Helvetica", 14),
            bg="#333333",
            fg="#FFFFFF"
        )
        self.status_label.pack(side=tk.RIGHT, padx=10)
        
        # Game buttons frame
        self.buttons_frame = tk.Frame(self.main_frame, bg="#333333")
        self.buttons_frame.pack(pady=20)
        
        # Create the four colored buttons
        self.game_buttons = {}
        
        # Red button (top-left)
        self.game_buttons["red"] = tk.Button(
            self.buttons_frame,
            text="",
            width=15,
            height=7,
            bg=self.button_colors["red"]["bg"],
            activebackground=self.button_colors["red"]["active_bg"],
            relief=tk.RAISED,
            command=lambda: self.handle_button_press("red")
        )
        self.game_buttons["red"].grid(row=0, column=0, padx=5, pady=5)
        
        # Green button (top-right)
        self.game_buttons["green"] = tk.Button(
            self.buttons_frame,
            text="",
            width=15,
            height=7,
            bg=self.button_colors["green"]["bg"],
            activebackground=self.button_colors["green"]["active_bg"],
            relief=tk.RAISED,
            command=lambda: self.handle_button_press("green")
        )
        self.game_buttons["green"].grid(row=0, column=1, padx=5, pady=5)
        
        # Blue button (bottom-left)
        self.game_buttons["blue"] = tk.Button(
            self.buttons_frame,
            text="",
            width=15,
            height=7,
            bg=self.button_colors["blue"]["bg"],
            activebackground=self.button_colors["blue"]["active_bg"],
            relief=tk.RAISED,
            command=lambda: self.handle_button_press("blue")
        )
        self.game_buttons["blue"].grid(row=1, column=0, padx=5, pady=5)
        
        # Yellow button (bottom-right)
        self.game_buttons["yellow"] = tk.Button(
            self.buttons_frame,
            text="",
            width=15,
            height=7,
            bg=self.button_colors["yellow"]["bg"],
            activebackground=self.button_colors["yellow"]["active_bg"],
            relief=tk.RAISED,
            command=lambda: self.handle_button_press("yellow")
        )
        self.game_buttons["yellow"].grid(row=1, column=1, padx=5, pady=5)
        
        # Difficulty selection frame
        self.difficulty_frame = tk.Frame(self.main_frame, bg="#333333")
        self.difficulty_frame.pack(fill=tk.X, pady=10)
        
        # Difficulty label
        self.difficulty_label = tk.Label(
            self.difficulty_frame,
            text="Difficulty:",
            font=("Helvetica", 12),
            bg="#333333",
            fg="#FFFFFF"
        )
        self.difficulty_label.pack(side=tk.LEFT, padx=10)
        
        # Difficulty radio buttons
        self.difficulty_var = tk.StringVar(value=self.difficulty)
        
        self.easy_radio = tk.Radiobutton(
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
        
        self.medium_radio = tk.Radiobutton(
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
        
        self.hard_radio = tk.Radiobutton(
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
        
        # Control buttons frame
        self.control_frame = tk.Frame(self.main_frame, bg="#333333")
        self.control_frame.pack(fill=tk.X, pady=20)
        
        # Start button
        self.start_button = tk.Button(
            self.control_frame,
            text="Start Game",
            font=("Helvetica", 12),
            bg="#4CAF50",
            fg="white",
            command=self.start_game
        )
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        # Quit button
        self.quit_button = tk.Button(
            self.control_frame,
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
        welcome_window.title("Welcome to Simon Says")
        welcome_window.geometry("500x400")
        welcome_window.configure(bg="#333333")
        welcome_window.transient(self.root)
        welcome_window.grab_set()
        welcome_window.resizable(True, True)
        
        # Welcome title
        welcome_label = tk.Label(
            welcome_window,
            text="Welcome to Simon Says",
            font=("Helvetica", 18, "bold"),
            bg="#333333",
            fg="#FFFFFF"
        )
        welcome_label.pack(pady=20)
        
        # Instructions
        instructions_frame = tk.Frame(welcome_window, bg="#333333", padx=20)
        instructions_frame.pack(fill=tk.BOTH, expand=True)
        
        instructions = [
            "Simon Says is a memory game where you need to repeat",
            "a growing sequence of colored buttons.",
            "",
            "How to play:",
            "1. Watch the sequence of colors",
            "2. Repeat the sequence by clicking the buttons in the same order",
            "3. Each round adds one more color to the sequence",
            "4. The game ends when you make a mistake or run out of time",
            "",
            "Difficulty levels:",
            "• Easy: Slow sequence, no time limit",
            "• Medium: Medium speed, 5 seconds per input",
            "• Hard: Fast sequence, 3 seconds per input",
            "",
            "Try to achieve the highest score possible!"
        ]
        
        for line in instructions:
            tk.Label(
                instructions_frame,
                text=line,
                font=("Helvetica", 12),
                bg="#333333",
                fg="#FFFFFF",
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
        self.difficulty = self.difficulty_var.get()
        
        # Update status message
        if not self.game_active:
            self.status_var.set(f"Difficulty set to {self.difficulty.capitalize()}")
    
    def start_game(self):
        """Start a new game."""
        if self.game_active and not messagebox.askyesno("New Game", "Are you sure you want to start a new game?"):
            return
        
        # Reset game state
        self.sequence = []
        self.player_sequence = []
        self.current_index = 0
        self.score = 0
        self.score_var.set("Score: 0")
        self.game_active = True
        self.player_turn = False
        
        # Disable difficulty selection during game
        self.easy_radio.config(state=tk.DISABLED)
        self.medium_radio.config(state=tk.DISABLED)
        self.hard_radio.config(state=tk.DISABLED)
        
        # Change start button to restart
        self.start_button.config(text="Restart Game")
        
        # Start the first round
        self.next_round()
    
    def next_round(self):
        """Start the next round by adding a new color to the sequence."""
        # Add a new random color to the sequence
        colors = ["red", "green", "blue", "yellow"]
        self.sequence.append(random.choice(colors))
        
        # Update status
        self.status_var.set("Watch the sequence...")
        
        # Schedule the sequence display
        self.root.after(1000, self.play_sequence)
    
    def play_sequence(self):
        """Display the sequence to the player."""
        self.animation_in_progress = True
        self.current_index = 0
        self.show_next_in_sequence()
    
    def show_next_in_sequence(self):
        """Show the next color in the sequence."""
        if self.current_index < len(self.sequence):
            color = self.sequence[self.current_index]
            self.flash_button(color)
            self.current_index += 1
            
            # Schedule the next color after a pause
            settings = self.difficulty_settings[self.difficulty]
            self.root.after(settings["display_time"] + settings["pause_time"], 
                           self.show_next_in_sequence)
        else:
            # Sequence complete, player's turn
            self.animation_in_progress = False
            self.start_player_turn()
    
    def flash_button(self, color):
        """Flash a button to indicate it's part of the sequence."""
        button = self.game_buttons[color]
        original_bg = button.cget("bg")
        flash_bg = self.button_colors[color]["flash_bg"]
        
        # Change to flash color
        button.config(bg=flash_bg)
        
        # Schedule change back to original color
        settings = self.difficulty_settings[self.difficulty]
        self.root.after(settings["display_time"], lambda: button.config(bg=original_bg))
    
    def start_player_turn(self):
        """Start the player's turn to repeat the sequence."""
        self.player_sequence = []
        self.player_turn = True
        self.status_var.set("Your turn! Repeat the sequence.")
        
        # Start timeout timer if applicable
        settings = self.difficulty_settings[self.difficulty]
        if settings["timeout"] > 0:
            self.timeout_id = self.root.after(settings["timeout"], self.handle_timeout)
    
    def handle_button_press(self, color):
        """Handle a button press during the player's turn."""
        if not self.player_turn or self.animation_in_progress:
            return
        
        # Flash the button
        self.flash_button(color)
        
        # Add to player sequence
        self.player_sequence.append(color)
        
        # Check if the input is correct so far
        current_index = len(self.player_sequence) - 1
        if self.player_sequence[current_index] != self.sequence[current_index]:
            # Wrong input
            self.game_over(False)
            return
        
        # Cancel timeout timer and restart it for the next input
        settings = self.difficulty_settings[self.difficulty]
        if settings["timeout"] > 0:
            self.root.after_cancel(self.timeout_id)
            if len(self.player_sequence) < len(self.sequence):
                self.timeout_id = self.root.after(settings["timeout"], self.handle_timeout)
        
        # Check if the sequence is complete
        if len(self.player_sequence) == len(self.sequence):
            # Correct sequence
            self.player_turn = False
            self.score = len(self.sequence)
            self.score_var.set(f"Score: {self.score}")
            self.status_var.set("Correct! Get ready for the next sequence...")
            
            # Start the next round after a delay
            self.root.after(1500, self.next_round)
    
    def handle_timeout(self):
        """Handle a timeout during the player's turn."""
        if self.player_turn:
            self.game_over(True)
    
    def game_over(self, timeout=False):
        """End the game."""
        self.game_active = False
        self.player_turn = False
        
        # Show game over message
        if timeout:
            messagebox.showinfo("Game Over", f"Time's up! Your final score: {self.score}")
            self.status_var.set("Game Over - Time's up!")
        else:
            messagebox.showinfo("Game Over", f"Wrong sequence! Your final score: {self.score}")
            self.status_var.set("Game Over - Wrong sequence!")
        
        # Re-enable difficulty selection
        self.easy_radio.config(state=tk.NORMAL)
        self.medium_radio.config(state=tk.NORMAL)
        self.hard_radio.config(state=tk.NORMAL)
        
        # Change restart button back to start
        self.start_button.config(text="Start Game")
    
    def quit_game(self):
        """Quit the game."""
        if messagebox.askyesno("Quit", "Are you sure you want to quit the game?"):
            self.root.destroy()

def main():
    """Main function to start the GUI game."""
    root = tk.Tk()
    app = SimonSaysGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 