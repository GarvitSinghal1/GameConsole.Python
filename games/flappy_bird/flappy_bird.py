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
    print(f"{Back.GREEN}{Fore.WHITE}║                     FLAPPY BIRD                              ║{Style.RESET_ALL}")
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

class FlappyBird:
    def __init__(self, width=70, height=25):
        """Initialize the Flappy Bird game."""
        self.width = width
        self.height = height
        self.bird_x = width // 3
        self.bird_y = height // 2
        self.bird_velocity = 0
        self.gravity = 0.5
        self.flap_strength = -2.0
        self.pipes = []
        self.pipe_width = 10
        self.pipe_gap = 10
        self.pipe_spacing = 30
        self.score = 0
        self.game_over = False
        self.paused = False
        
        # Initialize pipes
        self.generate_pipes()
    
    def generate_pipes(self):
        """Generate initial set of pipes."""
        for i in range(3):  # Start with 3 pipes
            x = self.width + i * self.pipe_spacing
            self.add_pipe(x)
    
    def add_pipe(self, x):
        """Add a new pipe at position x."""
        gap_start = random.randint(5, self.height - self.pipe_gap - 5)
        gap_end = gap_start + self.pipe_gap
        self.pipes.append({
            'x': x,
            'gap_start': gap_start,
            'gap_end': gap_end,
            'passed': False
        })
    
    def update(self):
        """Update game state for one frame."""
        if self.paused or self.game_over:
            return
        
        # Update bird position
        self.bird_velocity += self.gravity
        self.bird_y += self.bird_velocity
        
        # Check if bird hits the ground or ceiling
        if self.bird_y < 0:
            self.bird_y = 0
            self.bird_velocity = 0
        elif self.bird_y >= self.height:
            self.bird_y = self.height - 1
            self.game_over = True
        
        # Update pipe positions and check for collisions
        pipe_to_remove = None
        for pipe in self.pipes:
            pipe['x'] -= 1
            
            # Check if bird passes pipe
            if not pipe['passed'] and pipe['x'] + self.pipe_width < self.bird_x:
                pipe['passed'] = True
                self.score += 1
            
            # Check if pipe is off screen
            if pipe['x'] + self.pipe_width < 0:
                pipe_to_remove = pipe
            
            # Check for collision with pipe
            if (self.bird_x + 1 >= pipe['x'] and self.bird_x <= pipe['x'] + self.pipe_width and
                (self.bird_y < pipe['gap_start'] or self.bird_y >= pipe['gap_end'])):
                self.game_over = True
        
        # Remove pipes that are off screen
        if pipe_to_remove:
            self.pipes.remove(pipe_to_remove)
            # Add a new pipe
            last_pipe = max(self.pipes, key=lambda p: p['x'])
            self.add_pipe(last_pipe['x'] + self.pipe_spacing)
    
    def flap(self):
        """Make the bird flap upward."""
        if not self.game_over and not self.paused:
            self.bird_velocity = self.flap_strength
    
    def draw(self):
        """Draw the game state."""
        # Create an empty board
        board = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        
        # Draw pipes
        for pipe in self.pipes:
            for y in range(self.height):
                if pipe['x'] < self.width:  # Only draw if pipe is on screen
                    if y < pipe['gap_start'] or y >= pipe['gap_end']:
                        for x in range(pipe['x'], min(pipe['x'] + self.pipe_width, self.width)):
                            board[y][x] = '█'
        
        # Draw bird
        bird_y = int(self.bird_y)
        if 0 <= bird_y < self.height:
            board[bird_y][self.bird_x] = '>'
        
        # Print score
        print(f"{Fore.YELLOW}Score: {self.score}{Style.RESET_ALL}")
        
        # Print the board with a border
        print(f"{Fore.CYAN}╔{'═' * self.width}╗{Style.RESET_ALL}")
        
        for row in board:
            print(f"{Fore.CYAN}║{Style.RESET_ALL}", end="")
            for cell in row:
                if cell == ' ':
                    print(" ", end="")
                elif cell == '>':
                    print(f"{Fore.YELLOW}>{Style.RESET_ALL}", end="")
                else:
                    print(f"{Fore.GREEN}{cell}{Style.RESET_ALL}", end="")
            print(f"{Fore.CYAN}║{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}╚{'═' * self.width}╝{Style.RESET_ALL}")
        
        # Game controls
        print(f"{Fore.WHITE}Press SPACE to flap, P to pause, Q to quit{Style.RESET_ALL}")
        
        if self.paused:
            print(f"{Fore.YELLOW}PAUSED - Press P to continue{Style.RESET_ALL}")
        
        if self.game_over:
            print(f"{Fore.RED}GAME OVER - Final Score: {self.score}{Style.RESET_ALL}")

def show_instructions():
    """Display game instructions."""
    print(f"{Fore.CYAN}INSTRUCTIONS:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Flappy Bird is a side-scrolling game where you control a bird,")
    print(f"attempting to fly through columns of pipes without hitting them.{Style.RESET_ALL}")
    print()
    print(f"{Fore.WHITE}Controls:")
    print(f" - SPACE: Make the bird flap upward")
    print(f" - P: Pause/Resume the game")
    print(f" - Q: Quit the game{Style.RESET_ALL}")
    print()
    print(f"{Fore.WHITE}Tips:")
    print(f" - The bird constantly falls due to gravity")
    print(f" - Press SPACE repeatedly to maintain altitude")
    print(f" - Timing is crucial to navigate through the pipe gaps")
    print(f" - Each pipe you pass gives you one point{Style.RESET_ALL}")
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
        print(f"1. Easy (large gaps, slow speed)")
        print(f"2. Medium (medium gaps, medium speed)")
        print(f"3. Hard (small gaps, fast speed)")
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
        
        # Initialize game with difficulty settings
        game = FlappyBird()
        
        if choice == 1:  # Easy
            game.pipe_gap = 12
            game.gravity = 0.4
            frame_time = 0.15  # Seconds per frame
        elif choice == 2:  # Medium
            game.pipe_gap = 10
            game.gravity = 0.5
            frame_time = 0.12
        else:  # Hard
            game.pipe_gap = 8
            game.gravity = 0.6
            frame_time = 0.1
        
        # Re-initialize pipes with new gap size
        game.pipes = []
        game.generate_pipes()
        
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
                    elif key == ' ':
                        game.flap()
                    elif key == 'p':
                        game.paused = not game.paused
                
                # Update game state
                game.update()
                
                time.sleep(frame_time)
            
            # Game over
            clear_screen()
            print_header()
            game.draw()
            
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
    print(f"{Fore.GREEN}Thanks for playing Flappy Bird!{Style.RESET_ALL}")
    time.sleep(1.5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print_header()
        print(f"{Fore.GREEN}Thanks for playing Flappy Bird!{Style.RESET_ALL}")
        sys.exit(0) 