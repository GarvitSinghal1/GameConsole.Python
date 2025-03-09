#!/usr/bin/env python3
import os
import sys
import time
import random
import colorama
from colorama import Fore, Back, Style

# Initialize colorama for Windows
colorama.init(autoreset=True)

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the game header."""
    print(f"{Back.BLUE}{Fore.WHITE}╔═══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Back.BLUE}{Fore.WHITE}║                     CONNECT FOUR                              ║{Style.RESET_ALL}")
    print(f"{Back.BLUE}{Fore.WHITE}╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()

class ConnectFour:
    def __init__(self):
        self.ROWS = 6
        self.COLS = 7
        self.board = [[' ' for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.player1 = f"{Fore.RED}●{Style.RESET_ALL}"
        self.player2 = f"{Fore.YELLOW}●{Style.RESET_ALL}"
        self.current_player = self.player1
        self.current_player_num = 1
        self.game_over = False
        self.winner = None
    
    def print_board(self):
        """Print the game board."""
        # Print column numbers
        print('  ', end='')
        for col in range(self.COLS):
            print(f" {col+1}  ", end='')
        print()
        
        # Print top border
        print('  ' + '═══' * self.COLS + '═')
        
        # Print board contents
        for row in range(self.ROWS):
            print('║ ', end='')
            for col in range(self.COLS):
                print(f" {self.board[row][col]} ║", end='')
            print()
            if row < self.ROWS - 1:
                print('  ' + '═══' * self.COLS + '═')
        
        # Print bottom border
        print('  ' + '═══' * self.COLS + '═')
        
        # Print column numbers again
        print('  ', end='')
        for col in range(self.COLS):
            print(f" {col+1}  ", end='')
        print("\n")
    
    def is_valid_move(self, col):
        """Check if a move is valid."""
        # Check if the column is within range
        if col < 0 or col >= self.COLS:
            return False
        
        # Check if the top position in the column is empty
        return self.board[0][col] == ' '
    
    def drop_piece(self, col):
        """Drop a piece into the specified column."""
        # Find the lowest empty row in the column
        for row in range(self.ROWS-1, -1, -1):
            if self.board[row][col] == ' ':
                self.board[row][col] = self.current_player
                return row
        return -1  # Column is full (should not happen with is_valid_move check)
    
    def check_win(self, row, col):
        """Check if the current player has won after placing a piece."""
        piece = self.current_player
        
        # Check horizontal
        for c in range(max(0, col-3), min(col+1, self.COLS-3)):
            if (self.board[row][c] == piece and 
                self.board[row][c+1] == piece and 
                self.board[row][c+2] == piece and 
                self.board[row][c+3] == piece):
                return True
        
        # Check vertical
        for r in range(max(0, row-3), min(row+1, self.ROWS-3)):
            if (self.board[r][col] == piece and 
                self.board[r+1][col] == piece and 
                self.board[r+2][col] == piece and 
                self.board[r+3][col] == piece):
                return True
        
        # Check diagonal (down-right)
        for r, c in zip(range(max(0, row-3), min(row+1, self.ROWS-3)), 
                       range(max(0, col-3), min(col+1, self.COLS-3))):
            if (self.board[r][c] == piece and 
                self.board[r+1][c+1] == piece and 
                self.board[r+2][c+2] == piece and 
                self.board[r+3][c+3] == piece):
                return True
        
        # Check diagonal (up-right)
        for r, c in zip(range(min(self.ROWS-1, row+3), max(row, 2), -1), 
                       range(max(0, col-3), min(col+1, self.COLS-3))):
            if (self.board[r][c] == piece and 
                self.board[r-1][c+1] == piece and 
                self.board[r-2][c+2] == piece and 
                self.board[r-3][c+3] == piece):
                return True
        
        return False
    
    def is_board_full(self):
        """Check if the board is full."""
        for col in range(self.COLS):
            if self.board[0][col] == ' ':
                return False
        return True
    
    def switch_player(self):
        """Switch to the other player."""
        if self.current_player == self.player1:
            self.current_player = self.player2
            self.current_player_num = 2
        else:
            self.current_player = self.player1
            self.current_player_num = 1
    
    def play_turn(self):
        """Play a single turn."""
        player_name = f"Player {self.current_player_num}"
        
        while True:
            try:
                col = int(input(f"{player_name}, choose a column (1-{self.COLS}): ")) - 1
                
                if not self.is_valid_move(col):
                    print(f"{Fore.RED}Invalid move. Column is either full or out of range.{Style.RESET_ALL}")
                    continue
                
                # Drop the piece and get the row where it landed
                row = self.drop_piece(col)
                
                # Check for a win
                if self.check_win(row, col):
                    self.game_over = True
                    self.winner = player_name
                    return
                
                # Check for a draw
                if self.is_board_full():
                    self.game_over = True
                    return
                
                # Switch to the other player
                self.switch_player()
                return
                
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
    
    def display_result(self):
        """Display the game result."""
        self.print_board()
        
        if self.winner:
            print(f"{Fore.GREEN}Congratulations! {self.winner} wins!{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}It's a draw! The board is full.{Style.RESET_ALL}")
    
    def play_game(self):
        """Play the full game."""
        while not self.game_over:
            clear_screen()
            print_header()
            self.print_board()
            self.play_turn()
        
        # Show final result
        clear_screen()
        print_header()
        self.display_result()

def show_instructions():
    """Display game instructions."""
    print(f"{Fore.CYAN}INSTRUCTIONS:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Connect Four is a two-player game where players take turns")
    print(f"dropping colored discs into a vertical grid. The objective")
    print(f"is to be the first to form a horizontal, vertical, or")
    print(f"diagonal line of four of your own discs.{Style.RESET_ALL}")
    print()
    print(f"{Fore.WHITE}To play, enter the column number (1-7) where you want to")
    print(f"drop your disc. The disc will fall to the lowest available")
    print(f"position in that column.{Style.RESET_ALL}")
    print()
    print(f"{Fore.RED}Player 1: Red discs{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Player 2: Yellow discs{Style.RESET_ALL}")
    print()
    input(f"{Fore.GREEN}Press Enter to start the game...{Style.RESET_ALL}")

def main():
    """Main game function."""
    clear_screen()
    print_header()
    show_instructions()
    
    while True:
        game = ConnectFour()
        game.play_game()
        
        # Ask to play again
        print()
        play_again = input(f"{Fore.CYAN}Play again? (y/n): {Style.RESET_ALL}").lower()
        if play_again != 'y':
            clear_screen()
            print_header()
            print(f"{Fore.GREEN}Thanks for playing Connect Four!{Style.RESET_ALL}")
            time.sleep(2)
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print_header()
        print(f"{Fore.GREEN}Thanks for playing Connect Four!{Style.RESET_ALL}")
        sys.exit(0) 