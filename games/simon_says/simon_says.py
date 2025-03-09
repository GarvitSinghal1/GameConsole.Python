#!/usr/bin/env python3
import os
import sys
import time
import random
import colorama
from colorama import Fore, Back, Style

# Platform-specific imports
if os.name == 'nt':
    import msvcrt
else:
    import select
    import tty
    import termios

# Initialize colorama
colorama.init(autoreset=True)

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the game header."""
    print(f"{Back.BLUE}{Fore.WHITE}╔═══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Back.BLUE}{Fore.WHITE}║                     SIMON SAYS                               ║{Style.RESET_ALL}")
    print(f"{Back.BLUE}{Fore.WHITE}╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()

def print_buttons(highlighted=None):
    """Print the four colored buttons."""
    # Define the button colors and labels
    buttons = [
        (Fore.RED, "R", "RED"),
        (Fore.GREEN, "G", "GREEN"),
        (Fore.BLUE, "B", "BLUE"),
        (Fore.YELLOW, "Y", "YELLOW")
    ]
    
    # Print the top row (Red and Green)
    print("   ", end="")
    for i in range(2):
        color, key, name = buttons[i]
        if highlighted == key:
            print(f"{color}{Back.WHITE}  {key}: {name}  {Style.RESET_ALL}", end="   ")
        else:
            print(f"{color}  {key}: {name}  {Style.RESET_ALL}", end="   ")
    print()
    
    # Print the bottom row (Blue and Yellow)
    print("   ", end="")
    for i in range(2, 4):
        color, key, name = buttons[i]
        if highlighted == key:
            print(f"{color}{Back.WHITE}  {key}: {name}  {Style.RESET_ALL}", end="   ")
        else:
            print(f"{color}  {key}: {name}  {Style.RESET_ALL}", end="   ")
    print()
    print()

def get_key_press(timeout=None):
    """Get a single key press from the user with optional timeout."""
    if os.name == 'nt':
        # Windows implementation
        if timeout is None:
            # Wait indefinitely for a key press
            while True:
                if msvcrt.kbhit():
                    key = msvcrt.getch().decode('utf-8').upper()
                    return key
        else:
            # Wait for a key press with timeout
            start_time = time.time()
            while time.time() - start_time < timeout:
                if msvcrt.kbhit():
                    key = msvcrt.getch().decode('utf-8').upper()
                    return key
                time.sleep(0.01)
            return None
    else:
        # Unix/Linux/Mac implementation
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setcbreak(sys.stdin.fileno())
            if timeout is None:
                # Wait indefinitely for a key press
                key = sys.stdin.read(1).upper()
                return key
            else:
                # Wait for a key press with timeout
                rlist, _, _ = select.select([sys.stdin], [], [], timeout)
                if rlist:
                    key = sys.stdin.read(1).upper()
                    return key
                else:
                    return None
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

def play_sequence(sequence, speed=1.0):
    """Display the sequence to the player."""
    clear_screen()
    print_header()
    print(f"{Fore.CYAN}Watch the sequence...{Style.RESET_ALL}")
    print()
    
    # Base delay times in seconds
    display_time = 0.8 / speed
    pause_time = 0.3 / speed
    
    # Display each button in the sequence
    for button in sequence:
        print_buttons(button)
        time.sleep(display_time)
        print_buttons()
        time.sleep(pause_time)
    
    # Clear and show normal buttons
    clear_screen()
    print_header()
    print(f"{Fore.CYAN}Your turn! Repeat the sequence.{Style.RESET_ALL}")
    print()
    print_buttons()

def get_player_input(sequence_length, timeout=None):
    """Get the player's input sequence."""
    player_sequence = []
    
    for _ in range(sequence_length):
        # Wait for a valid key press
        while True:
            key = get_key_press(timeout)
            
            if key is None:  # Timeout
                return None
            
            if key in "RGBY":
                break
        
        # Show the pressed button
        clear_screen()
        print_header()
        print(f"{Fore.CYAN}Your turn! Repeat the sequence.{Style.RESET_ALL}")
        print()
        print_buttons(key)
        time.sleep(0.2)
        
        # Add to player sequence
        player_sequence.append(key)
        
        # Show normal buttons
        clear_screen()
        print_header()
        print(f"{Fore.CYAN}Your turn! Repeat the sequence.{Style.RESET_ALL}")
        print()
        print_buttons()
    
    return player_sequence

def show_instructions():
    """Display game instructions."""
    print(f"{Fore.CYAN}INSTRUCTIONS:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Simon Says is a memory game where you need to repeat")
    print(f"a growing sequence of colored buttons.{Style.RESET_ALL}")
    print()
    print(f"{Fore.WHITE}1. Watch the sequence of colors")
    print(f"2. Repeat the sequence by pressing the corresponding keys:")
    print(f"   - R for Red")
    print(f"   - G for Green")
    print(f"   - B for Blue")
    print(f"   - Y for Yellow")
    print(f"3. Each round adds one more color to the sequence")
    print(f"4. The game ends when you make a mistake or run out of time{Style.RESET_ALL}")
    print()
    print(f"{Fore.WHITE}Choose a difficulty level to adjust the speed and")
    print(f"response time allowed.{Style.RESET_ALL}")
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
        print(f"1. Easy (slow sequence, no time limit)")
        print(f"2. Medium (medium speed, 5 seconds per input)")
        print(f"3. Hard (fast sequence, 3 seconds per input)")
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
        
        # Set game parameters based on difficulty
        if choice == 1:  # Easy
            speed = 0.8
            timeout = None
        elif choice == 2:  # Medium
            speed = 1.0
            timeout = 5.0
        else:  # Hard
            speed = 1.5
            timeout = 3.0
        
        # Initialize game
        sequence = []
        score = 0
        game_over = False
        
        # Main game loop
        while not game_over:
            # Add a new random button to the sequence
            sequence.append(random.choice("RGBY"))
            
            # Display the current sequence
            play_sequence(sequence, speed)
            
            # Get player's input
            player_sequence = get_player_input(len(sequence), timeout)
            
            # Check if player timed out
            if player_sequence is None:
                clear_screen()
                print_header()
                print(f"{Fore.RED}Time's up! You took too long to respond.{Style.RESET_ALL}")
                game_over = True
                continue
            
            # Check if player's sequence matches
            if player_sequence != sequence:
                clear_screen()
                print_header()
                print(f"{Fore.RED}Wrong sequence! Game over.{Style.RESET_ALL}")
                game_over = True
                continue
            
            # Update score
            score = len(sequence)
            
            # Show success message
            clear_screen()
            print_header()
            print(f"{Fore.GREEN}Correct! Your score: {score}{Style.RESET_ALL}")
            print()
            print(f"{Fore.CYAN}Get ready for the next sequence...{Style.RESET_ALL}")
            time.sleep(1.5)
        
        # Game over
        print()
        print(f"{Fore.CYAN}Your final score: {score}{Style.RESET_ALL}")
        print()
        
        # Ask to play again
        play_again = input(f"{Fore.CYAN}Play again? (y/n): {Style.RESET_ALL}").lower()
        if play_again != 'y':
            clear_screen()
            print_header()
            print(f"{Fore.GREEN}Thanks for playing Simon Says!{Style.RESET_ALL}")
            time.sleep(1.5)
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print_header()
        print(f"{Fore.GREEN}Thanks for playing Simon Says!{Style.RESET_ALL}")
        sys.exit(0) 