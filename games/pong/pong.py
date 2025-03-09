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
    print(f"{Back.GREEN}{Fore.WHITE}╔═══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Back.GREEN}{Fore.WHITE}║                        PONG                                  ║{Style.RESET_ALL}")
    print(f"{Back.GREEN}{Fore.WHITE}╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()

def is_key_pressed():
    """Check if a key has been pressed."""
    if os.name == 'nt':
        return msvcrt.kbhit()
    else:
        dr, dw, de = select.select([sys.stdin], [], [], 0)
        return dr != []

def get_key():
    """Get a single key press."""
    if os.name == 'nt':
        return msvcrt.getch().decode('utf-8').lower()
    else:
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setcbreak(sys.stdin.fileno())
            key = sys.stdin.read(1)
            return key.lower()
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

class Pong:
    def __init__(self, width=60, height=20):
        """Initialize the Pong game."""
        self.width = width
        self.height = height
        self.paddle_height = 4
        self.paddle_speed = 1
        self.ball_x = width // 2
        self.ball_y = height // 2
        self.ball_dx = random.choice([-1, 1])
        self.ball_dy = random.choice([-1, 1])
        self.left_paddle_y = height // 2 - self.paddle_height // 2
        self.right_paddle_y = height // 2 - self.paddle_height // 2
        self.left_score = 0
        self.right_score = 0
        self.game_over = False
        self.pause = False
        self.winner = None
        self.ai_difficulty = 0.7  # AI reaction probability (0.0 to 1.0)

    def move_left_paddle(self, direction):
        """Move the left paddle up or down."""
        if direction == "up" and self.left_paddle_y > 0:
            self.left_paddle_y -= self.paddle_speed
        elif direction == "down" and self.left_paddle_y < self.height - self.paddle_height:
            self.left_paddle_y += self.paddle_speed

    def move_right_paddle(self, direction):
        """Move the right paddle up or down."""
        if direction == "up" and self.right_paddle_y > 0:
            self.right_paddle_y -= self.paddle_speed
        elif direction == "down" and self.right_paddle_y < self.height - self.paddle_height:
            self.right_paddle_y += self.paddle_speed

    def update_ball(self):
        """Update the ball position and handle collisions."""
        if self.pause:
            return

        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        # Check collision with top and bottom walls
        if self.ball_y <= 0 or self.ball_y >= self.height - 1:
            self.ball_dy *= -1

        # Check collision with paddles
        if (self.ball_x == 1 and 
            self.left_paddle_y <= self.ball_y < self.left_paddle_y + self.paddle_height):
            self.ball_dx *= -1
            # Adjust angle based on where the ball hits the paddle
            hit_pos = self.ball_y - self.left_paddle_y
            if hit_pos < self.paddle_height // 3:
                self.ball_dy = -1
            elif hit_pos < 2 * self.paddle_height // 3:
                self.ball_dy = 0
            else:
                self.ball_dy = 1

        if (self.ball_x == self.width - 2 and 
            self.right_paddle_y <= self.ball_y < self.right_paddle_y + self.paddle_height):
            self.ball_dx *= -1
            # Adjust angle based on where the ball hits the paddle
            hit_pos = self.ball_y - self.right_paddle_y
            if hit_pos < self.paddle_height // 3:
                self.ball_dy = -1
            elif hit_pos < 2 * self.paddle_height // 3:
                self.ball_dy = 0
            else:
                self.ball_dy = 1

        # Check if ball is out of bounds (scored)
        if self.ball_x < 0:
            self.right_score += 1
            self.reset_ball()
        elif self.ball_x >= self.width:
            self.left_score += 1
            self.reset_ball()

        # Check win condition
        if self.left_score >= 5:
            self.game_over = True
            self.winner = "Player 1"
        elif self.right_score >= 5:
            self.game_over = True
            self.winner = "Player 2"

    def reset_ball(self):
        """Reset the ball to the center of the screen."""
        self.ball_x = self.width // 2
        self.ball_y = self.height // 2
        self.ball_dx = random.choice([-1, 1])
        self.ball_dy = random.choice([-1, 1])
        self.pause = True  # Pause briefly after a score

    def move_ai(self):
        """AI controller for the right paddle."""
        if random.random() < self.ai_difficulty:  # Simulate imperfect AI
            ball_target = self.ball_y
            # Predict where the ball will be at the right paddle
            if self.ball_dx > 0:  # Ball moving toward right paddle
                # Simple prediction
                steps = (self.width - 2) - self.ball_x
                predicted_y = self.ball_y + (self.ball_dy * steps)
                predicted_y = max(0, min(self.height - 1, predicted_y))
                ball_target = predicted_y

            paddle_center = self.right_paddle_y + self.paddle_height // 2
            if paddle_center < ball_target - 1:
                self.move_right_paddle("down")
            elif paddle_center > ball_target + 1:
                self.move_right_paddle("up")

    def draw(self):
        """Draw the game board."""
        # Create an empty board
        board = [[" " for _ in range(self.width)] for _ in range(self.height)]

        # Draw the paddles
        for i in range(self.paddle_height):
            if 0 <= self.left_paddle_y + i < self.height:
                board[self.left_paddle_y + i][0] = "█"
            if 0 <= self.right_paddle_y + i < self.height:
                board[self.right_paddle_y + i][self.width - 1] = "█"

        # Draw the ball
        if 0 <= self.ball_y < self.height and 0 <= self.ball_x < self.width:
            board[self.ball_y][self.ball_x] = "●"

        # Draw the center line
        for i in range(0, self.height, 2):
            board[i][self.width // 2] = "│"

        # Print the scores and the board
        print(f"{Fore.CYAN}Player 1: {self.left_score} {Fore.WHITE}|{Fore.CYAN} Player 2: {self.right_score}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}╔{'═' * self.width}╗{Style.RESET_ALL}")
        
        for row in board:
            print(f"{Fore.WHITE}║{Style.RESET_ALL}", end="")
            for cell in row:
                if cell == "█":  # Paddle
                    print(f"{Fore.GREEN}{cell}{Style.RESET_ALL}", end="")
                elif cell == "●":  # Ball
                    print(f"{Fore.YELLOW}{cell}{Style.RESET_ALL}", end="")
                elif cell == "│":  # Center line
                    print(f"{Fore.WHITE}{cell}{Style.RESET_ALL}", end="")
                else:
                    print(cell, end="")
            print(f"{Fore.WHITE}║{Style.RESET_ALL}")
        
        print(f"{Fore.WHITE}╚{'═' * self.width}╝{Style.RESET_ALL}")
        
        # Instructions
        print(f"{Fore.CYAN}Controls: [W/S] - Move left paddle, [P] - Pause, [Q] - Quit{Style.RESET_ALL}")
        
        if self.pause:
            print(f"{Fore.YELLOW}PAUSED - Press [Space] to continue{Style.RESET_ALL}")

def show_instructions():
    """Display game instructions."""
    print(f"{Fore.CYAN}INSTRUCTIONS:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Pong is a two-player table tennis game where players control")
    print(f"paddles to hit a ball back and forth.{Style.RESET_ALL}")
    print()
    print(f"{Fore.WHITE}Controls:")
    print(f" - Player 1 (Left): W (up), S (down)")
    print(f" - Player 2 (Right): AI-controlled")
    print(f" - P: Pause/Unpause the game")
    print(f" - Q: Quit the game{Style.RESET_ALL}")
    print()
    print(f"{Fore.WHITE}Scoring:")
    print(f" - Score a point by getting the ball past your opponent's paddle")
    print(f" - First player to reach 5 points wins{Style.RESET_ALL}")
    print()
    print(f"{Fore.WHITE}Tips:")
    print(f" - The ball will bounce at different angles depending on where it")
    print(f"   hits your paddle")
    print(f" - Use this to your advantage to outsmart your opponent{Style.RESET_ALL}")
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
        print(f"{Fore.CYAN}Choose AI difficulty:{Style.RESET_ALL}")
        print(f"1. Easy (slow AI)")
        print(f"2. Medium (moderate AI)")
        print(f"3. Hard (challenging AI)")
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
        
        # Set AI difficulty based on choice
        if choice == 1:  # Easy
            difficulty = 0.5
            paddle_height = 5
        elif choice == 2:  # Medium
            difficulty = 0.7
            paddle_height = 4
        else:  # Hard
            difficulty = 0.9
            paddle_height = 3
        
        # Initialize game
        game = Pong(width=60, height=20)
        game.ai_difficulty = difficulty
        game.paddle_height = paddle_height
        
        frame_time = 0.1  # seconds per frame
        unpause_time = 0
        
        # Game loop
        try:
            while not game.game_over:
                clear_screen()
                print_header()
                game.draw()
                
                # Handle input
                if is_key_pressed():
                    key = get_key()
                    if key == 'q':
                        raise KeyboardInterrupt
                    elif key == 'w':
                        game.move_left_paddle("up")
                    elif key == 's':
                        game.move_left_paddle("down")
                    elif key == 'p':
                        game.pause = not game.pause
                    elif key == ' ' and game.pause:
                        game.pause = False
                
                # Move AI paddle
                game.move_ai()
                
                # Update ball position
                if game.pause and time.time() > unpause_time:
                    game.pause = False
                
                game.update_ball()
                
                # Set unpause time if ball was reset
                if game.pause:
                    unpause_time = time.time() + 1.5
                
                time.sleep(frame_time)
            
            # Game over
            clear_screen()
            print_header()
            game.draw()
            if game.winner == "Player 1":
                print(f"{Fore.GREEN}Congratulations! You win!{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Game over! The AI wins.{Style.RESET_ALL}")
            
            print()
            play_again = input(f"{Fore.CYAN}Play again? (y/n): {Style.RESET_ALL}").lower()
            if play_again != 'y':
                break
        
        except KeyboardInterrupt:
            clear_screen()
            print_header()
            print(f"{Fore.GREEN}Game aborted.{Style.RESET_ALL}")
            time.sleep(1)
            break
    
    clear_screen()
    print_header()
    print(f"{Fore.GREEN}Thanks for playing Pong!{Style.RESET_ALL}")
    time.sleep(1.5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print_header()
        print(f"{Fore.GREEN}Thanks for playing Pong!{Style.RESET_ALL}")
        sys.exit(0) 