#!/usr/bin/env python3
import os
import sys
import json
import time
import colorama
from colorama import Fore, Back, Style

# Initialize colorama for cross-platform color support
colorama.init()

class GameConsole:
    def __init__(self):
        self.games = []
        self.load_games()
        self.running = True
        self.interface_mode = None  # Will be set to "terminal" or "gui"
        self.clear_screen()
        
    def load_games(self):
        """Load the list of games from the catalog file."""
        try:
            with open('games/catalog.json', 'r') as f:
                self.games = json.load(f)
        except FileNotFoundError:
            print(f"{Fore.RED}Game catalog not found. Creating a new one.{Style.RESET_ALL}")
            # Create the games directory if it doesn't exist
            os.makedirs('games', exist_ok=True)
            self.games = []
            self.save_games()
    
    def save_games(self):
        """Save the list of games to the catalog file."""
        with open('games/catalog.json', 'w') as f:
            json.dump(self.games, f, indent=4)
    
    def clear_screen(self):
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print the console header."""
        print(f"{Back.BLUE}{Fore.WHITE}╔═══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Back.BLUE}{Fore.WHITE}║                     PYTHON GAME CONSOLE                       ║{Style.RESET_ALL}")
        print(f"{Back.BLUE}{Fore.WHITE}╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        print()
    
    def print_footer(self):
        """Print the console footer."""
        print()
        print(f"{Back.BLUE}{Fore.WHITE}╔═══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Back.BLUE}{Fore.WHITE}║ [Q]uit  [R]efresh  [I] Change Interface                       ║{Style.RESET_ALL}")
        print(f"{Back.BLUE}{Fore.WHITE}╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    def select_interface(self):
        """Ask the user to select between terminal or GUI interface."""
        # Check if the interface mode was specified as a command-line argument
        if len(sys.argv) > 1 and sys.argv[1].lower() in ["terminal", "gui"]:
            self.interface_mode = sys.argv[1].lower()
            return

        while True:
            self.clear_screen()
            self.print_header()
            
            print(f"{Fore.CYAN}Select your preferred interface:{Style.RESET_ALL}")
            print()
            print(f"{Fore.GREEN}1. Terminal{Style.RESET_ALL} - Text-based console interface")
            print(f"{Fore.GREEN}2. GUI{Style.RESET_ALL} - Graphical user interface")
            print()
            
            choice = input(f"{Fore.CYAN}Enter your choice (1-2): {Style.RESET_ALL}")
            
            if choice == "1":
                self.interface_mode = "terminal"
                return
            elif choice == "2":
                self.interface_mode = "gui"
                # Launch the GUI console and exit this one
                self.launch_gui_console()
                sys.exit(0)
            else:
                print(f"{Fore.RED}Invalid choice. Please enter 1 or 2.{Style.RESET_ALL}")
                time.sleep(1)
    
    def launch_gui_console(self):
        """Launch the GUI console."""
        try:
            # Check if tkinter is available
            import tkinter
            
            # Try to run the GUI console directly
            import gui_console
            gui_console.main()
        except ImportError:
            print(f"{Fore.RED}Could not import tkinter or gui_console. Running as process...{Style.RESET_ALL}")
            # If the direct import fails, run it as a separate process
            os.system('python gui_console.py')
    
    def display_menu(self):
        """Display the main menu."""
        self.clear_screen()
        self.print_header()
        
        # Show current interface mode
        mode_color = Fore.GREEN if self.interface_mode == "terminal" else Fore.CYAN
        print(f"Current Mode: {mode_color}{self.interface_mode.upper()}{Style.RESET_ALL}")
        print()
        
        if not self.games:
            print(f"{Fore.YELLOW}No games available. Please install some games!{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}Available Games:{Style.RESET_ALL}")
            print()
            
            for idx, game in enumerate(self.games, 1):
                print(f"{Fore.GREEN}{idx}.{Style.RESET_ALL} {Fore.WHITE}{game['name']}{Style.RESET_ALL}")
                print(f"   {Fore.YELLOW}{game['description']}{Style.RESET_ALL}")
                print()
        
        self.print_footer()
    
    def run_game(self, game_index):
        """Run a selected game."""
        if 0 <= game_index < len(self.games):
            game = self.games[game_index]
            game_module = game['module']
            
            self.clear_screen()
            print(f"{Fore.CYAN}Loading {game['name']}...{Style.RESET_ALL}")
            time.sleep(1)
            
            try:
                # Check if the game module path contains a dot, indicating a subdirectory
                if self.interface_mode == "terminal":
                    game_path = f"games.{game_module}"
                    __import__(game_path)
                    game_module_obj = sys.modules[game_path]
                    
                    # Clear screen before starting the game
                    self.clear_screen()
                    
                    # Run the game's main function
                    game_module_obj.main()
                else:  # GUI mode
                    # For modules with subdirectories, the GUI version is in the same directory
                    if '.' in game_module:
                        base_module = game_module.rsplit('.', 1)[0]
                        module_name = game_module.rsplit('.', 1)[1]
                        gui_game_path = f"games.{base_module}.{module_name}_gui"
                    else:
                        gui_game_path = f"games.{game_module}_gui"
                    
                    try:
                        __import__(gui_game_path)
                        gui_game_module = sys.modules[gui_game_path]
                        
                        # Run the GUI game's main function
                        gui_game_module.main()
                    except (ImportError, ModuleNotFoundError):
                        # GUI version not found, fall back to terminal
                        print(f"{Fore.YELLOW}GUI version not available for {game['name']}. Running terminal version...{Style.RESET_ALL}")
                        time.sleep(2)
                        
                        game_path = f"games.{game_module}"
                        __import__(game_path)
                        game_module_obj = sys.modules[game_path]
                        
                        # Clear screen before starting the game
                        self.clear_screen()
                        
                        # Run the game's main function
                        game_module_obj.main()
            except Exception as e:
                self.clear_screen()
                print(f"{Fore.RED}Error loading game: {e}{Style.RESET_ALL}")
                time.sleep(2)
        else:
            print(f"{Fore.RED}Invalid game selection.{Style.RESET_ALL}")
            time.sleep(1)
    
    def change_interface(self):
        """Change the interface mode between terminal and GUI."""
        if self.interface_mode == "terminal":
            print(f"{Fore.GREEN}Switching to GUI mode...{Style.RESET_ALL}")
            time.sleep(1)
            self.interface_mode = "gui"
            # Launch the GUI console and exit this one
            self.launch_gui_console()
            sys.exit(0)
        else:
            self.interface_mode = "terminal"
            print(f"{Fore.GREEN}Interface changed to TERMINAL{Style.RESET_ALL}")
            time.sleep(1)
    
    def run(self):
        """Run the game console."""
        # Only select interface mode if it hasn't been set already
        if self.interface_mode is None:
            self.select_interface()
        
        # If in terminal mode, continue with terminal interface
        if self.interface_mode == "terminal":
            while self.running:
                self.display_menu()
                
                choice = input(f"\n{Fore.CYAN}Enter your choice (1-{len(self.games)}), or [I] to change interface: {Style.RESET_ALL}").lower()
                
                if choice == 'q':
                    self.running = False
                elif choice == 'r':
                    self.load_games()
                elif choice == 'i':
                    self.change_interface()
                elif choice.isdigit():
                    game_idx = int(choice) - 1
                    self.run_game(game_idx)
                else:
                    print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
                    time.sleep(1)
    
    def shutdown(self):
        """Shutdown the console."""
        self.clear_screen()
        print(f"{Fore.CYAN}Thank you for playing!{Style.RESET_ALL}")
        time.sleep(1)

if __name__ == "__main__":
    console = GameConsole()
    try:
        console.run()
    except KeyboardInterrupt:
        pass
    finally:
        console.shutdown() 