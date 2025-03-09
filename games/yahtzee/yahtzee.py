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
    print(f"{Back.GREEN}{Fore.WHITE}╔═══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Back.GREEN}{Fore.WHITE}║                        YAHTZEE                               ║{Style.RESET_ALL}")
    print(f"{Back.GREEN}{Fore.WHITE}╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()

def print_dice(dice):
    """Print the current dice values."""
    dice_art = [
        ["┌───────┐", "│       │", "│   ●   │", "│       │", "└───────┘"],  # 1
        ["┌───────┐", "│ ●     │", "│       │", "│     ● │", "└───────┘"],  # 2
        ["┌───────┐", "│ ●     │", "│   ●   │", "│     ● │", "└───────┘"],  # 3
        ["┌───────┐", "│ ●   ● │", "│       │", "│ ●   ● │", "└───────┘"],  # 4
        ["┌───────┐", "│ ●   ● │", "│   ●   │", "│ ●   ● │", "└───────┘"],  # 5
        ["┌───────┐", "│ ●   ● │", "│ ●   ● │", "│ ●   ● │", "└───────┘"]   # 6
    ]
    
    # Print dice numbers
    print(f"{Fore.CYAN}   ", end="")
    for i in range(5):
        print(f"  Die {i+1}   ", end="")
    print(Style.RESET_ALL)
    
    # Print dice art
    for row in range(5):
        print(f"{Fore.CYAN}   ", end="")
        for die in dice:
            print(f"{dice_art[die-1][row]} ", end="")
        print(Style.RESET_ALL)
    
    print()

def print_scorecard(scorecard, possible_scores=None):
    """Print the current scorecard."""
    print(f"{Fore.YELLOW}╔═══════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}║                     SCORECARD                         ║{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}╠═══════════════════════════════════════════════════════╣{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}║ {Fore.WHITE}UPPER SECTION{Fore.YELLOW}                                         ║{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}╠═══════════════════════════════════════════════════════╣{Style.RESET_ALL}")
    
    # Upper section
    upper_categories = [
        ("Ones", "ones"),
        ("Twos", "twos"),
        ("Threes", "threes"),
        ("Fours", "fours"),
        ("Fives", "fives"),
        ("Sixes", "sixes")
    ]
    
    for name, key in upper_categories:
        score = scorecard.get(key, None)
        possible = possible_scores.get(key, None) if possible_scores else None
        
        if score is not None:
            print(f"{Fore.YELLOW}║ {Fore.WHITE}{name:<10} {Fore.CYAN}{score:>5}{Fore.YELLOW}                                  ║{Style.RESET_ALL}")
        elif possible is not None:
            print(f"{Fore.YELLOW}║ {Fore.WHITE}{name:<10} {Fore.GREEN}({possible:>3}){Fore.YELLOW}                                ║{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}║ {Fore.WHITE}{name:<10} {Fore.RED}(not filled){Fore.YELLOW}                           ║{Style.RESET_ALL}")
    
    # Upper section bonus
    upper_sum = sum(scorecard.get(key, 0) for _, key in upper_categories)
    bonus = 35 if upper_sum >= 63 else 0
    if all(scorecard.get(key, None) is not None for _, key in upper_categories):
        print(f"{Fore.YELLOW}╠═══════════════════════════════════════════════════════╣{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}║ {Fore.WHITE}Upper Section Sum: {Fore.CYAN}{upper_sum:>5}{Fore.YELLOW}                            ║{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}║ {Fore.WHITE}Bonus (63+ = 35): {Fore.CYAN}{bonus:>5}{Fore.YELLOW}                            ║{Style.RESET_ALL}")
    
    print(f"{Fore.YELLOW}╠═══════════════════════════════════════════════════════╣{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}║ {Fore.WHITE}LOWER SECTION{Fore.YELLOW}                                         ║{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}╠═══════════════════════════════════════════════════════╣{Style.RESET_ALL}")
    
    # Lower section
    lower_categories = [
        ("3 of a Kind", "three_of_a_kind"),
        ("4 of a Kind", "four_of_a_kind"),
        ("Full House", "full_house"),
        ("Sm. Straight", "small_straight"),
        ("Lg. Straight", "large_straight"),
        ("YAHTZEE", "yahtzee"),
        ("Chance", "chance")
    ]
    
    for name, key in lower_categories:
        score = scorecard.get(key, None)
        possible = possible_scores.get(key, None) if possible_scores else None
        
        if score is not None:
            print(f"{Fore.YELLOW}║ {Fore.WHITE}{name:<12} {Fore.CYAN}{score:>5}{Fore.YELLOW}                                ║{Style.RESET_ALL}")
        elif possible is not None:
            print(f"{Fore.YELLOW}║ {Fore.WHITE}{name:<12} {Fore.GREEN}({possible:>3}){Fore.YELLOW}                              ║{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}║ {Fore.WHITE}{name:<12} {Fore.RED}(not filled){Fore.YELLOW}                         ║{Style.RESET_ALL}")
    
    # Yahtzee bonus
    yahtzee_bonuses = scorecard.get("yahtzee_bonus", 0)
    if yahtzee_bonuses > 0:
        print(f"{Fore.YELLOW}║ {Fore.WHITE}YAHTZEE Bonus  {Fore.CYAN}{yahtzee_bonuses * 100:>5}{Fore.YELLOW}                                ║{Style.RESET_ALL}")
    
    # Total
    if len(scorecard) > 0:
        total = calculate_total_score(scorecard)
        print(f"{Fore.YELLOW}╠═══════════════════════════════════════════════════════╣{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}║ {Fore.WHITE}TOTAL SCORE    {Fore.CYAN}{total:>5}{Fore.YELLOW}                                ║{Style.RESET_ALL}")
    
    print(f"{Fore.YELLOW}╚═══════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()

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

def roll_dice(keep=None):
    """Roll the dice, keeping any that are specified."""
    if keep is None:
        keep = []
    
    dice = []
    for i in range(5):
        if i in keep:
            dice.append(keep[i])
        else:
            dice.append(random.randint(1, 6))
    
    return dice

def show_instructions():
    """Display game instructions."""
    print(f"{Fore.CYAN}INSTRUCTIONS:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Yahtzee is a dice game where you roll 5 dice up to 3 times per turn.")
    print(f"After each roll, you can choose which dice to keep and which to reroll.")
    print(f"After your rolls, you must choose a category to score in.")
    print(f"Each category can only be used once per game.{Style.RESET_ALL}")
    print()
    print(f"{Fore.CYAN}SCORING CATEGORIES:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Upper Section:")
    print(f" - Ones through Sixes: Sum of the specified die value")
    print(f" - Bonus: 35 points if upper section totals 63 or more")
    print()
    print(f"Lower Section:")
    print(f" - Three of a Kind: Sum of all dice if 3+ of one value")
    print(f" - Four of a Kind: Sum of all dice if 4+ of one value")
    print(f" - Full House: 25 points for 3 of one value and 2 of another")
    print(f" - Small Straight: 30 points for 4 consecutive values")
    print(f" - Large Straight: 40 points for 5 consecutive values")
    print(f" - YAHTZEE: 50 points for 5 of the same value")
    print(f" - Chance: Sum of all dice (can be used for any roll)")
    print(f" - YAHTZEE Bonus: 100 points for each additional YAHTZEE{Style.RESET_ALL}")
    print()
    input(f"{Fore.GREEN}Press Enter to start the game...{Style.RESET_ALL}")

def main():
    """Main game function."""
    clear_screen()
    print_header()
    show_instructions()
    
    while True:
        # Initialize game
        scorecard = {}
        yahtzee_bonus_available = False
        
        # Main game loop
        for _ in range(13):  # 13 rounds in a game of Yahtzee
            clear_screen()
            print_header()
            print(f"{Fore.CYAN}Round {len(scorecard) + 1}/13{Style.RESET_ALL}")
            print()
            
            # Print current scorecard
            print_scorecard(scorecard)
            
            # Roll dice up to 3 times
            dice = roll_dice()
            keep = []
            
            for roll in range(3):
                clear_screen()
                print_header()
                print(f"{Fore.CYAN}Round {len(scorecard) + 1}/13  |  Roll {roll + 1}/3{Style.RESET_ALL}")
                print()
                
                # Print current scorecard
                print_scorecard(scorecard)
                
                # Print current dice
                print_dice(dice)
                
                # If this is the third roll, break
                if roll == 2:
                    break
                
                # Ask which dice to keep
                print(f"{Fore.CYAN}Enter the numbers of the dice you want to keep (e.g., '125' to keep dice 1, 2, and 5)")
                print(f"Press Enter to reroll all dice, or 'q' to quit:{Style.RESET_ALL}")
                keep_input = input(f"{Fore.YELLOW}> {Style.RESET_ALL}").strip().lower()
                
                if keep_input == 'q':
                    clear_screen()
                    print_header()
                    print(f"{Fore.GREEN}Thanks for playing Yahtzee!{Style.RESET_ALL}")
                    time.sleep(1.5)
                    return
                
                # Parse which dice to keep
                keep = []
                for i, die in enumerate(dice):
                    if str(i + 1) in keep_input:
                        keep.append(die)
                    else:
                        keep.append(None)
                
                # Roll the dice again
                dice = []
                for i in range(5):
                    if keep[i] is not None:
                        dice.append(keep[i])
                    else:
                        dice.append(random.randint(1, 6))
            
            # Calculate possible scores
            possible_scores = calculate_possible_scores(dice)
            
            # Check for Yahtzee bonus
            if possible_scores["yahtzee"] == 50 and scorecard.get("yahtzee") == 50:
                yahtzee_bonus_available = True
            
            # Show possible scores
            clear_screen()
            print_header()
            print(f"{Fore.CYAN}Round {len(scorecard) + 1}/13  |  Choose a category to score{Style.RESET_ALL}")
            print()
            
            # Print current dice
            print_dice(dice)
            
            # Print scorecard with possible scores
            print_scorecard(scorecard, possible_scores)
            
            # Handle Yahtzee bonus
            if yahtzee_bonus_available:
                print(f"{Fore.GREEN}YAHTZEE BONUS! You rolled another YAHTZEE!{Style.RESET_ALL}")
                scorecard["yahtzee_bonus"] = scorecard.get("yahtzee_bonus", 0) + 1
                yahtzee_bonus_available = False
                print(f"{Fore.GREEN}You now have {scorecard['yahtzee_bonus']} YAHTZEE bonus(es) worth {scorecard['yahtzee_bonus'] * 100} points!{Style.RESET_ALL}")
                print()
                time.sleep(2)
            
            # Choose a category
            valid_categories = {
                "1": "ones",
                "2": "twos",
                "3": "threes",
                "4": "fours",
                "5": "fives",
                "6": "sixes",
                "7": "three_of_a_kind",
                "8": "four_of_a_kind",
                "9": "full_house",
                "10": "small_straight",
                "11": "large_straight",
                "12": "yahtzee",
                "13": "chance"
            }
            
            # Display category options
            print(f"{Fore.CYAN}Choose a category to score in:{Style.RESET_ALL}")
            print(f"{Fore.WHITE}Upper Section:")
            print(f"1. Ones")
            print(f"2. Twos")
            print(f"3. Threes")
            print(f"4. Fours")
            print(f"5. Fives")
            print(f"6. Sixes")
            print()
            print(f"Lower Section:")
            print(f"7. Three of a Kind")
            print(f"8. Four of a Kind")
            print(f"9. Full House")
            print(f"10. Small Straight")
            print(f"11. Large Straight")
            print(f"12. YAHTZEE")
            print(f"13. Chance{Style.RESET_ALL}")
            print()
            
            while True:
                choice = input(f"{Fore.YELLOW}Enter your choice (1-13): {Style.RESET_ALL}").strip()
                
                if choice in valid_categories:
                    category = valid_categories[choice]
                    
                    # Check if category is already filled
                    if category in scorecard:
                        print(f"{Fore.RED}That category is already filled. Please choose another.{Style.RESET_ALL}")
                        continue
                    
                    # Score the category
                    scorecard[category] = possible_scores[category]
                    break
                else:
                    print(f"{Fore.RED}Invalid choice. Please enter a number between 1 and 13.{Style.RESET_ALL}")
        
        # Game over
        clear_screen()
        print_header()
        print(f"{Fore.GREEN}Game Over!{Style.RESET_ALL}")
        print()
        
        # Print final scorecard
        print_scorecard(scorecard)
        
        # Print final score
        total_score = calculate_total_score(scorecard)
        print(f"{Fore.GREEN}Your final score is: {total_score}{Style.RESET_ALL}")
        print()
        
        # Ask to play again
        play_again = input(f"{Fore.CYAN}Play again? (y/n): {Style.RESET_ALL}").lower()
        if play_again != 'y':
            clear_screen()
            print_header()
            print(f"{Fore.GREEN}Thanks for playing Yahtzee!{Style.RESET_ALL}")
            time.sleep(1.5)
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print_header()
        print(f"{Fore.GREEN}Thanks for playing Yahtzee!{Style.RESET_ALL}")
        sys.exit(0) 