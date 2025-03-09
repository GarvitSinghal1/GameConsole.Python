#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
import random

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("500x600")
        self.root.configure(bg="#333333")
        self.root.resizable(False, False)
        
        # Game variables
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.player_x_name = "Player X"
        self.player_o_name = "Player O"
        self.game_over = False
        
        # Create UI elements
        self.create_widgets()
        
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
            text="Tic Tac Toe", 
            font=("Helvetica", 24, "bold"),
            bg="#333333",
            fg="#66CCFF"  # Blue
        )
        self.title_label.pack(pady=10)
        
        # Welcome frame (shown initially)
        self.welcome_frame = tk.Frame(main_frame, bg="#333333")
        self.welcome_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Player name entries will be added to welcome frame
        
        # Game frame (shown during gameplay)
        self.game_frame = tk.Frame(main_frame, bg="#333333")
        
        # Status label
        self.status_label = tk.Label(
            self.game_frame,
            text="",
            font=("Helvetica", 16, "bold"),
            bg="#333333",
            fg="#FFFFFF"
        )
        self.status_label.pack(pady=10)
        
        # Board frame
        self.board_frame = tk.Frame(
            self.game_frame,
            bg="#222222",
            bd=3,
            relief=tk.RAISED
        )
        self.board_frame.pack(padx=10, pady=10)
        
        # Create buttons for the board
        self.board_buttons = []
        for row in range(3):
            button_row = []
            for col in range(3):
                button = tk.Button(
                    self.board_frame,
                    text="",
                    font=("Helvetica", 36, "bold"),
                    width=3,
                    height=1,
                    bg="#111111",
                    fg="#FFFFFF",
                    activebackground="#222222",
                    activeforeground="#FFFFFF",
                    command=lambda r=row, c=col: self.make_move(r, c)
                )
                button.grid(row=row, column=col, padx=5, pady=5)
                button_row.append(button)
            self.board_buttons.append(button_row)
        
        # Control frame
        control_frame = tk.Frame(main_frame, bg="#333333")
        control_frame.pack(fill=tk.X, pady=10)
        
        # New Game button
        self.new_game_button = tk.Button(
            control_frame,
            text="New Game",
            command=self.confirm_new_game,
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
    
    def show_welcome(self):
        """Show the welcome screen."""
        # Clear welcome frame first
        for widget in self.welcome_frame.winfo_children():
            widget.destroy()
        
        # Hide game frame if visible
        self.game_frame.pack_forget()
        
        # Show welcome frame
        self.welcome_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Welcome message
        welcome_label = tk.Label(
            self.welcome_frame,
            text="Welcome to Tic Tac Toe!",
            font=("Helvetica", 18),
            bg="#333333",
            fg="#FFFFFF"
        )
        welcome_label.pack(pady=10)
        
        instructions = tk.Label(
            self.welcome_frame,
            text="Enter player names and click Start Game:",
            font=("Helvetica", 14),
            bg="#333333",
            fg="#FFFFFF"
        )
        instructions.pack(pady=10)
        
        # Player X name entry
        player_x_frame = tk.Frame(self.welcome_frame, bg="#333333")
        player_x_frame.pack(fill=tk.X, padx=50, pady=10)
        
        player_x_label = tk.Label(
            player_x_frame,
            text="Player X (goes first):",
            font=("Helvetica", 12),
            bg="#333333",
            fg="#FF6666"  # Red for X
        )
        player_x_label.pack(side=tk.LEFT, padx=5)
        
        self.player_x_entry = tk.Entry(
            player_x_frame,
            font=("Helvetica", 12),
            bg="#111111",
            fg="#FF6666",
            insertbackground="#FFFFFF"
        )
        self.player_x_entry.insert(0, "Player X")
        self.player_x_entry.pack(side=tk.RIGHT, padx=5, fill=tk.X, expand=True)
        
        # Player O name entry
        player_o_frame = tk.Frame(self.welcome_frame, bg="#333333")
        player_o_frame.pack(fill=tk.X, padx=50, pady=10)
        
        player_o_label = tk.Label(
            player_o_frame,
            text="Player O:",
            font=("Helvetica", 12),
            bg="#333333",
            fg="#66CCFF"  # Blue for O
        )
        player_o_label.pack(side=tk.LEFT, padx=5)
        
        self.player_o_entry = tk.Entry(
            player_o_frame,
            font=("Helvetica", 12),
            bg="#111111",
            fg="#66CCFF",
            insertbackground="#FFFFFF"
        )
        self.player_o_entry.insert(0, "Player O")
        self.player_o_entry.pack(side=tk.RIGHT, padx=5, fill=tk.X, expand=True)
        
        # Game rules
        rules_text = (
            "Game Rules:\n"
            "1. Players take turns placing their symbol on the board\n"
            "2. X always goes first\n"
            "3. The first player to get 3 in a row wins\n"
            "4. If the board fills up with no winner, it's a tie"
        )
        
        rules_label = tk.Label(
            self.welcome_frame,
            text=rules_text,
            font=("Helvetica", 12),
            bg="#333333",
            fg="#CCFF99",  # Green
            justify=tk.LEFT
        )
        rules_label.pack(pady=20)
        
        # Start Game button
        start_button = tk.Button(
            self.welcome_frame,
            text="Start Game",
            command=self.start_game,
            bg="#66CCFF",  # Blue
            fg="#000000",
            activebackground="#3399CC",
            activeforeground="#FFFFFF",
            font=("Helvetica", 14, "bold"),
            width=15,
            height=2
        )
        start_button.pack(pady=20)
    
    def start_game(self):
        """Start the game with entered player names."""
        # Get player names
        self.player_x_name = self.player_x_entry.get() or "Player X"
        self.player_o_name = self.player_o_entry.get() or "Player O"
        
        # Hide welcome frame
        self.welcome_frame.pack_forget()
        
        # Show game frame
        self.game_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Initialize a new game
        self.new_game()
    
    def new_game(self):
        """Start a new game."""
        # Reset the board
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        
        # Reset buttons
        for row in range(3):
            for col in range(3):
                self.board_buttons[row][col].config(
                    text="",
                    bg="#111111",
                    state=tk.NORMAL
                )
        
        # X always starts
        self.current_player = 'X'
        self.game_over = False
        
        # Update status
        self.status_label.config(
            text=f"{self.player_x_name}'s turn (X)",
            fg="#FF6666"  # Red for X
        )
    
    def confirm_new_game(self):
        """Confirm before starting a new game."""
        if not self.game_over:
            if not messagebox.askyesno("New Game", "Are you sure you want to start a new game?"):
                return
        self.new_game()
    
    def make_move(self, row, col):
        """Handle a player's move."""
        if self.game_over or self.board[row][col] != ' ':
            return
        
        # Update the board
        self.board[row][col] = self.current_player
        
        # Update the button
        text_color = "#FF6666" if self.current_player == 'X' else "#66CCFF"
        self.board_buttons[row][col].config(
            text=self.current_player,
            fg=text_color
        )
        
        # Check for winner or tie
        winner = self.check_winner()
        
        if winner:
            self.game_over = True
            if winner == 'X':
                self.status_label.config(
                    text=f"{self.player_x_name} (X) wins!",
                    fg="#FF6666"  # Red for X
                )
                self.highlight_winning_line()
            elif winner == 'O':
                self.status_label.config(
                    text=f"{self.player_o_name} (O) wins!",
                    fg="#66CCFF"  # Blue for O
                )
                self.highlight_winning_line()
            else:  # Tie
                self.status_label.config(
                    text="It's a tie!",
                    fg="#FFFF99"  # Yellow
                )
        else:
            # Switch players
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            
            # Update status
            if self.current_player == 'X':
                self.status_label.config(
                    text=f"{self.player_x_name}'s turn (X)",
                    fg="#FF6666"  # Red for X
                )
            else:
                self.status_label.config(
                    text=f"{self.player_o_name}'s turn (O)",
                    fg="#66CCFF"  # Blue for O
                )
    
    def check_winner(self):
        """Check if there's a winner or a tie."""
        # Check rows
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != ' ':
                self.winning_line = [(row, 0), (row, 1), (row, 2)]
                return self.board[row][0]
        
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                self.winning_line = [(0, col), (1, col), (2, col)]
                return self.board[0][col]
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            self.winning_line = [(0, 0), (1, 1), (2, 2)]
            return self.board[0][0]
        
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            self.winning_line = [(0, 2), (1, 1), (2, 0)]
            return self.board[0][2]
        
        # Check for a tie
        if all(self.board[i][j] != ' ' for i in range(3) for j in range(3)):
            return "Tie"
        
        # Game is still ongoing
        return None
    
    def highlight_winning_line(self):
        """Highlight the winning line of three."""
        highlight_color = "#444444"
        
        for row, col in self.winning_line:
            self.board_buttons[row][col].config(bg=highlight_color)
    
    def quit_game(self):
        """Quit the game."""
        if messagebox.askyesno("Quit Game", "Are you sure you want to quit?"):
            self.root.destroy()

def main():
    """Main function to start the GUI game."""
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 