#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
import sys
import os
import math

class Game2048GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("2048")
        self.root.geometry("600x700")
        self.root.configure(bg="#FAF8EF")  # Light beige background
        self.root.resizable(True, True)
        
        # Game parameters
        self.grid_size = 4
        self.cell_size = 100
        self.cell_padding = 10
        self.board = None
        self.score = 0
        self.high_score = 0
        self.game_over = False
        self.won = False
        self.has_moved = False
        
        # Cell colors and fonts
        self.cell_colors = {
            0: "#CCC0B3",       # Empty cell
            2: "#EEE4DA",       # 2
            4: "#EDE0C8",       # 4
            8: "#F2B179",       # 8
            16: "#F59563",      # 16
            32: "#F67C5F",      # 32
            64: "#F65E3B",      # 64
            128: "#EDCF72",     # 128
            256: "#EDCC61",     # 256
            512: "#EDC850",     # 512
            1024: "#EDC53F",    # 1024
            2048: "#EDC22E",    # 2048
            4096: "#3E3933",    # 4096 (darker colors for higher values)
            8192: "#3E3933"     # 8192
        }
        
        self.text_colors = {
            0: "#CCC0B3",       # Empty cell (same as background)
            2: "#776E65",       # 2 (dark gray)
            4: "#776E65",       # 4
            8: "#F9F6F2",       # 8 (white)
            16: "#F9F6F2",      # 16
            32: "#F9F6F2",      # 32
            64: "#F9F6F2",      # 64
            128: "#F9F6F2",     # 128
            256: "#F9F6F2",     # 256
            512: "#F9F6F2",     # 512
            1024: "#F9F6F2",    # 1024
            2048: "#F9F6F2",    # 2048
            4096: "#F9F6F2",    # 4096
            8192: "#F9F6F2"     # 8192
        }
        
        # Create widgets
        self.create_widgets()
        
        # Set up keyboard bindings
        self.setup_key_bindings()
        
        # Show welcome screen
        self.show_welcome()
    
    def create_widgets(self):
        """Create the GUI widgets."""
        # Main frame
        self.main_frame = tk.Frame(self.root, bg="#FAF8EF")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title and info frame
        self.title_frame = tk.Frame(self.main_frame, bg="#FAF8EF")
        self.title_frame.pack(fill=tk.X, pady=10)
        
        # Game title
        self.title_label = tk.Label(
            self.title_frame,
            text="2048",
            font=("Helvetica", 48, "bold"),
            bg="#FAF8EF",
            fg="#776E65"
        )
        self.title_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Score frame
        self.score_frame = tk.Frame(self.title_frame, bg="#FAF8EF")
        self.score_frame.pack(side=tk.RIGHT)
        
        # Score display
        self.score_header = tk.Label(
            self.score_frame,
            text="SCORE",
            font=("Helvetica", 12),
            bg="#BBADA0",
            fg="#FFFFFF",
            padx=10,
            pady=5
        )
        self.score_header.pack(fill=tk.X)
        
        self.score_var = tk.StringVar(value="0")
        self.score_label = tk.Label(
            self.score_frame,
            textvariable=self.score_var,
            font=("Helvetica", 20, "bold"),
            bg="#BBADA0",
            fg="#FFFFFF",
            padx=10,
            pady=5,
            width=8
        )
        self.score_label.pack(fill=tk.X)
        
        # High score display
        self.high_frame = tk.Frame(self.title_frame, bg="#FAF8EF")
        self.high_frame.pack(side=tk.RIGHT, padx=10)
        
        self.high_header = tk.Label(
            self.high_frame,
            text="BEST",
            font=("Helvetica", 12),
            bg="#BBADA0",
            fg="#FFFFFF",
            padx=10,
            pady=5
        )
        self.high_header.pack(fill=tk.X)
        
        self.high_var = tk.StringVar(value="0")
        self.high_label = tk.Label(
            self.high_frame,
            textvariable=self.high_var,
            font=("Helvetica", 20, "bold"),
            bg="#BBADA0",
            fg="#FFFFFF",
            padx=10,
            pady=5,
            width=8
        )
        self.high_label.pack(fill=tk.X)
        
        # Instructions
        self.instructions_label = tk.Label(
            self.main_frame,
            text="Join the tiles and get to 2048!",
            font=("Helvetica", 14),
            bg="#FAF8EF",
            fg="#776E65"
        )
        self.instructions_label.pack(pady=(10, 20))
        
        # Game canvas
        self.canvas_frame = tk.Frame(
            self.main_frame,
            bg="#BBADA0",
            padx=self.cell_padding,
            pady=self.cell_padding
        )
        self.canvas_frame.pack(pady=10)
        
        # Calculate canvas size
        canvas_width = self.grid_size * (self.cell_size + self.cell_padding) + self.cell_padding
        canvas_height = canvas_width
        
        self.canvas = tk.Canvas(
            self.canvas_frame,
            width=canvas_width,
            height=canvas_height,
            bg="#BBADA0",
            highlightthickness=0
        )
        self.canvas.pack()
        
        # Control buttons frame
        self.control_frame = tk.Frame(self.main_frame, bg="#FAF8EF")
        self.control_frame.pack(fill=tk.X, pady=20)
        
        # New Game button
        self.new_button = tk.Button(
            self.control_frame,
            text="New Game",
            font=("Helvetica", 14, "bold"),
            bg="#8F7A66",
            fg="#FFFFFF",
            padx=10,
            pady=5,
            command=self.new_game,
            activebackground="#9F8A76"
        )
        self.new_button.pack(side=tk.LEFT, padx=10)
        
        # Quit button
        self.quit_button = tk.Button(
            self.control_frame,
            text="Quit",
            font=("Helvetica", 14, "bold"),
            bg="#8F7A66",
            fg="#FFFFFF",
            padx=10,
            pady=5,
            command=self.quit_game,
            activebackground="#9F8A76"
        )
        self.quit_button.pack(side=tk.RIGHT, padx=10)
    
    def setup_key_bindings(self):
        """Setup keyboard bindings."""
        self.root.bind("<Up>", lambda e: self.move("up"))
        self.root.bind("<Down>", lambda e: self.move("down"))
        self.root.bind("<Left>", lambda e: self.move("left"))
        self.root.bind("<Right>", lambda e: self.move("right"))
        self.root.bind("w", lambda e: self.move("up"))
        self.root.bind("s", lambda e: self.move("down"))
        self.root.bind("a", lambda e: self.move("left"))
        self.root.bind("d", lambda e: self.move("right"))
    
    def show_welcome(self):
        """Show welcome screen and instructions."""
        welcome_window = tk.Toplevel(self.root)
        welcome_window.title("Welcome to 2048")
        welcome_window.geometry("500x450")
        welcome_window.configure(bg="#FAF8EF")
        welcome_window.transient(self.root)
        welcome_window.grab_set()
        welcome_window.resizable(True, True)
        
        # Welcome title
        tk.Label(
            welcome_window,
            text="Welcome to 2048",
            font=("Helvetica", 24, "bold"),
            bg="#FAF8EF",
            fg="#776E65"
        ).pack(pady=20)
        
        # Instructions
        instructions_frame = tk.Frame(welcome_window, bg="#FAF8EF", padx=20)
        instructions_frame.pack(fill=tk.BOTH, expand=True)
        
        instructions = [
            "HOW TO PLAY:",
            "Use your arrow keys or WASD to move the tiles.",
            "When two tiles with the same number touch,",
            "they merge into one with their sum!",
            "",
            "• You win when you create a tile with the number 2048",
            "• You lose when the board is full and no more moves are possible",
            "",
            "STRATEGY TIPS:",
            "• Try to keep your highest tile in a corner",
            "• Build a chain of decreasing tiles",
            "• Plan several moves ahead",
            "• Don't swipe in all four directions randomly",
            "",
            "Each game is unique - have fun!"
        ]
        
        for line in instructions:
            tk.Label(
                instructions_frame,
                text=line,
                font=("Helvetica", 12),
                bg="#FAF8EF",
                fg="#776E65" if not line.startswith("HOW TO PLAY") and not line.startswith("STRATEGY") else "#8F7A66",
                justify=tk.LEFT
            ).pack(anchor=tk.W, pady=1)
        
        # Start button
        tk.Button(
            welcome_window,
            text="Let's Play!",
            font=("Helvetica", 14, "bold"),
            bg="#8F7A66",
            fg="#FFFFFF",
            padx=15,
            pady=10,
            command=lambda: [welcome_window.destroy(), self.new_game()],
            activebackground="#9F8A76"
        ).pack(pady=20)
    
    def new_game(self):
        """Start a new game."""
        # Initialize the board
        self.board = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.score = 0
        self.score_var.set(str(self.score))
        self.game_over = False
        self.won = False
        
        # Add two initial tiles
        self.add_random_tile()
        self.add_random_tile()
        
        # Update the display
        self.draw_board()
        
        # Update game status
        self.instructions_label.config(text="Join the tiles and get to 2048!")
    
    def add_random_tile(self):
        """Add a random tile (2 or 4) to the board."""
        # Find all empty cells
        empty_cells = []
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.board[y][x] == 0:
                    empty_cells.append((x, y))
        
        if not empty_cells:
            return
        
        # Choose a random empty cell
        x, y = random.choice(empty_cells)
        
        # 90% chance of 2, 10% chance of 4
        self.board[y][x] = 2 if random.random() < 0.9 else 4
    
    def draw_board(self):
        """Draw the game board."""
        self.canvas.delete("all")
        
        # Draw the background grid
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                # Calculate position
                x1 = x * (self.cell_size + self.cell_padding) + self.cell_padding
                y1 = y * (self.cell_size + self.cell_padding) + self.cell_padding
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                # Draw empty cell
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill="#CCC0B3",
                    outline="",
                    width=0
                )
        
        # Draw the tiles
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                value = self.board[y][x]
                if value == 0:
                    continue
                
                # Calculate position
                x1 = x * (self.cell_size + self.cell_padding) + self.cell_padding
                y1 = y * (self.cell_size + self.cell_padding) + self.cell_padding
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                # Choose colors
                bg_color = self.cell_colors.get(value, "#3E3933")  # Default to dark color for very high values
                fg_color = self.text_colors.get(value, "#F9F6F2")  # Default to white for very high values
                
                # Calculate font size based on number of digits
                digits = int(math.log10(value)) + 1 if value > 0 else 1
                font_size = min(24, int(48 / (digits * 0.8)))
                
                # Draw tile
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=bg_color,
                    outline="",
                    width=0
                )
                
                # Draw value
                self.canvas.create_text(
                    (x1 + x2) / 2,
                    (y1 + y2) / 2,
                    text=str(value),
                    font=("Helvetica", font_size, "bold"),
                    fill=fg_color
                )
    
    def move(self, direction):
        """Move tiles in the specified direction."""
        if self.game_over:
            return
        
        # Save the original board for comparison
        original_board = [row[:] for row in self.board]
        
        # Apply the move
        self.has_moved = False
        if direction == "up":
            self.move_up()
        elif direction == "down":
            self.move_down()
        elif direction == "left":
            self.move_left()
        elif direction == "right":
            self.move_right()
        
        # Check if the board has changed
        if self.has_moved:
            self.add_random_tile()
            self.draw_board()
            
            # Update high score if needed
            if self.score > self.high_score:
                self.high_score = self.score
                self.high_var.set(str(self.high_score))
            
            # Check for game over or win
            self.check_game_state()
    
    def move_left(self):
        """Move and merge tiles to the left."""
        for y in range(self.grid_size):
            # Shift all non-zero tiles to the left
            row = [self.board[y][x] for x in range(self.grid_size) if self.board[y][x] != 0]
            row += [0] * (self.grid_size - len(row))
            
            # Merge adjacent identical tiles
            for x in range(self.grid_size - 1):
                if row[x] != 0 and row[x] == row[x + 1]:
                    row[x] *= 2
                    row[x + 1] = 0
                    self.score += row[x]
                    self.score_var.set(str(self.score))
                    
                    # Check for win condition
                    if row[x] == 2048 and not self.won:
                        self.won = True
                        self.show_win_message()
            
            # Shift again after merging
            row = [val for val in row if val != 0]
            row += [0] * (self.grid_size - len(row))
            
            # Update the board
            for x in range(self.grid_size):
                if self.board[y][x] != row[x]:
                    self.has_moved = True
                    self.board[y][x] = row[x]
    
    def move_right(self):
        """Move and merge tiles to the right."""
        for y in range(self.grid_size):
            # Shift all non-zero tiles to the right
            row = [self.board[y][x] for x in range(self.grid_size) if self.board[y][x] != 0]
            row = [0] * (self.grid_size - len(row)) + row
            
            # Merge adjacent identical tiles from right to left
            for x in range(self.grid_size - 1, 0, -1):
                if row[x] != 0 and row[x] == row[x - 1]:
                    row[x] *= 2
                    row[x - 1] = 0
                    self.score += row[x]
                    self.score_var.set(str(self.score))
                    
                    # Check for win condition
                    if row[x] == 2048 and not self.won:
                        self.won = True
                        self.show_win_message()
            
            # Shift again after merging
            row = [val for val in row if val != 0]
            row = [0] * (self.grid_size - len(row)) + row
            
            # Update the board
            for x in range(self.grid_size):
                if self.board[y][x] != row[x]:
                    self.has_moved = True
                    self.board[y][x] = row[x]
    
    def move_up(self):
        """Move and merge tiles upward."""
        for x in range(self.grid_size):
            # Shift all non-zero tiles upward
            col = [self.board[y][x] for y in range(self.grid_size) if self.board[y][x] != 0]
            col += [0] * (self.grid_size - len(col))
            
            # Merge adjacent identical tiles
            for y in range(self.grid_size - 1):
                if col[y] != 0 and col[y] == col[y + 1]:
                    col[y] *= 2
                    col[y + 1] = 0
                    self.score += col[y]
                    self.score_var.set(str(self.score))
                    
                    # Check for win condition
                    if col[y] == 2048 and not self.won:
                        self.won = True
                        self.show_win_message()
            
            # Shift again after merging
            col = [val for val in col if val != 0]
            col += [0] * (self.grid_size - len(col))
            
            # Update the board
            for y in range(self.grid_size):
                if self.board[y][x] != col[y]:
                    self.has_moved = True
                    self.board[y][x] = col[y]
    
    def move_down(self):
        """Move and merge tiles downward."""
        for x in range(self.grid_size):
            # Shift all non-zero tiles downward
            col = [self.board[y][x] for y in range(self.grid_size) if self.board[y][x] != 0]
            col = [0] * (self.grid_size - len(col)) + col
            
            # Merge adjacent identical tiles from bottom to top
            for y in range(self.grid_size - 1, 0, -1):
                if col[y] != 0 and col[y] == col[y - 1]:
                    col[y] *= 2
                    col[y - 1] = 0
                    self.score += col[y]
                    self.score_var.set(str(self.score))
                    
                    # Check for win condition
                    if col[y] == 2048 and not self.won:
                        self.won = True
                        self.show_win_message()
            
            # Shift again after merging
            col = [val for val in col if val != 0]
            col = [0] * (self.grid_size - len(col)) + col
            
            # Update the board
            for y in range(self.grid_size):
                if self.board[y][x] != col[y]:
                    self.has_moved = True
                    self.board[y][x] = col[y]
    
    def check_game_state(self):
        """Check if the game is over or won."""
        # Check if the board is full
        is_full = all(self.board[y][x] != 0 for y in range(self.grid_size) for x in range(self.grid_size))
        
        if is_full:
            # Check if there are any possible moves
            can_move = False
            
            # Check horizontal adjacency
            for y in range(self.grid_size):
                for x in range(self.grid_size - 1):
                    if self.board[y][x] == self.board[y][x + 1]:
                        can_move = True
                        break
            
            # Check vertical adjacency
            if not can_move:
                for x in range(self.grid_size):
                    for y in range(self.grid_size - 1):
                        if self.board[y][x] == self.board[y + 1][x]:
                            can_move = True
                            break
            
            if not can_move:
                self.game_over = True
                self.instructions_label.config(text="Game Over! No more moves possible.")
                messagebox.showinfo("Game Over", f"Game Over! Your final score is {self.score}.")
    
    def show_win_message(self):
        """Show a message when the player wins."""
        self.instructions_label.config(text="You won! You can continue playing.")
        
        if messagebox.askyesno("Congratulations!", "You reached 2048! Would you like to continue playing?"):
            return
        else:
            self.new_game()
    
    def quit_game(self):
        """Quit the game."""
        if messagebox.askyesno("Quit", "Are you sure you want to quit the game?"):
            self.root.destroy()

def main():
    """Main function to start the GUI game."""
    root = tk.Tk()
    app = Game2048GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 