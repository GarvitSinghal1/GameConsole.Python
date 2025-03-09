#!/usr/bin/env python3
import os
import sys
import time
import random
import colorama
from colorama import Fore, Back, Style

# Initialize colorama
colorama.init(autoreset=True)

# Color codes for the game
COLORS = {
    'R': (Fore.RED, "Red"),
    'G': (Fore.GREEN, "Green"),
    'B': (Fore.BLUE, "Blue"),
    'Y': (Fore.YELLOW, "Yellow"),
    'M': (Fore.MAGENTA, "Magenta"),
    'C': (Fore.CYAN, "Cyan"),
    'W': (Fore.WHITE, "White")
}

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the game header."""
    print(f"{Back.MAGENTA}{Fore.WHITE}╔═══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Back.MAGENTA}{Fore.WHITE}║                     MASTERMIND                               ║{Style.RESET_ALL}")
    print(f"{Back.MAGENTA}{Fore.WHITE}╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()

def print_color_guide():
    """Print a guide to the available colors."""
    print(f"{Fore.CYAN}Available colors:{Style.RESET_ALL}")
    for code, (color, name) in COLORS.items():
        print(f"{color}■{Style.RESET_ALL} - {code} ({name})")
    print()

class Mastermind:
    def __init__(self, code_length=4, max_attempts=10, allow_duplicates=True):
        """Initialize the Mastermind game."""
        self.code_length = code_length
        self.max_attempts = max_attempts
        self.allow_duplicates = allow_duplicates
        self.available_colors = list(COLORS.keys())
        
        # Generate the secret code
        self.secret_code = self.generate_code()
        
        # Game state
        self.attempts = []
        self.feedbacks = []
        self.current_attempt = 0
        self.game_over = False
        self.win = False
    
    def generate_code(self):
        """Generate a random secret code."""
        if self.allow_duplicates:
            return [random.choice(self.available_colors) for _ in range(self.code_length)]
        else:
            # Ensure no duplicates
            return random.sample(self.available_colors, self.code_length)
    
    def evaluate_guess(self, guess):
        """Evaluate a guess against the secret code."""
        if len(guess) != self.code_length:
            return None
        
        # Count exact matches (correct color in correct position)
        exact_matches = sum(1 for i in range(self.code_length) if guess[i] == self.secret_code[i])
        
        # Count color matches (correct color but wrong position)
        # We need to count each color only once
        guess_colors = {}
        secret_colors = {}
        
        for i in range(self.code_length):
            if guess[i] != self.secret_code[i]:  # Skip exact matches
                guess_colors[guess[i]] = guess_colors.get(guess[i], 0) + 1
                secret_colors[self.secret_code[i]] = secret_colors.get(self.secret_code[i], 0) + 1
        
        color_matches = sum(min(guess_colors.get(color, 0), secret_colors.get(color, 0)) for color in set(guess_colors) | set(secret_colors))
        
        return (exact_matches, color_matches)
    
    def make_guess(self, guess):
        """Make a guess and update game state."""
        if self.game_over:
            return False, "Game is already over."
        
        if self.current_attempt >= self.max_attempts:
            self.game_over = True
            return False, "Maximum number of attempts reached."
        
        # Validate guess
        if len(guess) != self.code_length:
            return False, f"Guess must be {self.code_length} colors long."
        
        for color in guess:
            if color not in self.available_colors:
                return False, f"Invalid color: {color}. Use one of {', '.join(self.available_colors)}."
        
        # Evaluate guess
        feedback = self.evaluate_guess(guess)
        
        # Update game state
        self.attempts.append(guess)
        self.feedbacks.append(feedback)
        self.current_attempt += 1
        
        # Check if the player has won
        if feedback[0] == self.code_length:
            self.win = True
            self.game_over = True
        
        # Check if the player has lost
        if self.current_attempt >= self.max_attempts and not self.win:
            self.game_over = True
        
        return True, ""
    
    def display_board(self, show_secret=False):
        """Display the current game board."""
        # Print attempts header
        print(f"{Fore.CYAN}Attempt | Guess{' ' * (self.code_length * 2)} | Feedback{Style.RESET_ALL}")
        print(f"{Fore.CYAN}--------+{'-' * (self.code_length * 2 + 2)}+----------{Style.RESET_ALL}")
        
        # Print each attempt and feedback
        for i in range(self.max_attempts):
            if i < self.current_attempt:
                # Print attempt number
                print(f"{Fore.CYAN}{i+1:7d} | {Style.RESET_ALL}", end="")
                
                # Print guess
                for color in self.attempts[i]:
                    color_code, _ = COLORS[color]
                    print(f"{color_code}■{Style.RESET_ALL} ", end="")
                
                # Print feedback
                exact, color = self.feedbacks[i]
                print(f"| {Fore.WHITE}{exact} exact{Style.RESET_ALL}, {Fore.YELLOW}{color} color{Style.RESET_ALL}")
            else:
                # Print empty row
                print(f"{Fore.CYAN}{i+1:7d} | {Style.RESET_ALL}" + "_ " * self.code_length + f"| {Fore.WHITE}0 exact{Style.RESET_ALL}, {Fore.YELLOW}0 color{Style.RESET_ALL}")
        
        print()
        
        # Print secret code if game is over or show_secret is True
        if self.game_over or show_secret:
            print(f"{Fore.CYAN}Secret: {Style.RESET_ALL}", end="")
            for color in self.secret_code:
                color_code, _ = COLORS[color]
                print(f"{color_code}■{Style.RESET_ALL} ", end="")
            print()
        
        print()

def show_instructions():
    """Display game instructions."""
    print(f"{Fore.CYAN}INSTRUCTIONS:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Mastermind is a code-breaking game. The computer will generate")
    print(f"a secret code of colored pegs, and you need to guess it.{Style.RESET_ALL}")
    print()
    print(f"{Fore.WHITE}After each guess, you'll receive feedback:")
    print(f" - The number of pegs that are the correct color and in the correct position")
    print(f" - The number of pegs that are the correct color but in the wrong position{Style.RESET_ALL}")
    print()
    print(f"{Fore.WHITE}Use this feedback to deduce the secret code within the allowed")
    print(f"number of attempts.{Style.RESET_ALL}")
    print()
    print_color_guide()
    print(f"{Fore.WHITE}To make a guess, enter the color codes without spaces.")
    print(f"For example, to guess Red, Green, Blue, Yellow, enter: RGBY{Style.RESET_ALL}")
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
        print(f"1. Easy (4 colors, 12 attempts, duplicates allowed)")
        print(f"2. Medium (5 colors, 10 attempts, duplicates allowed)")
        print(f"3. Hard (6 colors, 8 attempts, duplicates allowed)")
        print(f"4. Expert (6 colors, 8 attempts, no duplicates)")
        print()
        
        while True:
            try:
                choice = int(input(f"{Fore.YELLOW}Enter your choice (1-4): {Style.RESET_ALL}"))
                if 1 <= choice <= 4:
                    break
                else:
                    print(f"{Fore.RED}Please enter a number between 1 and 4.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
        
        # Set game parameters based on difficulty
        if choice == 1:  # Easy
            code_length, max_attempts, allow_duplicates = 4, 12, True
        elif choice == 2:  # Medium
            code_length, max_attempts, allow_duplicates = 5, 10, True
        elif choice == 3:  # Hard
            code_length, max_attempts, allow_duplicates = 6, 8, True
        else:  # Expert
            code_length, max_attempts, allow_duplicates = 6, 8, False
        
        # Create and play the game
        game = Mastermind(code_length, max_attempts, allow_duplicates)
        
        while not game.game_over:
            clear_screen()
            print_header()
            print(f"{Fore.CYAN}Difficulty: {['Easy', 'Medium', 'Hard', 'Expert'][choice-1]}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Attempts remaining: {max_attempts - game.current_attempt}{Style.RESET_ALL}")
            print()
            
            game.display_board()
            print_color_guide()
            
            # Get player's guess
            guess = input(f"{Fore.YELLOW}Enter your guess (or 'q' to quit): {Style.RESET_ALL}").upper()
            
            if guess.lower() == 'q':
                print(f"{Fore.YELLOW}Game aborted.{Style.RESET_ALL}")
                time.sleep(1)
                break
            
            # Make the guess
            success, message = game.make_guess(guess)
            if not success:
                print(f"{Fore.RED}{message}{Style.RESET_ALL}")
                time.sleep(1.5)
        
        # Game over
        if game.game_over:
            clear_screen()
            print_header()
            print(f"{Fore.CYAN}Difficulty: {['Easy', 'Medium', 'Hard', 'Expert'][choice-1]}{Style.RESET_ALL}")
            print()
            
            game.display_board(show_secret=True)
            
            if game.win:
                print(f"{Fore.GREEN}Congratulations! You cracked the code in {game.current_attempt} attempts!{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Game over! You failed to crack the code.{Style.RESET_ALL}")
        
        # Ask to play again
        print()
        play_again = input(f"{Fore.CYAN}Play again? (y/n): {Style.RESET_ALL}").lower()
        if play_again != 'y':
            clear_screen()
            print_header()
            print(f"{Fore.GREEN}Thanks for playing Mastermind!{Style.RESET_ALL}")
            time.sleep(1.5)
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print_header()
        print(f"{Fore.GREEN}Thanks for playing Mastermind!{Style.RESET_ALL}")
        sys.exit(0) 