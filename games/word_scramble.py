#!/usr/bin/env python3
import os
import random
import time
import colorama
from colorama import Fore, Back, Style

# Initialize colorama
colorama.init()

# Word banks by difficulty
EASY_WORDS = [
    "cat", "dog", "sun", "run", "hat", "box", "car", "pen", "cup", "fox",
    "toy", "ball", "book", "key", "door", "fish", "bird", "tree", "game",
    "home", "desk", "lamp", "ship", "star", "moon"
]

MEDIUM_WORDS = [
    "apple", "seven", "eight", "banana", "orange", "green", "purple", 
    "monkey", "tiger", "table", "music", "window", "garden", "school",
    "pencil", "marker", "family", "player", "laptop", "camera", "robot",
    "coffee", "dinner", "planet", "monkey", "guitar", "rabbit", "bottle"
]

HARD_WORDS = [
    "computer", "elephant", "adventure", "telephone", "television", "mountain",
    "beautiful", "chocolate", "knowledge", "university", "professor", "vegetable",
    "community", "friendship", "experience", "celebrate", "technology", "butterfly",
    "happiness", "character", "government", "environment", "restaurant", "challenge",
    "important", "fantastic", "wonderful", "brilliant", "different", "dangerous"
]

VERY_HARD_WORDS = [
    "encyclopedia", "extraordinary", "communication", "congratulations", "responsibility",
    "understanding", "international", "opportunity", "revolutionary", "determination",
    "investigation", "classification", "identification", "representative", "professional",
    "accomplishment", "concentration", "independence", "interpretation", "organization",
    "sophisticated", "significantly", "collaboration", "enthusiastic", "relationships"
]

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the game header."""
    print(f"{Back.MAGENTA}{Fore.WHITE}╔═══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Back.MAGENTA}{Fore.WHITE}║                     WORD SCRAMBLE                             ║{Style.RESET_ALL}")
    print(f"{Back.MAGENTA}{Fore.WHITE}╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()

def scramble_word(word):
    """Scramble the letters of a word."""
    word_list = list(word)
    
    # Keep shuffling until the word is actually scrambled
    scrambled = ''.join(word_list)
    while scrambled == word:
        random.shuffle(word_list)
        scrambled = ''.join(word_list)
    
    return scrambled

def get_word_list(level):
    """Get the word list for the selected difficulty level."""
    if level == 1:
        return EASY_WORDS
    elif level == 2:
        return MEDIUM_WORDS
    elif level == 3:
        return HARD_WORDS
    else:
        return VERY_HARD_WORDS

def get_hint(word, hint_level):
    """Generate a hint based on the hint level."""
    if hint_level == 1:
        # First letter hint
        return f"The word starts with '{word[0]}'"
    elif hint_level == 2:
        # First and last letter hint
        return f"The word starts with '{word[0]}' and ends with '{word[-1]}'"
    else:
        # Show random letters (about half)
        hint = ['_'] * len(word)
        positions = random.sample(range(len(word)), len(word) // 2)
        
        for pos in positions:
            hint[pos] = word[pos]
        
        return f"Partially revealed word: {' '.join(hint)}"

def main():
    """Main game function."""
    clear_screen()
    print_header()
    
    # Game rules
    print(f"{Fore.CYAN}Welcome to Word Scramble!{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Unscramble the given letters to form a valid word.{Style.RESET_ALL}")
    print(f"{Fore.WHITE}You can use hints if you get stuck, but they will reduce your score.{Style.RESET_ALL}")
    print()
    
    # Choose difficulty level
    print(f"{Fore.YELLOW}Choose a difficulty level:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}1. Easy (3-4 letter words){Style.RESET_ALL}")
    print(f"{Fore.YELLOW}2. Medium (5-6 letter words){Style.RESET_ALL}")
    print(f"{Fore.RED}3. Hard (7-10 letter words){Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}4. Very Hard (11+ letter words){Style.RESET_ALL}")
    print()
    
    # Get difficulty level
    while True:
        try:
            level = int(input(f"{Fore.CYAN}Select level (1-4): {Style.RESET_ALL}"))
            if 1 <= level <= 4:
                break
            else:
                print(f"{Fore.RED}Please enter a number between 1 and 4.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
    
    # Number of words
    while True:
        try:
            num_words = int(input(f"{Fore.CYAN}How many words would you like to unscramble (5-15)? {Style.RESET_ALL}"))
            if 5 <= num_words <= 15:
                break
            else:
                print(f"{Fore.RED}Please enter a number between 5 and 15.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
    
    print()
    print(f"{Fore.GREEN}Get ready!{Style.RESET_ALL}")
    time.sleep(1)
    
    # Game variables
    word_list = get_word_list(level)
    score = 0
    words_to_play = random.sample(word_list, min(num_words, len(word_list)))
    
    # Main game loop
    for i, word in enumerate(words_to_play, 1):
        clear_screen()
        print_header()
        
        print(f"{Fore.YELLOW}Word {i} of {len(words_to_play)}{Style.RESET_ALL}")
        print()
        
        # Scramble the word
        scrambled = scramble_word(word)
        
        # Calculate base points based on word length and difficulty
        base_points = len(word) * level * 10
        hint_level = 0
        attempts = 0
        
        # Word challenge loop
        solved = False
        while not solved and attempts < 3:
            print(f"{Fore.WHITE}Unscramble this word: {Fore.CYAN}{scrambled.upper()}{Style.RESET_ALL}")
            print()
            
            if hint_level > 0:
                hint = get_hint(word, hint_level)
                print(f"{Fore.YELLOW}Hint: {hint}{Style.RESET_ALL}")
                print()
            
            # Get the player's answer
            guess = input(f"{Fore.GREEN}Your answer: {Style.RESET_ALL}").lower().strip()
            
            # Check if player wants a hint
            if guess == "hint":
                if hint_level < 3:
                    hint_level += 1
                    base_points = max(base_points // 2, 5)  # Reduce points by half for each hint
                    print(f"{Fore.YELLOW}Here's a hint...{Style.RESET_ALL}")
                    time.sleep(1)
                    continue
                else:
                    print(f"{Fore.RED}You've used all available hints.{Style.RESET_ALL}")
                    time.sleep(1)
                    continue
            
            attempts += 1
            
            # Check the answer
            if guess == word:
                solved = True
                # Points calculation: base points - penalty for attempts
                points = max(base_points - ((attempts - 1) * (base_points // 4)), 5)
                score += points
                
                print()
                print(f"{Fore.GREEN}Correct! +{points} points{Style.RESET_ALL}")
            else:
                print()
                print(f"{Fore.RED}Sorry, that's not correct.{Style.RESET_ALL}")
                
                if attempts < 3:
                    print(f"{Fore.YELLOW}Attempts remaining: {3 - attempts}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}Type 'hint' for a hint (will reduce points).{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}The correct word was: {word.upper()}{Style.RESET_ALL}")
            
            time.sleep(2)
        
        # If the player didn't solve it in 3 attempts
        if not solved:
            print()
            print(f"{Fore.RED}Moving on to the next word...{Style.RESET_ALL}")
            time.sleep(2)
    
    # Game over - Show final results
    clear_screen()
    print_header()
    
    print(f"{Fore.CYAN}Game Over!{Style.RESET_ALL}")
    print()
    print(f"{Fore.YELLOW}Final Score: {score} points{Style.RESET_ALL}")
    
    # Performance evaluation
    print()
    max_possible = sum(len(w) * level * 10 for w in words_to_play)
    percentage = (score / max_possible) * 100 if max_possible > 0 else 0
    
    if percentage >= 90:
        print(f"{Fore.MAGENTA}Outstanding! You're a word wizard!{Style.RESET_ALL}")
    elif percentage >= 70:
        print(f"{Fore.GREEN}Great job! You have exceptional vocabulary skills!{Style.RESET_ALL}")
    elif percentage >= 50:
        print(f"{Fore.YELLOW}Good effort! Your word skills are solid.{Style.RESET_ALL}")
    elif percentage >= 30:
        print(f"{Fore.YELLOW}Not bad, keep practicing to improve your vocabulary.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Better luck next time! Try an easier level or use hints.{Style.RESET_ALL}")
    
    # Ask to play again
    print()
    play_again = input(f"{Fore.CYAN}Would you like to play again? (y/n): {Style.RESET_ALL}").lower()
    
    if play_again.startswith('y'):
        main()  # Restart the game

if __name__ == "__main__":
    main() 