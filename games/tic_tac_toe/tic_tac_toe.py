#!/usr/bin/env python3
import os
import time
import colorama
from colorama import Fore, Back, Style

# Initialize colorama
colorama.init()

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the game header."""
    print(f"{Back.BLUE}{Fore.WHITE}╔═══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Back.BLUE}{Fore.WHITE}║                      TIC TAC TOE                              ║{Style.RESET_ALL}")
    print(f"{Back.BLUE}{Fore.WHITE}╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()

def print_board(board):
    """Print the game board."""
    # Color mapping for X and O
    color_map = {
        'X': Fore.RED,
        'O': Fore.BLUE,
        ' ': Fore.WHITE
    }
    
    print(f"  {Fore.YELLOW}1   2   3{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}1{Style.RESET_ALL} {color_map[board[0][0]]}{board[0][0]}{Style.RESET_ALL} | {color_map[board[0][1]]}{board[0][1]}{Style.RESET_ALL} | {color_map[board[0][2]]}{board[0][2]}{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}-----------{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}2{Style.RESET_ALL} {color_map[board[1][0]]}{board[1][0]}{Style.RESET_ALL} | {color_map[board[1][1]]}{board[1][1]}{Style.RESET_ALL} | {color_map[board[1][2]]}{board[1][2]}{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}-----------{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}3{Style.RESET_ALL} {color_map[board[2][0]]}{board[2][0]}{Style.RESET_ALL} | {color_map[board[2][1]]}{board[2][1]}{Style.RESET_ALL} | {color_map[board[2][2]]}{board[2][2]}{Style.RESET_ALL}")

def check_winner(board):
    """Check if there's a winner or a tie."""
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] != ' ':
            return row[0]
    
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != ' ':
            return board[0][col]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]
    
    # Check for a tie
    if all(board[i][j] != ' ' for i in range(3) for j in range(3)):
        return "Tie"
    
    # Game is still ongoing
    return None

def make_move(board, player, row, col):
    """Make a move on the board."""
    if 0 <= row < 3 and 0 <= col < 3 and board[row][col] == ' ':
        board[row][col] = player
        return True
    return False

def main():
    """Main game function."""
    clear_screen()
    print_header()
    
    # Game rules
    print(f"{Fore.CYAN}Welcome to Tic Tac Toe!{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Take turns placing X's and O's on the 3x3 grid.{Style.RESET_ALL}")
    print(f"{Fore.WHITE}The first player to get 3 in a row (horizontally, vertically, or diagonally) wins!{Style.RESET_ALL}")
    print()
    
    # Initialize the game
    board = [[' ' for _ in range(3)] for _ in range(3)]
    current_player = 'X'
    
    # Get player names
    player_x = input(f"{Fore.RED}Enter name for Player X: {Style.RESET_ALL}") or "Player X"
    player_o = input(f"{Fore.BLUE}Enter name for Player O: {Style.RESET_ALL}") or "Player O"
    
    # Game loop
    winner = None
    
    while winner is None:
        clear_screen()
        print_header()
        
        # Show whose turn it is
        if current_player == 'X':
            print(f"{Fore.RED}{player_x}'s turn (X){Style.RESET_ALL}")
        else:
            print(f"{Fore.BLUE}{player_o}'s turn (O){Style.RESET_ALL}")
        
        print()
        print_board(board)
        print()
        
        # Get the player's move
        while True:
            try:
                print(f"{Fore.YELLOW}Enter row and column (1-3) separated by space: {Style.RESET_ALL}", end="")
                row, col = map(int, input().split())
                row -= 1  # Convert to 0-indexed
                col -= 1  # Convert to 0-indexed
                
                if make_move(board, current_player, row, col):
                    break
                else:
                    print(f"{Fore.RED}Invalid move. The cell is either occupied or out of bounds.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Please enter two numbers separated by a space.{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        
        # Check for a winner
        winner = check_winner(board)
        
        # Switch players
        current_player = 'O' if current_player == 'X' else 'X'
    
    # Game over
    clear_screen()
    print_header()
    print_board(board)
    print()
    
    if winner == 'X':
        print(f"{Fore.RED}{player_x} (X) wins!{Style.RESET_ALL}")
    elif winner == 'O':
        print(f"{Fore.BLUE}{player_o} (O) wins!{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}It's a tie!{Style.RESET_ALL}")
    
    # Ask to play again
    print()
    play_again = input(f"{Fore.CYAN}Would you like to play again? (y/n): {Style.RESET_ALL}").lower()
    
    if play_again.startswith('y'):
        main()  # Restart the game

if __name__ == "__main__":
    main() 