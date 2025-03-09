#!/usr/bin/env python3
import random
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
    print(f"{Back.MAGENTA}{Fore.WHITE}╔═══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Back.MAGENTA}{Fore.WHITE}║                       NUMBER GUESSER                          ║{Style.RESET_ALL}")
    print(f"{Back.MAGENTA}{Fore.WHITE}╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()

def main():
    """Main game function."""
    clear_screen()
    print_header()
    
    # Game rules
    print(f"{Fore.CYAN}Welcome to Number Guesser!{Style.RESET_ALL}")
    print(f"{Fore.WHITE}I'm thinking of a number between 1 and 100.{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Can you guess it in 10 tries or fewer?{Style.RESET_ALL}")
    print()
    
    # Generate a random number between 1 and 100
    secret_number = random.randint(1, 100)
    guesses_taken = 0
    max_guesses = 10
    
    while guesses_taken < max_guesses:
        # Get the player's guess
        try:
            print(f"{Fore.YELLOW}Guess #{guesses_taken + 1}/{max_guesses}:{Style.RESET_ALL} ", end="")
            guess = int(input())
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
            continue
        
        guesses_taken += 1
        
        # Check the guess
        if guess < secret_number:
            print(f"{Fore.BLUE}Too low! Try a higher number.{Style.RESET_ALL}")
        elif guess > secret_number:
            print(f"{Fore.RED}Too high! Try a lower number.{Style.RESET_ALL}")
        else:
            break  # Correct guess!
    
    # Game result
    if guess == secret_number:
        print()
        print(f"{Fore.GREEN}Congratulations! You guessed the number in {guesses_taken} tries!{Style.RESET_ALL}")
        if guesses_taken == 1:
            print(f"{Fore.GREEN}Incredible! A hole in one!{Style.RESET_ALL}")
        elif guesses_taken <= 3:
            print(f"{Fore.GREEN}Impressive! You're a natural!{Style.RESET_ALL}")
        elif guesses_taken <= 6:
            print(f"{Fore.GREEN}Well done! That was a good game!{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}You got it just in time!{Style.RESET_ALL}")
    else:
        print()
        print(f"{Fore.RED}Game over! You've used all your guesses.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}The number I was thinking of was {secret_number}.{Style.RESET_ALL}")
    
    # Ask to play again
    print()
    play_again = input(f"{Fore.CYAN}Would you like to play again? (y/n): {Style.RESET_ALL}").lower()
    
    if play_again.startswith('y'):
        main()  # Restart the game

if __name__ == "__main__":
    main() 