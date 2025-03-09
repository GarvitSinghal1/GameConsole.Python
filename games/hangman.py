#!/usr/bin/env python3
import random
import os
import string
import colorama
from colorama import Fore, Back, Style

# Initialize colorama
colorama.init()

# List of words to guess
WORDS = [
    "python", "java", "javascript", "programming", 
    "computer", "algorithm", "database", "network",
    "game", "console", "keyboard", "mouse", "monitor",
    "software", "hardware", "internet", "developer",
    "application", "function", "variable", "class",
    "method", "object", "array", "string", "integer"
]

# Hangman stages
HANGMAN_STAGES = [
    f"""
    {Fore.RED}+---+
    |   |
        |
        |
        |
        |
    =========={Style.RESET_ALL}""",
    f"""
    {Fore.RED}+---+
    |   |
    O   |
        |
        |
        |
    =========={Style.RESET_ALL}""",
    f"""
    {Fore.RED}+---+
    |   |
    O   |
    |   |
        |
        |
    =========={Style.RESET_ALL}""",
    f"""
    {Fore.RED}+---+
    |   |
    O   |
   /|   |
        |
        |
    =========={Style.RESET_ALL}""",
    f"""
    {Fore.RED}+---+
    |   |
    O   |
   /|\\  |
        |
        |
    =========={Style.RESET_ALL}""",
    f"""
    {Fore.RED}+---+
    |   |
    O   |
   /|\\  |
   /    |
        |
    =========={Style.RESET_ALL}""",
    f"""
    {Fore.RED}+---+
    |   |
    O   |
   /|\\  |
   / \\  |
        |
    =========={Style.RESET_ALL}"""
]

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the game header."""
    print(f"{Back.CYAN}{Fore.BLACK}╔═══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Back.CYAN}{Fore.BLACK}║                         HANGMAN                               ║{Style.RESET_ALL}")
    print(f"{Back.CYAN}{Fore.BLACK}╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()

def main():
    """Main game function."""
    clear_screen()
    print_header()
    
    # Game rules
    print(f"{Fore.CYAN}Welcome to Hangman!{Style.RESET_ALL}")
    print(f"{Fore.WHITE}I'm thinking of a word. Try to guess it one letter at a time.{Style.RESET_ALL}")
    print(f"{Fore.WHITE}But be careful - you can only make 6 wrong guesses before the hangman is complete!{Style.RESET_ALL}")
    print()
    
    # Select a random word
    word = random.choice(WORDS).upper()
    word_completion = "_" * len(word)  # Initially all letters are hidden
    guessed = False
    guessed_letters = []
    guessed_words = []
    tries = 6  # Number of wrong guesses allowed
    
    print(f"{Fore.YELLOW}The word has {len(word)} letters.{Style.RESET_ALL}")
    print(HANGMAN_STAGES[0])
    print(f"{Fore.CYAN}{word_completion}{Style.RESET_ALL}")
    print()
    
    while not guessed and tries > 0:
        guess = input(f"{Fore.GREEN}Please guess a letter or word: {Style.RESET_ALL}").upper()
        
        # If the input is a single letter
        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                print(f"{Fore.YELLOW}You already guessed the letter {guess}{Style.RESET_ALL}")
            elif guess not in word:
                print(f"{Fore.RED}Sorry, {guess} is not in the word.{Style.RESET_ALL}")
                tries -= 1
                guessed_letters.append(guess)
            else:
                print(f"{Fore.GREEN}Good job, {guess} is in the word!{Style.RESET_ALL}")
                guessed_letters.append(guess)
                
                # Update word_completion with correctly guessed letters
                word_as_list = list(word_completion)
                for i in range(len(word)):
                    if word[i] == guess:
                        word_as_list[i] = guess
                word_completion = "".join(word_as_list)
                
                # Check if the word has been fully guessed
                if "_" not in word_completion:
                    guessed = True
        
        # If the input is a full word
        elif len(guess) == len(word) and guess.isalpha():
            if guess in guessed_words:
                print(f"{Fore.YELLOW}You already guessed the word {guess}{Style.RESET_ALL}")
            elif guess != word:
                print(f"{Fore.RED}Sorry, {guess} is not the word.{Style.RESET_ALL}")
                tries -= 1
                guessed_words.append(guess)
            else:
                guessed = True
                word_completion = word
        
        else:
            print(f"{Fore.RED}Not a valid guess.{Style.RESET_ALL}")
        
        # Display the current state of the game
        print(HANGMAN_STAGES[6 - tries])
        print(f"{Fore.CYAN}{word_completion}{Style.RESET_ALL}")
        print()
        
        # Display guessed letters
        print(f"{Fore.YELLOW}Guessed letters: {' '.join(guessed_letters)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Guesses remaining: {tries}{Style.RESET_ALL}")
        print()
    
    # Game result
    if guessed:
        print(f"{Fore.GREEN}Congratulations! You guessed the word: {word}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Sorry, you ran out of tries. The word was: {word}{Style.RESET_ALL}")
    
    # Ask to play again
    print()
    play_again = input(f"{Fore.CYAN}Would you like to play again? (y/n): {Style.RESET_ALL}").lower()
    
    if play_again.startswith('y'):
        main()  # Restart the game

if __name__ == "__main__":
    main() 