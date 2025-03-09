#!/usr/bin/env python3
import os
import sys
import time
import random
import colorama
from colorama import Fore, Back, Style

# Initialize colorama
colorama.init(autoreset=True)

# Word lists of varying difficulty
EASY_WORDS = [
    "the", "and", "for", "are", "but", "not", "you", "all", "any", "can", "had", "her", "was", 
    "one", "our", "out", "day", "get", "has", "him", "his", "how", "man", "new", "now", "old", 
    "see", "two", "way", "who", "boy", "did", "its", "let", "put", "say", "she", "too", "use"
]

MEDIUM_WORDS = [
    "about", "after", "again", "along", "began", "below", "between", "thing", "think", "three", 
    "together", "under", "important", "plant", "cover", "mountain", "never", "notice", "world", 
    "paper", "group", "music", "river", "often", "second", "family", "listen", "travel", "friend", 
    "answer", "earth", "common", "enough", "people", "always", "animal", "follow", "mother", 
    "system", "number", "water", "person", "round", "father", "simple", "build", "before", "change"
]

HARD_WORDS = [
    "necessary", "according", "especially", "technology", "relationship", "experience", "government", 
    "understanding", "development", "information", "environment", "significant", "individual", 
    "successful", "international", "opportunity", "responsibility", "organization", "combination", 
    "determination", "conversation", "association", "professional", "distribution", "continuously", 
    "independent", "intelligence", "immediately", "championship", "comfortable", "revolutionary", 
    "extraordinary", "sophisticated", "comprehensive", "investigation", "disappointment", "entertainment"
]

