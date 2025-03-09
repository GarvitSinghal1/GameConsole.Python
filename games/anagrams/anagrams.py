#!/usr/bin/env python3
import os
import sys
import time
import random
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
    print(f"{Back.MAGENTA}{Fore.WHITE}║                      ANAGRAMS                                ║{Style.RESET_ALL}")
    print(f"{Back.MAGENTA}{Fore.WHITE}╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()

# Constants
EASY_WORDS = [
    "cat", "dog", "bat", "hat", "rat", "mat", "sat", "pat", "pan", "man",
    "fan", "can", "ran", "tan", "ban", "van", "jam", "ham", "ram", "dam",
    "map", "cap", "lap", "tap", "gap", "nap", "sap", "tag", "bag", "rag",
    "wag", "lag", "sag", "nag", "mad", "bad", "dad", "had", "lad", "pad",
    "sad", "box", "fox", "pen", "hen", "ten", "den", "men", "pin", "win"
]

MEDIUM_WORDS = [
    "apple", "baker", "cable", "dance", "eagle", "fable", "grape", "happy",
    "jolly", "kangaroo", "lemon", "mango", "night", "orange", "party", "quiet",
    "radio", "snake", "tiger", "uncle", "virus", "world", "xerox", "young",
    "zebra", "actor", "blend", "cream", "dream", "earth", "flame", "globe",
    "house", "igloo", "jumbo", "knife", "light", "music", "north", "ocean",
    "plane", "queen", "river", "space", "train", "utter", "vivid", "wrong",
    "yacht", "zesty"
]

HARD_WORDS = [
    "awesome", "balance", "captive", "diamond", "emperor", "fantasy", "genuine",
    "harmony", "imagine", "jumping", "kingdom", "liberty", "mystery", "network",
    "obvious", "phantom", "quality", "reflect", "society", "triumph", "upgrade",
    "veteran", "warranty", "xenolith", "youthful", "zeppelin", "abstract", "building",
    "campaign", "daughter", "electric", "fabulous", "grateful", "heritage", "invasion",
    "judgment", "keyboard", "language", "magazine", "navigate", "original", "powerful",
    "question", "romantic", "standard", "township", "universe", "validate", "wanderer",
    "xylophone", "yearning", "zoologist"
]

# Load our dictionary of valid English words
try:
    with open('/usr/share/dict/words', 'r') as f:
        ENGLISH_WORDS = set(word.strip().lower() for word in f)
except FileNotFoundError:
    # Fallback dictionary if system dictionary isn't available
    ENGLISH_WORDS = set(EASY_WORDS + MEDIUM_WORDS + HARD_WORDS)

class Anagrams:
    def __init__(self, difficulty="medium", time_limit=180):
        """Initialize the Anagrams game."""
        self.difficulty = difficulty
        self.time_limit = time_limit  # in seconds
        self.letters = []
        self.found_words = []
        self.all_possible_words = []
        self.score = 0
        self.start_time = None
        self.game_over = False
        
        # Set word list based on difficulty
        if difficulty == "easy":
            self.word_list = EASY_WORDS
            self.min_word_length = 3
        elif difficulty == "medium":
            self.word_list = MEDIUM_WORDS
            self.min_word_length = 4
        else:  # hard
            self.word_list = HARD_WORDS
            self.min_word_length = 5
        
        # Select a random word and scramble it
        self.base_word = random.choice(self.word_list)
        self.letters = list(self.base_word)
        random.shuffle(self.letters)
        
        # Find all possible words
        self.find_all_possible_words()
    
    def find_all_possible_words(self):
        """Find all possible valid English words that can be formed from the letters."""
        # Function to check if a word can be formed from our letters
        def can_form_word(word):
            letter_count = {}
            for char in self.base_word:
                letter_count[char] = letter_count.get(char, 0) + 1
            
            for char in word:
                if char not in letter_count or letter_count[char] == 0:
                    return False
                letter_count[char] -= 1
            return True
        
        # Check all English words
        for word in ENGLISH_WORDS:
            if len(word) >= self.min_word_length and can_form_word(word):
                self.all_possible_words.append(word)
    
    def start_game(self):
        """Start the game timer."""
        self.start_time = time.time()
    
    def time_remaining(self):
        """Get the time remaining in the game."""
        if self.start_time is None:
            return self.time_limit
        
        elapsed = time.time() - self.start_time
        remaining = self.time_limit - elapsed
        
        if remaining <= 0:
            self.game_over = True
            return 0
        
        return remaining
    
    def submit_word(self, word):
        """Submit a word and check if it's valid."""
        word = word.strip().lower()
        
        # Check if the word is already found
        if word in self.found_words:
            return False, f"You've already found '{word}'!"
        
        # Check if the word is valid
        if self.is_valid_word(word):
            self.found_words.append(word)
            
            # Score is based on word length
            points = len(word) ** 2
            self.score += points
            
            # Check if all possible words have been found
            if len(self.found_words) == len(self.all_possible_words):
                self.game_over = True
                return True, f"Amazing! You found all {len(self.all_possible_words)} possible words!"
            
            return True, f"Great! '{word}' is worth {points} points."
        
        return False, f"'{word}' is not a valid word."
    
    def is_valid_word(self, word):
        """Check if a word is valid."""
        # Word must be at least minimum length
        if len(word) < self.min_word_length:
            return False
        
        # Word must be in English dictionary
        if word not in ENGLISH_WORDS:
            return False
        
        # Word must be formable from the given letters
        letter_count = {}
        for char in self.base_word:
            letter_count[char] = letter_count.get(char, 0) + 1
        
        for char in word:
            if char not in letter_count or letter_count[char] == 0:
                return False
            letter_count[char] -= 1
        
        return True
    
    def display_game(self, message=""):
        """Display the current game state."""
        # Print game info
        print(f"{Fore.CYAN}Difficulty: {self.difficulty.capitalize()}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Time Remaining: {int(self.time_remaining())} seconds{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Score: {self.score}{Style.RESET_ALL}")
        print()
        
        # Print letters
        print(f"{Fore.YELLOW}Letters: {Style.RESET_ALL}", end="")
        for letter in self.letters:
            print(f"{Fore.GREEN}{letter.upper()}{Style.RESET_ALL} ", end="")
        print("\n")
        
        # Print found words with different colors based on length
        print(f"{Fore.YELLOW}Words Found ({len(self.found_words)}): {Style.RESET_ALL}")
        if self.found_words:
            # Sort words by length
            sorted_words = sorted(self.found_words, key=len)
            
            for word in sorted_words:
                if len(word) <= 4:
                    color = Fore.WHITE
                elif len(word) <= 6:
                    color = Fore.YELLOW
                else:
                    color = Fore.RED
                
                print(f"{color}{word}{Style.RESET_ALL} ", end="")
            print()
        else:
            print(f"{Fore.WHITE}None yet. Start guessing!{Style.RESET_ALL}")
        
        print()
        
        # Print message if any
        if message:
            print(f"{Fore.CYAN}{message}{Style.RESET_ALL}")
            print()
        
        # Print instructions
        print(f"{Fore.WHITE}Enter a word (at least {self.min_word_length} letters) or 'quit' to end game:{Style.RESET_ALL}")
        
        if self.game_over:
            # Display game over message
            print()
            print(f"{Fore.RED}Game Over!{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Final Score: {self.score}{Style.RESET_ALL}")
            
            # Show words not found
            words_not_found = [word for word in self.all_possible_words if word not in self.found_words]
            if words_not_found:
                print(f"{Fore.YELLOW}Words you missed ({len(words_not_found)}):{Style.RESET_ALL}")
                for word in sorted(words_not_found, key=len):
                    print(f"{Fore.WHITE}{word}{Style.RESET_ALL} ", end="")
                print()

def show_instructions():
    """Display game instructions."""
    print(f"{Fore.CYAN}INSTRUCTIONS:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Anagrams is a word game where you form words from a set of letters.")
    print(f"The goal is to find as many words as possible before time runs out.{Style.RESET_ALL}")
    print()
    print(f"{Fore.WHITE}Rules:")
    print(f" - All words must be valid English words")
    print(f" - Words must be at least the minimum length for your difficulty")
    print(f" - Words must be made from the available letters")
    print(f" - Each letter can only be used as many times as it appears in the set{Style.RESET_ALL}")
    print()
    print(f"{Fore.WHITE}Scoring:")
    print(f" - Longer words are worth more points")
    print(f" - Score for each word = (length of word)²{Style.RESET_ALL}")
    print()
    print(f"{Fore.WHITE}Difficulty Levels:")
    print(f" - Easy: Shorter words, 3-letter minimum, 3 minutes")
    print(f" - Medium: Medium-length words, 4-letter minimum, 2 minutes")
    print(f" - Hard: Longer words, 5-letter minimum, 1 minute{Style.RESET_ALL}")
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
        print(f"1. Easy (3-letter minimum, 3 minutes)")
        print(f"2. Medium (4-letter minimum, 2 minutes)")
        print(f"3. Hard (5-letter minimum, 1 minute)")
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
        
        # Set difficulty based on choice
        if choice == 1:
            difficulty = "easy"
            time_limit = 180  # 3 minutes
        elif choice == 2:
            difficulty = "medium"
            time_limit = 120  # 2 minutes
        else:
            difficulty = "hard"
            time_limit = 60   # 1 minute
        
        # Initialize game
        game = Anagrams(difficulty, time_limit)
        
        # Start the game
        clear_screen()
        print_header()
        game.display_game("Game starting! Make as many words as you can.")
        input(f"{Fore.GREEN}Press Enter to start the timer...{Style.RESET_ALL}")
        
        game.start_game()
        message = ""
        
        # Main game loop
        while not game.game_over:
            clear_screen()
            print_header()
            game.display_game(message)
            
            # Get user input with timeout
            user_input = input("> ").strip().lower()
            
            if user_input == "quit":
                break
            
            if user_input:
                success, message = game.submit_word(user_input)
            else:
                message = ""
            
            # Check if time's up
            game.time_remaining()
        
        # Game over
        clear_screen()
        print_header()
        game.display_game("")
        
        print()
        play_again = input(f"{Fore.CYAN}Play again? (y/n): {Style.RESET_ALL}").lower()
        if play_again != 'y':
            break
    
    clear_screen()
    print_header()
    print(f"{Fore.GREEN}Thanks for playing Anagrams!{Style.RESET_ALL}")
    time.sleep(1.5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print_header()
        print(f"{Fore.GREEN}Thanks for playing Anagrams!{Style.RESET_ALL}")
        sys.exit(0) 