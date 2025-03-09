#!/usr/bin/env python3
import os
import random
import time
import tkinter as tk
from tkinter import ttk, messagebox

# Import questions from terminal version
from games.quiz_game import QUESTIONS

class QuizGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Game")
        self.root.geometry("700x500")
        self.root.configure(bg="#333333")
        self.root.resizable(True, True)
        
        # Set minimum window size
        self.root.minsize(600, 450)
        
        # Game variables
        self.questions = []
        self.current_question = 0
        self.score = 0
        self.num_questions = 0
        self.selected_answer = tk.IntVar()
        self.question_in_progress = False
        self.timer_running = False
        self.start_time = 0
        
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
            text="Quiz Game", 
            font=("Helvetica", 24, "bold"),
            bg="#333333",
            fg="#66CCFF"  # Blue
        )
        self.title_label.pack(pady=(0, 10))
        
        # Game area frame
        self.game_frame = tk.Frame(main_frame, bg="#222222", relief=tk.RIDGE, bd=2)
        self.game_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Question display
        self.question_label = tk.Label(
            self.game_frame,
            text="",
            font=("Helvetica", 14, "bold"),
            bg="#222222",
            fg="#FFFFFF",
            wraplength=580,
            justify=tk.LEFT
        )
        self.question_label.pack(pady=15, padx=10, anchor=tk.W)
        
        # Options frame
        self.options_frame = tk.Frame(self.game_frame, bg="#222222")
        self.options_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Radio buttons for options (created when needed)
        self.option_buttons = []
        
        # Progress and score frame
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
        
        # Timer label
        self.timer_label = tk.Label(
            progress_frame,
            text="",
            font=("Helvetica", 12),
            bg="#222222",
            fg="#FF9999"  # Light red
        )
        self.timer_label.pack(side=tk.RIGHT)
        
        # Score display
        self.score_label = tk.Label(
            self.game_frame,
            text="",
            font=("Helvetica", 14, "bold"),
            bg="#222222",
            fg="#CCFF99"  # Green
        )
        self.score_label.pack(pady=10)
        
        # Control buttons frame
        control_frame = tk.Frame(main_frame, bg="#333333")
        control_frame.pack(fill=tk.X, pady=10)
        
        # Button to submit answer / next question
        self.action_button = tk.Button(
            control_frame,
            text="Start Quiz",
            command=self.setup_quiz,
            bg="#66CCFF",  # Blue
            fg="#000000",
            activebackground="#3399CC",
            activeforeground="#FFFFFF",
            font=("Helvetica", 12, "bold"),
            width=15
        )
        self.action_button.pack(side=tk.RIGHT, padx=5)
        
        # Button to go back to main menu / play again
        self.menu_button = tk.Button(
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
        self.menu_button.pack(side=tk.LEFT, padx=5)
        
        # Question number selector (for setup)
        self.question_selector_frame = tk.Frame(self.game_frame, bg="#222222")
        self.question_selector_label = tk.Label(
            self.question_selector_frame,
            text="How many questions would you like to answer?",
            font=("Helvetica", 14),
            bg="#222222",
            fg="#FFFFFF"
        )
        self.question_selector = ttk.Combobox(
            self.question_selector_frame,
            values=[str(i) for i in range(5, 16)],
            width=5,
            font=("Helvetica", 12)
        )
        self.question_selector.set("10")  # Default to 10 questions
    
    def show_welcome(self):
        """Show the welcome screen."""
        # Clear any existing widgets in options frame
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        
        # Update labels
        self.title_label.config(text="Quiz Game")
        self.question_label.config(text="Welcome to the Quiz Game!")
        
        # Add welcome message
        welcome_text = """
Test your knowledge with multiple-choice questions!

First, select how many questions you want to answer,
then click "Start Quiz" to begin. For each question,
select your answer and click "Submit".

Are you ready to start?
"""
        welcome_message = tk.Label(
            self.options_frame,
            text=welcome_text,
            font=("Helvetica", 12),
            bg="#222222",
            fg="#FFFFFF",
            justify=tk.LEFT
        )
        welcome_message.pack(padx=10, pady=10, anchor=tk.W)
        
        # Show question selector
        self.question_selector_frame.pack(pady=10)
        self.question_selector_label.pack(side=tk.LEFT, padx=5)
        self.question_selector.pack(side=tk.LEFT, padx=5)
        
        # Reset action button
        self.action_button.config(text="Start Quiz", command=self.setup_quiz)
        self.menu_button.config(text="Quit", command=self.quit_game)
        
        # Reset score and progress labels
        self.progress_label.config(text="")
        self.timer_label.config(text="")
        self.score_label.config(text="")
    
    def setup_quiz(self):
        """Set up the quiz with selected number of questions."""
        try:
            self.num_questions = int(self.question_selector.get())
            if not 5 <= self.num_questions <= 15:
                raise ValueError("Please select between 5 and 15 questions")
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            return
        
        # Hide question selector
        self.question_selector_frame.pack_forget()
        
        # Select random questions
        self.questions = random.sample(QUESTIONS, self.num_questions)
        self.current_question = 0
        self.score = 0
        
        # Start the quiz
        self.show_question()
    
    def show_question(self):
        """Display the current question."""
        # Clear any existing widgets in options frame
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        
        # Reset selected answer
        self.selected_answer.set(-1)
        
        if self.current_question < len(self.questions):
            # Get current question
            question = self.questions[self.current_question]
            
            # Update question display
            self.title_label.config(text=f"Question {self.current_question + 1}")
            self.question_label.config(text=question['question'])
            
            # Create radio buttons for options
            self.option_buttons = []
            for i, option in enumerate(question['options']):
                rb = tk.Radiobutton(
                    self.options_frame,
                    text=option,
                    variable=self.selected_answer,
                    value=i,
                    font=("Helvetica", 12),
                    bg="#222222",
                    fg="#FFFFFF",
                    selectcolor="#444444",
                    activebackground="#333333",
                    activeforeground="#FFFFFF",
                    pady=5
                )
                rb.pack(anchor=tk.W, padx=20, pady=5)
                self.option_buttons.append(rb)
            
            # Update action button
            self.action_button.config(text="Submit Answer", command=self.check_answer)
            
            # Update progress label
            self.progress_label.config(text=f"Question {self.current_question + 1} of {len(self.questions)}")
            
            # Start timer for this question
            self.start_time = time.time()
            self.timer_running = True
            self.update_timer()
            
            # Set question in progress
            self.question_in_progress = True
        else:
            # Quiz complete - show results
            self.show_results()
    
    def update_timer(self):
        """Update the timer display."""
        if self.timer_running:
            elapsed = time.time() - self.start_time
            self.timer_label.config(text=f"Time: {elapsed:.1f}s")
            self.root.after(100, self.update_timer)
    
    def check_answer(self):
        """Check the selected answer."""
        if not self.question_in_progress:
            return
        
        selected = self.selected_answer.get()
        
        if selected == -1:
            messagebox.showinfo("No Selection", "Please select an answer")
            return
        
        # Stop the timer
        self.timer_running = False
        self.question_in_progress = False
        
        # Get current question and check if answer is correct
        question = self.questions[self.current_question]
        correct_answer = question['answer']
        
        # Calculate response time
        response_time = time.time() - self.start_time
        
        # Update UI based on correctness
        for i, button in enumerate(self.option_buttons):
            if i == correct_answer:
                # Highlight correct answer in green
                button.config(bg="#CCFF99", fg="#000000")
            elif i == selected and i != correct_answer:
                # Highlight wrong selection in red
                button.config(bg="#FF6666", fg="#000000")
        
        if selected == correct_answer:
            # Correct answer
            self.score += 1
            self.score_label.config(text=f"Correct! +1 point (Response time: {response_time:.2f}s)")
        else:
            # Incorrect answer
            self.score_label.config(text=f"Incorrect! The correct answer is: {question['options'][correct_answer]}")
        
        # Change action button to proceed to next question
        self.action_button.config(text="Next Question", command=self.next_question)
    
    def next_question(self):
        """Proceed to the next question."""
        self.current_question += 1
        self.show_question()
    
    def show_results(self):
        """Show the final results."""
        # Clear options frame
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        
        # Update title and progress
        self.title_label.config(text="Quiz Complete!")
        self.question_label.config(text="Here are your results:")
        self.progress_label.config(text="")
        self.timer_label.config(text="")
        
        # Calculate percentage score
        percentage = (self.score / self.num_questions) * 100
        
        # Display final score
        result_text = f"You scored {self.score} out of {self.num_questions} ({percentage:.1f}%)"
        final_score = tk.Label(
            self.options_frame,
            text=result_text,
            font=("Helvetica", 16, "bold"),
            bg="#222222",
            fg="#CCFF99"  # Green
        )
        final_score.pack(pady=20)
        
        # Add performance feedback
        if percentage == 100:
            feedback = "Perfect score! Excellent work!"
            color = "#CCFF99"  # Green
        elif percentage >= 80:
            feedback = "Great job! You know your stuff!"
            color = "#CCFF99"  # Green
        elif percentage >= 60:
            feedback = "Good effort! Keep learning!"
            color = "#FFFF99"  # Yellow
        elif percentage >= 40:
            feedback = "Not bad, but there's room for improvement."
            color = "#FFFF99"  # Yellow
        else:
            feedback = "Better luck next time! Try again to improve your score."
            color = "#FF6666"  # Red
        
        feedback_label = tk.Label(
            self.options_frame,
            text=feedback,
            font=("Helvetica", 14),
            bg="#222222",
            fg=color
        )
        feedback_label.pack(pady=10)
        
        # Update action button
        self.action_button.config(text="Play Again", command=self.show_welcome)
        self.menu_button.config(text="Quit", command=self.quit_game)
    
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
    style.configure("TCombobox", fieldbackground="#111111", background="#222222", foreground="#FFFFFF")
    
    app = QuizGameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 