# Sample paragraphs for advanced tests
PARAGRAPHS = [
    "The quick brown fox jumps over the lazy dog. This sentence contains every letter in the English alphabet. It has been used for typing practice for many years. Typing quickly and accurately is a valuable skill in today's digital world.",
    
    "Learning to type without looking at the keyboard is called touch typing. It increases your typing speed significantly. The home row keys are where you place your fingers when touch typing. For the QWERTY keyboard, these are ASDF for the left hand and JKL; for the right hand.",
    
    "Programming requires good typing skills. Writing code involves not just letters and numbers but also special characters. The faster you can type, the more productive you can be as a programmer. Practice makes perfect when it comes to typing.",
    
    "Artificial intelligence is transforming how we interact with technology. Voice recognition and natural language processing are making typing less necessary in some contexts. However, typing remains an essential skill for detailed work and programming tasks."
]

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the game header."""
    print(f"{Back.CYAN}{Fore.BLACK}╔═══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Back.CYAN}{Fore.BLACK}║                   TYPING SPEED TEST                           ║{Style.RESET_ALL}")
    print(f"{Back.CYAN}{Fore.BLACK}╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()

def generate_word_test(difficulty, num_words=20):
    """Generate a list of random words based on difficulty."""
    if difficulty == "easy":
        return random.sample(EASY_WORDS * 3, num_words)
    elif difficulty == "medium":
        return random.sample(MEDIUM_WORDS * 2, num_words)
    else:  # hard
        return random.sample(HARD_WORDS + MEDIUM_WORDS, num_words)

def generate_paragraph_test():
    """Return a random paragraph for testing."""
    return random.choice(PARAGRAPHS)

def calculate_wpm(typed_chars, elapsed_time_sec):
    """Calculate words per minute (WPM) based on the standard 5 chars per word."""
    # Standard: 5 characters = 1 word
    words = typed_chars / 5
    minutes = elapsed_time_sec / 60
    return round(words / minutes) if minutes > 0 else 0

def calculate_accuracy(original_text, typed_text):
    """Calculate accuracy percentage based on character-by-character comparison."""
    # Trim typed_text to the length of original_text to avoid penalizing for missing chars
    typed_text = typed_text[:len(original_text)]
    
    # Count correct characters
    correct_chars = sum(1 for a, b in zip(original_text, typed_text) if a == b)
    
    # Calculate accuracy
    accuracy = (correct_chars / len(original_text)) * 100 if original_text else 0
    return round(accuracy, 1)

def show_instructions():
    """Display typing test instructions."""
    print(f"{Fore.CYAN}INSTRUCTIONS:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}This is a typing speed test. You'll be shown a series of")
    print(f"words or a paragraph to type. Type the text as accurately and")
    print(f"quickly as possible. Your typing speed (WPM) and accuracy")
    print(f"will be calculated at the end.{Style.RESET_ALL}")
    print()
    print(f"{Fore.WHITE}There are three difficulty levels:")
    print(f"  Easy   - Short, common words")
    print(f"  Medium - Longer, everyday words")
    print(f"  Hard   - Long, complex words{Style.RESET_ALL}")
    print()
    print(f"{Fore.WHITE}You can also choose to type a paragraph instead of individual words.{Style.RESET_ALL}")
    print()
    input(f"{Fore.GREEN}Press Enter to continue...{Style.RESET_ALL}")

def run_word_test(difficulty, num_words=20):
    """Run a typing test with random words."""
    # Generate test words
    words = generate_word_test(difficulty, num_words)
    test_text = " ".join(words)
    
    clear_screen()
    print_header()
    
    # Display the test text
    print(f"{Fore.YELLOW}Type the following words:{Style.RESET_ALL}")
    print()
    print(f"{Fore.WHITE}{test_text}{Style.RESET_ALL}")
    print()
    print(f"{Fore.CYAN}Press Enter and then start typing immediately...{Style.RESET_ALL}")
    input()
    
    # Start the timer
    start_time = time.time()
    
    # Get user input
    print(f"{Fore.GREEN}Start typing:{Style.RESET_ALL}")
    typed_text = input()
    
    # Stop the timer
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    # Calculate results
    wpm = calculate_wpm(len(typed_text), elapsed_time)
    accuracy = calculate_accuracy(test_text, typed_text)
    
    # Display results
    clear_screen()
    print_header()
    print(f"{Fore.YELLOW}Results:{Style.RESET_ALL}")
    print()
    print(f"{Fore.CYAN}Original: {Style.RESET_ALL}{test_text}")
    print(f"{Fore.CYAN}You typed: {Style.RESET_ALL}{typed_text}")
    print()
    print(f"{Fore.GREEN}Time: {Style.RESET_ALL}{elapsed_time:.2f} seconds")
    print(f"{Fore.GREEN}Speed: {Style.RESET_ALL}{wpm} WPM (Words Per Minute)")
    print(f"{Fore.GREEN}Accuracy: {Style.RESET_ALL}{accuracy}%")
    
    # Provide feedback
    if wpm < 20:
        print(f"\n{Fore.YELLOW}Keep practicing! You're building a good foundation.{Style.RESET_ALL}")
    elif wpm < 40:
        print(f"\n{Fore.YELLOW}Good job! You're approaching average typing speed.{Style.RESET_ALL}")
    elif wpm < 60:
        print(f"\n{Fore.GREEN}Nice work! You have a solid typing speed.{Style.RESET_ALL}")
    elif wpm < 80:
        print(f"\n{Fore.GREEN}Excellent! You're well above average typing speed.{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.MAGENTA}Amazing! You're at professional typing level!{Style.RESET_ALL}")
    
    print()
    input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

def run_paragraph_test():
    """Run a typing test with a paragraph."""
    # Generate test paragraph
    test_text = generate_paragraph_test()
    
    clear_screen()
    print_header()
    
    # Display the test text
    print(f"{Fore.YELLOW}Type the following paragraph:{Style.RESET_ALL}")
    print()
    print(f"{Fore.WHITE}{test_text}{Style.RESET_ALL}")
    print()
    print(f"{Fore.CYAN}Press Enter and then start typing immediately...{Style.RESET_ALL}")
    input()
    
    # Start the timer
    start_time = time.time()
    
    # Get user input
    print(f"{Fore.GREEN}Start typing:{Style.RESET_ALL}")
    typed_text = input()
    
    # Stop the timer
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    # Calculate results
    wpm = calculate_wpm(len(typed_text), elapsed_time)
    accuracy = calculate_accuracy(test_text, typed_text)
    
    # Display results
    clear_screen()
    print_header()
    print(f"{Fore.YELLOW}Results:{Style.RESET_ALL}")
    print()
    print(f"{Fore.CYAN}Original paragraph: {Style.RESET_ALL}")
    print(test_text)
    print()
    print(f"{Fore.CYAN}You typed: {Style.RESET_ALL}")
    print(typed_text)
    print()
    print(f"{Fore.GREEN}Time: {Style.RESET_ALL}{elapsed_time:.2f} seconds")
    print(f"{Fore.GREEN}Speed: {Style.RESET_ALL}{wpm} WPM (Words Per Minute)")
    print(f"{Fore.GREEN}Accuracy: {Style.RESET_ALL}{accuracy}%")
    
    # Provide feedback
    if wpm < 20:
        print(f"\n{Fore.YELLOW}Keep practicing! You're building a good foundation.{Style.RESET_ALL}")
    elif wpm < 40:
        print(f"\n{Fore.YELLOW}Good job! You're approaching average typing speed.{Style.RESET_ALL}")
    elif wpm < 60:
        print(f"\n{Fore.GREEN}Nice work! You have a solid typing speed.{Style.RESET_ALL}")
    elif wpm < 80:
        print(f"\n{Fore.GREEN}Excellent! You're well above average typing speed.{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.MAGENTA}Amazing! You're at professional typing level!{Style.RESET_ALL}")
    
    print()
    input(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

def main():
    """Main game function."""
    while True:
        clear_screen()
        print_header()
        show_instructions()
        
        # Choose test type
        clear_screen()
        print_header()
        print(f"{Fore.CYAN}Choose test type:{Style.RESET_ALL}")
        print(f"1. Word Test")
        print(f"2. Paragraph Test")
        print(f"3. Quit")
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
        
        if choice == 3:  # Quit
            clear_screen()
            print_header()
            print(f"{Fore.GREEN}Thanks for testing your typing speed!{Style.RESET_ALL}")
            time.sleep(1.5)
            break
        
        if choice == 1:  # Word Test
            # Choose difficulty
            clear_screen()
            print_header()
            print(f"{Fore.CYAN}Choose difficulty:{Style.RESET_ALL}")
            print(f"1. Easy")
            print(f"2. Medium")
            print(f"3. Hard")
            print()
            
            while True:
                try:
                    diff_choice = int(input(f"{Fore.YELLOW}Enter your choice (1-3): {Style.RESET_ALL}"))
                    if 1 <= diff_choice <= 3:
                        break
                    else:
                        print(f"{Fore.RED}Please enter a number between 1 and 3.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
            
            difficulty = {1: "easy", 2: "medium", 3: "hard"}[diff_choice]
            run_word_test(difficulty)
            
        elif choice == 2:  # Paragraph Test
            run_paragraph_test()
        
        # Ask to play again
        clear_screen()
        print_header()
        play_again = input(f"{Fore.CYAN}Would you like to try another test? (y/n): {Style.RESET_ALL}").lower()
        if play_again != 'y':
            clear_screen()
            print_header()
            print(f"{Fore.GREEN}Thanks for testing your typing speed!{Style.RESET_ALL}")
            time.sleep(1.5)
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print_header()
        print(f"{Fore.GREEN}Thanks for testing your typing speed!{Style.RESET_ALL}")
        sys.exit(0) 