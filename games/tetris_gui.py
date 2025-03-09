#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
import sys
import os

# Define tetromino shapes and colors
SHAPES = {
    'I': [
        [1, 1, 1, 1]
    ],
    'J': [
        [1, 0, 0],
        [1, 1, 1]
    ],
    'L': [
        [0, 0, 1],
        [1, 1, 1]
    ],
    'O': [
        [1, 1],
        [1, 1]
    ],
    'S': [
        [0, 1, 1],
        [1, 1, 0]
    ],
    'T': [
        [0, 1, 0],
        [1, 1, 1]
    ],
    'Z': [
        [1, 1, 0],
        [0, 1, 1]
    ]
}

COLORS = {
    'I': "#00FFFF",  # Cyan
    'J': "#0000FF",  # Blue
    'L': "#FF7F00",  # Orange
    'O': "#FFFF00",  # Yellow
    'S': "#00FF00",  # Green
    'T': "#800080",  # Purple
    'Z': "#FF0000"   # Red
}

class TetrisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tetris")
        self.root.geometry("600x700")
        self.root.configure(bg="#333333")
        self.root.resizable(True, True)
        
        # Game parameters
        self.cell_size = 30
        self.width = 10
        self.height = 20
        self.canvas_width = self.width * self.cell_size
        self.canvas_height = self.height * self.cell_size
        
        # Game state
        self.board = None
        self.current_piece = None
        self.current_shape = None
        self.current_x = 0
        self.current_y = 0
        self.next_piece = None
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_active = False
        self.paused = False
        self.game_over = False
        self.fall_speed = 1000  # milliseconds
        self.drop_callback_id = None
        
        # Create widgets
        self.create_widgets()
        
        # Set up keyboard bindings
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
            text="TETRIS",
            font=("Helvetica", 24, "bold"),
            bg="#333333",
            fg="#FFFFFF"
        )
        self.title_label.pack(pady=(0, 10))
        
        # Game info frame
        self.info_frame = tk.Frame(self.main_frame, bg="#333333")
        self.info_frame.pack(fill=tk.X, pady=5)
        
        # Score and level display
        self.score_frame = tk.Frame(self.info_frame, bg="#333333")
        self.score_frame.pack(side=tk.LEFT, padx=10)
        
        self.score_label = tk.Label(
            self.score_frame,
            text="Score:",
            font=("Helvetica", 12),
            bg="#333333",
            fg="#FFFFFF"
        )
        self.score_label.grid(row=0, column=0, sticky="w")
        
        self.score_var = tk.StringVar(value="0")
        self.score_value = tk.Label(
            self.score_frame,
            textvariable=self.score_var,
            font=("Helvetica", 12, "bold"),
            bg="#333333",
            fg="#FFFFFF"
        )
        self.score_value.grid(row=0, column=1, padx=5, sticky="w")
        
        self.level_label = tk.Label(
            self.score_frame,
            text="Level:",
            font=("Helvetica", 12),
            bg="#333333",
            fg="#FFFFFF"
        )
        self.level_label.grid(row=1, column=0, sticky="w")
        
        self.level_var = tk.StringVar(value="1")
        self.level_value = tk.Label(
            self.score_frame,
            textvariable=self.level_var,
            font=("Helvetica", 12, "bold"),
            bg="#333333",
            fg="#FFFFFF"
        )
        self.level_value.grid(row=1, column=1, padx=5, sticky="w")
        
        self.lines_label = tk.Label(
            self.score_frame,
            text="Lines:",
            font=("Helvetica", 12),
            bg="#333333",
            fg="#FFFFFF"
        )
        self.lines_label.grid(row=2, column=0, sticky="w")
        
        self.lines_var = tk.StringVar(value="0")
        self.lines_value = tk.Label(
            self.score_frame,
            textvariable=self.lines_var,
            font=("Helvetica", 12, "bold"),
            bg="#333333",
            fg="#FFFFFF"
        )
        self.lines_value.grid(row=2, column=1, padx=5, sticky="w")
        
        # Next piece preview
        self.next_piece_frame = tk.Frame(self.info_frame, bg="#333333")
        self.next_piece_frame.pack(side=tk.RIGHT, padx=10)
        
        self.next_piece_label = tk.Label(
            self.next_piece_frame,
            text="Next Piece:",
            font=("Helvetica", 12),
            bg="#333333",
            fg="#FFFFFF"
        )
        self.next_piece_label.pack(anchor="w")
        
        self.next_piece_canvas = tk.Canvas(
            self.next_piece_frame,
            width=4*self.cell_size,
            height=4*self.cell_size,
            bg="#000000",
            highlightthickness=1,
            highlightbackground="#FFFFFF"
        )
        self.next_piece_canvas.pack(pady=5)
        
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
            highlightthickness=1,
            highlightbackground="#FFFFFF"
        )
        self.canvas.pack(pady=10)
        
        # Draw grid on canvas
        self.draw_grid()
        
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
        self.difficulty_var = tk.StringVar(value="medium")
        
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
        self.root.bind("<Left>", lambda e: self.move_left())
        self.root.bind("<Right>", lambda e: self.move_right())
        self.root.bind("<Down>", lambda e: self.move_down())
        self.root.bind("<Up>", lambda e: self.rotate_piece())
        self.root.bind("<space>", lambda e: self.drop_piece())
        self.root.bind("<p>", lambda e: self.toggle_pause())
        self.root.bind("<P>", lambda e: self.toggle_pause())
    
    def draw_grid(self):
        """Draw the grid on the canvas."""
        for i in range(self.width + 1):
            x = i * self.cell_size
            self.canvas.create_line(x, 0, x, self.canvas_height, fill="#444444")
        
        for i in range(self.height + 1):
            y = i * self.cell_size
            self.canvas.create_line(0, y, self.canvas_width, y, fill="#444444")
    
    def show_welcome(self):
        """Show welcome screen and instructions."""
        welcome_window = tk.Toplevel(self.root)
        welcome_window.title("Welcome to Tetris")
        welcome_window.geometry("500x450")
        welcome_window.configure(bg="#333333")
        welcome_window.transient(self.root)
        welcome_window.grab_set()
        welcome_window.resizable(True, True)
        
        # Welcome title
        welcome_label = tk.Label(
            welcome_window,
            text="Welcome to Tetris",
            font=("Helvetica", 18, "bold"),
            bg="#333333",
            fg="#FFFFFF"
        )
        welcome_label.pack(pady=20)
        
        # Instructions
        instructions_frame = tk.Frame(welcome_window, bg="#333333", padx=20)
        instructions_frame.pack(fill=tk.BOTH, expand=True)
        
        instructions = [
            "Tetris is a tile-matching puzzle game where you arrange",
            "falling tetrominoes to create complete horizontal lines.",
            "",
            "Controls:",
            "• Left/Right Arrows: Move the tetromino horizontally",
            "• Down Arrow: Accelerate the tetromino's descent",
            "• Up Arrow: Rotate the tetromino clockwise",
            "• Space: Drop the tetromino instantly",
            "• P: Pause/Resume the game",
            "",
            "Scoring:",
            "• 1 line: 100 points × level",
            "• 2 lines: 300 points × level",
            "• 3 lines: 500 points × level",
            "• 4 lines: 800 points × level",
            "",
            "The game speeds up as you advance in levels,",
            "with each level requiring 10 cleared lines."
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
        """Change the game difficulty."""
        difficulty = self.difficulty_var.get()
        
        if difficulty == "easy":
            self.fall_speed = 1000  # 1 second
            self.level = 1
        elif difficulty == "medium":
            self.fall_speed = 750  # 0.75 seconds
            self.level = 3
        else:  # hard
            self.fall_speed = 500  # 0.5 seconds
            self.level = 5
        
        self.level_var.set(str(self.level))
        
        # Update status
        if not self.game_active:
            self.status_var.set(f"Difficulty set to {difficulty.capitalize()}")
    
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
        self.game_over = False
        
        # Update UI elements
        self.pause_button.config(state=tk.NORMAL, text="Pause")
        self.start_button.config(text="Restart Game")
        self.easy_radio.config(state=tk.DISABLED)
        self.medium_radio.config(state=tk.DISABLED)
        self.hard_radio.config(state=tk.DISABLED)
        
        # Update status
        self.status_var.set("Game started - Good luck!")
        
        # Start the game loop
        self.new_piece()
        self.schedule_drop()
    
    def reset_game(self):
        """Reset the game state."""
        # Clear any scheduled drops
        if self.drop_callback_id:
            self.root.after_cancel(self.drop_callback_id)
            self.drop_callback_id = None
        
        # Reset scores
        self.score = 0
        self.lines_cleared = 0
        self.score_var.set("0")
        self.lines_var.set("0")
        
        # Reset board
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.current_piece = None
        self.current_shape = None
        self.next_piece = self.get_random_shape()
        
        # Reset game state
        self.game_active = False
        self.paused = False
        self.game_over = False
        
        # Clear canvas
        self.canvas.delete("block")
        self.next_piece_canvas.delete("block")
        
        # Draw next piece
        self.draw_next_piece()
    
    def get_random_shape(self):
        """Get a random tetromino shape."""
        return random.choice(list(SHAPES.keys()))
    
    def new_piece(self):
        """Create a new tetromino piece."""
        self.current_shape = self.next_piece
        self.next_piece = self.get_random_shape()
        self.current_piece = SHAPES[self.current_shape]
        
        # Start position (centered at top)
        self.current_x = self.width // 2 - len(self.current_piece[0]) // 2
        self.current_y = 0
        
        # Draw next piece
        self.draw_next_piece()
        
        # Check if the new piece can be placed
        if not self.is_valid_position():
            self.game_over = True
            self.game_active = False
            self.status_var.set("Game Over!")
            messagebox.showinfo("Game Over", f"Game Over! Your final score is {self.score}.")
            
            # Enable UI elements
            self.easy_radio.config(state=tk.NORMAL)
            self.medium_radio.config(state=tk.NORMAL)
            self.hard_radio.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)
            self.start_button.config(text="Start Game")
            
            return False
        
        return True
    
    def draw_next_piece(self):
        """Draw the next piece in the preview area."""
        self.next_piece_canvas.delete("block")
        
        next_shape = SHAPES[self.next_piece]
        color = COLORS[self.next_piece]
        
        # Center the piece in the preview
        offset_x = (4 - len(next_shape[0])) * self.cell_size // 2
        offset_y = (4 - len(next_shape)) * self.cell_size // 2
        
        for y, row in enumerate(next_shape):
            for x, cell in enumerate(row):
                if cell:
                    self.next_piece_canvas.create_rectangle(
                        x * self.cell_size + offset_x,
                        y * self.cell_size + offset_y,
                        (x + 1) * self.cell_size + offset_x,
                        (y + 1) * self.cell_size + offset_y,
                        fill=color,
                        outline="#FFFFFF",
                        tags="block"
                    )
    
    def is_valid_position(self, x_offset=0, y_offset=0):
        """Check if the current piece can be at the current position with offsets."""
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    board_x = self.current_x + x + x_offset
                    board_y = self.current_y + y + y_offset
                    
                    # Check if out of bounds
                    if (board_x < 0 or board_x >= self.width or 
                        board_y < 0 or board_y >= self.height):
                        return False
                    
                    # Check if collides with locked piece
                    if board_y >= 0 and self.board[board_y][board_x]:
                        return False
        
        return True
    
    def rotate_piece(self):
        """Rotate the current piece clockwise."""
        if not self.game_active or self.paused or self.game_over:
            return
        
        # Save the original piece to restore if rotation is not valid
        original_piece = self.current_piece
        
        # Get dimensions
        rows = len(self.current_piece)
        cols = len(self.current_piece[0])
        
        # Create a new rotated piece
        rotated = [[0 for _ in range(rows)] for _ in range(cols)]
        
        # Fill the rotated piece
        for r in range(rows):
            for c in range(cols):
                rotated[c][rows - 1 - r] = self.current_piece[r][c]
        
        # Apply rotation if valid
        self.current_piece = rotated
        if not self.is_valid_position():
            self.current_piece = original_piece
            return False
        
        # Redraw the board
        self.draw_board()
        return True
    
    def move_left(self):
        """Move the current piece left if possible."""
        if not self.game_active or self.paused or self.game_over:
            return
        
        if self.is_valid_position(x_offset=-1):
            self.current_x -= 1
            self.draw_board()
            return True
        return False
    
    def move_right(self):
        """Move the current piece right if possible."""
        if not self.game_active or self.paused or self.game_over:
            return
        
        if self.is_valid_position(x_offset=1):
            self.current_x += 1
            self.draw_board()
            return True
        return False
    
    def move_down(self):
        """Move the current piece down if possible."""
        if not self.game_active or self.paused or self.game_over:
            return False
        
        if self.is_valid_position(y_offset=1):
            self.current_y += 1
            self.draw_board()
            return True
        
        # If can't move down, lock the piece
        self.lock_piece()
        return False
    
    def drop_piece(self):
        """Drop the piece to the bottom instantly."""
        if not self.game_active or self.paused or self.game_over:
            return
        
        while self.move_down():
            pass
    
    def lock_piece(self):
        """Lock the current piece into the board."""
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    board_y = self.current_y + y
                    board_x = self.current_x + x
                    if 0 <= board_y < self.height and 0 <= board_x < self.width:
                        self.board[board_y][board_x] = self.current_shape
        
        # Check for completed lines
        lines_cleared = self.clear_lines()
        
        # Create a new piece
        if not self.new_piece():
            return
        
        # Reschedule the drop
        self.schedule_drop()
    
    def clear_lines(self):
        """Clear completed lines and return the number of lines cleared."""
        lines_to_clear = []
        
        # Find lines to clear
        for y in range(self.height):
            if all(self.board[y]):
                lines_to_clear.append(y)
        
        # Clear the lines
        for y in lines_to_clear:
            # Remove the line
            self.board.pop(y)
            # Add a new empty line at the top
            self.board.insert(0, [0 for _ in range(self.width)])
        
        # Update score and level
        if lines_to_clear:
            self.lines_cleared += len(lines_to_clear)
            self.lines_var.set(str(self.lines_cleared))
            
            # Calculate score: more lines = more points per line
            line_score = {1: 100, 2: 300, 3: 500, 4: 800}
            self.score += line_score.get(len(lines_to_clear), 100) * self.level
            self.score_var.set(str(self.score))
            
            # Update level (every 10 lines)
            new_level = (self.lines_cleared // 10) + 1
            if new_level > self.level:
                self.level = new_level
                self.level_var.set(str(self.level))
                
                # Increase speed with level
                self.fall_speed = max(100, 1000 - (self.level - 1) * 100)
        
        # Redraw the board
        self.draw_board()
        
        return len(lines_to_clear)
    
    def schedule_drop(self):
        """Schedule the next automatic drop."""
        if self.game_active and not self.paused and not self.game_over:
            # Cancel any existing callback
            if self.drop_callback_id:
                self.root.after_cancel(self.drop_callback_id)
            
            # Schedule the next drop
            self.drop_callback_id = self.root.after(self.fall_speed, self.move_down)
    
    def toggle_pause(self):
        """Toggle the game pause state."""
        if not self.game_active or self.game_over:
            return
        
        self.paused = not self.paused
        
        if self.paused:
            self.pause_button.config(text="Resume")
            self.status_var.set("Game Paused")
            
            # Cancel the drop callback
            if self.drop_callback_id:
                self.root.after_cancel(self.drop_callback_id)
                self.drop_callback_id = None
        else:
            self.pause_button.config(text="Pause")
            self.status_var.set("Game Resumed")
            
            # Reschedule the drop
            self.schedule_drop()
    
    def draw_board(self):
        """Draw the game board on the canvas."""
        self.canvas.delete("block")
        
        # Draw ghost piece (preview of where the piece will land)
        ghost_y = self.current_y
        while self.is_valid_position(y_offset=ghost_y - self.current_y + 1):
            ghost_y += 1
        
        # Draw the ghost piece
        if self.current_piece:
            for y, row in enumerate(self.current_piece):
                for x, cell in enumerate(row):
                    if cell:
                        board_y = ghost_y + y
                        board_x = self.current_x + x
                        if 0 <= board_y < self.height and 0 <= board_x < self.width:
                            self.canvas.create_rectangle(
                                board_x * self.cell_size,
                                board_y * self.cell_size,
                                (board_x + 1) * self.cell_size,
                                (board_y + 1) * self.cell_size,
                                fill="#AAAAAA",
                                outline="#FFFFFF",
                                stipple="gray50",
                                tags="block"
                            )
        
        # Draw the current piece
        if self.current_piece:
            for y, row in enumerate(self.current_piece):
                for x, cell in enumerate(row):
                    if cell:
                        board_y = self.current_y + y
                        board_x = self.current_x + x
                        if 0 <= board_y < self.height and 0 <= board_x < self.width:
                            self.canvas.create_rectangle(
                                board_x * self.cell_size,
                                board_y * self.cell_size,
                                (board_x + 1) * self.cell_size,
                                (board_y + 1) * self.cell_size,
                                fill=COLORS[self.current_shape],
                                outline="#FFFFFF",
                                tags="block"
                            )
        
        # Draw the locked pieces on the board
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x]:
                    shape = self.board[y][x]
                    self.canvas.create_rectangle(
                        x * self.cell_size,
                        y * self.cell_size,
                        (x + 1) * self.cell_size,
                        (y + 1) * self.cell_size,
                        fill=COLORS[shape],
                        outline="#FFFFFF",
                        tags="block"
                    )
    
    def quit_game(self):
        """Quit the game."""
        if messagebox.askyesno("Quit", "Are you sure you want to quit the game?"):
            self.root.destroy()

def main():
    """Main function to start the GUI game."""
    root = tk.Tk()
    app = TetrisGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 