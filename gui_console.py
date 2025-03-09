#!/usr/bin/env python3
import os
import sys
import json
import importlib
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class GameConsoleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Game Console - GUI Mode")
        self.root.geometry("800x600")
        self.root.configure(bg="#333333")
        self.root.minsize(700, 500)
        
        self.games = []
        self.load_games()
        
        # Create UI elements
        self.create_widgets()
        
        # Show welcome message
        self.show_welcome()
    
    def load_games(self):
        """Load the list of games from the catalog file."""
        try:
            with open('games/catalog.json', 'r') as f:
                self.games = json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Error", "Game catalog not found!")
            self.games = []
    
    def create_widgets(self):
        """Create the GUI widgets."""
        # Main frame
        main_frame = tk.Frame(self.root, bg="#333333")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header frame
        header_frame = tk.Frame(main_frame, bg="#333333")
        header_frame.pack(fill=tk.X, pady=10)
        
        # Title label
        title_label = tk.Label(
            header_frame, 
            text="PYTHON GAME CONSOLE", 
            font=("Helvetica", 24, "bold"),
            bg="#333333",
            fg="#66CCFF"  # Blue
        )
        title_label.pack(side=tk.LEFT, padx=10)
        
        # Mode label
        mode_label = tk.Label(
            header_frame, 
            text="GUI MODE", 
            font=("Helvetica", 16, "bold"),
            bg="#333333",
            fg="#CCFF99"  # Green
        )
        mode_label.pack(side=tk.RIGHT, padx=10)
        
        # Games list frame
        games_frame = tk.Frame(main_frame, bg="#222222", relief=tk.RIDGE, bd=2)
        games_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Game information text
        self.game_info = scrolledtext.ScrolledText(
            games_frame,
            width=40,
            height=10,
            font=("Helvetica", 12),
            bg="#111111",
            fg="#FFFFFF",
            wrap=tk.WORD
        )
        self.game_info.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.game_info.config(state=tk.DISABLED)
        
        # Games listbox with scrollbar
        list_frame = tk.Frame(games_frame, bg="#222222")
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)
        
        list_label = tk.Label(
            list_frame,
            text="Available Games",
            font=("Helvetica", 14, "bold"),
            bg="#222222",
            fg="#FFFFFF"
        )
        list_label.pack(pady=(0, 10))
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.games_listbox = tk.Listbox(
            list_frame,
            font=("Helvetica", 12),
            bg="#111111",
            fg="#FFFFFF",
            selectbackground="#444444",
            selectforeground="#FFFFFF",
            width=25,
            height=15
        )
        self.games_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure the scrollbar
        self.games_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.games_listbox.yview)
        
        # Bind selection event
        self.games_listbox.bind("<<ListboxSelect>>", self.on_game_select)
        self.games_listbox.bind("<Double-1>", self.launch_selected_game)
        
        # Control buttons frame
        controls_frame = tk.Frame(main_frame, bg="#333333")
        controls_frame.pack(fill=tk.X, pady=10)
        
        # Play button
        play_button = tk.Button(
            controls_frame,
            text="Play Game",
            command=self.launch_selected_game,
            bg="#66CCFF",  # Blue
            fg="#000000",
            activebackground="#3399CC",
            activeforeground="#FFFFFF",
            font=("Helvetica", 14, "bold"),
            width=12,
            height=2
        )
        play_button.pack(side=tk.LEFT, padx=10)
        
        # Mode switch button
        mode_button = tk.Button(
            controls_frame,
            text="Switch to Terminal",
            command=self.switch_to_terminal,
            bg="#FFFF99",  # Yellow
            fg="#000000",
            activebackground="#CCCC66",
            activeforeground="#000000",
            font=("Helvetica", 12),
            width=15
        )
        mode_button.pack(side=tk.LEFT, padx=10)
        
        # Refresh button
        refresh_button = tk.Button(
            controls_frame,
            text="Refresh Games",
            command=self.refresh_games,
            bg="#444444",
            fg="#FFFFFF",
            activebackground="#666666",
            activeforeground="#FFFFFF",
            font=("Helvetica", 12),
            width=12
        )
        refresh_button.pack(side=tk.LEFT, padx=10)
        
        # Quit button
        quit_button = tk.Button(
            controls_frame,
            text="Quit",
            command=self.quit_console,
            bg="#663333",
            fg="#FFFFFF",
            activebackground="#993333",
            activeforeground="#FFFFFF",
            font=("Helvetica", 12),
            width=8
        )
        quit_button.pack(side=tk.RIGHT, padx=10)
    
    def show_welcome(self):
        """Show a welcome message and populate the games list."""
        # Populate games listbox
        for i, game in enumerate(self.games):
            self.games_listbox.insert(tk.END, f"{i+1}. {game['name']}")
        
        # Select the first game by default if available
        if self.games:
            self.games_listbox.selection_set(0)
            self.on_game_select(None)
    
    def write_text(self, text, tag="normal"):
        """Write text to the game info area."""
        self.game_info.config(state=tk.NORMAL)
        self.game_info.delete(1.0, tk.END)
        self.game_info.insert(tk.END, text)
        self.game_info.config(state=tk.DISABLED)
    
    def on_game_select(self, event):
        """Handle game selection from the listbox."""
        if not self.games_listbox.curselection():
            return
        
        index = self.games_listbox.curselection()[0]
        game = self.games[index]
        
        # Display game information
        info_text = f"{game['name']}\n\n"
        info_text += f"Description:\n{game['description']}\n\n"
        info_text += f"Difficulty: {game.get('difficulty', 'N/A')}\n"
        info_text += f"Players: {game.get('players', 1)}\n\n"
        info_text += "Double-click to play or click the Play Game button."
        
        self.write_text(info_text)
    
    def launch_selected_game(self, event=None):
        """Launch the selected game."""
        if not self.games_listbox.curselection():
            messagebox.showinfo("Select Game", "Please select a game first!")
            return
        
        index = self.games_listbox.curselection()[0]
        game = self.games[index]
        game_module = game['module']
        
        # Try to import and run the GUI version of the game
        try:
            # Hide the console window temporarily
            self.root.withdraw()
            
            # Import and run the game
            game_path = f"games.{game_module}_gui"
            
            try:
                game_module = importlib.import_module(game_path)
                game_module.main()
            except (ImportError, ModuleNotFoundError):
                # If GUI version fails, ask if they want to try terminal version
                result = messagebox.askyesno(
                    "GUI Version Not Available", 
                    f"The GUI version of {game['name']} is not available. Would you like to run the terminal version instead?"
                )
                
                if result:
                    # Fall back to terminal version
                    os.system(f"python -m games.{game['module']}")
            
            # Show the console window again
            self.root.deiconify()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error launching game: {str(e)}")
            self.root.deiconify()
    
    def refresh_games(self):
        """Refresh the list of games."""
        self.load_games()
        
        # Clear and repopulate the listbox
        self.games_listbox.delete(0, tk.END)
        for i, game in enumerate(self.games):
            self.games_listbox.insert(tk.END, f"{i+1}. {game['name']}")
        
        # Select the first game if available
        if self.games:
            self.games_listbox.selection_set(0)
            self.on_game_select(None)
    
    def switch_to_terminal(self):
        """Switch to terminal mode."""
        if messagebox.askyesno("Switch Mode", "Are you sure you want to switch to Terminal mode?"):
            self.root.destroy()
            # Launch the main console in terminal mode
            os.system("python console.py terminal")
    
    def quit_console(self):
        """Quit the game console."""
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            self.root.destroy()

def main():
    """Main function to start the GUI console."""
    root = tk.Tk()
    app = GameConsoleGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 