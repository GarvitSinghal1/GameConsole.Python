#!/usr/bin/env python3
import random
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import time

class RockPaperScissorsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors")
        self.root.geometry("700x500")
        self.root.configure(bg="#333333")
        self.root.resizable(True, True)
        
        # Set minimum window size
        self.root.minsize(650, 450)
        
        # Game variables
        self.player_score = 0
        self.computer_score = 0
        self.rounds_played = 0
        self.player_choice = None
        self.computer_choice = None
        self.choices = ["rock", "paper", "scissors"]
        
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
            text="Rock Paper Scissors", 
            font=("Helvetica", 24, "bold"),
            bg="#333333",
            fg="#FFFF99"  # Yellow
        )
        title_label.pack(pady=(0, 10))
        
        # Game area frame
        game_frame = tk.Frame(main_frame, bg="#333333")
        game_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Player and computer frames (side by side)
        player_frame = tk.Frame(game_frame, bg="#222222", borderwidth=2, relief=tk.RIDGE)
        player_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        computer_frame = tk.Frame(game_frame, bg="#222222", borderwidth=2, relief=tk.RIDGE)
        computer_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Player labels and choice display
        player_title = tk.Label(
            player_frame, 
            text="Player", 
            font=("Helvetica", 16, "bold"),
            bg="#222222",
            fg="#66CCFF"  # Blue
        )
        player_title.pack(pady=5)
        
        self.player_choice_label = tk.Label(
            player_frame,
            text="",
            font=("Helvetica", 14),
            bg="#222222",
            fg="#FFFFFF"
        )
        self.player_choice_label.pack(pady=5)
        
        self.player_image_label = tk.Label(
            player_frame,
            bg="#222222"
        )
        self.player_image_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Computer labels and choice display
        computer_title = tk.Label(
            computer_frame, 
            text="Computer", 
            font=("Helvetica", 16, "bold"),
            bg="#222222",
            fg="#FF6666"  # Red
        )
        computer_title.pack(pady=5)
        
        self.computer_choice_label = tk.Label(
            computer_frame,
            text="",
            font=("Helvetica", 14),
            bg="#222222",
            fg="#FFFFFF"
        )
        self.computer_choice_label.pack(pady=5)
        
        self.computer_image_label = tk.Label(
            computer_frame,
            bg="#222222"
        )
        self.computer_image_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Result display
        self.result_label = tk.Label(
            main_frame, 
            text="", 
            font=("Helvetica", 18, "bold"),
            bg="#333333",
            fg="#FFFFFF"
        )
        self.result_label.pack(pady=10)
        
        # Score frame
        score_frame = tk.Frame(main_frame, bg="#333333")
        score_frame.pack(fill=tk.X, pady=5)
        
        self.score_label = tk.Label(
            score_frame, 
            text="Player: 0  -  Computer: 0", 
            font=("Helvetica", 14),
            bg="#333333",
            fg="#CCFF99"  # Green
        )
        self.score_label.pack(side=tk.LEFT, padx=5)
        
        self.rounds_label = tk.Label(
            score_frame, 
            text="Rounds: 0", 
            font=("Helvetica", 14),
            bg="#333333",
            fg="#CCFF99"  # Green
        )
        self.rounds_label.pack(side=tk.RIGHT, padx=5)
        
        # Choice buttons frame
        buttons_frame = tk.Frame(main_frame, bg="#333333")
        buttons_frame.pack(fill=tk.X, pady=10)
        
        # Rock button
        self.rock_button = tk.Button(
            buttons_frame, 
            text="Rock", 
            command=lambda: self.play_round("rock"),
            bg="#FF6666",  # Red
            fg="#FFFFFF",
            activebackground="#CC3333",
            activeforeground="#FFFFFF",
            font=("Helvetica", 14, "bold"),
            width=10,
            height=2
        )
        self.rock_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Paper button
        self.paper_button = tk.Button(
            buttons_frame, 
            text="Paper", 
            command=lambda: self.play_round("paper"),
            bg="#66CCFF",  # Blue
            fg="#FFFFFF",
            activebackground="#3399CC",
            activeforeground="#FFFFFF",
            font=("Helvetica", 14, "bold"),
            width=10,
            height=2
        )
        self.paper_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Scissors button
        self.scissors_button = tk.Button(
            buttons_frame, 
            text="Scissors", 
            command=lambda: self.play_round("scissors"),
            bg="#CCFF99",  # Green
            fg="#000000",
            activebackground="#99CC66",
            activeforeground="#000000",
            font=("Helvetica", 14, "bold"),
            width=10,
            height=2
        )
        self.scissors_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Control buttons frame
        control_frame = tk.Frame(main_frame, bg="#333333")
        control_frame.pack(fill=tk.X, pady=5)
        
        # New Game button
        self.new_game_button = tk.Button(
            control_frame, 
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
        
        # Load images for Rock, Paper, Scissors
        self.load_images()
    
    def load_images(self):
        """Load and prepare images for the game."""
        self.images = {}
        
        # Try to create images directory if it doesn't exist
        images_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images")
        os.makedirs(images_dir, exist_ok=True)
        
        # Create placeholder images with text
        for choice in self.choices:
            img = tk.PhotoImage(width=150, height=150)
            self.images[choice] = img
        
        # Draw text on the placeholder images
        self.draw_text_on_image(self.images["rock"], "ROCK")
        self.draw_text_on_image(self.images["paper"], "PAPER")
        self.draw_text_on_image(self.images["scissors"], "SCISSORS")
        
        # Question mark image for initial state
        self.question_mark = tk.PhotoImage(width=150, height=150)
        self.draw_text_on_image(self.question_mark, "?")
        
        # Set initial images
        self.player_image_label.config(image=self.question_mark)
        self.computer_image_label.config(image=self.question_mark)
    
    def draw_text_on_image(self, image, text):
        """Draw text on a PhotoImage."""
        # Clear the image
        image.blank()
        
        # Get text dimensions
        text_width = len(text) * 10
        text_x = max(0, (150 - text_width) // 2)
        
        # Draw text
        for i, char in enumerate(text):
            x = text_x + i * 10
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    image.put("#000000", (x+dx, 75+dy))
            image.put("#FFFFFF", (x, 75))
    
    def show_instructions(self):
        """Display the game instructions."""
        messagebox.showinfo(
            "Rock Paper Scissors",
            "Welcome to Rock Paper Scissors!\n\n"
            "Click one of the three buttons at the bottom to make your choice.\n"
            "Rock beats Scissors, Scissors beats Paper, and Paper beats Rock.\n\n"
            "Good luck!"
        )
    
    def play_round(self, player_choice):
        """Play a round of the game."""
        self.player_choice = player_choice
        self.computer_choice = random.choice(self.choices)
        
        # Update the display
        self.player_choice_label.config(text=f"You chose: {player_choice.upper()}")
        self.player_image_label.config(image=self.images[player_choice])
        
        # Simulate computer "thinking"
        self.computer_choice_label.config(text="Computer is choosing...")
        self.root.update()
        time.sleep(0.5)
        
        self.computer_choice_label.config(text=f"Computer chose: {self.computer_choice.upper()}")
        self.computer_image_label.config(image=self.images[self.computer_choice])
        
        # Determine the winner
        result = self.get_winner(player_choice, self.computer_choice)
        
        if result == "player":
            self.player_score += 1
            self.result_label.config(text="You win this round!", fg="#CCFF99")  # Green
        elif result == "computer":
            self.computer_score += 1
            self.result_label.config(text="Computer wins this round!", fg="#FF6666")  # Red
        else:
            self.result_label.config(text="It's a tie!", fg="#FFFF99")  # Yellow
        
        self.rounds_played += 1
        
        # Update score display
        self.score_label.config(text=f"Player: {self.player_score}  -  Computer: {self.computer_score}")
        self.rounds_label.config(text=f"Rounds: {self.rounds_played}")
    
    def get_winner(self, player_choice, computer_choice):
        """Determine the winner of the round."""
        if player_choice == computer_choice:
            return "tie"
        
        if (player_choice == "rock" and computer_choice == "scissors") or \
           (player_choice == "paper" and computer_choice == "rock") or \
           (player_choice == "scissors" and computer_choice == "paper"):
            return "player"
        
        return "computer"
    
    def new_game(self):
        """Start a new game."""
        # Reset game variables
        self.player_score = 0
        self.computer_score = 0
        self.rounds_played = 0
        self.player_choice = None
        self.computer_choice = None
        
        # Reset UI
        self.player_choice_label.config(text="")
        self.computer_choice_label.config(text="")
        self.player_image_label.config(image=self.question_mark)
        self.computer_image_label.config(image=self.question_mark)
        self.result_label.config(text="")
        self.score_label.config(text="Player: 0  -  Computer: 0")
        self.rounds_label.config(text="Rounds: 0")
    
    def quit_game(self):
        """Quit the game."""
        if messagebox.askyesno("Quit Game", "Are you sure you want to quit?"):
            self.root.destroy()

def main():
    """Main function to start the GUI game."""
    root = tk.Tk()
    app = RockPaperScissorsGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 