#!/usr/bin/env python3
import os
import time
import random
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import colorama

# Initialize colorama for color codes in terminal (not used in GUI but kept for consistency)
colorama.init()

# Import the game logic from the terminal version
from games.text_adventure import Player, Location, Event, Combat, create_game_world

class TextAdventureGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Adventure")
        self.root.geometry("800x600")
        self.root.configure(bg="#333333")
        self.root.resizable(True, True)
        
        # Set the game icon
        # self.root.iconbitmap('icon.ico')  # Uncomment and add an icon if available
        
        # Set minimum window size
        self.root.minsize(600, 500)
        
        # Variables for game state
        self.player = None
        self.game_running = False
        self.current_event = None
        
        # Create UI elements
        self.create_widgets()
        
        # Start with intro screen
        self.show_intro()
    
    def create_widgets(self):
        """Create the GUI widgets."""
        # Main frame
        main_frame = tk.Frame(self.root, bg="#333333")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title label
        title_label = tk.Label(
            main_frame, 
            text="Text Adventure", 
            font=("Helvetica", 24, "bold"),
            bg="#333333",
            fg="#66CCFF"
        )
        title_label.pack(pady=(0, 10))
        
        # Game text area
        self.game_text = scrolledtext.ScrolledText(
            main_frame, 
            wrap=tk.WORD, 
            font=("Courier New", 12),
            bg="#000000",
            fg="#CCCCCC",
            insertbackground="#FFFFFF"
        )
        self.game_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.game_text.config(state=tk.DISABLED)  # Make read-only initially
        
        # Command frame
        cmd_frame = tk.Frame(main_frame, bg="#333333")
        cmd_frame.pack(fill=tk.X, pady=5)
        
        # Command entry
        cmd_label = tk.Label(
            cmd_frame, 
            text="What will you do?", 
            font=("Helvetica", 12),
            bg="#333333",
            fg="#FFFFFF"
        )
        cmd_label.pack(side=tk.LEFT, padx=5)
        
        self.cmd_entry = tk.Entry(
            cmd_frame,
            font=("Courier New", 12),
            bg="#000000",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
            width=40
        )
        self.cmd_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.cmd_entry.bind("<Return>", self.process_command)
        
        # Command button
        cmd_button = tk.Button(
            cmd_frame, 
            text="Submit", 
            command=self.process_command,
            bg="#444444",
            fg="#FFFFFF",
            activebackground="#666666",
            activeforeground="#FFFFFF"
        )
        cmd_button.pack(side=tk.RIGHT, padx=5)
        
        # Status frame
        status_frame = tk.Frame(main_frame, bg="#333333")
        status_frame.pack(fill=tk.X, pady=5)
        
        # Health bar
        health_label = tk.Label(
            status_frame, 
            text="Health:", 
            font=("Helvetica", 12),
            bg="#333333",
            fg="#FFFFFF"
        )
        health_label.pack(side=tk.LEFT, padx=5)
        
        self.health_var = tk.IntVar(value=100)
        self.health_bar = ttk.Progressbar(
            status_frame, 
            orient=tk.HORIZONTAL, 
            length=200, 
            mode='determinate',
            variable=self.health_var
        )
        self.health_bar.pack(side=tk.LEFT, padx=5)
        
        # Health text
        self.health_text = tk.Label(
            status_frame, 
            text="100/100", 
            font=("Helvetica", 12),
            bg="#333333",
            fg="#FFFFFF"
        )
        self.health_text.pack(side=tk.LEFT, padx=5)
        
        # Location text
        self.location_text = tk.Label(
            status_frame, 
            text="", 
            font=("Helvetica", 12, "italic"),
            bg="#333333",
            fg="#CCFF99"
        )
        self.location_text.pack(side=tk.RIGHT, padx=5)
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg="#333333")
        buttons_frame.pack(fill=tk.X, pady=5)
        
        # Help button
        help_button = tk.Button(
            buttons_frame, 
            text="Help", 
            command=self.show_help,
            bg="#444444",
            fg="#FFFFFF",
            activebackground="#666666",
            activeforeground="#FFFFFF"
        )
        help_button.pack(side=tk.LEFT, padx=5)
        
        # Inventory button
        inventory_button = tk.Button(
            buttons_frame, 
            text="Inventory", 
            command=self.show_inventory,
            bg="#444444",
            fg="#FFFFFF",
            activebackground="#666666",
            activeforeground="#FFFFFF"
        )
        inventory_button.pack(side=tk.LEFT, padx=5)
        
        # Look button
        look_button = tk.Button(
            buttons_frame, 
            text="Look Around", 
            command=self.look_around,
            bg="#444444",
            fg="#FFFFFF",
            activebackground="#666666",
            activeforeground="#FFFFFF"
        )
        look_button.pack(side=tk.LEFT, padx=5)
        
        # Quit button
        quit_button = tk.Button(
            buttons_frame, 
            text="Quit Game", 
            command=self.quit_game,
            bg="#663333",
            fg="#FFFFFF",
            activebackground="#993333",
            activeforeground="#FFFFFF"
        )
        quit_button.pack(side=tk.RIGHT, padx=5)
        
        # Configure tag colors for text highlighting
        self.game_text.tag_configure("normal", foreground="#CCCCCC")
        self.game_text.tag_configure("blue", foreground="#66CCFF")
        self.game_text.tag_configure("green", foreground="#CCFF99")
        self.game_text.tag_configure("yellow", foreground="#FFFF99")
        self.game_text.tag_configure("red", foreground="#FF6666")
        self.game_text.tag_configure("cyan", foreground="#66FFFF")
        self.game_text.tag_configure("magenta", foreground="#FF99FF")
        self.game_text.tag_configure("white", foreground="#FFFFFF")
        self.game_text.tag_configure("bold", font=("Courier New", 12, "bold"))
    
    def show_intro(self):
        """Display the intro screen."""
        self.write_text("Welcome to the Text Adventure!", "cyan")
        self.write_text("\nYou are about to embark on a perilous journey to find the legendary Crystal of Power.")
        self.write_text("Legend says it's hidden deep within an ancient temple, guarded by fearsome creatures.")
        self.write_text("Your choices will determine your fate. Choose wisely...\n")
        
        self.write_text("\nPlease enter your name to begin your adventure:", "yellow")
        
        # Set up for name entry
        self.cmd_entry.delete(0, tk.END)
        self.game_running = False
        self.waiting_for_name = True
    
    def start_game(self, player_name):
        """Start the game with the given player name."""
        # Create player
        self.player = Player(player_name)
        
        # Create game world
        start_location = create_game_world()
        self.player.location = start_location
        
        # Update location display
        self.update_location_display()
        
        # Clear text and show initial location
        self.game_text.config(state=tk.NORMAL)
        self.game_text.delete(1.0, tk.END)
        self.game_text.config(state=tk.DISABLED)
        
        self.write_text(f"Welcome, {player_name}! Your adventure begins.\n", "green")
        self.write_text(self.player.location.describe(), "normal")
        
        # Start game
        self.game_running = True
        
        # Check for events
        self.check_for_events()
    
    def update_location_display(self):
        """Update the location display."""
        if self.player and self.player.location:
            self.location_text.config(text=f"Location: {self.player.location.name}")
    
    def update_health_display(self):
        """Update the health display."""
        if self.player:
            self.health_var.set(self.player.health)
            self.health_text.config(text=f"{self.player.health}/100")
            
            # Change color based on health
            if self.player.health > 50:
                self.health_bar.config(style="green.Horizontal.TProgressbar")
                self.health_text.config(fg="#CCFF99")  # Green
            elif self.player.health > 25:
                self.health_bar.config(style="yellow.Horizontal.TProgressbar")
                self.health_text.config(fg="#FFFF99")  # Yellow
            else:
                self.health_bar.config(style="red.Horizontal.TProgressbar")
                self.health_text.config(fg="#FF6666")  # Red
    
    def write_text(self, text, tag="normal"):
        """Write text to the game text area with the specified tag."""
        self.game_text.config(state=tk.NORMAL)
        self.game_text.insert(tk.END, text + "\n", tag)
        self.game_text.see(tk.END)  # Scroll to the end
        self.game_text.config(state=tk.DISABLED)
    
    def process_command(self, event=None):
        """Process the user's command."""
        command = self.cmd_entry.get().lower().strip()
        self.cmd_entry.delete(0, tk.END)
        
        if not command:
            return
        
        # Handle waiting for name
        if hasattr(self, 'waiting_for_name') and self.waiting_for_name:
            self.waiting_for_name = False
            self.start_game(command)
            return
        
        # Handle combat event
        if self.current_event and isinstance(self.current_event, Combat):
            self.handle_combat_command(command)
            return
        
        # Write the command to the text area
        self.write_text(f"> {command}", "white")
        
        # Process the command if the game is running
        if self.game_running:
            if command == "quit":
                self.quit_game()
            
            elif command == "help":
                self.show_help()
            
            elif command == "look":
                self.look_around()
            
            elif command.startswith("go "):
                direction = command[3:].strip()
                self.go_direction(direction)
            
            elif command.startswith("take "):
                item = command[5:].strip()
                self.take_item(item)
            
            elif command == "inventory":
                self.show_inventory()
            
            elif command == "health":
                self.show_health()
            
            elif command.startswith("use "):
                item = command[4:].strip()
                self.use_item(item)
            
            else:
                self.write_text("I don't understand that command. Type 'help' for a list of commands.", "red")
    
    def handle_combat_command(self, command):
        """Handle commands during combat."""
        combat = self.current_event
        
        if command == "1" or command == "attack":
            # Attack
            player_damage = random.randint(10, 20)
            combat.enemy_health -= player_damage
            self.write_text(f"You attack the {combat.enemy_name} for {player_damage} damage!", "green")
            
            if combat.enemy_health <= 0:
                self.write_text(f"You defeated the {combat.enemy_name}!", "green")
                self.current_event = None
                combat.triggered = True
                return
        
        elif command == "2" or command == "use item":
            # Show inventory for item selection
            if not self.player.inventory:
                self.write_text("You don't have any items!", "red")
            else:
                self.write_text("Your inventory:", "yellow")
                for i, item in enumerate(self.player.inventory, 1):
                    self.write_text(f"{i}. {item}", "cyan")
                
                # Set up for item selection
                self.waiting_for_item = True
                return
        
        elif self.waiting_for_item and command.isdigit():
            # Handle item selection
            self.waiting_for_item = False
            try:
                item_idx = int(command) - 1
                if 0 <= item_idx < len(self.player.inventory):
                    item = self.player.inventory[item_idx]
                    
                    if item == "Health Potion":
                        self.player.heal(30)
                        self.player.remove_item(item)
                        self.write_text("You used a Health Potion and recovered 30 health!", "green")
                        self.update_health_display()
                    elif item == "Sword":
                        player_damage = random.randint(15, 25)
                        combat.enemy_health -= player_damage
                        self.write_text(f"You attack with your Sword for {player_damage} damage!", "green")
                        
                        if combat.enemy_health <= 0:
                            self.write_text(f"You defeated the {combat.enemy_name}!", "green")
                            self.current_event = None
                            combat.triggered = True
                            return
                    else:
                        self.write_text("You can't use that item in combat!", "yellow")
                else:
                    self.write_text("Invalid choice.", "red")
            except (ValueError, IndexError):
                self.write_text("Invalid choice.", "red")
        
        elif command == "3" or command == "run":
            # Run away
            escape_chance = random.random()
            if escape_chance > 0.5:
                self.write_text(f"You successfully escaped from the {combat.enemy_name}!", "green")
                self.current_event = None
                return
            else:
                self.write_text("You failed to escape!", "red")
        
        else:
            self.write_text("Invalid combat command. Enter 1 to attack, 2 to use an item, or 3 to run.", "red")
            return
        
        # Enemy's turn if still in combat
        if self.current_event and combat.enemy_health > 0:
            enemy_damage = random.randint(5, combat.damage)
            self.player.take_damage(enemy_damage)
            self.update_health_display()
            self.write_text(f"The {combat.enemy_name} attacks you for {enemy_damage} damage!", "red")
            
            if self.player.health <= 0:
                self.write_text(f"You were defeated by the {combat.enemy_name}!", "red")
                self.game_over()
                self.current_event = None
                combat.triggered = True
    
    def check_for_events(self):
        """Check for events at the current location."""
        if self.player and self.player.location and self.game_running:
            for event in self.player.location.events:
                if not event.triggered:
                    if isinstance(event, Combat):
                        # Handle combat event
                        self.current_event = event
                        self.write_text(event.description, "red")
                        self.write_text(f"\nYou are in combat with a {event.enemy_name}!", "red")
                        self.write_text(f"Your health: {self.player.health}/100", "green")
                        self.write_text(f"{event.enemy_name}'s health: {event.enemy_health}/100", "red")
                        self.write_text("\nWhat will you do?", "yellow")
                        self.write_text("1. Attack", "green")
                        self.write_text("2. Use item", "cyan")
                        self.write_text("3. Run away", "red")
                        return
                    else:
                        # Handle regular event
                        self.write_text(event.description, "yellow")
                        event.triggered = True
    
    def show_help(self):
        """Display available commands."""
        self.write_text("\nAvailable Commands:", "cyan")
        self.write_text("look - Look around your current location", "green")
        self.write_text("go [direction] - Move in a direction (north, south, east, west)", "green")
        self.write_text("take [item] - Pick up an item", "green")
        self.write_text("inventory - Check your inventory", "green")
        self.write_text("health - Check your health", "green")
        self.write_text("use [item] - Use an item", "green")
        self.write_text("help - Show this help message", "green")
        self.write_text("quit - Exit the game", "green")
    
    def look_around(self):
        """Look around the current location."""
        if self.player and self.player.location:
            self.write_text(self.player.location.describe(), "normal")
        else:
            self.write_text("You are nowhere... which is strange.", "red")
    
    def go_direction(self, direction):
        """Move in the specified direction."""
        if self.player and self.player.location:
            if direction in self.player.location.connections:
                self.player.location = self.player.location.connections[direction]
                self.update_location_display()
                self.write_text(f"You go {direction}.\n", "green")
                self.write_text(self.player.location.describe(), "normal")
                
                # Check for events at the new location
                self.check_for_events()
            else:
                self.write_text(f"You can't go {direction}.", "red")
    
    def take_item(self, item):
        """Take an item."""
        if self.player and self.player.location:
            if item in self.player.location.items:
                self.player.add_item(item)
                self.player.location.remove_item(item)
                self.write_text(f"You took the {item}.", "green")
            else:
                self.write_text(f"There's no {item} here.", "red")
    
    def show_inventory(self):
        """Show the player's inventory."""
        if self.player:
            if self.player.inventory:
                self.write_text("You are carrying:", "yellow")
                for item in self.player.inventory:
                    self.write_text(f"- {item}", "cyan")
            else:
                self.write_text("Your inventory is empty.", "yellow")
    
    def show_health(self):
        """Show the player's health."""
        if self.player:
            health_color = "green" if self.player.health > 50 else "yellow" if self.player.health > 25 else "red"
            self.write_text(f"Your health: {self.player.health}/100", health_color)
    
    def use_item(self, item):
        """Use an item."""
        if self.player and self.player.has_item(item):
            if item == "Health Potion":
                self.player.heal(30)
                self.player.remove_item(item)
                self.write_text("You used the Health Potion and recovered 30 health!", "green")
                self.update_health_display()
            elif item == "Torch" and self.player.location.name == "Dark Cave":
                self.write_text("You light the torch, illuminating the cave. You notice a small passage you missed before.", "yellow")
            elif item == "Map":
                self.write_text("You consult the map. It shows the general layout of the area, but some parts are faded or missing.", "yellow")
            elif item == "Ancient Key" and self.player.location.name == "Hidden Temple":
                self.write_text("You insert the key into a hidden keyhole on the pedestal. With a rumble, the pedestal opens to reveal...", "yellow")
                self.root.after(2000, lambda: self.write_text("The Crystal of Power! You've found it!", "cyan"))
                self.root.after(3000, lambda: self.write_text(f"Congratulations, {self.player.name}! You've completed your quest and found the legendary artifact!", "green"))
                self.root.after(4000, self.game_won)
            else:
                self.write_text("You can't use that item here.", "yellow")
        else:
            self.write_text("You don't have that item.", "red")
    
    def game_over(self):
        """End the game (player lost)."""
        self.game_running = False
        self.write_text("\nGame Over! Your health reached zero.", "red")
        
        # Ask to play again
        if messagebox.askyesno("Game Over", "Would you like to play again?"):
            self.show_intro()
        else:
            self.root.destroy()
    
    def game_won(self):
        """End the game (player won)."""
        self.game_running = False
        self.write_text("\nYou have completed your adventure successfully!", "cyan")
        
        # Ask to play again
        if messagebox.askyesno("Victory", "Would you like to play again?"):
            self.show_intro()
        else:
            self.root.destroy()
    
    def quit_game(self):
        """Quit the game."""
        if messagebox.askyesno("Quit Game", "Are you sure you want to quit?"):
            self.root.destroy()

def main():
    """Main function to start the GUI game."""
    root = tk.Tk()
    
    # Set style for the progress bar
    style = ttk.Style()
    style.theme_use('default')
    style.configure("green.Horizontal.TProgressbar", background='#CCFF99')
    style.configure("yellow.Horizontal.TProgressbar", background='#FFFF99')
    style.configure("red.Horizontal.TProgressbar", background='#FF6666')
    
    app = TextAdventureGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 