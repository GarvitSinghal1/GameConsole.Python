#!/usr/bin/env python3
import random
import os
import time
import colorama
from colorama import Fore, Back, Style

# Initialize colorama
colorama.init()

# Game choices
CHOICES = ["rock", "paper", "scissors"]

# ASCII art for choices
CHOICE_ART = {
    "rock": f"""
    {Fore.RED}    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
    {Style.RESET_ALL}""",
    "paper": f"""
    {Fore.GREEN}    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
    {Style.RESET_ALL}""",
    "scissors": f"""
    {Fore.BLUE}    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
    {Style.RESET_ALL}"""
}

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the game header."""
    print(f"{Back.YELLOW}{Fore.BLACK}╔═══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Back.YELLOW}{Fore.BLACK}║                   ROCK PAPER SCISSORS                         ║{Style.RESET_ALL}")
    print(f"{Back.YELLOW}{Fore.BLACK}╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()

def get_winner(player_choice, computer_choice):
    """Determine the winner of the game."""
    if player_choice == computer_choice:
        return "tie"
    
    if (player_choice == "rock" and computer_choice == "scissors") or \
       (player_choice == "paper" and computer_choice == "rock") or \
       (player_choice == "scissors" and computer_choice == "paper"):
        return "player"
    
    return "computer"

def main():
    """Main game function."""
    clear_screen()
    print_header()
    
    # Game rules
    print(f"{Fore.CYAN}Welcome to Rock Paper Scissors!{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Play against the computer by choosing rock, paper, or scissors.{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Rock crushes scissors, scissors cut paper, and paper covers rock.{Style.RESET_ALL}")
    print()
    
    player_score = 0
    computer_score = 0
    rounds_played = 0
    
    while True:
        # Get player's choice
        print(f"{Fore.YELLOW}Choose your move:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}1. Rock{Style.RESET_ALL}")
        print(f"{Fore.WHITE}2. Paper{Style.RESET_ALL}")
        print(f"{Fore.WHITE}3. Scissors{Style.RESET_ALL}")
        print(f"{Fore.WHITE}q. Quit{Style.RESET_ALL}")
        print()
        
        choice = input(f"{Fore.CYAN}Enter your choice (1-3 or q): {Style.RESET_ALL}").lower()
        
        if choice == 'q':
            break
        
        if choice in ['1', '2', '3']:
            index = int(choice) - 1
            player_choice = CHOICES[index]
        else:
            print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
            time.sleep(1)
            clear_screen()
            print_header()
            continue
        
        # Computer's choice
        computer_choice = random.choice(CHOICES)
        
        # Display choices
        clear_screen()
        print_header()
        
        print(f"{Fore.YELLOW}Round {rounds_played + 1}:{Style.RESET_ALL}")
        print()
        
        print(f"{Fore.GREEN}Your choice: {player_choice.upper()}{Style.RESET_ALL}")
        print(CHOICE_ART[player_choice])
        
        print(f"{Fore.RED}Computer's choice: {computer_choice.upper()}{Style.RESET_ALL}")
        print(CHOICE_ART[computer_choice])
        
        # Determine the winner
        winner = get_winner(player_choice, computer_choice)
        
        if winner == "player":
            player_score += 1
            print(f"{Fore.GREEN}You win this round!{Style.RESET_ALL}")
        elif winner == "computer":
            computer_score += 1
            print(f"{Fore.RED}Computer wins this round!{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}It's a tie!{Style.RESET_ALL}")
        
        rounds_played += 1
        
        # Display the score
        print()
        print(f"{Fore.CYAN}Score:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}You: {player_score}{Style.RESET_ALL}")
        print(f"{Fore.RED}Computer: {computer_score}{Style.RESET_ALL}")
        print()
        
        # Ask to play another round
        play_again = input(f"{Fore.CYAN}Play another round? (y/n): {Style.RESET_ALL}").lower()
        
        if not play_again.startswith('y'):
            break
        
        clear_screen()
        print_header()
    
    # Final results
    clear_screen()
    print_header()
    
    print(f"{Fore.CYAN}Game Over!{Style.RESET_ALL}")
    print()
    print(f"{Fore.YELLOW}Final Score:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}You: {player_score}{Style.RESET_ALL}")
    print(f"{Fore.RED}Computer: {computer_score}{Style.RESET_ALL}")
    print()
    
    if player_score > computer_score:
        print(f"{Fore.GREEN}Congratulations! You won the game!{Style.RESET_ALL}")
    elif computer_score > player_score:
        print(f"{Fore.RED}Better luck next time! The computer won the game.{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}It's a tie! What a close game!{Style.RESET_ALL}")
    
    print()
    input(f"{Fore.CYAN}Press Enter to finish...{Style.RESET_ALL}")

if __name__ == "__main__":
    main() 