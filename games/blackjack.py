#!/usr/bin/env python3
import os
import random
import time
import colorama
from colorama import Fore, Back, Style

# Initialize colorama
colorama.init()

# Card suits and values
SUITS = ["♥", "♦", "♣", "♠"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
VALUES = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
    "J": 10, "Q": 10, "K": 10, "A": 11
}

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the game header."""
    print(f"{Back.BLACK}{Fore.GREEN}╔═══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Back.BLACK}{Fore.GREEN}║                       BLACKJACK                               ║{Style.RESET_ALL}")
    print(f"{Back.BLACK}{Fore.GREEN}╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()

class Card:
    """Class to represent a playing card."""
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        
        # Color cards according to suit (red for hearts/diamonds, default for clubs/spades)
        if suit in ["♥", "♦"]:
            self.color = Fore.RED
        else:
            self.color = Fore.WHITE
    
    def __str__(self):
        return f"{self.color}{self.rank}{self.suit}{Style.RESET_ALL}"

class Deck:
    """Class to represent a deck of cards."""
    def __init__(self):
        self.cards = []
        self.build()
    
    def build(self):
        """Build a deck of 52 cards."""
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]
    
    def shuffle(self):
        """Shuffle the deck."""
        random.shuffle(self.cards)
    
    def deal(self):
        """Deal a card from the deck."""
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            # If deck is empty, rebuild and shuffle
            self.build()
            self.shuffle()
            return self.cards.pop()

class Hand:
    """Class to represent a hand of cards."""
    def __init__(self):
        self.cards = []
        self.value = 0
    
    def add_card(self, card):
        """Add a card to the hand."""
        self.cards.append(card)
        self.calculate_value()
    
    def calculate_value(self):
        """Calculate the value of the hand."""
        self.value = 0
        aces = 0
        
        for card in self.cards:
            self.value += VALUES[card.rank]
            if card.rank == "A":
                aces += 1
        
        # Adjust for aces if necessary
        while self.value > 21 and aces > 0:
            self.value -= 10  # Change Ace from 11 to 1
            aces -= 1

def display_hands(player_hand, dealer_hand, hide_dealer=True):
    """Display the player's and dealer's hands."""
    print(f"{Fore.CYAN}Dealer's Hand:{Style.RESET_ALL}")
    if hide_dealer:
        # Show only the first card of the dealer's hand
        print(f"  {dealer_hand.cards[0]} {Fore.BLUE}[?]{Style.RESET_ALL}")
        print(f"  Value: {Fore.YELLOW}?{Style.RESET_ALL}")
    else:
        # Show all cards in the dealer's hand
        for card in dealer_hand.cards:
            print(f"  {card}", end=" ")
        print()  # New line after cards
        print(f"  Value: {Fore.YELLOW}{dealer_hand.value}{Style.RESET_ALL}")
    
    print()
    print(f"{Fore.CYAN}Your Hand:{Style.RESET_ALL}")
    for card in player_hand.cards:
        print(f"  {card}", end=" ")
    print()  # New line after cards
    print(f"  Value: {Fore.YELLOW}{player_hand.value}{Style.RESET_ALL}")
    print()

def main():
    """Main game function."""
    clear_screen()
    print_header()
    
    # Game rules
    print(f"{Fore.CYAN}Welcome to Blackjack!{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Try to get as close to 21 as possible without going over.{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Number cards are worth their value, face cards are worth 10, and Aces are worth 11 or 1.{Style.RESET_ALL}")
    print(f"{Fore.WHITE}The dealer will hit until they have at least 17.{Style.RESET_ALL}")
    print()
    
    # Initialize the game
    deck = Deck()
    deck.shuffle()
    
    # Initialize player's balance
    balance = 1000
    
    # Game loop
    playing = True
    while playing and balance > 0:
        # Betting phase
        print(f"{Fore.GREEN}Your balance: ${balance}{Style.RESET_ALL}")
        bet = 0
        
        while True:
            try:
                bet_input = input(f"{Fore.YELLOW}Place your bet (10-{balance}): ${Style.RESET_ALL}")
                bet = int(bet_input)
                
                if 10 <= bet <= balance:
                    break
                else:
                    print(f"{Fore.RED}Please enter a bet between $10 and ${balance}.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
        
        # Dealing phase
        player_hand = Hand()
        dealer_hand = Hand()
        
        # Deal initial cards (2 each)
        player_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())
        player_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())
        
        clear_screen()
        print_header()
        print(f"{Fore.GREEN}Your bet: ${bet}{Style.RESET_ALL}")
        print()
        
        # Display initial hands (hide dealer's second card)
        display_hands(player_hand, dealer_hand, hide_dealer=True)
        
        # Check for natural blackjack
        if player_hand.value == 21:
            print(f"{Fore.GREEN}Blackjack! You win 1.5x your bet!{Style.RESET_ALL}")
            balance += int(bet * 1.5)
            time.sleep(2)
            clear_screen()
            print_header()
            continue
        
        # Player's turn
        while player_hand.value < 21:
            choice = input(f"{Fore.CYAN}Would you like to (H)it or (S)tand? {Style.RESET_ALL}").lower()
            
            if choice.startswith('h'):
                # Player hits (draws a card)
                player_hand.add_card(deck.deal())
                
                clear_screen()
                print_header()
                print(f"{Fore.GREEN}Your bet: ${bet}{Style.RESET_ALL}")
                print()
                display_hands(player_hand, dealer_hand, hide_dealer=True)
                
                if player_hand.value > 21:
                    print(f"{Fore.RED}Bust! You went over 21.{Style.RESET_ALL}")
                    balance -= bet
                    time.sleep(2)
                    break
            
            elif choice.startswith('s'):
                # Player stands (no more cards)
                break
            
            else:
                print(f"{Fore.RED}Invalid choice. Please enter H or S.{Style.RESET_ALL}")
        
        # Dealer's turn (if player hasn't bust)
        if player_hand.value <= 21:
            # Reveal dealer's hand
            clear_screen()
            print_header()
            print(f"{Fore.GREEN}Your bet: ${bet}{Style.RESET_ALL}")
            print()
            display_hands(player_hand, dealer_hand, hide_dealer=False)
            time.sleep(1)
            
            # Dealer hits until they have at least 17
            while dealer_hand.value < 17:
                print(f"{Fore.CYAN}Dealer hits...{Style.RESET_ALL}")
                time.sleep(1)
                dealer_hand.add_card(deck.deal())
                
                clear_screen()
                print_header()
                print(f"{Fore.GREEN}Your bet: ${bet}{Style.RESET_ALL}")
                print()
                display_hands(player_hand, dealer_hand, hide_dealer=False)
            
            # Determine the winner
            if dealer_hand.value > 21:
                print(f"{Fore.GREEN}Dealer busts! You win!{Style.RESET_ALL}")
                balance += bet
            elif dealer_hand.value > player_hand.value:
                print(f"{Fore.RED}Dealer wins.{Style.RESET_ALL}")
                balance -= bet
            elif dealer_hand.value < player_hand.value:
                print(f"{Fore.GREEN}You win!{Style.RESET_ALL}")
                balance += bet
            else:
                print(f"{Fore.YELLOW}Push! It's a tie.{Style.RESET_ALL}")
        
        # Check if player is out of money
        if balance <= 0:
            print(f"{Fore.RED}You're out of money! Game over.{Style.RESET_ALL}")
            break
        
        # Ask to play another round
        print()
        play_again = input(f"{Fore.CYAN}Would you like to play another round? (y/n): {Style.RESET_ALL}").lower()
        
        if not play_again.startswith('y'):
            playing = False
        
        clear_screen()
        print_header()
    
    # Game over
    print(f"{Fore.CYAN}Thanks for playing Blackjack!{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Final balance: ${balance}{Style.RESET_ALL}")
    
    # Ask to restart the game
    print()
    restart = input(f"{Fore.CYAN}Would you like to restart with a fresh balance? (y/n): {Style.RESET_ALL}").lower()
    
    if restart.startswith('y'):
        main()  # Restart the game

if __name__ == "__main__":
    main() 