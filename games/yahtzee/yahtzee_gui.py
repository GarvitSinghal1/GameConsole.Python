#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox, ttk
import random
import sys
import os
from PIL import Image, ImageTk
import time

# Try to import scoring functions from terminal version
try:
    from games.yahtzee import calculate_possible_scores, calculate_total_score
except ImportError:
    # Define scoring functions if import fails
    def calculate_possible_scores(dice):
        """Calculate all possible scores for the current dice."""
        dice_counts = [0] * 7  # Index 0 will be unused
        for die in dice:
            dice_counts[die] += 1
        
        scores = {}
        
        # Upper section
        scores["ones"] = sum(die for die in dice if die == 1)
        scores["twos"] = sum(die for die in dice if die == 2)
        scores["threes"] = sum(die for die in dice if die == 3)
        scores["fours"] = sum(die for die in dice if die == 4)
        scores["fives"] = sum(die for die in dice if die == 5)
        scores["sixes"] = sum(die for die in dice if die == 6)
        
        # Lower section
        # Three of a kind
        if any(count >= 3 for count in dice_counts):
            scores["three_of_a_kind"] = sum(dice)
        else:
            scores["three_of_a_kind"] = 0
        
        # Four of a kind
        if any(count >= 4 for count in dice_counts):
            scores["four_of_a_kind"] = sum(dice)
        else:
            scores["four_of_a_kind"] = 0
        
        # Full house
        if (3 in dice_counts and 2 in dice_counts) or dice_counts.count(3) > 1:
            scores["full_house"] = 25
        else:
            scores["full_house"] = 0
        
        # Small straight
        if (1 in dice and 2 in dice and 3 in dice and 4 in dice) or \
           (2 in dice and 3 in dice and 4 in dice and 5 in dice) or \
           (3 in dice and 4 in dice and 5 in dice and 6 in dice):
            scores["small_straight"] = 30
        else:
            scores["small_straight"] = 0
        
        # Large straight
        if (1 in dice and 2 in dice and 3 in dice and 4 in dice and 5 in dice) or \
           (2 in dice and 3 in dice and 4 in dice and 5 in dice and 6 in dice):
            scores["large_straight"] = 40
        else:
            scores["large_straight"] = 0
        
        # Yahtzee
        if 5 in dice_counts:
            scores["yahtzee"] = 50
        else:
            scores["yahtzee"] = 0
        
        # Chance
        scores["chance"] = sum(dice)
        
        return scores

    def calculate_total_score(scorecard):
        """Calculate the total score from the scorecard."""
        # Upper section
        upper_categories = ["ones", "twos", "threes", "fours", "fives", "sixes"]
        upper_sum = sum(scorecard.get(key, 0) for key in upper_categories)
        
        # Bonus for upper section
        bonus = 35 if upper_sum >= 63 else 0
        
        # Lower section
        lower_categories = ["three_of_a_kind", "four_of_a_kind", "full_house", 
                            "small_straight", "large_straight", "yahtzee", "chance"]
        lower_sum = sum(scorecard.get(key, 0) for key in lower_categories)
        
        # Yahtzee bonus
        yahtzee_bonus = scorecard.get("yahtzee_bonus", 0) * 100
        
        return upper_sum + bonus + lower_sum + yahtzee_bonus

class DiceButton(tk.Button):
    """Custom button class for dice."""
    def __init__(self, master, value=1, **kwargs):
        super().__init__(master, **kwargs)
        self.value = value
        self.kept = False
        self.update_appearance()
    
    def toggle_kept(self):
        """Toggle whether this die is kept or not."""
        if not self.master.rolling:  # Only allow toggling if not currently rolling
            self.kept = not self.kept
            self.update_appearance()
    
    def update_appearance(self):
        """Update the button appearance based on its state."""
        # Update text and colors based on kept state
        self.config(
            text=str(self.value),
            bg="#4CAF50" if self.kept else "#f0f0f0",
            fg="white" if self.kept else "black",
            relief=tk.SUNKEN if self.kept else tk.RAISED
        )

class YahtzeeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Yahtzee")
        self.root.geometry("800x700")
        self.root.configure(bg="#f0f0f0")
        self.root.resizable(True, True)
        
        # Game state
        self.dice = [1, 1, 1, 1, 1]  # Initial dice values
        self.scorecard = {}
        self.current_roll = 0
        self.max_rolls = 3
        self.rolling = False
        self.yahtzee_bonus_available = False
        self.game_over = False
        
        # Create widgets
        self.create_widgets()
        
        # Show welcome screen
        self.show_welcome()
    
    def create_widgets(self):
        """Create the GUI widgets."""
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title label
        self.title_label = ttk.Label(
            self.main_frame,
            text="YAHTZEE",
            font=("Helvetica", 24, "bold")
        )
        self.title_label.pack(pady=(0, 10))
        
        # Game info frame
        self.info_frame = ttk.Frame(self.main_frame)
        self.info_frame.pack(fill=tk.X, pady=5)
        
        # Roll counter
        self.roll_var = tk.StringVar(value="Roll: 0/3")
        self.roll_label = ttk.Label(
            self.info_frame,
            textvariable=self.roll_var,
            font=("Helvetica", 12)
        )
        self.roll_label.pack(side=tk.LEFT, padx=10)
        
        # Dice frame
        self.dice_frame = ttk.Frame(self.main_frame)
        self.dice_frame.pack(pady=10)
        
        # Create dice buttons
        self.dice_buttons = []
        for i in range(5):
            die = DiceButton(
                self.dice_frame,
                value=self.dice[i],
                width=3,
                height=1,
                font=("Helvetica", 24, "bold"),
                command=lambda i=i: self.toggle_die(i)
            )
            die.grid(row=0, column=i, padx=10, pady=10)
            self.dice_buttons.append(die)
        
        # Roll button
        self.roll_button = ttk.Button(
            self.main_frame,
            text="Roll Dice",
            command=self.roll_dice
        )
        self.roll_button.pack(pady=10)
        
        # Scorecard frame
        self.scorecard_frame = ttk.Frame(self.main_frame)
        self.scorecard_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Upper section frame
        self.upper_frame = ttk.LabelFrame(
            self.scorecard_frame,
            text="Upper Section",
            padding=10
        )
        self.upper_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Upper section categories
        self.upper_buttons = {}
        upper_categories = [
            ("Ones", "ones", "Sum of all ones"),
            ("Twos", "twos", "Sum of all twos"),
            ("Threes", "threes", "Sum of all threes"),
            ("Fours", "fours", "Sum of all fours"),
            ("Fives", "fives", "Sum of all fives"),
            ("Sixes", "sixes", "Sum of all sixes")
        ]
        
        for i, (name, key, tooltip) in enumerate(upper_categories):
            # Category label
            ttk.Label(self.upper_frame, text=name).grid(row=i, column=0, sticky="w", padx=5, pady=2)
            
            # Score button
            score_button = ttk.Button(
                self.upper_frame,
                text="Score",
                width=10,
                command=lambda k=key: self.score_category(k)
            )
            score_button.grid(row=i, column=1, padx=5, pady=2)
            
            # Score value label
            score_var = tk.StringVar(value="")
            score_label = ttk.Label(
                self.upper_frame,
                textvariable=score_var,
                width=5,
                anchor="center"
            )
            score_label.grid(row=i, column=2, padx=5, pady=2)
            
            self.upper_buttons[key] = {
                "button": score_button,
                "var": score_var,
                "tooltip": tooltip
            }
        
        # Upper section bonus
        ttk.Label(self.upper_frame, text="Bonus (63+ = 35)").grid(row=6, column=0, sticky="w", padx=5, pady=2)
        self.bonus_var = tk.StringVar(value="0")
        ttk.Label(self.upper_frame, textvariable=self.bonus_var, width=5, anchor="center").grid(row=6, column=2, padx=5, pady=2)
        
        # Lower section frame
        self.lower_frame = ttk.LabelFrame(
            self.scorecard_frame,
            text="Lower Section",
            padding=10
        )
        self.lower_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Lower section categories
        self.lower_buttons = {}
        lower_categories = [
            ("3 of a Kind", "three_of_a_kind", "Sum of all dice if 3+ of one value"),
            ("4 of a Kind", "four_of_a_kind", "Sum of all dice if 4+ of one value"),
            ("Full House", "full_house", "25 points for 3 of one value and 2 of another"),
            ("Sm. Straight", "small_straight", "30 points for 4 consecutive values"),
            ("Lg. Straight", "large_straight", "40 points for 5 consecutive values"),
            ("YAHTZEE", "yahtzee", "50 points for 5 of the same value"),
            ("Chance", "chance", "Sum of all dice")
        ]
        
        for i, (name, key, tooltip) in enumerate(lower_categories):
            # Category label
            ttk.Label(self.lower_frame, text=name).grid(row=i, column=0, sticky="w", padx=5, pady=2)
            
            # Score button
            score_button = ttk.Button(
                self.lower_frame,
                text="Score",
                width=10,
                command=lambda k=key: self.score_category(k)
            )
            score_button.grid(row=i, column=1, padx=5, pady=2)
            
            # Score value label
            score_var = tk.StringVar(value="")
            score_label = ttk.Label(
                self.lower_frame,
                textvariable=score_var,
                width=5,
                anchor="center"
            )
            score_label.grid(row=i, column=2, padx=5, pady=2)
            
            self.lower_buttons[key] = {
                "button": score_button,
                "var": score_var,
                "tooltip": tooltip
            }
        
        # Yahtzee bonus
        ttk.Label(self.lower_frame, text="YAHTZEE Bonus").grid(row=7, column=0, sticky="w", padx=5, pady=2)
        self.yahtzee_bonus_var = tk.StringVar(value="0")
        ttk.Label(self.lower_frame, textvariable=self.yahtzee_bonus_var, width=5, anchor="center").grid(row=7, column=2, padx=5, pady=2)
        
        # Total score
        self.total_frame = ttk.Frame(self.main_frame)
        self.total_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(self.total_frame, text="TOTAL SCORE:", font=("Helvetica", 14, "bold")).pack(side=tk.LEFT, padx=10)
        
        self.total_var = tk.StringVar(value="0")
        ttk.Label(self.total_frame, textvariable=self.total_var, font=("Helvetica", 14, "bold")).pack(side=tk.LEFT)
        
        # Control buttons
        self.control_frame = ttk.Frame(self.main_frame)
        self.control_frame.pack(fill=tk.X, pady=10)
        
        # New Game button
        self.new_game_button = ttk.Button(
            self.control_frame,
            text="New Game",
            command=self.new_game
        )
        self.new_game_button.pack(side=tk.LEFT, padx=10)
        
        # Quit button
        self.quit_button = ttk.Button(
            self.control_frame,
            text="Quit",
            command=self.quit_game
        )
        self.quit_button.pack(side=tk.RIGHT, padx=10)
        
        # Configure grid weights
        self.scorecard_frame.columnconfigure(0, weight=1)
        self.scorecard_frame.columnconfigure(1, weight=1)
        self.scorecard_frame.rowconfigure(0, weight=1)
    
    def show_welcome(self):
        """Show welcome screen and instructions."""
        welcome_window = tk.Toplevel(self.root)
        welcome_window.title("Welcome to Yahtzee")
        welcome_window.geometry("500x500")
        welcome_window.transient(self.root)
        welcome_window.grab_set()
        welcome_window.resizable(True, True)
        
        # Welcome title
        ttk.Label(
            welcome_window,
            text="Welcome to Yahtzee",
            font=("Helvetica", 18, "bold")
        ).pack(pady=20)
        
        # Instructions
        instructions_frame = ttk.Frame(welcome_window, padding=20)
        instructions_frame.pack(fill=tk.BOTH, expand=True)
        
        instructions = [
            "Yahtzee is a dice game where you roll 5 dice up to 3 times per turn.",
            "",
            "How to play:",
            "1. Click 'Roll Dice' to roll all five dice",
            "2. Click on dice you want to keep (they'll turn green)",
            "3. Roll again to reroll the dice you didn't keep",
            "4. After up to 3 rolls, you must choose a category to score in",
            "5. Each category can only be used once per game",
            "",
            "Scoring Categories:",
            "• Upper Section (Ones through Sixes):",
            "  Sum of the specified die value",
            "• Bonus: 35 points if upper section totals 63 or more",
            "",
            "• Three of a Kind: Sum of all dice if 3+ of one value",
            "• Four of a Kind: Sum of all dice if 4+ of one value",
            "• Full House: 25 points for 3 of one value and 2 of another",
            "• Small Straight: 30 points for 4 consecutive values",
            "• Large Straight: 40 points for 5 consecutive values",
            "• YAHTZEE: 50 points for 5 of the same value",
            "• Chance: Sum of all dice (can be used for any roll)",
            "• YAHTZEE Bonus: 100 points for each additional YAHTZEE",
            "",
            "The game consists of 13 rounds. Try to get the highest score!"
        ]
        
        for line in instructions:
            ttk.Label(
                instructions_frame,
                text=line,
                justify=tk.LEFT
            ).pack(anchor=tk.W, pady=1)
        
        # Start button
        ttk.Button(
            welcome_window,
            text="Start Game",
            command=welcome_window.destroy
        ).pack(pady=20)
    
    def toggle_die(self, index):
        """Toggle whether a die is kept or not."""
        if self.current_roll > 0 and not self.rolling and not self.game_over:
            self.dice_buttons[index].toggle_kept()
    
    def roll_dice(self):
        """Roll the dice, keeping any that are marked as kept."""
        if self.current_roll >= self.max_rolls or self.rolling or self.game_over:
            return
        
        self.rolling = True
        self.roll_button.config(state=tk.DISABLED)
        
        # Increment roll counter
        self.current_roll += 1
        self.roll_var.set(f"Roll: {self.current_roll}/3")
        
        # Animate dice rolling
        self.animate_roll(10)
    
    def animate_roll(self, remaining):
        """Animate the dice rolling with a decreasing interval."""
        if remaining <= 0:
            # Final roll
            for i in range(5):
                if not self.dice_buttons[i].kept:
                    self.dice[i] = random.randint(1, 6)
                    self.dice_buttons[i].value = self.dice[i]
                    self.dice_buttons[i].update_appearance()
            
            # Update possible scores
            self.update_possible_scores()
            
            # Check for Yahtzee bonus
            if self.dice.count(self.dice[0]) == 5 and self.scorecard.get("yahtzee") == 50:
                self.yahtzee_bonus_available = True
                messagebox.showinfo("YAHTZEE Bonus!", "You rolled another YAHTZEE! 100 bonus points!")
                self.scorecard["yahtzee_bonus"] = self.scorecard.get("yahtzee_bonus", 0) + 1
                self.yahtzee_bonus_var.set(str(self.scorecard["yahtzee_bonus"] * 100))
                self.update_total_score()
            
            # Enable roll button if not at max rolls
            if self.current_roll < self.max_rolls:
                self.roll_button.config(state=tk.NORMAL)
            
            self.rolling = False
            return
        
        # Randomly change non-kept dice
        for i in range(5):
            if not self.dice_buttons[i].kept:
                self.dice[i] = random.randint(1, 6)
                self.dice_buttons[i].value = self.dice[i]
                self.dice_buttons[i].update_appearance()
        
        # Schedule next animation frame with decreasing interval
        delay = 50 if remaining > 5 else 100
        self.root.after(delay, lambda: self.animate_roll(remaining - 1))
    
    def update_possible_scores(self):
        """Update the possible scores for each category."""
        possible_scores = calculate_possible_scores(self.dice)
        
        # Update upper section
        for key, button_info in self.upper_buttons.items():
            if key not in self.scorecard:
                score = possible_scores[key]
                button_info["var"].set(f"({score})")
                button_info["button"].config(state=tk.NORMAL)
            else:
                button_info["button"].config(state=tk.DISABLED)
        
        # Update lower section
        for key, button_info in self.lower_buttons.items():
            if key not in self.scorecard:
                score = possible_scores[key]
                button_info["var"].set(f"({score})")
                button_info["button"].config(state=tk.NORMAL)
            else:
                button_info["button"].config(state=tk.DISABLED)
    
    def score_category(self, category):
        """Score the current dice in the selected category."""
        if self.current_roll == 0 or category in self.scorecard or self.game_over:
            return
        
        # Calculate score for this category
        possible_scores = calculate_possible_scores(self.dice)
        score = possible_scores[category]
        
        # Update scorecard
        self.scorecard[category] = score
        
        # Update display
        if category in self.upper_buttons:
            self.upper_buttons[category]["var"].set(str(score))
            self.upper_buttons[category]["button"].config(state=tk.DISABLED)
        else:
            self.lower_buttons[category]["var"].set(str(score))
            self.lower_buttons[category]["button"].config(state=tk.DISABLED)
        
        # Update bonus and total
        self.update_bonus()
        self.update_total_score()
        
        # Reset for next turn
        self.reset_turn()
        
        # Check if game is over
        if len(self.scorecard) >= 13:  # All categories filled
            self.game_over = True
            self.roll_button.config(state=tk.DISABLED)
            messagebox.showinfo("Game Over", f"Game Over! Your final score is {self.total_var.get()}")
    
    def update_bonus(self):
        """Update the upper section bonus."""
        upper_categories = ["ones", "twos", "threes", "fours", "fives", "sixes"]
        upper_sum = sum(self.scorecard.get(key, 0) for key in upper_categories)
        
        # Check if all upper categories are filled
        if all(key in self.scorecard for key in upper_categories):
            bonus = 35 if upper_sum >= 63 else 0
            self.bonus_var.set(str(bonus))
    
    def update_total_score(self):
        """Update the total score display."""
        total = calculate_total_score(self.scorecard)
        self.total_var.set(str(total))
    
    def reset_turn(self):
        """Reset for the next turn."""
        # Reset dice
        for i in range(5):
            self.dice[i] = 1
            self.dice_buttons[i].value = 1
            self.dice_buttons[i].kept = False
            self.dice_buttons[i].update_appearance()
        
        # Reset roll counter
        self.current_roll = 0
        self.roll_var.set(f"Roll: {self.current_roll}/3")
        
        # Enable roll button
        self.roll_button.config(state=tk.NORMAL)
        
        # Clear possible scores
        for key, button_info in self.upper_buttons.items():
            if key not in self.scorecard:
                button_info["var"].set("")
                button_info["button"].config(state=tk.DISABLED)
        
        for key, button_info in self.lower_buttons.items():
            if key not in self.scorecard:
                button_info["var"].set("")
                button_info["button"].config(state=tk.DISABLED)
    
    def new_game(self):
        """Start a new game."""
        if self.game_over or messagebox.askyesno("New Game", "Are you sure you want to start a new game?"):
            # Reset game state
            self.scorecard = {}
            self.current_roll = 0
            self.yahtzee_bonus_available = False
            self.game_over = False
            
            # Reset display
            self.roll_var.set(f"Roll: {self.current_roll}/3")
            self.bonus_var.set("0")
            self.yahtzee_bonus_var.set("0")
            self.total_var.set("0")
            
            # Reset dice
            for i in range(5):
                self.dice[i] = 1
                self.dice_buttons[i].value = 1
                self.dice_buttons[i].kept = False
                self.dice_buttons[i].update_appearance()
            
            # Reset score buttons
            for key, button_info in self.upper_buttons.items():
                button_info["var"].set("")
                button_info["button"].config(state=tk.DISABLED)
            
            for key, button_info in self.lower_buttons.items():
                button_info["var"].set("")
                button_info["button"].config(state=tk.DISABLED)
            
            # Enable roll button
            self.roll_button.config(state=tk.NORMAL)
    
    def quit_game(self):
        """Quit the game."""
        if messagebox.askyesno("Quit", "Are you sure you want to quit the game?"):
            self.root.destroy()

def main():
    """Main function to start the GUI game."""
    root = tk.Tk()
    app = YahtzeeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 