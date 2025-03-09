#!/usr/bin/env python3
import os
import sys
import time
import random
import colorama
from colorama import Fore, Back, Style

# Initialize colorama
colorama.init()

# Word list (common 5-letter words)
WORD_LIST = [
    "about", "above", "actor", "acute", "admit", "adopt", "adore", "adult", "after", "again",
    "agent", "agree", "ahead", "album", "alert", "alike", "alive", "allow", "alone", "along",
    "alter", "among", "anger", "angle", "angry", "anime", "ankle", "annoy", "apart", "apple",
    "apply", "arena", "argue", "arise", "armor", "array", "arrow", "asset", "avoid", "award",
    "aware", "awful", "bacon", "badge", "badly", "baker", "bases", "basic", "basin", "basis",
    "batch", "beach", "beard", "beast", "begin", "being", "below", "bench", "berry", "birth",
    "black", "blade", "blame", "blank", "blast", "blaze", "bleak", "blend", "bless", "blind",
    "block", "blood", "bloom", "blues", "blunt", "board", "boast", "bonus", "boost", "booth",
    "born", "bound", "brace", "brain", "brake", "brand", "brave", "bread", "break", "breed",
    "brick", "brief", "bring", "broad", "brown", "brush", "build", "built", "bunch", "burst",
    "cabin", "cable", "camel", "canal", "candy", "canon", "cargo", "carry", "carve", "catch",
    "cause", "cease", "chain", "chair", "chalk", "charm", "chart", "chase", "cheap", "check",
    "cheer", "chess", "chief", "child", "chill", "china", "chips", "choir", "choke", "chord",
    "civil", "claim", "clash", "class", "clean", "clear", "clerk", "click", "cliff", "climb",
    "cling", "clock", "close", "cloth", "cloud", "clown", "coast", "comic", "comma", "coral",
    "count", "court", "cover", "craft", "crash", "crawl", "crazy", "cream", "crime", "crisp",
    "cross", "crowd", "crown", "crude", "cruel", "crush", "crust", "crypt", "cubic", "curry",
    "cycle", "daily", "dairy", "dance", "datum", "dealt", "death", "debit", "debut", "decay",
    "deck", "deem", "delay", "delta", "dense", "depth", "devil", "diary", "digit", "diner",
    "dirty", "disco", "ditch", "diver", "dodge", "doing", "donor", "doubt", "dough", "draft",
    "drain", "drama", "drank", "dread", "dream", "dress", "dried", "drift", "drill", "drink",
    "drive", "drone", "drown", "drunk", "dryer", "dummy", "dusty", "eager", "eagle", "early",
    "earth", "elder", "elect", "elite", "email", "empty", "enact", "enjoy", "enter", "entry",
    "equal", "equip", "erase", "error", "essay", "evade", "event", "every", "exact", "exist",
    "extra", "fable", "facet", "facto", "faint", "fairy", "faith", "false", "fancy", "fault",
    "favor", "feast", "fence", "ferry", "fetch", "fever", "fiber", "field", "fifth", "fight",
    "final", "first", "flame", "flash", "fleet", "flesh", "flick", "float", "flock", "flood",
    "floor", "flora", "flour", "flown", "fluid", "flush", "flute", "focus", "foggy", "force",
    "forge", "forth", "found", "frame", "frank", "fraud", "freak", "fresh", "front", "frost",
    "frown", "fruity", "fully", "funny", "given", "glass", "gleam", "glory", "glove", "grape",
    "grasp", "grass", "grate", "great", "greed", "green", "greet", "grief", "grill", "grind",
    "groan", "groom", "gross", "group", "grove", "growl", "grown", "guard", "guess", "guest",
    "guide", "guild", "guilt", "habit", "happy", "hardy", "hatch", "havoc", "heart", "heavy",
    "hello", "hence", "hinge", "hobby", "holly", "honey", "honor", "horse", "hotel", "house",
    "human", "hurry", "ideal", "image", "imply", "index", "inner", "input", "intro", "issue",
    "ivory", "jeans", "joint", "jolly", "judge", "juice", "juicy", "jumbo", "jumpy", "kayak",
    "kebab", "kiosk", "knife", "knock", "known", "label", "labor", "laden", "lance", "large",
    "laser", "laugh", "layer", "learn", "lease", "leave", "legal", "lemon", "level", "lever",
    "light", "limit", "linen", "liver", "lobby", "local", "lodge", "logic", "loose", "lorry",
    "lower", "loyal", "lucky", "lunar", "lunch", "lyric", "magic", "major", "maker", "manor",
    "march", "match", "maybe", "mayor", "medal", "media", "mercy", "merge", "merit", "merry",
    "metal", "meter", "midst", "might", "minor", "mixed", "model", "moist", "money", "month",
    "moral", "motor", "mount", "mourn", "mouse", "mouth", "movie", "music", "naive", "naked",
    "nasty", "naval", "nerve", "never", "newly", "niche", "night", "noble", "noise", "noisy",
    "north", "notch", "noted", "novel", "nurse", "oasis", "occur", "ocean", "offer", "often",
    "olive", "onion", "onset", "opera", "orbit", "order", "organ", "other", "ought", "ounce",
    "outer", "owing", "owner", "oxide", "paced", "panel", "panic", "paper", "party", "pasta",
    "patch", "patio", "pause", "peace", "pearl", "phase", "phone", "photo", "piano", "piece",
    "pilot", "pitch", "pivot", "pixel", "pizzo", "place", "plain", "plane", "plant", "plate",
    "plead", "pluck", "point", "porch", "pouch", "pound", "power", "press", "price", "pride",
    "prime", "print", "prior", "prize", "probe", "prone", "proof", "prose", "proud", "prove",
    "proxy", "pulse", "punch", "pupil", "puppy", "purse", "queen", "query", "quest", "quick",
    "quiet", "quilt", "quirk", "quite", "quota", "quote", "radar", "radio", "raise", "rally",
    "ramen", "ranch", "range", "rapid", "ratio", "reach", "react", "ready", "realm", "rebel",
    "refer", "reign", "relax", "reply", "reset", "resin", "retro", "rider", "ridge", "rifle",
    "right", "rigid", "rigor", "rinse", "rival", "river", "roast", "robot", "rocky", "rogue",
    "roman", "rotor", "rough", "round", "route", "royal", "rugby", "ruins", "ruler", "rural",
    "sadly", "safer", "saint", "salad", "salon", "salty", "salve", "sandy", "sauce", "scale",
    "scare", "scarf", "scary", "scene", "scent", "scold", "scope", "score", "scout", "scrap",
    "screw", "scrub", "seize", "sense", "serum", "serve", "setup", "seven", "shade", "shaft",
    "shake", "shall", "shame", "shape", "share", "shark", "sharp", "shave", "sheep", "sheet",
    "shelf", "shell", "shift", "shine", "shirt", "shock", "shore", "short", "shout", "shown",
    "shrimp", "sight", "sigma", "silky", "silly", "since", "siren", "skill", "skirt", "skull",
    "slate", "slave", "sleep", "slice", "slide", "slime", "slope", "small", "smart", "smile",
    "smoke", "snack", "snake", "sneak", "sniff", "solar", "solid", "solve", "sorry", "sound",
    "south", "space", "spare", "spark", "speak", "speed", "spell", "spend", "spice", "spicy",
    "spike", "spine", "spoon", "sport", "spray", "squad", "stack", "staff", "stage", "stain",
    "stair", "stake", "stand", "stark", "start", "state", "steak", "steal", "steam", "steel",
    "steep", "steer", "stern", "stick", "stiff", "still", "stock", "stone", "store", "storm",
    "story", "stove", "strap", "straw", "strip", "study", "stuff", "style", "sugar", "suite",
    "sunny", "super", "surge", "sushi", "swamp", "swarm", "swear", "sweat", "sweep", "sweet",
    "swell", "swift", "swing", "swiss", "sword", "syrup", "table", "taken", "tales", "tango",
    "tardy", "taste", "tasty", "taunt", "teach", "tease", "teddy", "tempo", "thank", "theft",
    "theme", "thick", "thief", "thing", "think", "third", "thorn", "those", "three", "throw",
    "thumb", "tiger", "tight", "timer", "tired", "title", "toast", "today", "token", "tonic",
    "tooth", "topic", "torch", "total", "touch", "tough", "towel", "tower", "toxic", "trace",
    "track", "trade", "trail", "train", "trait", "tramp", "trash", "tray", "treat", "trend",
    "trial", "tribe", "trick", "troop", "truck", "truly", "trunk", "trust", "truth", "tulip",
    "twice", "twist", "tying", "ultra", "uncle", "under", "undue", "union", "unite", "unity",
    "upset", "urban", "usage", "usher", "usual", "utter", "vague", "valid", "value", "valve",
    "vapor", "vault", "vegan", "venom", "venue", "verse", "video", "view", "viral", "virus",
    "visit", "vital", "vivid", "vocal", "vodka", "voice", "voila", "vowel", "wafer", "wagon",
    "waist", "waive", "waste", "watch", "water", "waver", "weary", "weave", "wedge", "weigh",
    "weird", "whale", "wheat", "wheel", "where", "which", "while", "white", "whole", "whose",
    "widen", "width", "witch", "woman", "words", "world", "worry", "worse", "worst", "worth",
    "would", "wound", "woven", "wreck", "write", "wrong", "yacht", "yield", "young", "youth",
    "zebra", "zesty", "zonal"
]

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the game header."""
    print(f"{Back.GREEN}{Fore.WHITE}╔═══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Back.GREEN}{Fore.WHITE}║                        WORDLE                                 ║{Style.RESET_ALL}")
    print(f"{Back.GREEN}{Fore.WHITE}╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()

def get_secret_word():
    """Randomly select a secret word from the word list."""
    return random.choice(WORD_LIST).upper()

def is_valid_guess(guess, word_list):
    """Check if the guess is a valid 5-letter word in our word list."""
    return guess.lower() in word_list

def format_guess_result(guess, secret):
    """Format the guess result with color coding:
    - Green: Correct letter in correct position
    - Yellow: Correct letter in wrong position
    - Gray: Letter not in the word
    """
    guess = guess.upper()
    secret = secret.upper()
    result = ""
    
    # First, handle exact matches (green)
    used_secret_positions = set()
    for i in range(len(guess)):
        if guess[i] == secret[i]:
            result += f"{Back.GREEN}{Fore.WHITE}{guess[i]}{Style.RESET_ALL} "
            used_secret_positions.add(i)
        else:
            # Placeholder for now
            result += f"_ "
    
    # Now handle partial matches (yellow) and misses (gray)
    result_list = result.split()
    
    for i in range(len(guess)):
        if result_list[i] != "_":
            # Already processed as a green match
            continue
        
        # Check if this letter exists elsewhere in the secret word
        found = False
        for j in range(len(secret)):
            if j not in used_secret_positions and guess[i] == secret[j]:
                result_list[i] = f"{Back.YELLOW}{Fore.BLACK}{guess[i]}{Style.RESET_ALL}"
                used_secret_positions.add(j)
                found = True
                break
        
        # If not found, it's a miss
        if not found:
            result_list[i] = f"{Back.WHITE}{Fore.BLACK}{guess[i]}{Style.RESET_ALL}"
    
    return " ".join(result_list)

def show_instructions():
    """Display game instructions."""
    print(f"{Fore.CYAN}INSTRUCTIONS:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Wordle is a word-guessing game where you need to guess")
    print(f"the secret five-letter word in six tries or fewer.{Style.RESET_ALL}")
    print()
    print(f"{Fore.WHITE}After each guess, you'll see color-coded feedback:{Style.RESET_ALL}")
    print(f"{Back.GREEN}{Fore.WHITE}A{Style.RESET_ALL} - The letter A is in the word and in the correct position.")
    print(f"{Back.YELLOW}{Fore.BLACK}B{Style.RESET_ALL} - The letter B is in the word but in the wrong position.")
    print(f"{Back.WHITE}{Fore.BLACK}C{Style.RESET_ALL} - The letter C is not in the word.")
    print()
    print(f"{Fore.WHITE}All guesses must be valid five-letter words.{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Good luck!{Style.RESET_ALL}")
    print()
    input(f"{Fore.GREEN}Press Enter to start the game...{Style.RESET_ALL}")

def play_wordle():
    """Play a single game of Wordle."""
    secret_word = get_secret_word()
    max_attempts = 6
    attempts = 0
    guesses = []
    guess_results = []
    
    while attempts < max_attempts:
        clear_screen()
        print_header()
        
        # Show previous guesses
        for i, (guess, result) in enumerate(zip(guesses, guess_results)):
            print(f"Guess {i+1}: {result}")
        
        # Show blank lines for remaining guesses
        for i in range(len(guesses), max_attempts):
            print(f"Guess {i+1}: _ _ _ _ _")
        
        print()
        
        # Check if the player has won
        if guesses and guesses[-1].upper() == secret_word:
            print(f"{Fore.GREEN}Congratulations! You guessed the word {secret_word} in {attempts} attempts!{Style.RESET_ALL}")
            return True
        
        # Get the next guess
        print(f"{Fore.CYAN}Attempts remaining: {max_attempts - attempts}{Style.RESET_ALL}")
        guess = input(f"{Fore.WHITE}Enter your guess (5 letters): {Style.RESET_ALL}").strip().upper()
        
        # Validate the guess
        if len(guess) != 5:
            print(f"{Fore.RED}Your guess must be exactly 5 letters.{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            continue
        
        if not guess.isalpha():
            print(f"{Fore.RED}Your guess must contain only letters.{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            continue
        
        if not is_valid_guess(guess, WORD_LIST):
            print(f"{Fore.RED}'{guess}' is not in the word list.{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            continue
        
        # Process the valid guess
        attempts += 1
        guesses.append(guess)
        guess_results.append(format_guess_result(guess, secret_word))
        
        # Check if the player has lost
        if attempts >= max_attempts and guess.upper() != secret_word:
            clear_screen()
            print_header()
            
            # Show all guesses
            for i, (guess, result) in enumerate(zip(guesses, guess_results)):
                print(f"Guess {i+1}: {result}")
            
            print()
            print(f"{Fore.RED}Game over! The word was {Fore.WHITE}{secret_word}{Fore.RED}.{Style.RESET_ALL}")
            return False
    
    return False

def main():
    """Main game function."""
    clear_screen()
    print_header()
    show_instructions()
    
    while True:
        play_wordle()
        
        # Ask to play again
        print()
        play_again = input(f"{Fore.CYAN}Play again? (y/n): {Style.RESET_ALL}").lower()
        if play_again != 'y':
            clear_screen()
            print_header()
            print(f"{Fore.GREEN}Thanks for playing Wordle!{Style.RESET_ALL}")
            time.sleep(2)
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print_header()
        print(f"{Fore.GREEN}Thanks for playing Wordle!{Style.RESET_ALL}")
        sys.exit(0) 