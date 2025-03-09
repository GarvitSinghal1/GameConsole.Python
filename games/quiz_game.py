#!/usr/bin/env python3
import os
import random
import time
import colorama
from colorama import Fore, Back, Style

# Initialize colorama
colorama.init()

# Quiz questions
QUESTIONS = [
    {
        "question": "Which programming language was created by Guido van Rossum?",
        "options": ["Java", "Python", "C++", "JavaScript"],
        "answer": 1  # Python (0-indexed)
    },
    {
        "question": "What does CPU stand for?",
        "options": ["Central Processing Unit", "Computer Personal Unit", "Central Process Utility", "Central Processor Unifier"],
        "answer": 0  # Central Processing Unit
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Mars", "Jupiter", "Saturn"],
        "answer": 1  # Mars
    },
    {
        "question": "What is the largest ocean on Earth?",
        "options": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
        "answer": 3  # Pacific Ocean
    },
    {
        "question": "Which famous scientist developed the theory of relativity?",
        "options": ["Isaac Newton", "Albert Einstein", "Galileo Galilei", "Nikola Tesla"],
        "answer": 1  # Albert Einstein
    },
    {
        "question": "What is the main component of the Sun?",
        "options": ["Liquid Lava", "Molten Iron", "Hydrogen", "Oxygen"],
        "answer": 2  # Hydrogen
    },
    {
        "question": "Which language has the most native speakers in the world?",
        "options": ["English", "Spanish", "Hindi", "Mandarin Chinese"],
        "answer": 3  # Mandarin Chinese
    },
    {
        "question": "What's the capital city of Australia?",
        "options": ["Sydney", "Melbourne", "Canberra", "Perth"],
        "answer": 2  # Canberra
    },
    {
        "question": "What is the smallest prime number?",
        "options": ["0", "1", "2", "3"],
        "answer": 2  # 2
    },
    {
        "question": "Which data structure follows the Last In First Out (LIFO) principle?",
        "options": ["Queue", "Stack", "List", "Tree"],
        "answer": 1  # Stack
    },
    {
        "question": "Which of these is NOT a programming paradigm?",
        "options": ["Procedural", "Object-Oriented", "Functional", "Algorithmic"],
        "answer": 3  # Algorithmic
    },
    {
        "question": "Which of these is a valid Python data type?",
        "options": ["Integer", "String", "List", "All of the above"],
        "answer": 3  # All of the above
    },
    {
        "question": "What is the chemical symbol for gold?",
        "options": ["Go", "Gd", "Au", "Ag"],
        "answer": 2  # Au
    },
    {
        "question": "What is the largest mammal on Earth?",
        "options": ["Elephant", "Blue Whale", "Giraffe", "Polar Bear"],
        "answer": 1  # Blue Whale
    },
    {
        "question": "How many sides does a hexagon have?",
        "options": ["4", "6", "8", "10"],
        "answer": 1  # 6
    }
]

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the game header."""
    print(f"{Back.GREEN}{Fore.BLACK}╔═══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Back.GREEN}{Fore.BLACK}║                       QUIZ GAME                               ║{Style.RESET_ALL}")
    print(f"{Back.GREEN}{Fore.BLACK}╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()

def main():
    """Main game function."""
    clear_screen()
    print_header()
    
    # Game rules
    print(f"{Fore.CYAN}Welcome to the Quiz Game!{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Test your knowledge with these multiple-choice questions.{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Select the correct answer from the given options.{Style.RESET_ALL}")
    print()
    
    # Ask how many questions to answer
    while True:
        try:
            num_questions = input(f"{Fore.YELLOW}How many questions would you like to answer (1-15)? {Style.RESET_ALL}")
            num_questions = int(num_questions)
            if 1 <= num_questions <= 15:
                break
            else:
                print(f"{Fore.RED}Please enter a number between 1 and 15.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
    
    # Randomly select questions
    quiz_questions = random.sample(QUESTIONS, num_questions)
    
    # Start the quiz
    print()
    print(f"{Fore.GREEN}Let's begin!{Style.RESET_ALL}")
    time.sleep(1)
    
    score = 0
    
    for i, q in enumerate(quiz_questions, 1):
        clear_screen()
        print_header()
        
        print(f"{Fore.YELLOW}Question {i} of {num_questions}:{Style.RESET_ALL}")
        print()
        print(f"{Fore.WHITE}{q['question']}{Style.RESET_ALL}")
        print()
        
        # Display options
        for j, option in enumerate(q['options']):
            print(f"{Fore.CYAN}{j+1}. {option}{Style.RESET_ALL}")
        
        print()
        
        # Get player's answer
        while True:
            try:
                answer = input(f"{Fore.GREEN}Your answer (1-{len(q['options'])}): {Style.RESET_ALL}")
                answer = int(answer) - 1  # Convert to 0-indexed
                
                if 0 <= answer < len(q['options']):
                    break
                else:
                    print(f"{Fore.RED}Please enter a number between 1 and {len(q['options'])}.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
        
        # Check the answer
        if answer == q['answer']:
            score += 1
            print()
            print(f"{Fore.GREEN}Correct! Well done!{Style.RESET_ALL}")
        else:
            print()
            print(f"{Fore.RED}Sorry, that's incorrect.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}The correct answer is: {q['options'][q['answer']]}{Style.RESET_ALL}")
        
        time.sleep(2)
    
    # Final score
    clear_screen()
    print_header()
    
    print(f"{Fore.CYAN}Quiz Complete!{Style.RESET_ALL}")
    print()
    print(f"{Fore.YELLOW}Your final score: {score}/{num_questions}{Style.RESET_ALL}")
    print()
    
    # Performance feedback
    percentage = (score / num_questions) * 100
    
    if percentage == 100:
        print(f"{Fore.GREEN}Perfect score! Excellent work!{Style.RESET_ALL}")
    elif percentage >= 80:
        print(f"{Fore.GREEN}Great job! You know your stuff!{Style.RESET_ALL}")
    elif percentage >= 60:
        print(f"{Fore.YELLOW}Good effort! Keep learning!{Style.RESET_ALL}")
    elif percentage >= 40:
        print(f"{Fore.YELLOW}Not bad, but there's room for improvement.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Better luck next time! Try again to improve your score.{Style.RESET_ALL}")
    
    # Ask to play again
    print()
    play_again = input(f"{Fore.CYAN}Would you like to play again? (y/n): {Style.RESET_ALL}").lower()
    
    if play_again.startswith('y'):
        main()  # Restart the game

if __name__ == "__main__":
    main() 