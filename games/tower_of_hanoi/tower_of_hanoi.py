#!/usr/bin/env python3
import os
import sys
import time
import colorama
from colorama import Fore, Back, Style

# Initialize colorama
colorama.init(autoreset=True)

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the game header."""
    print(f"{Back.MAGENTA}{Fore.WHITE}╔═══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Back.MAGENTA}{Fore.WHITE}║                    TOWER OF HANOI                             ║{Style.RESET_ALL}")
    print(f"{Back.MAGENTA}{Fore.WHITE}╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()

class TowerOfHanoi:
    def __init__(self, num_discs=3):
        """Initialize the Tower of Hanoi game."""
        self.num_discs = num_discs
        # Initialize the 3 pegs (towers)
        self.pegs = [
            list(range(num_discs, 0, -1)),  # First peg with all discs (largest disc at bottom)
            [],  # Second peg (empty)
            []   # Third peg (empty)
        ]
        self.moves = 0
        self.min_moves = 2 ** num_discs - 1  # Minimum number of moves required
        
    def display_towers(self):
        """Display the current state of the towers."""
        # Find the maximum height of any tower
        max_height = self.num_discs
        
        # Display the towers
        for height in range(max_height - 1, -1, -1):
            line = ""
            for peg_idx in range(3):
                if height < len(self.pegs[peg_idx]):
                    disc_size = self.pegs[peg_idx][height]
                    spaces = self.num_discs - disc_size
                    disc = " " * spaces + "=" * (disc_size * 2 - 1) + " " * spaces
                else:
                    disc = " " * (self.num_discs * 2 - 1)
                line += f"│{disc}│ "
            print(line)
        
        # Display the base
        base_line = ""
        for _ in range(3):
            base_line += "└" + "─" * (self.num_discs * 2 - 1) + "┘ "
        print(base_line)
        
        # Display the peg numbers
        labels_line = ""
        for i in range(3):
            spaces = self.num_discs
            labels_line += " " * spaces + f"{i+1}" + " " * spaces + " "
        print(labels_line)
        
        # Display move count
        print(f"\nMoves: {self.moves} (Minimum required: {self.min_moves})")
        
    def is_valid_move(self, from_peg, to_peg):
        """Check if a move is valid."""
        # Check if pegs are valid
        if from_peg < 1 or from_peg > 3 or to_peg < 1 or to_peg > 3:
            return False
        
        # Convert to 0-based indexing
        from_idx = from_peg - 1
        to_idx = to_peg - 1
        
        # Check if from_peg has discs
        if not self.pegs[from_idx]:
            return False
        
        # Check if the move is valid (smaller disc onto larger disc or empty peg)
        if not self.pegs[to_idx] or self.pegs[from_idx][-1] < self.pegs[to_idx][-1]:
            return True
        
        return False
    
    def make_move(self, from_peg, to_peg):
        """Move a disc from one peg to another."""
        # Convert to 0-based indexing
        from_idx = from_peg - 1
        to_idx = to_peg - 1
        
        # Move the disc
        disc = self.pegs[from_idx].pop()
        self.pegs[to_idx].append(disc)
        self.moves += 1
    
    def check_win(self):
        """Check if the game is won."""
        # The game is won if all discs are on the third peg
        return len(self.pegs[2]) == self.num_discs
    
    def solve_recursive(self, n, source, auxiliary, target):
        """Solve the Tower of Hanoi recursively."""
        if n > 0:
            # Move n-1 discs from source to auxiliary peg
            self.solve_recursive(n-1, source, target, auxiliary)
            
            # Move the nth disc from source to target peg
            self.make_move(source, target)
            clear_screen()
            print_header()
            self.display_towers()
            print(f"\nMoving disc from peg {source} to peg {target}")
            time.sleep(0.5)  # Pause for visualization
            
            # Move n-1 discs from auxiliary to target peg
            self.solve_recursive(n-1, auxiliary, source, target)

def show_instructions():
    """Display the game instructions."""
    print(f"{Fore.CYAN}INSTRUCTIONS:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}The Tower of Hanoi is a classic puzzle game. The goal is to move all discs")
    print(f"from the first peg to the third peg, following these rules:{Style.RESET_ALL}")
    print()
    print(f"{Fore.WHITE}1. Only one disc can be moved at a time.")
    print(f"2. Each move consists of taking the upper disc from one stack")
    print(f"   and placing it on top of another stack.")
    print(f"3. No disc may be placed on top of a smaller disc.{Style.RESET_ALL}")
    print()
    print(f"{Fore.WHITE}To make a move, enter the source peg (1-3) and the target peg (1-3)")
    print(f"when prompted. For example: '1 3' moves a disc from peg 1 to peg 3.{Style.RESET_ALL}")
    print()
    print(f"{Fore.YELLOW}You can also type 'solve' to see the solution or 'quit' to exit.{Style.RESET_ALL}")
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
        
        # Ask for number of discs
        while True:
            try:
                discs_input = input(f"{Fore.CYAN}Enter number of discs (3-7, default is 3): {Style.RESET_ALL}")
                if discs_input.strip() == "":
                    num_discs = 3
                    break
                num_discs = int(discs_input)
                if 3 <= num_discs <= 7:
                    break
                print(f"{Fore.RED}Please enter a number between 3 and 7.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
        
        # Create a new game
        game = TowerOfHanoi(num_discs)
        
        # Game loop
        while not game.check_win():
            clear_screen()
            print_header()
            game.display_towers()
            
            # Get user input
            move_input = input(f"{Fore.CYAN}Enter move (from to) or 'solve'/'quit': {Style.RESET_ALL}")
            
            # Check for special commands
            if move_input.lower() == 'quit':
                print(f"{Fore.GREEN}Thanks for playing!{Style.RESET_ALL}")
                return
            
            if move_input.lower() == 'solve':
                clear_screen()
                print_header()
                print(f"{Fore.YELLOW}Solving automatically...{Style.RESET_ALL}")
                time.sleep(1)
                
                # Reset the game
                game = TowerOfHanoi(num_discs)
                game.display_towers()
                print("\nSolving...")
                time.sleep(1)
                
                # Solve automatically
                game.solve_recursive(num_discs, 1, 2, 3)
                break
            
            # Process normal move
            try:
                from_peg, to_peg = map(int, move_input.split())
                
                if game.is_valid_move(from_peg, to_peg):
                    game.make_move(from_peg, to_peg)
                else:
                    print(f"{Fore.RED}Invalid move! Please try again.{Style.RESET_ALL}")
                    time.sleep(1)
            except ValueError:
                print(f"{Fore.RED}Invalid input! Please enter two numbers.{Style.RESET_ALL}")
                time.sleep(1)
        
        # Game is won
        clear_screen()
        print_header()
        game.display_towers()
        
        if game.moves == game.min_moves:
            print(f"\n{Fore.GREEN}Congratulations! You solved the puzzle in the minimum number of moves ({game.moves})!{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.GREEN}Congratulations! You solved the puzzle in {game.moves} moves!{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}The minimum number of moves required is {game.min_moves}.{Style.RESET_ALL}")
        
        # Ask to play again
        play_again = input(f"\n{Fore.CYAN}Play again? (y/n): {Style.RESET_ALL}")
        if play_again.lower() != 'y':
            print(f"{Fore.GREEN}Thanks for playing!{Style.RESET_ALL}")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print_header()
        print(f"{Fore.GREEN}Thanks for playing Tower of Hanoi!{Style.RESET_ALL}")
        sys.exit(0) 