#!/usr/bin/env python3
import os
import random
import time
import msvcrt
import colorama
from colorama import Fore, Back, Style

# Initialize colorama
colorama.init()

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the game header."""
    print(f"{Back.GREEN}{Fore.BLACK}╔═══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Back.GREEN}{Fore.BLACK}║                         SNAKE                                 ║{Style.RESET_ALL}")
    print(f"{Back.GREEN}{Fore.BLACK}╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()

def is_key_pressed():
    """Check if a key is pressed (Windows only)."""
    return msvcrt.kbhit()

def get_key():
    """Get the pressed key (Windows only)."""
    if is_key_pressed():
        key = msvcrt.getch()
        return key
    return None

class Snake:
    """Snake game class."""
    def __init__(self, width=20, height=10):
        self.width = width
        self.height = height
        self.snake = [(width // 2, height // 2)]  # Snake starts in the middle
        self.direction = (1, 0)  # Initial direction: right
        self.food = self.new_food()
        self.score = 0
        self.game_over = False
        self.speed = 0.2  # Initial delay between moves in seconds
    
    def new_food(self):
        """Generate a new food position."""
        while True:
            food = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            if food not in self.snake:
                return food
    
    def change_direction(self, new_dir):
        """Change snake's direction."""
        # Prevent 180-degree turns
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.direction = new_dir
    
    def move(self):
        """Move the snake in the current direction."""
        if self.game_over:
            return
        
        # Calculate new head position
        head_x, head_y = self.snake[0]
        dir_x, dir_y = self.direction
        new_x = (head_x + dir_x) % self.width  # Wrap around the edges
        new_y = (head_y + dir_y) % self.height
        
        # Check if snake hits itself
        if (new_x, new_y) in self.snake:
            self.game_over = True
            return
        
        # Add new head
        self.snake.insert(0, (new_x, new_y))
        
        # Check if snake eats food
        if (new_x, new_y) == self.food:
            self.score += 1
            self.food = self.new_food()
            # Increase speed slightly
            self.speed = max(0.05, self.speed * 0.95)
        else:
            # Remove tail if no food eaten
            self.snake.pop()
    
    def draw(self):
        """Draw the game board."""
        clear_screen()
        print_header()
        print(f"{Fore.YELLOW}Score: {self.score}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Use WASD keys to move. Press Q to quit.{Style.RESET_ALL}")
        print()
        
        # Draw the game board
        print(f"{Fore.WHITE}╔{'═' * (self.width * 2)}╗{Style.RESET_ALL}")
        
        for y in range(self.height):
            print(f"{Fore.WHITE}║{Style.RESET_ALL}", end="")
            
            for x in range(self.width):
                if (x, y) == self.snake[0]:
                    # Snake head
                    print(f"{Back.GREEN}{Fore.WHITE}▓▓{Style.RESET_ALL}", end="")
                elif (x, y) in self.snake[1:]:
                    # Snake body
                    print(f"{Back.GREEN}  {Style.RESET_ALL}", end="")
                elif (x, y) == self.food:
                    # Food
                    print(f"{Back.RED}  {Style.RESET_ALL}", end="")
                else:
                    # Empty space
                    print("  ", end="")
            
            print(f"{Fore.WHITE}║{Style.RESET_ALL}")
        
        print(f"{Fore.WHITE}╚{'═' * (self.width * 2)}╝{Style.RESET_ALL}")
        
        if self.game_over:
            print()
            print(f"{Fore.RED}Game Over! Your final score: {self.score}{Style.RESET_ALL}")

def main():
    """Main game function."""
    clear_screen()
    print_header()
    
    # Game rules
    print(f"{Fore.CYAN}Welcome to Snake!{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Use the WASD keys to navigate the snake:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}  W - Up{Style.RESET_ALL}")
    print(f"{Fore.WHITE}  A - Left{Style.RESET_ALL}")
    print(f"{Fore.WHITE}  S - Down{Style.RESET_ALL}")
    print(f"{Fore.WHITE}  D - Right{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Collect the {Fore.RED}red{Style.RESET_ALL}{Fore.WHITE} food to grow longer.{Style.RESET_ALL}")
    print(f"{Fore.WHITE}The game ends if the snake runs into itself.{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Press Q at any time to quit the game.{Style.RESET_ALL}")
    print()
    
    # Choose difficulty (affects board size and initial speed)
    print(f"{Fore.YELLOW}Choose a difficulty level:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}1. Easy (Large board, slow speed){Style.RESET_ALL}")
    print(f"{Fore.YELLOW}2. Medium (Medium board, medium speed){Style.RESET_ALL}")
    print(f"{Fore.RED}3. Hard (Small board, fast speed){Style.RESET_ALL}")
    print()
    
    # Get difficulty level
    while True:
        try:
            level = int(input(f"{Fore.CYAN}Select level (1-3): {Style.RESET_ALL}"))
            if 1 <= level <= 3:
                break
            else:
                print(f"{Fore.RED}Please enter a number between 1 and 3.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
    
    # Set game parameters based on difficulty
    if level == 1:  # Easy
        game = Snake(width=30, height=15)
        game.speed = 0.2
    elif level == 2:  # Medium
        game = Snake(width=20, height=10)
        game.speed = 0.15
    else:  # Hard
        game = Snake(width=15, height=8)
        game.speed = 0.1
    
    print()
    print(f"{Fore.GREEN}Starting game in 3 seconds...{Style.RESET_ALL}")
    time.sleep(3)
    
    # Game loop
    last_move_time = time.time()
    
    while not game.game_over:
        # Draw the game
        game.draw()
        
        # Check for user input
        if is_key_pressed():
            key = get_key()
            
            if key == b'w':  # Up
                game.change_direction((0, -1))
            elif key == b's':  # Down
                game.change_direction((0, 1))
            elif key == b'a':  # Left
                game.change_direction((-1, 0))
            elif key == b'd':  # Right
                game.change_direction((1, 0))
            elif key == b'q':  # Quit
                game.game_over = True
                print(f"{Fore.YELLOW}Game exited by player.{Style.RESET_ALL}")
        
        # Move the snake at regular intervals
        current_time = time.time()
        if current_time - last_move_time > game.speed:
            game.move()
            last_move_time = current_time
        
        # Small delay to prevent excessive CPU usage
        time.sleep(0.05)
    
    # Final game state
    game.draw()
    
    # Ask to play again
    print()
    play_again = input(f"{Fore.CYAN}Would you like to play again? (y/n): {Style.RESET_ALL}").lower()
    
    if play_again.startswith('y'):
        main()  # Restart the game

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print_header()
        print(f"{Fore.YELLOW}Game interrupted by user.{Style.RESET_ALL}")
    finally:
        print(f"\n{Fore.CYAN}Thanks for playing Snake!{Style.RESET_ALL}") 