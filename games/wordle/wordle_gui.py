#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox, Label, Button, Frame, Entry, StringVar
import random
import sys
import os
from PIL import Image, ImageTk

# Import the word list from the terminal version
try:
    from games.wordle import WORD_LIST
except ImportError:
    # Full word list copied from terminal version as fallback
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

class WordleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Wordle")
        self.root.geometry("600x700")  # Increased size for better visibility
        self.root.configure(bg="#121213")
        self.root.resizable(True, True)  # Allow resizing
        
        # Game parameters
        self.MAX_ATTEMPTS = 6
        self.WORD_LENGTH = 5
        self.current_attempt = 0
        self.current_letter = 0
        self.game_over = False
        self.secret_word = self.get_secret_word()
        
        # Colors
        self.COLORS = {
            "background": "#121213",
            "text": "#FFFFFF",
            "title": "#FFFFFF",
            "border": "#3A3A3C",
            "empty": "#121213",
            "keyboard": "#818384",
            "keyboard_text": "#FFFFFF",
            "correct": "#538D4E",  # Green
            "present": "#B59F3B",  # Yellow
            "absent": "#3A3A3C",   # Gray
        }
        
        # Keyboard layout
        self.KEYBOARD_ROWS = [
            "QWERTYUIOP",
            "ASDFGHJKL",
            "ZXCVBNM"
        ]
        
        # Track guessed letters
        self.letter_states = {}  # Maps letter to state (correct, present, absent)
        
        # Initialize the game board
        self.board = []
        for _ in range(self.MAX_ATTEMPTS):
            row = [""] * self.WORD_LENGTH
            self.board.append(row)
        
        # Create widgets
        self.create_widgets()
        
        # Show welcome screen
        self.show_welcome()
        
        # Set up keyboard bindings
        self.root.bind("<Key>", self.on_key_press)
        self.root.bind("<Return>", self.check_guess)
        self.root.bind("<BackSpace>", self.backspace)
    
    def create_widgets(self):
        """Create the GUI widgets."""
        # Main frame
        self.main_frame = Frame(self.root, bg=self.COLORS["background"])
        self.main_frame.pack(pady=10, expand=True, fill=tk.BOTH)
        
        # Game title
        self.title_label = Label(
            self.main_frame,
            text="WORDLE",
            font=("Helvetica", 28, "bold"),
            bg=self.COLORS["background"],
            fg=self.COLORS["title"]
        )
        self.title_label.pack(pady=(10, 20))
        
        # Game board frame
        self.board_frame = Frame(
            self.main_frame,
            bg=self.COLORS["background"]
        )
        self.board_frame.pack(pady=10)
        
        # Create the game board grid
        self.tile_frames = []
        self.tile_labels = []
        
        for row in range(self.MAX_ATTEMPTS):
            tile_row_frames = []
            tile_row_labels = []
            
            for col in range(self.WORD_LENGTH):
                # Create a frame for each tile with a border
                tile_frame = Frame(
                    self.board_frame,
                    width=54,
                    height=54,
                    bg=self.COLORS["background"],
                    highlightbackground=self.COLORS["border"],
                    highlightthickness=2
                )
                tile_frame.grid(row=row, column=col, padx=5, pady=5)
                tile_frame.grid_propagate(False)  # Maintain the frame size
                
                # Create a label for the letter inside the tile
                tile_label = Label(
                    tile_frame,
                    text="",
                    font=("Helvetica", 24, "bold"),
                    bg=self.COLORS["background"],
                    fg=self.COLORS["text"]
                )
                tile_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
                
                tile_row_frames.append(tile_frame)
                tile_row_labels.append(tile_label)
            
            self.tile_frames.append(tile_row_frames)
            self.tile_labels.append(tile_row_labels)
        
        # Virtual keyboard frame
        self.keyboard_frame = Frame(
            self.main_frame,
            bg=self.COLORS["background"]
        )
        self.keyboard_frame.pack(pady=20, fill=tk.X)
        
        # Create virtual keyboard
        self.keyboard_buttons = {}
        
        for i, row in enumerate(self.KEYBOARD_ROWS):
            row_frame = Frame(self.keyboard_frame, bg=self.COLORS["background"])
            row_frame.pack(pady=2)
            
            # Add extra padding for the middle row
            if i == 1:
                padding_frame = Frame(row_frame, width=15, bg=self.COLORS["background"])
                padding_frame.pack(side=tk.LEFT)
            
            # Add Enter button at the beginning of the last row
            if i == 2:
                enter_btn = Button(
                    row_frame,
                    text="ENTER",
                    font=("Helvetica", 10, "bold"),
                    width=5,
                    height=1,
                    bg=self.COLORS["keyboard"],
                    fg=self.COLORS["keyboard_text"],
                    relief=tk.FLAT,
                    command=self.check_guess
                )
                enter_btn.pack(side=tk.LEFT, padx=2, pady=2)
            
            # Add letter buttons
            for letter in row:
                key_btn = Button(
                    row_frame,
                    text=letter,
                    font=("Helvetica", 11, "bold"),
                    width=2,
                    height=1,
                    bg=self.COLORS["keyboard"],
                    fg=self.COLORS["keyboard_text"],
                    relief=tk.FLAT,
                    command=lambda l=letter: self.key_press(l)
                )
                key_btn.pack(side=tk.LEFT, padx=2, pady=2)
                self.keyboard_buttons[letter] = key_btn
            
            # Add Backspace button at the end of the last row
            if i == 2:
                backspace_btn = Button(
                    row_frame,
                    text="⌫",
                    font=("Helvetica", 10, "bold"),
                    width=2,
                    height=1,
                    bg=self.COLORS["keyboard"],
                    fg=self.COLORS["keyboard_text"],
                    relief=tk.FLAT,
                    command=self.backspace
                )
                backspace_btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # Control buttons at the bottom
        self.control_frame = Frame(self.main_frame, bg=self.COLORS["background"])
        self.control_frame.pack(pady=10, fill=tk.X)
        
        # New Game button
        self.new_game_button = Button(
            self.control_frame,
            text="New Game",
            font=("Helvetica", 12),
            bg="#4CAF50",
            fg="white",
            command=self.new_game
        )
        self.new_game_button.pack(side=tk.LEFT, padx=10)
        
        # Quit button
        self.quit_button = Button(
            self.control_frame,
            text="Quit",
            font=("Helvetica", 12),
            bg="#F44336",
            fg="white",
            command=self.quit_game
        )
        self.quit_button.pack(side=tk.RIGHT, padx=10)
        
        # Status label
        self.status_label = Label(
            self.main_frame,
            text="",
            font=("Helvetica", 12),
            bg=self.COLORS["background"],
            fg=self.COLORS["text"]
        )
        self.status_label.pack(pady=10)
    
    def show_welcome(self):
        """Show the welcome screen."""
        welcome_window = tk.Toplevel(self.root)
        welcome_window.title("Welcome to Wordle")
        welcome_window.geometry("450x400")  # Increased size
        welcome_window.configure(bg="#121213")
        welcome_window.transient(self.root)
        welcome_window.grab_set()
        welcome_window.resizable(True, True)  # Allow resizing
        
        # Welcome title
        welcome_label = Label(
            welcome_window,
            text="Welcome to Wordle",
            font=("Helvetica", 18, "bold"),
            bg="#121213",
            fg="#FFFFFF"
        )
        welcome_label.pack(pady=(20, 10))
        
        # Instructions
        instructions_frame = Frame(welcome_window, bg="#121213", padx=20)
        instructions_frame.pack(fill=tk.BOTH, expand=True)
        
        # Example tiles for instructions
        example_frame = Frame(instructions_frame, bg="#121213")
        example_frame.pack(pady=10)
        
        # Correct letter example
        correct_frame = Frame(
            example_frame,
            width=40,
            height=40,
            bg="#538D4E",  # Green
        )
        correct_frame.grid(row=0, column=0, padx=5)
        correct_frame.grid_propagate(False)
        
        Label(
            correct_frame,
            text="A",
            font=("Helvetica", 18, "bold"),
            bg="#538D4E",
            fg="#FFFFFF"
        ).place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        Label(
            example_frame,
            text="is in the word and in the correct spot",
            font=("Helvetica", 10),
            bg="#121213",
            fg="#FFFFFF",
            justify=tk.LEFT
        ).grid(row=0, column=1, padx=5, sticky=tk.W)
        
        # Present letter example
        present_frame = Frame(
            example_frame,
            width=40,
            height=40,
            bg="#B59F3B",  # Yellow
        )
        present_frame.grid(row=1, column=0, padx=5, pady=5)
        present_frame.grid_propagate(False)
        
        Label(
            present_frame,
            text="B",
            font=("Helvetica", 18, "bold"),
            bg="#B59F3B",
            fg="#FFFFFF"
        ).place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        Label(
            example_frame,
            text="is in the word but in the wrong spot",
            font=("Helvetica", 10),
            bg="#121213",
            fg="#FFFFFF",
            justify=tk.LEFT
        ).grid(row=1, column=1, padx=5, sticky=tk.W)
        
        # Absent letter example
        absent_frame = Frame(
            example_frame,
            width=40,
            height=40,
            bg="#3A3A3C",  # Gray
        )
        absent_frame.grid(row=2, column=0, padx=5)
        absent_frame.grid_propagate(False)
        
        Label(
            absent_frame,
            text="C",
            font=("Helvetica", 18, "bold"),
            bg="#3A3A3C",
            fg="#FFFFFF"
        ).place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        Label(
            example_frame,
            text="is not in the word",
            font=("Helvetica", 10),
            bg="#121213",
            fg="#FFFFFF",
            justify=tk.LEFT
        ).grid(row=2, column=1, padx=5, sticky=tk.W)
        
        # Rules text
        rules_text = [
            "Guess the WORDLE in six tries.",
            "Each guess must be a valid 5-letter word.",
            "After each guess, the color of the tiles will change",
            "to show how close your guess was to the word.",
            "",
            "You can type on your keyboard or use the on-screen",
            "keyboard to enter letters. Press ENTER to submit",
            "your guess."
        ]
        
        for text in rules_text:
            Label(
                instructions_frame,
                text=text,
                font=("Helvetica", 10),
                bg="#121213",
                fg="#FFFFFF",
                justify=tk.LEFT
            ).pack(anchor=tk.W, pady=1)
        
        # Start button
        start_button = Button(
            welcome_window,
            text="Start Game",
            font=("Helvetica", 14, "bold"),
            bg="#538D4E",  # Green
            fg="white",
            command=welcome_window.destroy
        )
        start_button.pack(pady=20)
    
    def get_secret_word(self):
        """Randomly select a secret word from the word list."""
        return random.choice(WORD_LIST).upper()
    
    def on_key_press(self, event):
        """Handle physical keyboard input."""
        if self.game_over:
            return
        
        key = event.char.upper()
        if key.isalpha() and len(key) == 1:
            self.key_press(key)
    
    def key_press(self, letter):
        """Handle a key press (virtual or physical keyboard)."""
        if self.game_over:
            return
        
        # Add the letter to the current word if there's space
        if self.current_letter < self.WORD_LENGTH:
            row = self.current_attempt
            col = self.current_letter
            
            # Update the board and display
            self.board[row][col] = letter
            self.tile_labels[row][col].config(text=letter)
            
            # Move to the next position
            self.current_letter += 1
    
    def backspace(self, event=None):
        """Handle a backspace key press."""
        if self.game_over:
            return
        
        # Remove the last letter if there is one
        if self.current_letter > 0:
            self.current_letter -= 1
            row = self.current_attempt
            col = self.current_letter
            
            # Update the board and display
            self.board[row][col] = ""
            self.tile_labels[row][col].config(text="")
    
    def check_guess(self, event=None):
        """Check the current guess."""
        if self.game_over:
            return
        
        # Make sure the guess is complete
        if self.current_letter < self.WORD_LENGTH:
            self.status_label.config(text="Not enough letters")
            return
        
        # Get the current guess
        row = self.current_attempt
        guess = "".join(self.board[row])
        
        # Check if it's a valid word
        if guess.lower() not in WORD_LIST:
            self.status_label.config(text="Not in word list")
            return
        
        # Clear the status
        self.status_label.config(text="")
        
        # Check each letter against the secret word
        correct_count = 0
        secret = self.secret_word
        
        # First, mark exact matches (green)
        used_indices = set()
        for i in range(self.WORD_LENGTH):
            letter = guess[i]
            if letter == secret[i]:
                self.update_tile(row, i, "correct")
                self.update_keyboard_key(letter, "correct")
                correct_count += 1
                used_indices.add(i)
            else:
                # Temporarily leave these as is
                pass
        
        # Then, mark partial matches (yellow) and misses (gray)
        for i in range(self.WORD_LENGTH):
            if i in used_indices:
                continue
            
            letter = guess[i]
            
            # Check if the letter exists elsewhere in the secret word
            found = False
            for j in range(self.WORD_LENGTH):
                if j not in used_indices and letter == secret[j]:
                    self.update_tile(row, i, "present")
                    self.update_keyboard_key(letter, "present")
                    used_indices.add(j)
                    found = True
                    break
            
            # If not found, it's a miss
            if not found:
                self.update_tile(row, i, "absent")
                # Only update keyboard if this key doesn't already have a better status
                if letter not in self.letter_states or self.letter_states[letter] == "absent":
                    self.update_keyboard_key(letter, "absent")
        
        # Check if the player has won
        if correct_count == self.WORD_LENGTH:
            self.game_over = True
            attempts = self.current_attempt + 1
            self.status_label.config(text=f"Congratulations! You guessed the word in {attempts} attempts!")
            return
        
        # Move to the next attempt
        self.current_attempt += 1
        self.current_letter = 0
        
        # Check if the player has lost
        if self.current_attempt >= self.MAX_ATTEMPTS:
            self.game_over = True
            self.status_label.config(text=f"Game over! The word was {self.secret_word}")
    
    def update_tile(self, row, col, state):
        """Update the visual appearance of a tile based on its state."""
        colors = {
            "correct": self.COLORS["correct"],
            "present": self.COLORS["present"],
            "absent": self.COLORS["absent"]
        }
        
        # Update the tile's color
        self.tile_frames[row][col].config(bg=colors[state], highlightbackground=colors[state])
        self.tile_labels[row][col].config(bg=colors[state])
    
    def update_keyboard_key(self, letter, state):
        """Update the visual appearance of a keyboard key based on its state."""
        button = self.keyboard_buttons.get(letter)
        if not button:
            return
        
        # State precedence: correct > present > absent
        if letter in self.letter_states:
            current_state = self.letter_states[letter]
            if current_state == "correct" or (current_state == "present" and state == "absent"):
                return
        
        colors = {
            "correct": self.COLORS["correct"],
            "present": self.COLORS["present"],
            "absent": self.COLORS["absent"]
        }
        
        # Update the key's color
        button.config(bg=colors[state])
        
        # Update the letter state
        self.letter_states[letter] = state
    
    def new_game(self):
        """Start a new game."""
        # Reset game state
        self.current_attempt = 0
        self.current_letter = 0
        self.game_over = False
        self.secret_word = self.get_secret_word()
        self.letter_states = {}
        
        # Reset the board
        self.board = []
        for _ in range(self.MAX_ATTEMPTS):
            row = [""] * self.WORD_LENGTH
            self.board.append(row)
        
        # Reset the visual board
        for row in range(self.MAX_ATTEMPTS):
            for col in range(self.WORD_LENGTH):
                self.tile_frames[row][col].config(
                    bg=self.COLORS["background"],
                    highlightbackground=self.COLORS["border"]
                )
                self.tile_labels[row][col].config(
                    text="",
                    bg=self.COLORS["background"]
                )
        
        # Reset the keyboard
        for letter, button in self.keyboard_buttons.items():
            button.config(bg=self.COLORS["keyboard"])
        
        # Reset the status
        self.status_label.config(text="")
    
    def quit_game(self):
        """Quit the game."""
        if messagebox.askyesno("Quit", "Are you sure you want to quit the game?"):
            self.root.destroy()

def main():
    """Main function to start the GUI game."""
    root = tk.Tk()
    app = WordleGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 