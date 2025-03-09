#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
import sys
import os

class PongGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pong")
        self.root.geometry("800x600")
        self.root.configure(bg="#333333")
        self.root.resizable(True, True)
        
        # Game parameters
        self.canvas_width = 700
        self.canvas_height = 500
        self.paddle_width = 10
        self.paddle_height = 80
        self.ball_size = 15
        self.paddle_speed = 8
        self.ball_speed_x = 5
        self.ball_speed_y = 5
        self.difficulty = "medium"  # Default difficulty
        self.game_active = False
        self.paused = False
        
        # Game state
        self.left_paddle_y = self.canvas_height // 2 - self.paddle_height // 2
        self.right_paddle_y = self.canvas_height // 2 - self.paddle_height // 2
        self.ball_x = self.canvas_width // 2
        self.ball_y = self.canvas_height // 2
        self.ball_dx = random.choice([-1, 1]) * self.ball_speed_x
        self.ball_dy = random.choice([-1, 1]) * self.ball_speed_y
        self.left_score = 0
        self.right_score = 0
        self.ai_difficulty = 0.7  # AI prediction accuracy (0.0 to 1.0)
        
        # Key states
        self.keys = {"w": False, "s": False, "up": False, "down": False}
        
        # Create widgets
        self.create_widgets()
        
        # Setup key bindings
        self.setup_key_bindings()
        
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
            text="PONG",
            font=("Helvetica", 24, "bold"),
            bg="#333333",
            fg="#FFFFFF"
        )
        self.title_label.pack(pady=(0, 10))
        
        # Game info frame
        self.info_frame = tk.Frame(self.main_frame, bg="#333333")
        self.info_frame.pack(fill=tk.X, pady=5)
        
        # Score display
        self.score_frame = tk.Frame(self.info_frame, bg="#333333")
        self.score_frame.pack()
        
        self.left_score_var = tk.StringVar(value="0")
        self.left_score_label = tk.Label(
            self.score_frame,
            textvariable=self.left_score_var,
            font=("Helvetica", 36, "bold"),
            bg="#333333",
            fg="#4CAF50",
            width=3
        )
        self.left_score_label.grid(row=0, column=0, padx=20)
        
        tk.Label(
            self.score_frame,
            text=":",
            font=("Helvetica", 36, "bold"),
            bg="#333333",
            fg="#FFFFFF"
        ).grid(row=0, column=1)
        
        self.right_score_var = tk.StringVar(value="0")
        self.right_score_label = tk.Label(
            self.score_frame,
            textvariable=self.right_score_var,
            font=("Helvetica", 36, "bold"),
            bg="#333333",
            fg="#F44336",
            width=3
        )
        self.right_score_label.grid(row=0, column=2, padx=20)
        
        # Status label
        self.status_var = tk.StringVar(value="Press Start to begin")
        self.status_label = tk.Label(
            self.main_frame,
            textvariable=self.status_var,
            font=("Helvetica", 12),
            bg="#333333",
            fg="#FFFFFF"
        )
        self.status_label.pack(pady=5)
        
        # Game canvas
        self.canvas = tk.Canvas(
            self.main_frame,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="#000000",
            highlightthickness=0
        )
        self.canvas.pack(pady=10)
        
        # Draw initial game state
        self.draw_canvas()
        
        # Difficulty selection frame
        self.difficulty_frame = tk.Frame(self.main_frame, bg="#333333")
        self.difficulty_frame.pack(fill=tk.X, pady=10)
        
        # Difficulty label
        self.difficulty_label = tk.Label(
            self.difficulty_frame,
            text="AI Difficulty:",
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
        self.control_frame.pack(fill=tk.X, pady=10)
        
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
        
        # Pause button
        self.pause_button = tk.Button(
            self.control_frame,
            text="Pause",
            font=("Helvetica", 12),
            bg="#2196F3",
            fg="white",
            command=self.toggle_pause,
            state=tk.DISABLED
        )
        self.pause_button.pack(side=tk.LEFT, padx=10)
        
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
    
    def setup_key_bindings(self):
        """Setup keyboard bindings."""
        # Key press events
        self.root.bind("<KeyPress-w>", lambda e: self.set_key_state("w", True))
        self.root.bind("<KeyPress-s>", lambda e: self.set_key_state("s", True))
        self.root.bind("<KeyPress-Up>", lambda e: self.set_key_state("up", True))
        self.root.bind("<KeyPress-Down>", lambda e: self.set_key_state("down", True))
        self.root.bind("<KeyPress-space>", lambda e: self.toggle_pause())
        self.root.bind("<KeyPress-p>", lambda e: self.toggle_pause())
        
        # Key release events
        self.root.bind("<KeyRelease-w>", lambda e: self.set_key_state("w", False))
        self.root.bind("<KeyRelease-s>", lambda e: self.set_key_state("s", False))
        self.root.bind("<KeyRelease-Up>", lambda e: self.set_key_state("up", False))
        self.root.bind("<KeyRelease-Down>", lambda e: self.set_key_state("down", False))
    
    def set_key_state(self, key, state):
        """Set the state of a key."""
        self.keys[key] = state
    
    def show_welcome(self):
        """Show welcome screen and instructions."""
        welcome_window = tk.Toplevel(self.root)
        welcome_window.title("Welcome to Pong")
        welcome_window.geometry("500x400")
        welcome_window.configure(bg="#333333")
        welcome_window.transient(self.root)
        welcome_window.grab_set()
        welcome_window.resizable(True, True)
        
        # Welcome title
        welcome_label = tk.Label(
            welcome_window,
            text="Welcome to Pong",
            font=("Helvetica", 18, "bold"),
            bg="#333333",
            fg="#FFFFFF"
        )
        welcome_label.pack(pady=20)
        
        # Instructions
        instructions_frame = tk.Frame(welcome_window, bg="#333333", padx=20)
        instructions_frame.pack(fill=tk.BOTH, expand=True)
        
        instructions = [
            "Pong is a two-player table tennis game where players control",
            "paddles to hit a ball back and forth.",
            "",
            "Controls:",
            "• Player 1 (Left): W (up), S (down)",
            "• Player 2 (Right): AI-controlled",
            "• P or Space: Pause/Resume the game",
            "",
            "Scoring:",
            "• Score a point by getting the ball past your opponent's paddle",
            "• First player to reach 5 points wins!",
            "",
            "Tip: The ball will bounce at different angles depending on",
            "where it hits your paddle. Use this to your advantage!"
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
            text="Let's Play!",
            font=("Helvetica", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            command=welcome_window.destroy
        )
        start_button.pack(pady=20)
    
    def change_difficulty(self):
        """Change the AI difficulty."""
        self.difficulty = self.difficulty_var.get()
        
        if self.difficulty == "easy":
            self.ai_difficulty = 0.5
            self.paddle_height = 100
        elif self.difficulty == "medium":
            self.ai_difficulty = 0.7
            self.paddle_height = 80
        else:  # hard
            self.ai_difficulty = 0.9
            self.paddle_height = 60
        
        # Update the paddle display
        self.draw_canvas()
        
        # Update status
        self.status_var.set(f"AI Difficulty set to {self.difficulty.capitalize()}")
    
    def start_game(self):
        """Start a new game."""
        if self.game_active and not self.paused:
            # If game is already running, restart it
            if messagebox.askyesno("New Game", "Are you sure you want to start a new game?"):
                self.reset_game()
            else:
                return
        
        # Reset game state
        self.reset_game()
        
        # Start the game loop
        self.game_active = True
        self.paused = False
        
        # Update UI elements
        self.pause_button.config(state=tk.NORMAL, text="Pause")
        self.start_button.config(text="Restart Game")
        self.easy_radio.config(state=tk.DISABLED)
        self.medium_radio.config(state=tk.DISABLED)
        self.hard_radio.config(state=tk.DISABLED)
        
        # Update status
        self.status_var.set("Game started - Good luck!")
        
        # Start game loop
        self.update_game()
    
    def reset_game(self):
        """Reset the game state."""
        # Reset scores
        self.left_score = 0
        self.right_score = 0
        self.left_score_var.set("0")
        self.right_score_var.set("0")
        
        # Reset paddle positions
        self.left_paddle_y = self.canvas_height // 2 - self.paddle_height // 2
        self.right_paddle_y = self.canvas_height // 2 - self.paddle_height // 2
        
        # Reset ball position and direction
        self.reset_ball()
        
        # Adjust speed based on difficulty
        if self.difficulty == "easy":
            self.ball_speed_x = 4
            self.ball_speed_y = 4
        elif self.difficulty == "medium":
            self.ball_speed_x = 6
            self.ball_speed_y = 6
        else:  # hard
            self.ball_speed_x = 8
            self.ball_speed_y = 8
    
    def reset_ball(self):
        """Reset the ball to the center with a random direction."""
        self.ball_x = self.canvas_width // 2
        self.ball_y = self.canvas_height // 2
        self.ball_dx = random.choice([-1, 1]) * self.ball_speed_x
        self.ball_dy = random.choice([-1, 1]) * self.ball_speed_y
    
    def toggle_pause(self):
        """Toggle the game pause state."""
        if not self.game_active:
            return
        
        self.paused = not self.paused
        
        if self.paused:
            self.pause_button.config(text="Resume")
            self.status_var.set("Game Paused")
        else:
            self.pause_button.config(text="Pause")
            self.status_var.set("Game Resumed")
            # Continue game loop
            self.update_game()
    
    def update_game(self):
        """Update the game state and redraw."""
        if not self.game_active or self.paused:
            return
        
        # Check if any player has won
        if self.left_score >= 5 or self.right_score >= 5:
            self.game_over()
            return
        
        # Move paddles based on key states
        self.move_paddles()
        
        # Move AI paddle
        self.move_ai_paddle()
        
        # Move ball
        self.move_ball()
        
        # Redraw everything
        self.draw_canvas()
        
        # Schedule next update
        self.root.after(16, self.update_game)  # ~60 FPS
    
    def move_paddles(self):
        """Move paddles based on key states."""
        # Player 1 (Left paddle)
        if self.keys["w"] and self.left_paddle_y > 0:
            self.left_paddle_y -= self.paddle_speed
        if self.keys["s"] and self.left_paddle_y < self.canvas_height - self.paddle_height:
            self.left_paddle_y += self.paddle_speed
        
        # Ensure paddles stay within canvas bounds
        self.left_paddle_y = max(0, min(self.canvas_height - self.paddle_height, self.left_paddle_y))
    
    def move_ai_paddle(self):
        """Move the AI paddle based on ball position."""
        if random.random() < self.ai_difficulty:  # Simulate imperfect AI
            target_y = self.ball_y
            
            # Predict where the ball will be when it reaches the right side
            if self.ball_dx > 0:  # Ball is moving toward right paddle
                # Calculate time until ball reaches right side
                steps = (self.canvas_width - self.paddle_width - self.ball_size - self.ball_x) / self.ball_dx
                # Predict y position
                predicted_y = self.ball_y + (self.ball_dy * steps)
                # Keep prediction within canvas bounds
                predicted_y = max(self.ball_size, min(self.canvas_height - self.ball_size, predicted_y))
                target_y = predicted_y
            
            # Move paddle toward target
            paddle_center = self.right_paddle_y + (self.paddle_height / 2)
            if paddle_center < target_y - 10:
                self.right_paddle_y += self.paddle_speed
            elif paddle_center > target_y + 10:
                self.right_paddle_y -= self.paddle_speed
            
            # Ensure paddle stays within canvas bounds
            self.right_paddle_y = max(0, min(self.canvas_height - self.paddle_height, self.right_paddle_y))
    
    def move_ball(self):
        """Move the ball and handle collisions."""
        # Update ball position
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy
        
        # Check collision with top and bottom walls
        if self.ball_y <= self.ball_size / 2 or self.ball_y >= self.canvas_height - self.ball_size / 2:
            self.ball_dy *= -1
        
        # Check collision with left paddle
        left_paddle_right = self.paddle_width
        if (self.ball_x - self.ball_size / 2 <= left_paddle_right and 
            self.left_paddle_y <= self.ball_y <= self.left_paddle_y + self.paddle_height and
            self.ball_dx < 0):
            
            # Calculate relative hit position (0 to 1)
            relative_hit = (self.ball_y - self.left_paddle_y) / self.paddle_height
            
            # Change angle based on where ball hits the paddle
            self.ball_dx = abs(self.ball_dx)  # Reverse direction
            self.ball_dy = (relative_hit - 0.5) * 2 * self.ball_speed_y
        
        # Check collision with right paddle
        right_paddle_left = self.canvas_width - self.paddle_width
        if (self.ball_x + self.ball_size / 2 >= right_paddle_left and 
            self.right_paddle_y <= self.ball_y <= self.right_paddle_y + self.paddle_height and
            self.ball_dx > 0):
            
            # Calculate relative hit position (0 to 1)
            relative_hit = (self.ball_y - self.right_paddle_y) / self.paddle_height
            
            # Change angle based on where ball hits the paddle
            self.ball_dx = -abs(self.ball_dx)  # Reverse direction
            self.ball_dy = (relative_hit - 0.5) * 2 * self.ball_speed_y
        
        # Check if ball is out of bounds (scored)
        if self.ball_x < 0:
            # Right player scores
            self.right_score += 1
            self.right_score_var.set(str(self.right_score))
            self.reset_ball()
        elif self.ball_x > self.canvas_width:
            # Left player scores
            self.left_score += 1
            self.left_score_var.set(str(self.left_score))
            self.reset_ball()
    
    def draw_canvas(self):
        """Draw the game elements on the canvas."""
        # Clear canvas
        self.canvas.delete("all")
        
        # Draw center line
        for y in range(0, self.canvas_height, 20):
            self.canvas.create_line(
                self.canvas_width / 2, y,
                self.canvas_width / 2, y + 10,
                fill="#FFFFFF", width=2, dash=(2, 5)
            )
        
        # Draw paddles
        self.canvas.create_rectangle(
            0, self.left_paddle_y,
            self.paddle_width, self.left_paddle_y + self.paddle_height,
            fill="#4CAF50", outline=""
        )
        
        self.canvas.create_rectangle(
            self.canvas_width - self.paddle_width, self.right_paddle_y,
            self.canvas_width, self.right_paddle_y + self.paddle_height,
            fill="#F44336", outline=""
        )
        
        # Draw ball
        self.canvas.create_oval(
            self.ball_x - self.ball_size / 2, self.ball_y - self.ball_size / 2,
            self.ball_x + self.ball_size / 2, self.ball_y + self.ball_size / 2,
            fill="#FFFFFF", outline=""
        )
    
    def game_over(self):
        """Handle game over state."""
        self.game_active = False
        
        # Enable UI elements
        self.easy_radio.config(state=tk.NORMAL)
        self.medium_radio.config(state=tk.NORMAL)
        self.hard_radio.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.start_button.config(text="Start Game")
        
        # Show game over message
        if self.left_score >= 5:
            winner_msg = "Player 1 wins!"
            self.status_var.set(winner_msg)
            messagebox.showinfo("Game Over", winner_msg)
        else:
            winner_msg = "AI wins!"
            self.status_var.set(winner_msg)
            messagebox.showinfo("Game Over", winner_msg)
    
    def quit_game(self):
        """Quit the game."""
        if messagebox.askyesno("Quit", "Are you sure you want to quit the game?"):
            self.root.destroy()

def main():
    """Main function to start the GUI game."""
    root = tk.Tk()
    app = PongGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 