#!/usr/bin/env python3
import os
import random
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# Import classes from terminal version
from games.blackjack import Card, Deck, Hand, VALUES

class BlackjackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack")
        self.root.geometry("800x700")
        self.root.configure(bg="#003300")  # Dark green background like a casino table
        self.root.resizable(True, True)
        
        # Set minimum window size
        self.root.minsize(700, 600)
        
        # Game variables
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.balance = 1000
        self.bet = 0
        self.game_in_progress = False
        self.player_turn = False
        
        # Card images
        self.card_images = {}
        self.card_back_image = None
        self.load_card_images()
        
        # Create UI elements
        self.create_widgets()
        
        # Show welcome screen
        self.show_welcome()
    
    def load_card_images(self):
        """Create simple card images using PIL since we can't load from files."""
        # Colors
        card_colors = {
            "♥": "#FF0000",  # Red for hearts
            "♦": "#FF0000",  # Red for diamonds
            "♣": "#000000",  # Black for clubs
            "♠": "#000000"   # Black for spades
        }
        
        # Create card images
        for suit in ["♥", "♦", "♣", "♠"]:
            for rank in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]:
                # Create a blank image
                img = Image.new('RGB', (100, 140), "#FFFFFF")
                
                # Create a PhotoImage from it
                photo = ImageTk.PhotoImage(img)
                
                # Store the image
                self.card_images[(rank, suit)] = photo
        
        # Create card back image (simple red background)
        back_img = Image.new('RGB', (100, 140), "#880000")
        self.card_back_image = ImageTk.PhotoImage(back_img)
    
    def create_widgets(self):
        """Create the GUI widgets."""
        # Main frame
        main_frame = tk.Frame(self.root, bg="#003300")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title label
        self.title_label = tk.Label(
            main_frame, 
            text="Blackjack", 
            font=("Helvetica", 24, "bold"),
            bg="#003300",
            fg="#FFFFFF"
        )
        self.title_label.pack(pady=(0, 10))
        
        # Balance display
        self.balance_label = tk.Label(
            main_frame,
            text=f"Balance: ${self.balance}",
            font=("Helvetica", 16),
            bg="#003300",
            fg="#CCFF99"  # Green
        )
        self.balance_label.pack(pady=5)
        
        # Dealer area
        dealer_frame = tk.Frame(main_frame, bg="#004400", relief=tk.RIDGE, bd=2)
        dealer_frame.pack(fill=tk.X, padx=5, pady=5)
        
        dealer_label = tk.Label(
            dealer_frame,
            text="Dealer",
            font=("Helvetica", 14, "bold"),
            bg="#004400",
            fg="#FFFFFF"
        )
        dealer_label.pack(pady=5)
        
        # Frame to hold dealer's cards
        self.dealer_cards_frame = tk.Frame(dealer_frame, bg="#004400")
        self.dealer_cards_frame.pack(pady=5)
        
        # Dealer hand value display
        self.dealer_value_label = tk.Label(
            dealer_frame,
            text="Value: ??",
            font=("Helvetica", 12),
            bg="#004400",
            fg="#FFFFFF"
        )
        self.dealer_value_label.pack(pady=5)
        
        # Message display
        self.message_label = tk.Label(
            main_frame,
            text="",
            font=("Helvetica", 16, "bold"),
            bg="#003300",
            fg="#FFFFFF"
        )
        self.message_label.pack(pady=10)
        
        # Player area
        player_frame = tk.Frame(main_frame, bg="#004400", relief=tk.RIDGE, bd=2)
        player_frame.pack(fill=tk.X, padx=5, pady=5)
        
        player_label = tk.Label(
            player_frame,
            text="Player",
            font=("Helvetica", 14, "bold"),
            bg="#004400",
            fg="#FFFFFF"
        )
        player_label.pack(pady=5)
        
        # Frame to hold player's cards
        self.player_cards_frame = tk.Frame(player_frame, bg="#004400")
        self.player_cards_frame.pack(pady=5)
        
        # Player hand value display
        self.player_value_label = tk.Label(
            player_frame,
            text="Value: 0",
            font=("Helvetica", 12),
            bg="#004400",
            fg="#FFFFFF"
        )
        self.player_value_label.pack(pady=5)
        
        # Betting controls frame
        self.betting_frame = tk.Frame(main_frame, bg="#003300")
        self.betting_frame.pack(pady=10)
        
        # Bet display
        self.bet_label = tk.Label(
            self.betting_frame,
            text="Bet: $0",
            font=("Helvetica", 14),
            bg="#003300",
            fg="#FFFFFF"
        )
        self.bet_label.pack(side=tk.LEFT, padx=10)
        
        # Bet amount entry
        bet_frame = tk.Frame(self.betting_frame, bg="#003300")
        bet_frame.pack(side=tk.LEFT, padx=10)
        
        bet_amount_label = tk.Label(
            bet_frame,
            text="Bet Amount: $",
            font=("Helvetica", 12),
            bg="#003300",
            fg="#FFFFFF"
        )
        bet_amount_label.pack(side=tk.LEFT)
        
        # Validate bet amount (only numbers)
        vcmd = (self.root.register(self.validate_bet), '%P')
        
        self.bet_entry = tk.Entry(
            bet_frame,
            font=("Helvetica", 12),
            width=5,
            bg="#111111",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
            validate="key",
            validatecommand=vcmd
        )
        self.bet_entry.pack(side=tk.LEFT, padx=5)
        
        # Place bet button
        self.place_bet_button = tk.Button(
            self.betting_frame,
            text="Place Bet",
            command=self.place_bet,
            bg="#CCFF99",  # Green
            fg="#000000",
            activebackground="#99CC66",
            activeforeground="#000000",
            font=("Helvetica", 12),
            width=10
        )
        self.place_bet_button.pack(side=tk.LEFT, padx=10)
        
        # Game controls frame
        self.controls_frame = tk.Frame(main_frame, bg="#003300")
        self.controls_frame.pack(pady=10)
        
        # Hit button
        self.hit_button = tk.Button(
            self.controls_frame,
            text="Hit",
            command=self.hit,
            bg="#66CCFF",  # Blue
            fg="#000000",
            activebackground="#3399CC",
            activeforeground="#000000",
            font=("Helvetica", 14, "bold"),
            width=8,
            state=tk.DISABLED
        )
        self.hit_button.pack(side=tk.LEFT, padx=5)
        
        # Stand button
        self.stand_button = tk.Button(
            self.controls_frame,
            text="Stand",
            command=self.stand,
            bg="#FF9999",  # Red
            fg="#000000",
            activebackground="#CC6666",
            activeforeground="#000000",
            font=("Helvetica", 14, "bold"),
            width=8,
            state=tk.DISABLED
        )
        self.stand_button.pack(side=tk.LEFT, padx=5)
        
        # New game button
        self.new_game_button = tk.Button(
            self.controls_frame,
            text="New Game",
            command=self.new_game,
            bg="#444444",
            fg="#FFFFFF",
            activebackground="#666666",
            activeforeground="#FFFFFF",
            font=("Helvetica", 12),
            width=10,
            state=tk.DISABLED
        )
        self.new_game_button.pack(side=tk.LEFT, padx=20)
        
        # Quit button
        quit_button = tk.Button(
            main_frame,
            text="Quit",
            command=self.quit_game,
            bg="#663333",
            fg="#FFFFFF",
            activebackground="#993333",
            activeforeground="#FFFFFF",
            font=("Helvetica", 12),
            width=8
        )
        quit_button.pack(side=tk.BOTTOM, pady=10)
    
    def validate_bet(self, value):
        """Validate bet entry to ensure it only contains digits."""
        if value == "":
            return True
        try:
            bet_amount = int(value)
            return True
        except ValueError:
            return False
    
    def show_welcome(self):
        """Show welcome message and reset the UI."""
        # Clear any displayed cards
        for widget in self.dealer_cards_frame.winfo_children():
            widget.destroy()
        for widget in self.player_cards_frame.winfo_children():
            widget.destroy()
        
        # Reset labels
        self.dealer_value_label.config(text="Value: ??")
        self.player_value_label.config(text="Value: 0")
        self.bet_label.config(text="Bet: $0")
        self.bet = 0
        
        # Update balance
        self.balance_label.config(text=f"Balance: ${self.balance}")
        
        # Set welcome message
        self.message_label.config(
            text="Welcome to Blackjack! Place your bet to start.",
            fg="#FFFFFF"
        )
        
        # Enable betting controls
        self.bet_entry.config(state=tk.NORMAL)
        self.place_bet_button.config(state=tk.NORMAL)
        
        # Disable game controls
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.new_game_button.config(state=tk.DISABLED)
        
        # Reset game state
        self.game_in_progress = False
        self.player_turn = False
    
    def place_bet(self):
        """Process the player's bet and start a new round."""
        try:
            bet_amount = int(self.bet_entry.get())
            
            if bet_amount < 10:
                messagebox.showwarning("Invalid Bet", "Minimum bet is $10.")
                return
            
            if bet_amount > self.balance:
                messagebox.showwarning("Invalid Bet", f"You can't bet more than your balance (${self.balance}).")
                return
            
            # Set the bet
            self.bet = bet_amount
            self.bet_label.config(text=f"Bet: ${self.bet}")
            
            # Disable betting controls
            self.bet_entry.config(state=tk.DISABLED)
            self.place_bet_button.config(state=tk.DISABLED)
            
            # Start the game
            self.start_round()
        except ValueError:
            messagebox.showwarning("Invalid Bet", "Please enter a valid bet amount.")
    
    def start_round(self):
        """Start a new round of blackjack."""
        # Reset hands
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        
        # Clear any displayed cards
        for widget in self.dealer_cards_frame.winfo_children():
            widget.destroy()
        for widget in self.player_cards_frame.winfo_children():
            widget.destroy()
        
        # Shuffle the deck
        self.deck = Deck()
        self.deck.shuffle()
        
        # Deal initial cards
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())
        
        # Display cards
        self.display_dealer_cards(hide_hole_card=True)
        self.display_player_cards()
        
        # Update game state
        self.game_in_progress = True
        self.player_turn = True
        
        # Check for natural blackjack
        if self.player_hand.value == 21:
            self.player_turn = False
            
            # Check if dealer also has blackjack
            if self.dealer_hand.value == 21:
                self.message_label.config(
                    text="Both have Blackjack! Push (tie).",
                    fg="#FFFF99"  # Yellow
                )
                self.end_round("push")
            else:
                self.message_label.config(
                    text="Blackjack! You win 3:2!",
                    fg="#CCFF99"  # Green
                )
                self.end_round("blackjack")
        else:
            # Enable player controls
            self.hit_button.config(state=tk.NORMAL)
            self.stand_button.config(state=tk.NORMAL)
            
            self.message_label.config(
                text="Your turn. Hit or Stand?",
                fg="#FFFFFF"
            )
    
    def display_dealer_cards(self, hide_hole_card=False):
        """Display the dealer's cards."""
        # Clear previous cards
        for widget in self.dealer_cards_frame.winfo_children():
            widget.destroy()
        
        # Display cards
        for i, card in enumerate(self.dealer_hand.cards):
            # For the second card (hole card), show face down if hide_hole_card is True
            if i == 1 and hide_hole_card:
                card_image = self.card_back_image
            else:
                card_image = self.card_images.get((card.rank, card.suit), self.card_back_image)
            
            card_label = tk.Label(
                self.dealer_cards_frame,
                image=card_image,
                bg="#004400"
            )
            card_label.image = card_image  # Keep a reference to prevent garbage collection
            card_label.pack(side=tk.LEFT, padx=2)
        
        # Update dealer's hand value
        if hide_hole_card:
            # Only show the value of the first card
            first_card_value = VALUES[self.dealer_hand.cards[0].rank]
            self.dealer_value_label.config(text=f"Value: {first_card_value}+?")
        else:
            self.dealer_value_label.config(text=f"Value: {self.dealer_hand.value}")
    
    def display_player_cards(self):
        """Display the player's cards."""
        # Clear previous cards
        for widget in self.player_cards_frame.winfo_children():
            widget.destroy()
        
        # Display cards
        for card in self.player_hand.cards:
            card_image = self.card_images.get((card.rank, card.suit), self.card_back_image)
            
            card_label = tk.Label(
                self.player_cards_frame,
                image=card_image,
                bg="#004400"
            )
            card_label.image = card_image  # Keep a reference to prevent garbage collection
            card_label.pack(side=tk.LEFT, padx=2)
        
        # Update player's hand value
        self.player_value_label.config(text=f"Value: {self.player_hand.value}")
    
    def hit(self):
        """Player takes another card."""
        if not self.player_turn:
            return
        
        # Deal a card to the player
        self.player_hand.add_card(self.deck.deal())
        
        # Update display
        self.display_player_cards()
        
        # Check for bust or 21
        if self.player_hand.value > 21:
            self.player_turn = False
            self.message_label.config(
                text="Bust! You went over 21.",
                fg="#FF6666"  # Red
            )
            self.end_round("dealer")
        elif self.player_hand.value == 21:
            self.stand()  # Automatically stand on 21
    
    def stand(self):
        """Player stands (no more cards)."""
        if not self.player_turn:
            return
        
        # End player's turn
        self.player_turn = False
        
        # Disable player controls
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        
        # Reveal dealer's hole card
        self.display_dealer_cards(hide_hole_card=False)
        
        # Dealer's turn - dealer must hit until 17 or higher
        self.message_label.config(
            text="Dealer's turn...",
            fg="#FFFFFF"
        )
        
        # Schedule dealer's play with a slight delay for animation
        self.root.after(1000, self.dealer_play)
    
    def dealer_play(self):
        """Dealer takes cards until reaching at least 17."""
        # Check if dealer needs to take another card
        if self.dealer_hand.value < 17:
            # Deal a card to the dealer
            self.dealer_hand.add_card(self.deck.deal())
            
            # Update display
            self.display_dealer_cards(hide_hole_card=False)
            
            # Schedule next dealer action with a delay
            self.root.after(1000, self.dealer_play)
        else:
            # Dealer is done, determine the winner
            self.determine_winner()
    
    def determine_winner(self):
        """Determine the winner of the round."""
        dealer_value = self.dealer_hand.value
        player_value = self.player_hand.value
        
        # Dealer busts
        if dealer_value > 21:
            self.message_label.config(
                text="Dealer busts! You win!",
                fg="#CCFF99"  # Green
            )
            self.end_round("player")
        # Player has higher value
        elif player_value > dealer_value:
            self.message_label.config(
                text=f"You win with {player_value} vs dealer's {dealer_value}!",
                fg="#CCFF99"  # Green
            )
            self.end_round("player")
        # Dealer has higher value
        elif dealer_value > player_value:
            self.message_label.config(
                text=f"Dealer wins with {dealer_value} vs your {player_value}.",
                fg="#FF6666"  # Red
            )
            self.end_round("dealer")
        # Push (tie)
        else:
            self.message_label.config(
                text=f"Push! Both have {player_value}.",
                fg="#FFFF99"  # Yellow
            )
            self.end_round("push")
    
    def end_round(self, result):
        """End the current round and update the balance."""
        # Update balance based on result
        if result == "player":
            self.balance += self.bet
        elif result == "dealer":
            self.balance -= self.bet
        elif result == "blackjack":
            # Blackjack pays 3:2
            self.balance += int(self.bet * 1.5)
        # No change in balance for "push"
        
        # Update balance display
        self.balance_label.config(text=f"Balance: ${self.balance}")
        
        # Enable new game button
        self.new_game_button.config(state=tk.NORMAL)
        
        # Check if player is out of money
        if self.balance <= 0:
            messagebox.showinfo("Game Over", "You're out of money! Game over.")
            self.balance = 1000  # Reset balance for next game
            self.balance_label.config(text=f"Balance: ${self.balance}")
    
    def new_game(self):
        """Start a new game after a round has finished."""
        self.show_welcome()
    
    def quit_game(self):
        """Quit the game."""
        if messagebox.askyesno("Quit Game", "Are you sure you want to quit?"):
            self.root.destroy()

def main():
    """Main function to start the GUI game."""
    root = tk.Tk()
    app = BlackjackGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 