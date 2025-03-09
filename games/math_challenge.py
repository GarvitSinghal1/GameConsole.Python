#!/usr/bin/env python3
import os
import random
import time
import colorama
from colorama import Fore, Back, Style

# Initialize colorama
colorama.init()

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the game header."""
    print(f"{Back.RED}{Fore.WHITE}╔═══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Back.RED}{Fore.WHITE}║                    MATH CHALLENGE                             ║{Style.RESET_ALL}")
    print(f"{Back.RED}{Fore.WHITE}╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()

def generate_problem(level):
    """Generate a math problem based on the difficulty level."""
    if level == 1:  # Easy: Addition and subtraction with small numbers
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        op = random.choice(['+', '-'])
        
        if op == '+':
            result = a + b
            problem = f"{a} + {b}"
        else:
            # Ensure the result is positive
            if a < b:
                a, b = b, a
            result = a - b
            problem = f"{a} - {b}"
    
    elif level == 2:  # Medium: Addition, subtraction, and multiplication
        a = random.randint(5, 30)
        b = random.randint(5, 15)
        op = random.choice(['+', '-', '*'])
        
        if op == '+':
            result = a + b
            problem = f"{a} + {b}"
        elif op == '-':
            # Ensure the result is positive
            if a < b:
                a, b = b, a
            result = a - b
            problem = f"{a} - {b}"
        else:
            result = a * b
            problem = f"{a} × {b}"
    
    elif level == 3:  # Hard: All operations including division
        op = random.choice(['+', '-', '*', '/'])
        
        if op == '+':
            a = random.randint(20, 100)
            b = random.randint(20, 100)
            result = a + b
            problem = f"{a} + {b}"
        elif op == '-':
            a = random.randint(20, 100)
            b = random.randint(1, a)  # Ensure result is positive
            result = a - b
            problem = f"{a} - {b}"
        elif op == '*':
            a = random.randint(5, 20)
            b = random.randint(5, 20)
            result = a * b
            problem = f"{a} × {b}"
        else:  # Division with integer result
            b = random.randint(2, 12)
            a = b * random.randint(1, 10)  # Ensure clean division
            result = a // b
            problem = f"{a} ÷ {b}"
    
    else:  # Very Hard: Multi-step problems
        op1 = random.choice(['+', '-', '*'])
        op2 = random.choice(['+', '-', '*'])
        
        a = random.randint(5, 20)
        b = random.randint(5, 20)
        c = random.randint(5, 20)
        
        # Format the problem with appropriate operators
        if op1 == '+':
            if op2 == '+':
                result = a + b + c
                problem = f"{a} + {b} + {c}"
            elif op2 == '-':
                result = a + b - c
                problem = f"{a} + {b} - {c}"
            else:  # op2 == '*'
                result = a + (b * c)
                problem = f"{a} + ({b} × {c})"
        elif op1 == '-':
            if op2 == '+':
                result = a - b + c
                problem = f"{a} - {b} + {c}"
            elif op2 == '-':
                result = a - b - c
                problem = f"{a} - {b} - {c}"
            else:  # op2 == '*'
                result = a - (b * c)
                problem = f"{a} - ({b} × {c})"
        else:  # op1 == '*'
            if op2 == '+':
                result = a * b + c
                problem = f"{a} × {b} + {c}"
            elif op2 == '-':
                result = a * b - c
                problem = f"{a} × {b} - {c}"
            else:  # op2 == '*'
                result = a * b * c
                problem = f"{a} × {b} × {c}"
    
    return problem, result

def main():
    """Main game function."""
    clear_screen()
    print_header()
    
    # Game rules
    print(f"{Fore.CYAN}Welcome to Math Challenge!{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Test your math skills with problems of increasing difficulty.{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Answer quickly to earn more points!{Style.RESET_ALL}")
    print()
    
    # Choose difficulty level
    print(f"{Fore.YELLOW}Choose a difficulty level:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}1. Easy (Addition and Subtraction){Style.RESET_ALL}")
    print(f"{Fore.YELLOW}2. Medium (Addition, Subtraction, and Multiplication){Style.RESET_ALL}")
    print(f"{Fore.RED}3. Hard (All operations including Division){Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}4. Very Hard (Multi-step problems){Style.RESET_ALL}")
    print()
    
    # Get difficulty level
    while True:
        try:
            level = int(input(f"{Fore.CYAN}Select level (1-4): {Style.RESET_ALL}"))
            if 1 <= level <= 4:
                break
            else:
                print(f"{Fore.RED}Please enter a number between 1 and 4.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
    
    # Number of questions
    while True:
        try:
            num_questions = int(input(f"{Fore.CYAN}How many questions would you like (5-20)? {Style.RESET_ALL}"))
            if 5 <= num_questions <= 20:
                break
            else:
                print(f"{Fore.RED}Please enter a number between 5 and 20.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
    
    print()
    print(f"{Fore.GREEN}Get ready!{Style.RESET_ALL}")
    time.sleep(1)
    
    # Game variables
    score = 0
    total_time = 0
    
    # Main game loop
    for i in range(1, num_questions + 1):
        clear_screen()
        print_header()
        
        print(f"{Fore.YELLOW}Question {i} of {num_questions}{Style.RESET_ALL}")
        print()
        
        # Generate a problem
        problem, answer = generate_problem(level)
        
        # Display the problem
        print(f"{Fore.WHITE}What is {problem}?{Style.RESET_ALL}")
        
        # Time the response
        start_time = time.time()
        
        # Get the player's answer
        try:
            user_answer = int(input(f"{Fore.GREEN}Your answer: {Style.RESET_ALL}"))
            end_time = time.time()
            response_time = end_time - start_time
        except ValueError:
            print(f"{Fore.RED}That's not a valid number.{Style.RESET_ALL}")
            user_answer = None
            response_time = 15  # Penalty for invalid input
        
        # Calculate points (faster answers get more points)
        if user_answer == answer:
            # Points calculation: base points for the level + speed bonus
            base_points = level * 10
            speed_factor = max(0, 10 - response_time)  # Time bonus decreases as time increases
            points = int(base_points + (speed_factor * level))
            
            score += points
            total_time += response_time
            
            print()
            print(f"{Fore.GREEN}Correct! +{points} points{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Time: {response_time:.2f} seconds{Style.RESET_ALL}")
        else:
            print()
            print(f"{Fore.RED}Incorrect. The correct answer is {answer}.{Style.RESET_ALL}")
        
        time.sleep(2)
    
    # Game over - Show final results
    clear_screen()
    print_header()
    
    print(f"{Fore.CYAN}Game Over!{Style.RESET_ALL}")
    print()
    print(f"{Fore.YELLOW}Final Score: {score} points{Style.RESET_ALL}")
    
    if num_questions > 0:
        avg_time = total_time / num_questions
        print(f"{Fore.YELLOW}Average Time: {avg_time:.2f} seconds per question{Style.RESET_ALL}")
    
    # Performance evaluation
    print()
    if score == 0:
        print(f"{Fore.RED}Keep practicing. You'll improve!{Style.RESET_ALL}")
    elif score < level * num_questions * 5:
        print(f"{Fore.YELLOW}Good effort! You're getting there.{Style.RESET_ALL}")
    elif score < level * num_questions * 10:
        print(f"{Fore.GREEN}Great job! You have solid math skills.{Style.RESET_ALL}")
    else:
        print(f"{Fore.MAGENTA}Outstanding! You're a math wizard!{Style.RESET_ALL}")
    
    # Ask to play again
    print()
    play_again = input(f"{Fore.CYAN}Would you like to play again? (y/n): {Style.RESET_ALL}").lower()
    
    if play_again.startswith('y'):
        main()  # Restart the game

if __name__ == "__main__":
    main() 