#!/usr/bin/env python3
"""
Python Game Console - Main Entry Point

This file serves as a single entry point for the entire game console system.
It will first ask the user which interface they prefer (terminal or GUI),
then launch the appropriate console.
"""

import os
import sys
import subprocess
import argparse

def check_gui_availability():
    """Check if the GUI mode is available (tkinter is installed)."""
    try:
        import tkinter
        return True
    except ImportError:
        return False

def ask_user_for_mode():
    """Ask the user which mode they want to use."""
    has_gui = check_gui_availability()
    
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║                     PYTHON GAME CONSOLE                       ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print()
    print("Select your preferred interface:")
    print()
    print("1. Terminal - Text-based console interface")
    
    if has_gui:
        print("2. GUI - Graphical user interface")
        valid_choices = ['1', '2', 'terminal', 'gui']
    else:
        print("2. GUI - [NOT AVAILABLE - tkinter is not installed]")
        valid_choices = ['1', 'terminal']
    
    print()
    
    while True:
        choice = input("Enter your choice (1/2 or terminal/gui): ").lower().strip()
        
        if choice in valid_choices:
            if choice == '1' or choice == 'terminal':
                return "terminal"
            elif (choice == '2' or choice == 'gui') and has_gui:
                return "gui"
            else:
                print("GUI mode is not available. Please install tkinter.")
        else:
            print("Invalid choice. Please try again.")

def main():
    """Main entry point for the game console."""
    parser = argparse.ArgumentParser(description="Python Game Console")
    parser.add_argument("--mode", "-m", choices=["ask", "terminal", "gui"], 
                        default="ask", help="Interface mode: ask, terminal, or gui")
    args = parser.parse_args()
    
    # Determine which mode to use
    mode = args.mode
    
    if mode == "ask":
        # Ask the user which mode they want to use
        mode = ask_user_for_mode()
    
    # Launch the appropriate console
    if mode == "gui":
        if check_gui_availability():
            try:
                # Try to import and run directly
                import gui_console
                gui_console.main()
            except ImportError:
                # If that fails, try running as a subprocess
                print("Launching GUI console...")
                subprocess.run([sys.executable, "gui_console.py"])
        else:
            print("GUI mode requires tkinter, which is not available.")
            print("Falling back to terminal mode...")
            # Fall back to terminal mode
            subprocess.run([sys.executable, "console.py", "terminal"])
    else:  # terminal mode
        try:
            # Import console and run it with the terminal mode already set
            # This prevents it from asking for the interface mode again
            import console
            console_instance = console.GameConsole()
            # Set the interface mode directly to skip the selection prompt
            console_instance.interface_mode = "terminal"
            # Run the console
            console_instance.run()
        except ImportError:
            # If that fails, try running as a subprocess with the mode argument
            print("Launching terminal console...")
            subprocess.run([sys.executable, "console.py", "terminal"])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting game console...")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("If the problem persists, please report it to the developers.")
        sys.exit(1) 