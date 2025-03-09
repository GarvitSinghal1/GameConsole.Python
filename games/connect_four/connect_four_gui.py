#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox, Label, Button, Frame
import sys
import os

class ConnectFourGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect Four")
        self.root.geometry("750x650")  # Increased size for better visibility
        self.root.configure(bg="#333333")
        self.root.resizable(True, True)  # Allow resizing
        
        # Game parameters
        self.ROWS = 6
        self.COLS = 7
        self.CELL_SIZE = 60
        self.board = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.current_player = 1  # 1 for red, 2 for yellow
        self.game_over = False
        
        # Colors
        self.COLORS = {
            0: "#333333",  # Empty - dark gray (background)
            1: "#FF3333",  # Player 1 - red
            2: "#FFCC33",  # Player 2 - yellow
            "board": "#2233AA"  # Board - blue
        }
        
        # Create widgets
        self.create_widgets()
        
        # Show welcome screen
        self.show_welcome()
    
    def create_widgets(self):
        """Create the GUI widgets."""
        # Main frame with scrollbar
        self.main_frame = Frame(self.root, bg="#333333")
        self.main_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Game title
        self.title_label = Label(
            self.main_frame,
            text="Connect Four",
            font=("Helvetica", 24, "bold"),
            bg="#333333",
            fg="#FFFFFF"
        )
        self.title_label.pack(pady=10)
        
        # Status label
        self.status_label = Label(
            self.main_frame,
            text="Player 1's Turn",
            font=("Helvetica", 16),
            bg="#333333",
            fg="#FF3333"
        )
        self.status_label.pack(pady=5)
        
        # Game board frame
        self.board_frame = Frame(
            self.main_frame,
            bg=self.COLORS["board"],
            padx=10,
            pady=10
        )
        self.board_frame.pack(pady=10)
        
        # Button frame for column selection
        self.button_frame = Frame(
            self.main_frame,
            bg="#333333"
        )
        self.button_frame.pack(pady=5)
        
        # Column buttons
        self.column_buttons = []
        for col in range(self.COLS):
            btn = Button(
                self.button_frame,
                text=f"{col+1}",
                font=("Helvetica", 12),
                width=4,
                command=lambda c=col: self.make_move(c)
            )
            btn.grid(row=0, column=col, padx=5)
            self.column_buttons.append(btn)
        
        # Game board canvas
        self.canvas = tk.Canvas(
            self.board_frame,
            width=self.COLS * self.CELL_SIZE + 20,
            height=self.ROWS * self.CELL_SIZE + 20,
            bg=self.COLORS["board"],
            highlightthickness=0
        )
        self.canvas.pack()
        
        # Create the board cells
        self.cells = []
        for row in range(self.ROWS):
            cell_row = []
            for col in range(self.COLS):
                x = col * self.CELL_SIZE + 10 + self.CELL_SIZE // 2
                y = row * self.CELL_SIZE + 10 + self.CELL_SIZE // 2
                radius = self.CELL_SIZE // 2 - 5
                cell = self.canvas.create_oval(
                    x - radius, y - radius, 
                    x + radius, y + radius,
                    fill=self.COLORS[0],
                    outline="#222222",
                    width=2
                )
                cell_row.append(cell)
            self.cells.append(cell_row)
        
        # Control buttons at the bottom
        self.control_frame = Frame(self.main_frame, bg="#333333")
        self.control_frame.pack(pady=10, fill=tk.X)
        
        # New Game button
        self.new_game_button = Button(
            self.control_frame,
            text="New Game",
            font=("Helvetica", 12),
            bg="#4CAF50",
            fg="white",
            command=self.new_game
        )
        self.new_game_button.pack(side=tk.LEFT, padx=10)
        
        # Quit button
        self.quit_button = Button(
            self.control_frame,
            text="Quit",
            font=("Helvetica", 12),
            bg="#F44336",
            fg="white",
            command=self.quit_game
        )
        self.quit_button.pack(side=tk.RIGHT, padx=10)
        
        # Add keyboard binding for column selection
        self.root.bind("<Key>", self.key_press)
    
    def key_press(self, event):
        """Handle keyboard input for column selection."""
        if self.game_over:
            return
            
        # Check if the key is a number between 1-7
        try:
            col = int(event.char) - 1
            if 0 <= col < self.COLS:
                self.make_move(col)
        except ValueError:
            pass  # Not a number key, ignore
    
    def show_welcome(self):
        """Show the welcome screen."""
        welcome_window = tk.Toplevel(self.root)
        welcome_window.title("Welcome to Connect Four")
        welcome_window.geometry("450x350")  # Slightly larger
        welcome_window.configure(bg="#333333")
        welcome_window.transient(self.root)
        welcome_window.grab_set()
        welcome_window.resizable(True, True)  # Allow resizing
        
        # Welcome title
        welcome_label = Label(
            welcome_window,
            text="Welcome to Connect Four",
            font=("Helvetica", 18, "bold"),
            bg="#333333",
            fg="#FFFFFF"
        )
        welcome_label.pack(pady=(20, 10))
        
        # Instructions
        instructions_frame = Frame(welcome_window, bg="#333333", padx=20)
        instructions_frame.pack(fill=tk.BOTH, expand=True)
        
        instructions = [
            "Connect Four is a two-player game where players take",
            "turns dropping colored discs into a vertical grid.",
            "",
            "The objective is to be the first to form a horizontal,",
            "vertical, or diagonal line of four of your own discs.",
            "",
            "Click the column number buttons to drop your disc.",
            "You can also press keys 1-7 to drop pieces.",
            "",
            "Player 1: Red discs",
            "Player 2: Yellow discs"
        ]
        
        for i, text in enumerate(instructions):
            fg_color = "#FFFFFF"  # Default white
            if "Player 1" in text:
                fg_color = "#FF3333"  # Red
            elif "Player 2" in text:
                fg_color = "#FFCC33"  # Yellow
            
            Label(
                instructions_frame,
                text=text,
                font=("Helvetica", 12),
                bg="#333333",
                fg=fg_color,
                justify=tk.LEFT
            ).pack(anchor=tk.W)
        
        # Start button
        start_button = Button(
            welcome_window,
            text="Start Game",
            font=("Helvetica", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            command=welcome_window.destroy
        )
        start_button.pack(pady=20)
    
    def make_move(self, col):
        """Make a move in the selected column."""
        if self.game_over:
            return
        
        # Find the first empty row in the selected column (from bottom up)
        row = -1
        for r in range(self.ROWS-1, -1, -1):
            if self.board[r][col] == 0:
                row = r
                break
        
        # If the column is full, ignore the move
        if row == -1:
            return
        
        # Update the board
        self.board[row][col] = self.current_player
        
        # Update the visual representation
        self.canvas.itemconfig(
            self.cells[row][col],
            fill=self.COLORS[self.current_player]
        )
        
        # Check for a win
        if self.check_win(row, col):
            self.game_over = True
            winner = "Player 1" if self.current_player == 1 else "Player 2"
            self.status_label.config(
                text=f"{winner} Wins!",
                fg=self.COLORS[self.current_player]
            )
            self.highlight_winning_cells()
            return
        
        # Check for a draw
        if self.is_board_full():
            self.game_over = True
            self.status_label.config(text="It's a Draw!", fg="#FFFFFF")
            return
        
        # Switch to the other player
        self.current_player = 3 - self.current_player  # Toggle between 1 and 2
        player_color = "#FF3333" if self.current_player == 1 else "#FFCC33"
        self.status_label.config(
            text=f"Player {self.current_player}'s Turn",
            fg=player_color
        )
    
    def check_win(self, row, col):
        """Check if the current player has won after placing a piece."""
        player = self.current_player
        
        # Variables to track consecutive pieces in different directions
        directions = [
            [(0, 1)],  # Horizontal
            [(1, 0)],  # Vertical
            [(1, 1)],  # Diagonal (down-right)
            [(1, -1)]  # Diagonal (down-left)
        ]
        
        # For each direction, count consecutive pieces
        for dir_list in directions:
            count = 1  # Start with the current piece
            
            # Store winning cells for highlighting
            winning_cells = [(row, col)]
            
            for dr, dc in dir_list:
                # Check forward direction
                r, c = row, col
                for _ in range(3):  # Need 3 more for a total of 4
                    r += dr
                    c += dc
                    if (0 <= r < self.ROWS and 0 <= c < self.COLS and 
                            self.board[r][c] == player):
                        count += 1
                        winning_cells.append((r, c))
                    else:
                        break
                
                # Check backward direction (if needed)
                r, c = row, col
                for _ in range(3):  # Need 3 more for a total of 4
                    r -= dr
                    c -= dc
                    if (0 <= r < self.ROWS and 0 <= c < self.COLS and 
                            self.board[r][c] == player):
                        count += 1
                        winning_cells.append((r, c))
                    else:
                        break
            
            # If we have 4 or more in a row, it's a win
            if count >= 4:
                self.winning_cells = winning_cells
                return True
        
        return False
    
    def is_board_full(self):
        """Check if the board is full."""
        for col in range(self.COLS):
            if self.board[0][col] == 0:
                return False
        return True
    
    def highlight_winning_cells(self):
        """Highlight the winning cells."""
        for row, col in self.winning_cells:
            # Create a pulsating effect by adding a different colored outline
            self.canvas.itemconfig(
                self.cells[row][col],
                outline="#FFFFFF",
                width=3
            )
    
    def new_game(self):
        """Start a new game."""
        # Reset game state
        self.board = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.current_player = 1
        self.game_over = False
        
        # Reset visual board
        for row in range(self.ROWS):
            for col in range(self.COLS):
                self.canvas.itemconfig(
                    self.cells[row][col],
                    fill=self.COLORS[0],
                    outline="#222222",
                    width=2
                )
        
        # Reset status
        self.status_label.config(text="Player 1's Turn", fg="#FF3333")
    
    def quit_game(self):
        """Quit the game."""
        if messagebox.askyesno("Quit", "Are you sure you want to quit the game?"):
            self.root.destroy()

def main():
    """Main function to start the GUI game."""
    root = tk.Tk()
    app = ConnectFourGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 