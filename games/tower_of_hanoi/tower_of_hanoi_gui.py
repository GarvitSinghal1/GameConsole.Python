#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox, Label, Button, Frame, Scale, StringVar, IntVar
import random
import sys
import os
import time

class TowerOfHanoiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tower of Hanoi")
        self.root.geometry("800x600")  # Larger window size
        self.root.configure(bg="#333333")
        self.root.resizable(True, True)  # Allow resizing
        
        # Game parameters
        self.num_discs = 3
        self.max_disc_width = 200
        self.disc_height = 20
        self.peg_width = 10
        self.peg_height = self.disc_height * (self.num_discs + 0.5)
        self.base_height = 20
        self.moves = 0
        self.min_moves = 2 ** self.num_discs - 1
        self.auto_solving = False
        self.animation_speed = 500  # ms
        
        # State variables
        self.selected_peg = None
        
        # Initialize the pegs (towers)
        self.pegs = [
            list(range(self.num_discs, 0, -1)),  # First peg with all discs
            [],  # Second peg (empty)
            []   # Third peg (empty)
        ]
        
        # Colors
        self.disc_colors = [
            "#FF5555", "#55FF55", "#5555FF", "#FFFF55", 
            "#FF55FF", "#55FFFF", "#FF9955", "#FF5599"
        ]
        
        # Create widgets
        self.create_widgets()
        
        # Show welcome screen
        self.show_welcome()
    
    def create_widgets(self):
        """Create the GUI widgets."""
        # Main frame
        self.main_frame = Frame(self.root, bg="#333333")
        self.main_frame.pack(pady=10, expand=True, fill=tk.BOTH)
        
        # Game title
        self.title_label = Label(
            self.main_frame,
            text="Tower of Hanoi",
            font=("Helvetica", 24, "bold"),
            bg="#333333",
            fg="#FFFFFF"
        )
        self.title_label.pack(pady=10)
        
        # Status and moves display
        self.status_frame = Frame(self.main_frame, bg="#333333")
        self.status_frame.pack(pady=5, fill=tk.X)
        
        self.moves_var = StringVar()
        self.moves_var.set(f"Moves: 0 / {self.min_moves}")
        
        self.moves_label = Label(
            self.status_frame,
            textvariable=self.moves_var,
            font=("Helvetica", 14),
            bg="#333333",
            fg="#FFFFFF"
        )
        self.moves_label.pack(side=tk.LEFT, padx=20)
        
        self.status_var = StringVar()
        self.status_var.set("Select a peg to move a disc")
        
        self.status_label = Label(
            self.status_frame,
            textvariable=self.status_var,
            font=("Helvetica", 14),
            bg="#333333",
            fg="#FFFF55"
        )
        self.status_label.pack(side=tk.RIGHT, padx=20)
        
        # Game canvas
        self.canvas_frame = Frame(self.main_frame, bg="#333333")
        self.canvas_frame.pack(pady=10, expand=True, fill=tk.BOTH)
        
        self.canvas = tk.Canvas(
            self.canvas_frame,
            bg="#222222",
            highlightthickness=0
        )
        self.canvas.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
        
        # Disc size slider
        self.disc_frame = Frame(self.main_frame, bg="#333333")
        self.disc_frame.pack(pady=5, fill=tk.X)
        
        self.disc_label = Label(
            self.disc_frame,
            text="Number of Discs:",
            font=("Helvetica", 12),
            bg="#333333",
            fg="#FFFFFF"
        )
        self.disc_label.pack(side=tk.LEFT, padx=20)
        
        self.disc_slider = Scale(
            self.disc_frame,
            from_=3,
            to=8,
            orient=tk.HORIZONTAL,
            length=200,
            bg="#333333",
            fg="#FFFFFF",
            troughcolor="#555555",
            highlightthickness=0,
            command=self.change_disc_count
        )
        self.disc_slider.set(self.num_discs)
        self.disc_slider.pack(side=tk.LEFT, padx=5)
        
        # Control buttons
        self.control_frame = Frame(self.main_frame, bg="#333333")
        self.control_frame.pack(pady=10, fill=tk.X)
        
        self.new_game_button = Button(
            self.control_frame,
            text="New Game",
            font=("Helvetica", 12),
            bg="#4CAF50",
            fg="white",
            command=self.new_game
        )
        self.new_game_button.pack(side=tk.LEFT, padx=20)
        
        self.solve_button = Button(
            self.control_frame,
            text="Auto Solve",
            font=("Helvetica", 12),
            bg="#2196F3",
            fg="white",
            command=self.auto_solve
        )
        self.solve_button.pack(side=tk.LEFT, padx=10)
        
        self.reset_button = Button(
            self.control_frame,
            text="Reset",
            font=("Helvetica", 12),
            bg="#FF9800",
            fg="white",
            command=self.reset_game
        )
        self.reset_button.pack(side=tk.LEFT, padx=10)
        
        self.quit_button = Button(
            self.control_frame,
            text="Quit",
            font=("Helvetica", 12),
            bg="#F44336",
            fg="white",
            command=self.quit_game
        )
        self.quit_button.pack(side=tk.RIGHT, padx=20)
        
        # Set up canvas to be responsive
        self.root.bind("<Configure>", self.on_resize)
        
        # Initial rendering
        self.draw_towers()
    
    def show_welcome(self):
        """Show the welcome screen."""
        welcome_window = tk.Toplevel(self.root)
        welcome_window.title("Welcome to Tower of Hanoi")
        welcome_window.geometry("500x400")
        welcome_window.configure(bg="#333333")
        welcome_window.transient(self.root)
        welcome_window.grab_set()
        welcome_window.resizable(True, True)
        
        # Welcome title
        welcome_label = Label(
            welcome_window,
            text="Welcome to Tower of Hanoi",
            font=("Helvetica", 18, "bold"),
            bg="#333333",
            fg="#FFFFFF"
        )
        welcome_label.pack(pady=20)
        
        # Instructions
        instructions_frame = Frame(welcome_window, bg="#333333", padx=20)
        instructions_frame.pack(fill=tk.BOTH, expand=True)
        
        instructions = [
            "The Tower of Hanoi is a classic puzzle game.",
            "",
            "The goal is to move all the discs from the first peg to the",
            "third peg, following these rules:",
            "",
            "1. Only one disc can be moved at a time.",
            "2. Each move consists of taking the upper disc from one",
            "   stack and placing it on top of another stack.",
            "3. No disc may be placed on top of a smaller disc.",
            "",
            "To move a disc, simply click on the source peg, then click",
            "on the destination peg. The game will validate if the move",
            "is legal.",
            "",
            "You can adjust the number of discs using the slider at the",
            "bottom of the screen.",
            "",
            "Good luck!"
        ]
        
        for i, text in enumerate(instructions):
            Label(
                instructions_frame,
                text=text,
                font=("Helvetica", 12),
                bg="#333333",
                fg="#FFFFFF",
                justify=tk.LEFT
            ).pack(anchor=tk.W, pady=1)
        
        # Start button
        start_button = Button(
            welcome_window,
            text="Start Game",
            font=("Helvetica", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            command=welcome_window.destroy
        )
        start_button.pack(pady=20)
    
    def on_resize(self, event):
        """Handle window resize events."""
        if event.widget == self.root or event.widget == self.canvas:
            self.draw_towers()
    
    def draw_towers(self):
        """Draw the towers and discs on the canvas."""
        # Clear the canvas
        self.canvas.delete("all")
        
        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            # Canvas not properly initialized yet
            return
        
        # Calculate peg positions
        peg_spacing = canvas_width / 4
        peg_x = [peg_spacing, 2 * peg_spacing, 3 * peg_spacing]
        peg_top_y = canvas_height / 3
        base_y = peg_top_y + self.peg_height
        
        # Adjust disc width based on canvas size
        max_disc_width = min(peg_spacing * 0.8, self.max_disc_width)
        disc_width_unit = max_disc_width / self.num_discs
        
        # Draw the base
        self.canvas.create_rectangle(
            peg_spacing / 2, base_y,
            3.5 * peg_spacing, base_y + self.base_height,
            fill="#8B4513", outline=""
        )
        
        # Draw the pegs
        for i in range(3):
            self.canvas.create_rectangle(
                peg_x[i] - self.peg_width / 2, peg_top_y,
                peg_x[i] + self.peg_width / 2, base_y,
                fill="#A0522D", outline=""
            )
            
            # Make the peg clickable
            peg_area = self.canvas.create_rectangle(
                peg_x[i] - peg_spacing / 3, peg_top_y,
                peg_x[i] + peg_spacing / 3, base_y,
                fill="", outline="", tags=f"peg_{i}"
            )
            self.canvas.tag_bind(f"peg_{i}", "<Button-1>", lambda e, i=i: self.on_peg_click(i))
            
            # Draw discs for this peg
            for j, disc_size in enumerate(reversed(self.pegs[i])):
                disc_width = disc_size * disc_width_unit
                disc_y = base_y - (j + 1) * self.disc_height
                
                # Account for custom colors by using modulo on disc_size
                color_idx = (disc_size - 1) % len(self.disc_colors)
                
                self.canvas.create_rectangle(
                    peg_x[i] - disc_width / 2, disc_y,
                    peg_x[i] + disc_width / 2, disc_y + self.disc_height,
                    fill=self.disc_colors[color_idx],
                    outline="#222222",
                    width=1
                )
        
        # Draw peg labels
        for i in range(3):
            self.canvas.create_text(
                peg_x[i], base_y + self.base_height + 20,
                text=f"Peg {i + 1}",
                fill="#FFFFFF",
                font=("Helvetica", 12)
            )
    
    def on_peg_click(self, peg_idx):
        """Handle peg click events."""
        if self.auto_solving:
            return
        
        if self.selected_peg is None:
            # No peg selected yet
            if not self.pegs[peg_idx]:
                # Can't select an empty peg
                self.status_var.set("Cannot select an empty peg")
                return
                
            self.selected_peg = peg_idx
            self.status_var.set(f"Selected Peg {peg_idx + 1}. Click destination peg.")
        else:
            # Peg already selected, attempt to move
            from_peg = self.selected_peg
            to_peg = peg_idx
            
            # Reset selection
            self.selected_peg = None
            
            # Check if the move is valid
            if from_peg == to_peg:
                self.status_var.set("Select a different peg")
                return
            
            if not self.pegs[from_peg]:
                self.status_var.set("Source peg is empty")
                return
            
            if self.pegs[to_peg] and self.pegs[from_peg][-1] > self.pegs[to_peg][-1]:
                self.status_var.set("Cannot place a larger disc on a smaller disc")
                return
            
            # Make the move
            disc = self.pegs[from_peg].pop()
            self.pegs[to_peg].append(disc)
            self.moves += 1
            self.moves_var.set(f"Moves: {self.moves} / {self.min_moves}")
            
            # Redraw the towers
            self.draw_towers()
            
            # Check if the game is won
            if len(self.pegs[2]) == self.num_discs:
                if self.moves == self.min_moves:
                    message = f"Congratulations! You solved the puzzle in the minimum number of moves ({self.moves})!"
                else:
                    message = f"Congratulations! You solved the puzzle in {self.moves} moves!\nThe minimum possible is {self.min_moves} moves."
                
                self.status_var.set("Puzzle solved!")
                messagebox.showinfo("Tower of Hanoi", message)
            else:
                self.status_var.set("Select a peg to move a disc")
    
    def change_disc_count(self, value):
        """Change the number of discs and reset the game."""
        self.num_discs = int(value)
        self.reset_game()
    
    def reset_game(self):
        """Reset the game to its initial state."""
        self.pegs = [
            list(range(self.num_discs, 0, -1)),
            [],
            []
        ]
        self.moves = 0
        self.min_moves = 2 ** self.num_discs - 1
        self.moves_var.set(f"Moves: {self.moves} / {self.min_moves}")
        self.status_var.set("Select a peg to move a disc")
        self.selected_peg = None
        self.auto_solving = False
        self.draw_towers()
    
    def new_game(self):
        """Start a new game."""
        if messagebox.askyesno("New Game", "Start a new game?"):
            self.reset_game()
    
    def solve_step(self, n, source, auxiliary, target):
        """Perform one step of the Tower of Hanoi solution algorithm."""
        if n > 0 and self.auto_solving:
            # Move n-1 discs from source to auxiliary
            self.solve_step(n-1, source, target, auxiliary)
            
            # Move one disc from source to target
            if self.auto_solving:  # Check if still auto solving
                disc = self.pegs[source].pop()
                self.pegs[target].append(disc)
                self.moves += 1
                self.moves_var.set(f"Moves: {self.moves} / {self.min_moves}")
                self.draw_towers()
                self.root.update()
                self.canvas.after(self.animation_speed)
            
            # Move n-1 discs from auxiliary to target
            self.solve_step(n-1, auxiliary, source, target)
    
    def auto_solve(self):
        """Automatically solve the Tower of Hanoi puzzle."""
        if messagebox.askyesno("Auto Solve", "Let the computer solve the puzzle?"):
            self.reset_game()
            self.auto_solving = True
            self.status_var.set("Auto solving...")
            
            # Start the solving process
            self.root.after(500, lambda: self.solve_step(self.num_discs, 0, 1, 2))
            
            # Update status when finished
            self.root.after((2**self.num_discs) * self.animation_speed, self.finish_auto_solve)
    
    def finish_auto_solve(self):
        """Called when auto-solving is complete."""
        if self.auto_solving:
            self.auto_solving = False
            self.status_var.set("Puzzle solved automatically!")
            messagebox.showinfo("Tower of Hanoi", "The puzzle has been solved automatically!")
    
    def quit_game(self):
        """Quit the game."""
        if messagebox.askyesno("Quit", "Are you sure you want to quit the game?"):
            self.root.destroy()

def main():
    """Main function to start the GUI game."""
    root = tk.Tk()
    app = TowerOfHanoiGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 