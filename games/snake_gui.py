#!/usr/bin/env python3
import os
import random
import time
import tkinter as tk
from tkinter import messagebox

class SnakeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake")
        self.root.geometry("600x700")  # Increased height from 650 to 700
        self.root.configure(bg="#333333")
        self.root.resizable(True, True)  # Changed from False, False to True, True to allow resizing
        
        # Set minimum window size to ensure all elements are visible
        self.root.minsize(600, 700)
        
        # Game variables
        self.width = 20  # Game grid width
        self.height = 20  # Game grid height
        self.cell_size = 25  # Size of each cell in pixels
        self.delay = 150  # Milliseconds between updates (lower = faster)
        
        self.snake = [(self.width // 2, self.height // 2)]  # Start in the middle
        self.direction = (1, 0)  # Initial direction: right
        self.food = None
        self.score = 0
        self.game_over = False
        self.game_running = False
        self.level = 1
        
        # Create UI elements
        self.create_widgets()
        
        # Bind keyboard events
        self.root.bind("<Up>", lambda e: self.change_direction((0, -1)))
        self.root.bind("<Down>", lambda e: self.change_direction((0, 1)))
        self.root.bind("<Left>", lambda e: self.change_direction((-1, 0)))
        self.root.bind("<Right>", lambda e: self.change_direction((1, 0)))
        self.root.bind("w", lambda e: self.change_direction((0, -1)))
        self.root.bind("s", lambda e: self.change_direction((0, 1)))
        self.root.bind("a", lambda e: self.change_direction((-1, 0)))
        self.root.bind("d", lambda e: self.change_direction((1, 0)))
        
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
            text="Snake", 
            font=("Helvetica", 24, "bold"),
            bg="#333333",
            fg="#CCFF99"  # Green
        )
        self.title_label.pack(pady=(0, 10))
        
        # Score display
        self.score_label = tk.Label(
            main_frame,
            text="Score: 0",
            font=("Helvetica", 16),
            bg="#333333",
            fg="#FFFFFF"
        )
        self.score_label.pack(pady=5)
        
        # Instructions label
        self.info_label = tk.Label(
            main_frame,
            text="Use arrow keys or WASD to move",
            font=("Helvetica", 12),
            bg="#333333",
            fg="#FFFF99"  # Yellow
        )
        self.info_label.pack(pady=5)
        
        # Game canvas
        canvas_width = self.width * self.cell_size
        canvas_height = self.height * self.cell_size
        
        self.canvas = tk.Canvas(
            main_frame,
            width=canvas_width,
            height=canvas_height,
            bg="#000000",
            highlightthickness=1,
            highlightbackground="#444444"
        )
        self.canvas.pack(pady=10)
        
        # Control buttons frame - changed to separate controls into two rows for better visibility
        buttons_frame = tk.Frame(main_frame, bg="#333333")
        buttons_frame.pack(fill=tk.X, pady=10)
        
        # Start button - moved to top of controls for better visibility
        self.start_button = tk.Button(
            buttons_frame,
            text="Start Game",
            command=self.start_game,
            bg="#CCFF99",  # Green
            fg="#000000",
            activebackground="#99CC66",
            activeforeground="#000000",
            font=("Helvetica", 12, "bold"),
            width=12,
            height=2  # Made button taller for better visibility
        )
        self.start_button.pack(side=tk.TOP, pady=5)
        
        # Bottom frame for difficulty controls
        difficulty_frame = tk.Frame(buttons_frame, bg="#333333")
        difficulty_frame.pack(fill=tk.X, pady=5)
        
        # Level selector
        level_label = tk.Label(
            difficulty_frame,
            text="Difficulty:",
            font=("Helvetica", 12),
            bg="#333333",
            fg="#FFFFFF"
        )
        level_label.pack(side=tk.LEFT, padx=5)
        
        self.level_var = tk.IntVar(value=1)
        
        level1_radio = tk.Radiobutton(
            difficulty_frame,
            text="Easy",
            variable=self.level_var,
            value=1,
            font=("Helvetica", 12),
            bg="#333333",
            fg="#CCFF99",  # Green
            selectcolor="#222222",
            activebackground="#333333",
            activeforeground="#CCFF99"
        )
        level1_radio.pack(side=tk.LEFT, padx=5)
        
        level2_radio = tk.Radiobutton(
            difficulty_frame,
            text="Medium",
            variable=self.level_var,
            value=2,
            font=("Helvetica", 12),
            bg="#333333",
            fg="#FFFF99",  # Yellow
            selectcolor="#222222",
            activebackground="#333333",
            activeforeground="#FFFF99"
        )
        level2_radio.pack(side=tk.LEFT, padx=5)
        
        level3_radio = tk.Radiobutton(
            difficulty_frame,
            text="Hard",
            variable=self.level_var,
            value=3,
            font=("Helvetica", 12),
            bg="#333333",
            fg="#FF6666",  # Red
            selectcolor="#222222",
            activebackground="#333333",
            activeforeground="#FF6666"
        )
        level3_radio.pack(side=tk.LEFT, padx=5)
        
        # Quit button
        quit_button = tk.Button(
            difficulty_frame,
            text="Quit",
            command=self.quit_game,
            bg="#663333",
            fg="#FFFFFF",
            activebackground="#993333",
            activeforeground="#FFFFFF",
            font=("Helvetica", 12),
            width=8
        )
        quit_button.pack(side=tk.RIGHT, padx=5)
    
    def show_welcome(self):
        """Show welcome screen with instructions."""
        self.clear_canvas()
        
        # Draw welcome message on canvas
        self.canvas.create_text(
            self.width * self.cell_size // 2,
            self.height * self.cell_size // 2 - 40,
            text="Welcome to Snake!",
            font=("Helvetica", 20, "bold"),
            fill="#CCFF99"  # Green
        )
        
        instructions = [
            "Control the snake using arrow keys or WASD",
            "Collect food to grow longer",
            "Avoid hitting the walls or yourself",
            "Select difficulty and click 'Start Game' to play"
        ]
        
        y_offset = 0
        for instruction in instructions:
            self.canvas.create_text(
                self.width * self.cell_size // 2,
                self.height * self.cell_size // 2 + y_offset,
                text=instruction,
                font=("Helvetica", 14),
                fill="#FFFFFF"
            )
            y_offset += 30
        
        # Enable start button and difficulty selection
        self.start_button.config(state=tk.NORMAL)
    
    def start_game(self):
        """Start a new game."""
        # Set game parameters based on difficulty level
        level = self.level_var.get()
        if level == 1:  # Easy
            self.delay = 150
        elif level == 2:  # Medium
            self.delay = 100
        else:  # Hard
            self.delay = 70
        
        # Reset game variables
        self.snake = [(self.width // 2, self.height // 2)]
        self.direction = (1, 0)
        self.score = 0
        self.game_over = False
        self.score_label.config(text="Score: 0")
        
        # Create new food
        self.create_food()
        
        # Update start button
        self.start_button.config(text="Restart", state=tk.DISABLED)
        self.info_label.config(text="Game in progress...")
        
        # Start game loop
        self.game_running = True
        self.update()
    
    def clear_canvas(self):
        """Clear the canvas."""
        self.canvas.delete("all")
    
    def create_food(self):
        """Create a new food item at a random location."""
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            
            # Make sure food doesn't appear on the snake
            if (x, y) not in self.snake:
                self.food = (x, y)
                break
    
    def change_direction(self, new_dir):
        """Change snake's direction if it's not going in the opposite direction."""
        if not self.game_running or self.game_over:
            return
        
        # Prevent 180-degree turns
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.direction = new_dir
    
    def update(self):
        """Update the game state and redraw."""
        if not self.game_running:
            return
        
        if self.game_over:
            self.start_button.config(state=tk.NORMAL)
            self.show_game_over()
            return
        
        # Move the snake
        self.move_snake()
        
        # Check for collisions
        self.check_collisions()
        
        # Redraw everything
        self.redraw()
        
        # Schedule the next update
        self.root.after(self.delay, self.update)
    
    def move_snake(self):
        """Move the snake in the current direction."""
        if self.game_over:
            return
        
        # Calculate new head position
        head_x, head_y = self.snake[0]
        dir_x, dir_y = self.direction
        
        # New position with wrap-around
        new_x = (head_x + dir_x) % self.width
        new_y = (head_y + dir_y) % self.height
        
        # Add new head
        self.snake.insert(0, (new_x, new_y))
        
        # Check if snake eats food
        if (new_x, new_y) == self.food:
            # Snake grows and doesn't remove tail
            self.score += 10
            self.score_label.config(text=f"Score: {self.score}")
            
            # Create new food
            self.create_food()
            
            # Speed up the game slightly as the snake grows
            if self.delay > 30:  # Minimum delay to keep the game playable
                self.delay = int(self.delay * 0.98)
        else:
            # Remove tail if no food eaten
            self.snake.pop()
    
    def check_collisions(self):
        """Check for collisions with self."""
        head = self.snake[0]
        
        # Check if snake hits itself
        if head in self.snake[1:]:
            self.game_over = True
    
    def redraw(self):
        """Redraw the game."""
        self.clear_canvas()
        
        # Draw food
        if self.food:
            x, y = self.food
            food_x1 = x * self.cell_size + 2
            food_y1 = y * self.cell_size + 2
            food_x2 = (x + 1) * self.cell_size - 2
            food_y2 = (y + 1) * self.cell_size - 2
            
            self.canvas.create_oval(
                food_x1, food_y1, food_x2, food_y2,
                fill="#FF6666",  # Red
                outline="#FF6666"
            )
        
        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            snake_x1 = x * self.cell_size + 1
            snake_y1 = y * self.cell_size + 1
            snake_x2 = (x + 1) * self.cell_size - 1
            snake_y2 = (y + 1) * self.cell_size - 1
            
            # Head is a different color
            if i == 0:
                color = "#CCFF99"  # Bright green for head
            else:
                color = "#669966"  # Darker green for body
            
            self.canvas.create_rectangle(
                snake_x1, snake_y1, snake_x2, snake_y2,
                fill=color,
                outline="#000000"
            )
        
        # Draw grid lines (optional)
        if self.level_var.get() == 1:  # Only draw grid in easy mode
            for x in range(self.width):
                self.canvas.create_line(
                    x * self.cell_size, 0, 
                    x * self.cell_size, self.height * self.cell_size,
                    fill="#111111"
                )
            
            for y in range(self.height):
                self.canvas.create_line(
                    0, y * self.cell_size, 
                    self.width * self.cell_size, y * self.cell_size,
                    fill="#111111"
                )
    
    def show_game_over(self):
        """Show game over screen."""
        self.info_label.config(text="Game Over! Click 'Restart' to play again")
        
        # Draw game over text
        self.canvas.create_rectangle(
            self.width * self.cell_size // 4,
            self.height * self.cell_size // 3 - 20,
            self.width * self.cell_size * 3 // 4,
            self.height * self.cell_size * 2 // 3 + 20,
            fill="#000000",
            outline="#FF6666",
            width=3
        )
        
        self.canvas.create_text(
            self.width * self.cell_size // 2,
            self.height * self.cell_size // 2 - 20,
            text="GAME OVER",
            font=("Helvetica", 20, "bold"),
            fill="#FF6666"  # Red
        )
        
        self.canvas.create_text(
            self.width * self.cell_size // 2,
            self.height * self.cell_size // 2 + 20,
            text=f"Final Score: {self.score}",
            font=("Helvetica", 16),
            fill="#FFFFFF"
        )
        
        self.game_running = False
    
    def quit_game(self):
        """Quit the game."""
        if messagebox.askyesno("Quit Game", "Are you sure you want to quit?"):
            self.root.destroy()

def main():
    """Main function to start the GUI game."""
    root = tk.Tk()
    app = SnakeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 