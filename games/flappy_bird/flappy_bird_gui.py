#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
import sys
import os

class FlappyBirdGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Flappy Bird")
        self.root.geometry("800x600")
        self.root.configure(bg="#87CEEB")  # Sky blue background
        self.root.resizable(True, True)
        
        # Game parameters
        self.canvas_width = 700
        self.canvas_height = 500
        self.bird_radius = 15
        self.bird_x = self.canvas_width // 3
        self.bird_y = self.canvas_height // 2
        self.bird_velocity = 0
        self.gravity = 0.5
        self.flap_strength = -8.0
        self.pipes = []
        self.pipe_width = 80
        self.pipe_gap = 150
        self.pipe_color = "#74BF2E"  # Green
        self.ground_height = 50
        self.score = 0
        self.game_active = False
        self.paused = False
        self.pipe_speed = 3
        self.pipe_frequency = 1800  # milliseconds between new pipes
        self.difficulty = "medium"
        
        # Animation IDs for cancellation
        self.animation_id = None
        self.pipe_generator_id = None
        
        # Create widgets
        self.create_widgets()
        
        # Set up keyboard bindings
        self.setup_key_bindings()
        
        # Show welcome screen
        self.show_welcome()
    
    def create_widgets(self):
        """Create the GUI widgets."""
        # Main frame
        self.main_frame = tk.Frame(self.root, bg="#87CEEB")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title label
        self.title_label = tk.Label(
            self.main_frame,
            text="FLAPPY BIRD",
            font=("Helvetica", 24, "bold"),
            bg="#87CEEB",
            fg="#FFFFFF"
        )
        self.title_label.pack(pady=(0, 10))
        
        # Game info frame
        self.info_frame = tk.Frame(self.main_frame, bg="#87CEEB")
        self.info_frame.pack(fill=tk.X, pady=5)
        
        # Score display
        self.score_var = tk.StringVar(value="Score: 0")
        self.score_label = tk.Label(
            self.info_frame,
            textvariable=self.score_var,
            font=("Helvetica", 16, "bold"),
            bg="#87CEEB",
            fg="#FFFFFF"
        )
        self.score_label.pack(side=tk.LEFT, padx=10)
        
        # Status label
        self.status_var = tk.StringVar(value="Press Start to begin")
        self.status_label = tk.Label(
            self.info_frame,
            textvariable=self.status_var,
            font=("Helvetica", 12),
            bg="#87CEEB",
            fg="#FFFFFF"
        )
        self.status_label.pack(side=tk.RIGHT, padx=10)
        
        # Game canvas
        self.canvas = tk.Canvas(
            self.main_frame,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="#87CEEB",
            highlightthickness=1,
            highlightbackground="#FFFFFF"
        )
        self.canvas.pack(pady=10)
        
        # Draw the ground
        self.canvas.create_rectangle(
            0, self.canvas_height - self.ground_height,
            self.canvas_width, self.canvas_height,
            fill="#8B4513",  # Brown
            outline="",
            tags="ground"
        )
        
        # Draw initial bird
        self.bird = self.canvas.create_oval(
            self.bird_x - self.bird_radius, self.bird_y - self.bird_radius,
            self.bird_x + self.bird_radius, self.bird_y + self.bird_radius,
            fill="#FFFF00",  # Yellow
            outline="#000000",
            tags="bird"
        )
        
        # Difficulty selection frame
        self.difficulty_frame = tk.Frame(self.main_frame, bg="#87CEEB")
        self.difficulty_frame.pack(fill=tk.X, pady=10)
        
        # Difficulty label
        self.difficulty_label = tk.Label(
            self.difficulty_frame,
            text="Difficulty:",
            font=("Helvetica", 12),
            bg="#87CEEB",
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
            bg="#87CEEB",
            fg="#FFFFFF",
            selectcolor="#4477AA",
            activebackground="#87CEEB",
            activeforeground="#FFFFFF"
        )
        self.easy_radio.pack(side=tk.LEFT, padx=5)
        
        self.medium_radio = tk.Radiobutton(
            self.difficulty_frame,
            text="Medium",
            variable=self.difficulty_var,
            value="medium",
            command=self.change_difficulty,
            bg="#87CEEB",
            fg="#FFFFFF",
            selectcolor="#4477AA",
            activebackground="#87CEEB",
            activeforeground="#FFFFFF"
        )
        self.medium_radio.pack(side=tk.LEFT, padx=5)
        
        self.hard_radio = tk.Radiobutton(
            self.difficulty_frame,
            text="Hard",
            variable=self.difficulty_var,
            value="hard",
            command=self.change_difficulty,
            bg="#87CEEB",
            fg="#FFFFFF",
            selectcolor="#4477AA",
            activebackground="#87CEEB",
            activeforeground="#FFFFFF"
        )
        self.hard_radio.pack(side=tk.LEFT, padx=5)
        
        # Control buttons frame
        self.control_frame = tk.Frame(self.main_frame, bg="#87CEEB")
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
        self.root.bind("<space>", lambda e: self.flap())
        self.root.bind("<Up>", lambda e: self.flap())
        self.root.bind("<p>", lambda e: self.toggle_pause())
        self.root.bind("<P>", lambda e: self.toggle_pause())
    
    def show_welcome(self):
        """Show welcome screen and instructions."""
        welcome_window = tk.Toplevel(self.root)
        welcome_window.title("Welcome to Flappy Bird")
        welcome_window.geometry("500x400")
        welcome_window.configure(bg="#87CEEB")
        welcome_window.transient(self.root)
        welcome_window.grab_set()
        welcome_window.resizable(True, True)
        
        # Welcome title
        welcome_label = tk.Label(
            welcome_window,
            text="Welcome to Flappy Bird",
            font=("Helvetica", 18, "bold"),
            bg="#87CEEB",
            fg="#FFFFFF"
        )
        welcome_label.pack(pady=20)
        
        # Instructions
        instructions_frame = tk.Frame(welcome_window, bg="#87CEEB", padx=20)
        instructions_frame.pack(fill=tk.BOTH, expand=True)
        
        instructions = [
            "Flappy Bird is a side-scrolling game where you control a bird,",
            "attempting to fly through columns of pipes without hitting them.",
            "",
            "Controls:",
            "• SPACE or UP ARROW: Make the bird flap upward",
            "• P: Pause/Resume the game",
            "",
            "Tips:",
            "• The bird constantly falls due to gravity",
            "• Press SPACE repeatedly to maintain altitude",
            "• Timing is crucial to navigate through the pipe gaps",
            "• Each pipe you pass gives you one point",
            "",
            "Difficulty levels adjust the gap size, pipe frequency, and gravity!"
        ]
        
        for line in instructions:
            tk.Label(
                instructions_frame,
                text=line,
                font=("Helvetica", 12),
                bg="#87CEEB",
                fg="#FFFFFF",
                justify=tk.LEFT
            ).pack(anchor=tk.W, pady=1)
        
        # Start button
        start_button = tk.Button(
            welcome_window,
            text="Let's Fly!",
            font=("Helvetica", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            command=welcome_window.destroy
        )
        start_button.pack(pady=20)
    
    def change_difficulty(self):
        """Change the game difficulty."""
        self.difficulty = self.difficulty_var.get()
        
        if self.difficulty == "easy":
            self.pipe_gap = 180
            self.gravity = 0.4
            self.pipe_frequency = 2200
            self.pipe_speed = 2
        elif self.difficulty == "medium":
            self.pipe_gap = 150
            self.gravity = 0.5
            self.pipe_frequency = 1800
            self.pipe_speed = 3
        else:  # hard
            self.pipe_gap = 120
            self.gravity = 0.6
            self.pipe_frequency = 1500
            self.pipe_speed = 4
        
        # Update status if game isn't active
        if not self.game_active:
            self.status_var.set(f"Difficulty set to {self.difficulty.capitalize()}")
    
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
        
        # Start the game
        self.game_active = True
        
        # Update UI elements
        self.pause_button.config(state=tk.NORMAL, text="Pause")
        self.start_button.config(text="Restart Game")
        self.easy_radio.config(state=tk.DISABLED)
        self.medium_radio.config(state=tk.DISABLED)
        self.hard_radio.config(state=tk.DISABLED)
        
        # Update status
        self.status_var.set("Game started - Press SPACE to flap!")
        
        # Start the game loop and pipe generator
        self.animation_id = self.root.after(16, self.update_game)  # ~60 FPS
        self.pipe_generator_id = self.root.after(1500, self.add_pipe)  # First pipe comes a bit later
    
    def reset_game(self):
        """Reset the game state."""
        # Cancel any animations or timers
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None
        
        if self.pipe_generator_id:
            self.root.after_cancel(self.pipe_generator_id)
            self.pipe_generator_id = None
        
        # Reset score
        self.score = 0
        self.score_var.set("Score: 0")
        
        # Reset bird position and velocity
        self.bird_y = self.canvas_height // 2
        self.bird_velocity = 0
        
        # Clear pipes
        for pipe in self.pipes:
            self.canvas.delete(pipe["top"])
            self.canvas.delete(pipe["bottom"])
        self.pipes = []
        
        # Redraw the bird
        self.canvas.delete("bird")
        self.bird = self.canvas.create_oval(
            self.bird_x - self.bird_radius, self.bird_y - self.bird_radius,
            self.bird_x + self.bird_radius, self.bird_y + self.bird_radius,
            fill="#FFFF00",  # Yellow
            outline="#000000",
            tags="bird"
        )
        
        # Reset game state
        self.game_active = False
        self.paused = False
    
    def add_pipe(self):
        """Add a new pipe to the game."""
        if not self.game_active or self.paused:
            return
        
        # Calculate gap position
        gap_y = random.randint(100, self.canvas_height - self.ground_height - 100)
        gap_top = gap_y - self.pipe_gap // 2
        gap_bottom = gap_y + self.pipe_gap // 2
        
        # Create pipe
        top_pipe = self.canvas.create_rectangle(
            self.canvas_width, 0,
            self.canvas_width + self.pipe_width, gap_top,
            fill=self.pipe_color,
            outline="",
            tags="pipe"
        )
        
        bottom_pipe = self.canvas.create_rectangle(
            self.canvas_width, gap_bottom,
            self.canvas_width + self.pipe_width, self.canvas_height - self.ground_height,
            fill=self.pipe_color,
            outline="",
            tags="pipe"
        )
        
        # Add to pipes list
        self.pipes.append({
            "top": top_pipe,
            "bottom": bottom_pipe,
            "x": self.canvas_width,
            "gap_top": gap_top,
            "gap_bottom": gap_bottom,
            "passed": False
        })
        
        # Schedule next pipe
        self.pipe_generator_id = self.root.after(self.pipe_frequency, self.add_pipe)
    
    def update_game(self):
        """Update the game state and redraw."""
        if not self.game_active or self.paused:
            return
        
        # Update bird position
        self.bird_velocity += self.gravity
        self.bird_y += self.bird_velocity
        
        # Update bird on canvas
        self.canvas.coords(
            self.bird,
            self.bird_x - self.bird_radius, self.bird_y - self.bird_radius,
            self.bird_x + self.bird_radius, self.bird_y + self.bird_radius
        )
        
        # Check collision with ground or ceiling
        if self.bird_y - self.bird_radius <= 0:
            self.bird_y = self.bird_radius
            self.bird_velocity = 0
        elif self.bird_y + self.bird_radius >= self.canvas_height - self.ground_height:
            self.game_over()
            return
        
        # Update pipes and check for collisions
        pipes_to_remove = []
        for pipe in self.pipes:
            # Move pipe
            pipe["x"] -= self.pipe_speed
            self.canvas.move(pipe["top"], -self.pipe_speed, 0)
            self.canvas.move(pipe["bottom"], -self.pipe_speed, 0)
            
            # Check if bird passes pipe
            if not pipe["passed"] and pipe["x"] + self.pipe_width < self.bird_x - self.bird_radius:
                pipe["passed"] = True
                self.score += 1
                self.score_var.set(f"Score: {self.score}")
            
            # Check if pipe is off screen
            if pipe["x"] + self.pipe_width < 0:
                pipes_to_remove.append(pipe)
            
            # Check for collision with pipe
            bird_right = self.bird_x + self.bird_radius
            bird_left = self.bird_x - self.bird_radius
            bird_top = self.bird_y - self.bird_radius
            bird_bottom = self.bird_y + self.bird_radius
            
            pipe_left = pipe["x"]
            pipe_right = pipe["x"] + self.pipe_width
            
            if (bird_right > pipe_left and bird_left < pipe_right and
                (bird_top < pipe["gap_top"] or bird_bottom > pipe["gap_bottom"])):
                self.game_over()
                return
        
        # Remove pipes that are off screen
        for pipe in pipes_to_remove:
            self.pipes.remove(pipe)
            self.canvas.delete(pipe["top"])
            self.canvas.delete(pipe["bottom"])
        
        # Schedule next update
        self.animation_id = self.root.after(16, self.update_game)  # ~60 FPS
    
    def flap(self):
        """Make the bird flap upward."""
        if not self.game_active or self.paused:
            return
        
        self.bird_velocity = self.flap_strength
    
    def toggle_pause(self):
        """Toggle the game pause state."""
        if not self.game_active:
            return
        
        self.paused = not self.paused
        
        if self.paused:
            self.pause_button.config(text="Resume")
            self.status_var.set("Game Paused")
            
            # Cancel animations
            if self.animation_id:
                self.root.after_cancel(self.animation_id)
                self.animation_id = None
            
            if self.pipe_generator_id:
                self.root.after_cancel(self.pipe_generator_id)
                self.pipe_generator_id = None
        else:
            self.pause_button.config(text="Pause")
            self.status_var.set("Game Resumed")
            
            # Restart animations
            self.animation_id = self.root.after(16, self.update_game)
            self.pipe_generator_id = self.root.after(self.pipe_frequency, self.add_pipe)
    
    def game_over(self):
        """Handle game over."""
        self.game_active = False
        
        # Cancel animations
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None
        
        if self.pipe_generator_id:
            self.root.after_cancel(self.pipe_generator_id)
            self.pipe_generator_id = None
        
        # Enable UI elements
        self.easy_radio.config(state=tk.NORMAL)
        self.medium_radio.config(state=tk.NORMAL)
        self.hard_radio.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.start_button.config(text="Start Game")
        
        # Update status
        self.status_var.set("Game Over!")
        
        # Show game over message
        messagebox.showinfo("Game Over", f"Game Over! Your score: {self.score}")
    
    def quit_game(self):
        """Quit the game."""
        if messagebox.askyesno("Quit", "Are you sure you want to quit the game?"):
            self.root.destroy()

def main():
    """Main function to start the GUI game."""
    root = tk.Tk()
    app = FlappyBirdGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 