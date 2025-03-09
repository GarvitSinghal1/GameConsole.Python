#!/usr/bin/env python3
import os
import random
import time
import tkinter as tk
from tkinter import ttk, messagebox

# Import functions from terminal version
from games.math_challenge import generate_problem

class MathChallengeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Challenge")
        self.root.geometry("600x500")
        self.root.configure(bg="#333333")
        self.root.resizable(True, True)
        
        # Set minimum window size
        self.root.minsize(500, 400)
        
        # Game variables
        self.level = 1
        self.num_questions = 10
        self.score = 0
        self.current_question = 0
        self.total_time = 0
        self.start_time = 0
        self.timer_running = False
        self.current_problem = None
        self.current_answer = None
        
        # Create UI elements
        self.create_widgets()
        
        # Show welcome screen
        self.show_welcome()
    
    def create_widgets(self):
        """Create the GUI widgets."""
        # Main frame
        main_frame = tk.Frame(self.root, bg="#333333")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title label
        self.title_label = tk.Label(
            main_frame, 
            text="Math Challenge", 
            font=("Helvetica", 24, "bold"),
            bg="#333333",
            fg="#FF6666"  # Red
        )
        self.title_label.pack(pady=(0, 10))
        
        # Game area frame
        self.game_frame = tk.Frame(main_frame, bg="#222222", relief=tk.RIDGE, bd=2)
        self.game_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Problem display
        self.problem_label = tk.Label(
            self.game_frame,
            text="",
            font=("Helvetica", 28, "bold"),
            bg="#222222",
            fg="#FFFFFF"
        )
        self.problem_label.pack(pady=30)
        
        # Answer entry frame
        answer_frame = tk.Frame(self.game_frame, bg="#222222")
        answer_frame.pack(pady=10)
        
        answer_label = tk.Label(
            answer_frame,
            text="Your answer:",
            font=("Helvetica", 14),
            bg="#222222",
            fg="#FFFFFF"
        )
        answer_label.pack(side=tk.LEFT, padx=5)
        
        # Only allow numbers to be entered
        vcmd = (self.root.register(self.validate_input), '%P')
        
        self.answer_entry = tk.Entry(
            answer_frame,
            font=("Helvetica", 14, "bold"),
            width=10,
            bg="#111111",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
            validate="key",
            validatecommand=vcmd
        )
        self.answer_entry.pack(side=tk.LEFT, padx=5)
        self.answer_entry.bind("<Return>", self.check_answer)
        
        # Submit button
        self.submit_button = tk.Button(
            answer_frame,
            text="Submit",
            command=self.check_answer,
            bg="#FF6666",  # Red
            fg="#FFFFFF",
            activebackground="#993333",
            activeforeground="#FFFFFF",
            font=("Helvetica", 12, "bold"),
            width=10
        )
        self.submit_button.pack(side=tk.LEFT, padx=10)
        
        # Feedback display
        self.feedback_label = tk.Label(
            self.game_frame,
            text="",
            font=("Helvetica", 14, "bold"),
            bg="#222222",
            fg="#FFFFFF"
        )
        self.feedback_label.pack(pady=20)
        
        # Progress and timer frame
        progress_frame = tk.Frame(self.game_frame, bg="#222222")
        progress_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Question progress
        self.progress_label = tk.Label(
            progress_frame,
            text="",
            font=("Helvetica", 12),
            bg="#222222",
            fg="#FFFF99"  # Yellow
        )
        self.progress_label.pack(side=tk.LEFT)
        
        # Timer display
        self.timer_label = tk.Label(
            progress_frame,
            text="",
            font=("Helvetica", 12),
            bg="#222222",
            fg="#66CCFF"  # Blue
        )
        self.timer_label.pack(side=tk.RIGHT)
        
        # Score display
        self.score_label = tk.Label(
            self.game_frame,
            text="Score: 0",
            font=("Helvetica", 14, "bold"),
            bg="#222222",
            fg="#CCFF99"  # Green
        )
        self.score_label.pack(pady=5)
        
        # Level indicator frame (used during setup)
        self.setup_frame = tk.Frame(self.game_frame, bg="#222222")
        
        # Control buttons frame
        control_frame = tk.Frame(main_frame, bg="#333333")
        control_frame.pack(fill=tk.X, pady=10)
        
        # New Game button
        self.new_game_button = tk.Button(
            control_frame,
            text="New Game",
            command=self.show_welcome,
            bg="#444444",
            fg="#FFFFFF",
            activebackground="#666666",
            activeforeground="#FFFFFF",
            font=("Helvetica", 12),
            width=10
        )
        self.new_game_button.pack(side=tk.LEFT, padx=5)
        
        # Quit button
        quit_button = tk.Button(
            control_frame,
            text="Quit",
            command=self.quit_game,
            bg="#663333",
            fg="#FFFFFF",
            activebackground="#993333",
            activeforeground="#FFFFFF",
            font=("Helvetica", 12),
            width=10
        )
        quit_button.pack(side=tk.RIGHT, padx=5)
    
    def validate_input(self, text):
        """Validate input to only allow numbers."""
        if text == "":
            return True
        try:
            int(text)
            return True
        except ValueError:
            return False
    
    def show_welcome(self):
        """Show the welcome screen with level selection."""
        # Clear problem and feedback
        self.problem_label.config(text="")
        self.feedback_label.config(text="")
        self.progress_label.config(text="")
        self.timer_label.config(text="")
        self.score_label.config(text="Score: 0")
        
        # Clear answer entry
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.config(state=tk.DISABLED)
        self.submit_button.config(state=tk.DISABLED)
        
        # Reset game variables
        self.score = 0
        self.current_question = 0
        self.total_time = 0
        
        # Stop any running timer
        self.timer_running = False
        
        # Clear previous setup widgets
        for widget in self.setup_frame.winfo_children():
            widget.destroy()
        
        # Show setup frame
        self.setup_frame.pack(pady=10)
        
        # Welcome message
        welcome_label = tk.Label(
            self.setup_frame,
            text="Welcome to Math Challenge!",
            font=("Helvetica", 18, "bold"),
            bg="#222222",
            fg="#FFFFFF"
        )
        welcome_label.pack(pady=10)
        
        instructions = tk.Label(
            self.setup_frame,
            text="Test your math skills with problems of increasing difficulty.\nAnswer quickly to earn more points!",
            font=("Helvetica", 12),
            bg="#222222",
            fg="#FFFFFF",
            justify=tk.CENTER
        )
        instructions.pack(pady=5)
        
        # Level selection
        level_frame = tk.Frame(self.setup_frame, bg="#222222")
        level_frame.pack(pady=15)
        
        level_label = tk.Label(
            level_frame,
            text="Choose difficulty level:",
            font=("Helvetica", 14),
            bg="#222222",
            fg="#FFFFFF"
        )
        level_label.pack(side=tk.LEFT, padx=10)
        
        self.level_var = tk.IntVar(value=1)
        
        # Create radio buttons for levels
        level_descriptions = [
            "Easy (Addition and Subtraction)",
            "Medium (Addition, Subtraction, and Multiplication)",
            "Hard (All operations including Division)",
            "Very Hard (Multi-step problems)"
        ]
        
        level_colors = ["#CCFF99", "#FFFF99", "#FF9999", "#FF99FF"]  # Green, Yellow, Red, Magenta
        
        for i, (desc, color) in enumerate(zip(level_descriptions, level_colors), 1):
            level_button = tk.Radiobutton(
                self.setup_frame,
                text=f"{i}. {desc}",
                variable=self.level_var,
                value=i,
                font=("Helvetica", 12),
                bg="#222222",
                fg=color,
                selectcolor="#333333",
                activebackground="#222222",
                activeforeground=color
            )
            level_button.pack(anchor=tk.W, padx=30, pady=3)
        
        # Number of questions selection
        questions_frame = tk.Frame(self.setup_frame, bg="#222222")
        questions_frame.pack(pady=15)
        
        questions_label = tk.Label(
            questions_frame,
            text="Number of questions:",
            font=("Helvetica", 14),
            bg="#222222",
            fg="#FFFFFF"
        )
        questions_label.pack(side=tk.LEFT, padx=10)
        
        self.questions_var = tk.IntVar(value=10)
        questions_slider = ttk.Scale(
            questions_frame,
            from_=5,
            to=20,
            orient=tk.HORIZONTAL,
            variable=self.questions_var,
            length=200,
            command=self.update_questions_label
        )
        questions_slider.pack(side=tk.LEFT, padx=10)
        
        self.questions_value_label = tk.Label(
            questions_frame,
            text="10",
            font=("Helvetica", 14),
            bg="#222222",
            fg="#FFFFFF",
            width=2
        )
        self.questions_value_label.pack(side=tk.LEFT, padx=5)
        
        # Start game button
        start_button = tk.Button(
            self.setup_frame,
            text="Start Challenge",
            command=self.start_game,
            bg="#FF6666",  # Red
            fg="#FFFFFF",
            activebackground="#993333",
            activeforeground="#FFFFFF",
            font=("Helvetica", 14, "bold"),
            width=15,
            height=2
        )
        start_button.pack(pady=20)
    
    def update_questions_label(self, *args):
        """Update the label showing number of questions."""
        value = int(float(self.questions_var.get()))
        self.questions_value_label.config(text=str(value))
    
    def start_game(self):
        """Start the game with selected settings."""
        # Get selected level and number of questions
        self.level = self.level_var.get()
        self.num_questions = int(self.questions_var.get())
        
        # Hide setup frame
        self.setup_frame.pack_forget()
        
        # Reset game variables
        self.score = 0
        self.current_question = 0
        self.total_time = 0
        
        # Update score display
        self.score_label.config(text="Score: 0")
        
        # Enable answer entry
        self.answer_entry.config(state=tk.NORMAL)
        self.submit_button.config(state=tk.NORMAL)
        self.answer_entry.focus_set()
        
        # Start the first question
        self.next_question()
    
    def next_question(self):
        """Present the next math problem."""
        if self.current_question >= self.num_questions:
            # End of game
            self.show_results()
            return
        
        # Clear answer entry
        self.answer_entry.delete(0, tk.END)
        
        # Generate a new problem
        self.current_problem, self.current_answer = generate_problem(self.level)
        
        # Update problem display
        self.problem_label.config(text=f"What is {self.current_problem}?")
        
        # Update progress display
        self.current_question += 1
        self.progress_label.config(text=f"Question {self.current_question} of {self.num_questions}")
        self.feedback_label.config(text="")
        
        # Start timer for this question
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()
        
        # Set focus to answer entry
        self.answer_entry.focus_set()
    
    def update_timer(self):
        """Update the timer display."""
        if self.timer_running:
            elapsed = time.time() - self.start_time
            self.timer_label.config(text=f"Time: {elapsed:.1f}s")
            self.root.after(100, self.update_timer)
    
    def check_answer(self, event=None):
        """Check the player's answer."""
        if not self.timer_running:
            return
        
        # Stop the timer
        self.timer_running = False
        response_time = time.time() - self.start_time
        self.total_time += response_time
        
        # Get player's answer
        try:
            user_answer = int(self.answer_entry.get())
        except ValueError:
            # Handle empty or invalid input
            self.feedback_label.config(text="Please enter a number!", fg="#FF6666")
            self.timer_running = True  # Restart timer
            return
        
        # Calculate points
        if user_answer == self.current_answer:
            # Correct answer - calculate points
            base_points = self.level * 10
            speed_factor = max(0, 10 - response_time)
            points = int(base_points + (speed_factor * self.level))
            
            self.score += points
            self.score_label.config(text=f"Score: {self.score}")
            
            # Show positive feedback
            self.feedback_label.config(
                text=f"Correct! +{points} points (Time: {response_time:.2f}s)",
                fg="#CCFF99"  # Green
            )
        else:
            # Incorrect answer
            self.feedback_label.config(
                text=f"Incorrect. The correct answer is {self.current_answer}.",
                fg="#FF6666"  # Red
            )
        
        # Schedule the next question
        self.root.after(2000, self.next_question)
    
    def show_results(self):
        """Show the final results."""
        # Clear the game area
        self.problem_label.config(text="Challenge Complete!")
        self.answer_entry.config(state=tk.DISABLED)
        self.submit_button.config(state=tk.DISABLED)
        self.timer_label.config(text="")
        self.progress_label.config(text="")
        
        # Calculate average time
        if self.num_questions > 0:
            avg_time = self.total_time / self.num_questions
            time_text = f"Average time: {avg_time:.2f}s per question"
        else:
            time_text = ""
        
        # Determine performance level
        if self.score == 0:
            feedback = "Keep practicing. You'll improve!"
            color = "#FF6666"  # Red
        elif self.score < self.level * self.num_questions * 5:
            feedback = "Good effort! You're getting there."
            color = "#FFFF99"  # Yellow
        elif self.score < self.level * self.num_questions * 10:
            feedback = "Great job! You have solid math skills."
            color = "#CCFF99"  # Green
        else:
            feedback = "Outstanding! You're a math wizard!"
            color = "#FF99FF"  # Magenta
        
        # Create results text
        results_text = f"Final Score: {self.score} points\n\n{time_text}\n\n{feedback}"
        
        # Show feedback
        self.feedback_label.config(text=results_text, fg=color)
    
    def quit_game(self):
        """Quit the game."""
        if messagebox.askyesno("Quit Game", "Are you sure you want to quit?"):
            self.root.destroy()

def main():
    """Main function to start the GUI game."""
    root = tk.Tk()
    
    # Configure style for progress bar
    style = ttk.Style()
    style.theme_use('default')
    style.configure("TScale", background="#222222", troughcolor="#111111")
    
    app = MathChallengeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 