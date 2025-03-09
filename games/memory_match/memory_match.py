#!/usr/bin/env python3
import os
import sys
import time
import random
import colorama
from colorama import Fore, Back, Style

# Initialize colorama
colorama.init(autoreset=True)

# Card symbols for different difficulties
CARD_SYMBOLS = {
    "easy": ['♥', '♦', '♠', '♣', '★', '●', '■', '▲'],  # 8 symbols (16 cards total)
    "medium": ['♥', '♦', '♠', '♣', '★', '●', '■', '▲', '◆', '□', '△', '○'],  # 12 symbols (24 cards total)
    "hard": ['♥', '♦', '♠', '♣', '★', '●', '■', '▲', '◆', '□', '△', '○', '♪', '♫', '☼', '☀', '☁', '☂']  # 18 symbols (36 cards total)
}

# Card colors
CARD_COLORS = [
    Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW, 
    Fore.MAGENTA, Fore.CYAN, Fore.WHITE
]

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the game header."""
    print(f"{Back.MAGENTA}{Fore.WHITE}╔═══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Back.MAGENTA}{Fore.WHITE}║                     MEMORY MATCH                              ║{Style.RESET_ALL}")
    print(f"{Back.MAGENTA}{Fore.WHITE}╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()

class MemoryMatch:
    def __init__(self, difficulty="medium"):
        """Initialize the Memory Match game."""
        self.difficulty = difficulty
        self.symbols = CARD_SYMBOLS[difficulty]
        self.num_pairs = len(self.symbols)
        
        # Create the deck with pairs of symbols
        self.deck = self.symbols * 2
        random.shuffle(self.deck)
        
        # Assign random colors to symbols
        self.symbol_colors = {}
        for symbol in self.symbols:
            self.symbol_colors[symbol] = random.choice(CARD_COLORS)
        
        # Determine grid size based on difficulty
        if difficulty == "easy":
            self.rows, self.cols = 4, 4
        elif difficulty == "medium":
            self.rows, self.cols = 4, 6
        else:  # hard
            self.rows, self.cols = 6, 6
        
        # Reshape deck to grid
        self.grid = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                if i * self.cols + j < len(self.deck):
                    row.append(self.deck[i * self.cols + j])
                else:
                    row.append(None)  # Empty cell for odd-sized grids
            self.grid.append(row)
        
        # Game state
        self.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.matched = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.moves = 0
        self.matches = 0
        self.first_card = None
    
    def display_board(self):
        """Display the current game board."""
        # Print column headers
        print("    ", end="")
        for j in range(self.cols):
            print(f" {j+1}  ", end="")
        print("\n")
        
        # Print rows
        for i in range(self.rows):
            print(f" {i+1} ", end="")
            for j in range(self.cols):
                if self.grid[i][j] is None:
                    # Empty cell
                    print("    ", end="")
                elif self.matched[i][j]:
                    # Matched card
                    symbol = self.grid[i][j]
                    color = self.symbol_colors[symbol]
                    print(f" {color}{symbol} {Style.RESET_ALL}", end="")
                elif self.revealed[i][j]:
                    # Currently revealed card
                    symbol = self.grid[i][j]
                    color = self.symbol_colors[symbol]
                    print(f" {color}{symbol} {Style.RESET_ALL}", end="")
                else:
                    # Hidden card
                    print(f" {Fore.WHITE}? {Style.RESET_ALL}", end="")
            print()
        print()
    
    def reveal_card(self, row, col):
        """Reveal a card at the specified position."""
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return False, "Invalid position. Please try again."
        
        if self.grid[row][col] is None:
            return False, "There is no card at this position."
        
        if self.matched[row][col] or self.revealed[row][col]:
            return False, "This card is already revealed."
        
        # Reveal the card
        self.revealed[row][col] = True
        
        return True, ""
    
    def hide_unmatched(self):
        """Hide all unmatched cards."""
        for i in range(self.rows):
            for j in range(self.cols):
                if not self.matched[i][j]:
                    self.revealed[i][j] = False
    
    def check_match(self, row1, col1, row2, col2):
        """Check if two revealed cards match."""
        if self.grid[row1][col1] == self.grid[row2][col2]:
            self.matched[row1][col1] = True
            self.matched[row2][col2] = True
            self.matches += 1
            return True
        return False
    
    def is_game_over(self):
        """Check if the game is over (all matches found)."""
        return self.matches == self.num_pairs
    
    def play_turn(self):
        """Play a single turn (reveal two cards)."""
        # First card
        while True:
            clear_screen()
            print_header()
            print(f"{Fore.CYAN}Moves: {self.moves} | Matches: {self.matches}/{self.num_pairs}{Style.RESET_ALL}")
            print()
            self.display_board()
            
            try:
                card1_input = input(f"{Fore.YELLOW}Enter position of first card (row,col) or 'q' to quit: {Style.RESET_ALL}")
                
                if card1_input.lower() == 'q':
                    return "quit"
                
                row1, col1 = map(int, card1_input.split(','))
                row1 -= 1  # Convert to 0-indexed
                col1 -= 1
                
                success, message = self.reveal_card(row1, col1)
                if not success:
                    print(f"{Fore.RED}{message}{Style.RESET_ALL}")
                    time.sleep(1)
                    continue
                
                break
            except (ValueError, IndexError):
                print(f"{Fore.RED}Invalid input. Please enter row,col (e.g., 1,2){Style.RESET_ALL}")
                time.sleep(1)
        
        # Second card
        while True:
            clear_screen()
            print_header()
            print(f"{Fore.CYAN}Moves: {self.moves} | Matches: {self.matches}/{self.num_pairs}{Style.RESET_ALL}")
            print()
            self.display_board()
            
            try:
                card2_input = input(f"{Fore.YELLOW}Enter position of second card (row,col) or 'q' to quit: {Style.RESET_ALL}")
                
                if card2_input.lower() == 'q':
                    return "quit"
                
                row2, col2 = map(int, card2_input.split(','))
                row2 -= 1  # Convert to 0-indexed
                col2 -= 1
                
                # Can't select the same card
                if row1 == row2 and col1 == col2:
                    print(f"{Fore.RED}You can't select the same card twice.{Style.RESET_ALL}")
                    time.sleep(1)
                    continue
                
                success, message = self.reveal_card(row2, col2)
                if not success:
                    print(f"{Fore.RED}{message}{Style.RESET_ALL}")
                    time.sleep(1)
                    continue
                
                break
            except (ValueError, IndexError):
                print(f"{Fore.RED}Invalid input. Please enter row,col (e.g., 1,2){Style.RESET_ALL}")
                time.sleep(1)
        
        # Increment move counter
        self.moves += 1
        
        # Show both cards
        clear_screen()
        print_header()
        print(f"{Fore.CYAN}Moves: {self.moves} | Matches: {self.matches}/{self.num_pairs}{Style.RESET_ALL}")
        print()
        self.display_board()
        
        # Check for match
        if self.check_match(row1, col1, row2, col2):
            print(f"{Fore.GREEN}Match found!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}No match.{Style.RESET_ALL}")
            time.sleep(1.5)
            self.hide_unmatched()
        
        time.sleep(0.5)
        return "continue"

def show_instructions():
    """Display game instructions."""
    print(f"{Fore.CYAN}INSTRUCTIONS:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Memory Match is a card-matching game where you need to find all")
    print(f"matching pairs of symbols. The game starts with all cards face down.{Style.RESET_ALL}")
    print()
    print(f"{Fore.WHITE}Each turn, you select two cards to reveal by entering their")
    print(f"row and column coordinates (e.g., 1,2 for row 1, column 2).{Style.RESET_ALL}")
    print()
    print(f"{Fore.WHITE}If the two cards match, they remain face up. If not, they")
    print(f"are turned face down again. The game ends when all pairs are found.{Style.RESET_ALL}")
    print()
    print(f"{Fore.WHITE}Try to complete the game in as few moves as possible!{Style.RESET_ALL}")
    print()
    input(f"{Fore.GREEN}Press Enter to start the game...{Style.RESET_ALL}")

def main():
    """Main game function."""
    clear_screen()
    print_header()
    show_instructions()
    
    while True:
        clear_screen()
        print_header()
        
        # Choose difficulty
        print(f"{Fore.CYAN}Choose difficulty:{Style.RESET_ALL}")
        print(f"1. Easy (4x4 grid, 8 pairs)")
        print(f"2. Medium (4x6 grid, 12 pairs)")
        print(f"3. Hard (6x6 grid, 18 pairs)")
        print()
        
        while True:
            try:
                choice = int(input(f"{Fore.YELLOW}Enter your choice (1-3): {Style.RESET_ALL}"))
                if 1 <= choice <= 3:
                    break
                else:
                    print(f"{Fore.RED}Please enter a number between 1 and 3.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
        
        difficulty = {1: "easy", 2: "medium", 3: "hard"}[choice]
        
        # Create and play the game
        game = MemoryMatch(difficulty)
        game_result = "continue"
        
        while game_result == "continue" and not game.is_game_over():
            game_result = game.play_turn()
        
        if game_result == "quit":
            clear_screen()
            print_header()
            print(f"{Fore.YELLOW}Game aborted. Thanks for playing!{Style.RESET_ALL}")
        elif game.is_game_over():
            clear_screen()
            print_header()
            print(f"{Fore.CYAN}Moves: {game.moves} | Matches: {game.matches}/{game.num_pairs}{Style.RESET_ALL}")
            print()
            game.display_board()
            print(f"{Fore.GREEN}Congratulations! You found all pairs in {game.moves} moves!{Style.RESET_ALL}")
            
            # Provide rating based on number of moves
            perfect_score = game.num_pairs * 2  # Theoretical minimum number of moves
            if game.moves <= perfect_score:
                print(f"{Fore.MAGENTA}Perfect memory! Incredible performance!{Style.RESET_ALL}")
            elif game.moves <= perfect_score * 1.5:
                print(f"{Fore.CYAN}Excellent! You have a great memory!{Style.RESET_ALL}")
            elif game.moves <= perfect_score * 2:
                print(f"{Fore.GREEN}Very good! You have a good memory!{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}Good job! Keep practicing to improve your memory!{Style.RESET_ALL}")
        
        # Ask to play again
        print()
        play_again = input(f"{Fore.CYAN}Play again? (y/n): {Style.RESET_ALL}").lower()
        if play_again != 'y':
            clear_screen()
            print_header()
            print(f"{Fore.GREEN}Thanks for playing Memory Match!{Style.RESET_ALL}")
            time.sleep(1.5)
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print_header()
        print(f"{Fore.GREEN}Thanks for playing Memory Match!{Style.RESET_ALL}")
        sys.exit(0) 