#!/usr/bin/env python3
import os
import time
import random
import colorama
from colorama import Fore, Back, Style

# Initialize colorama
colorama.init()

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the game header."""
    print(f"{Back.BLUE}{Fore.BLACK}╔═══════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Back.BLUE}{Fore.BLACK}║                    TEXT ADVENTURE                             ║{Style.RESET_ALL}")
    print(f"{Back.BLUE}{Fore.BLACK}╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()

def slow_print(text, delay=0.03):
    """Print text with a slight delay for effect."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

class Player:
    """Class representing the player character."""
    def __init__(self, name):
        self.name = name
        self.inventory = []
        self.health = 100
        self.location = None
        
    def add_item(self, item):
        """Add an item to the player's inventory."""
        self.inventory.append(item)
        
    def remove_item(self, item):
        """Remove an item from the player's inventory."""
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False
    
    def has_item(self, item):
        """Check if the player has a specific item."""
        return item in self.inventory
    
    def take_damage(self, amount):
        """Reduce player's health by the specified amount."""
        self.health -= amount
        if self.health < 0:
            self.health = 0
    
    def heal(self, amount):
        """Increase player's health by the specified amount."""
        self.health += amount
        if self.health > 100:
            self.health = 100

class Location:
    """Class representing a location in the game."""
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.connections = {}  # direction: location
        self.items = []
        self.events = []
    
    def add_connection(self, direction, location):
        """Add a connection to another location."""
        self.connections[direction] = location
    
    def add_item(self, item):
        """Add an item to this location."""
        self.items.append(item)
    
    def remove_item(self, item):
        """Remove an item from this location."""
        if item in self.items:
            self.items.remove(item)
            return True
        return False
    
    def add_event(self, event):
        """Add an event to this location."""
        self.events.append(event)
    
    def describe(self):
        """Return a full description of the location."""
        desc = f"{Fore.CYAN}{self.name}{Style.RESET_ALL}\n\n"
        desc += f"{Fore.WHITE}{self.description}{Style.RESET_ALL}\n\n"
        
        # List available directions
        if self.connections:
            desc += f"{Fore.YELLOW}You can go: {Style.RESET_ALL}"
            desc += ", ".join([f"{Fore.GREEN}{direction}{Style.RESET_ALL}" for direction in self.connections.keys()])
            desc += "\n"
        
        # List items at this location
        if self.items:
            desc += f"{Fore.YELLOW}You see: {Style.RESET_ALL}"
            desc += ", ".join([f"{Fore.MAGENTA}{item}{Style.RESET_ALL}" for item in self.items])
            desc += "\n"
        
        return desc

class Event:
    """Base class for game events."""
    def __init__(self, description):
        self.description = description
        self.triggered = False
    
    def trigger(self, player):
        """Trigger the event."""
        if not self.triggered:
            slow_print(f"{Fore.YELLOW}{self.description}{Style.RESET_ALL}")
            self.triggered = True
            return True
        return False

class Combat(Event):
    """Combat event with an enemy."""
    def __init__(self, description, enemy_name, enemy_health, damage):
        super().__init__(description)
        self.enemy_name = enemy_name
        self.enemy_health = enemy_health
        self.damage = damage
    
    def trigger(self, player):
        """Initiate combat with the enemy."""
        if not self.triggered:
            slow_print(f"{Fore.RED}{self.description}{Style.RESET_ALL}")
            
            while self.enemy_health > 0 and player.health > 0:
                # Display health
                print(f"\n{Fore.GREEN}Your health: {player.health}/100{Style.RESET_ALL}")
                print(f"{Fore.RED}{self.enemy_name}'s health: {self.enemy_health}/100{Style.RESET_ALL}\n")
                
                # Player's turn
                print(f"{Fore.YELLOW}What will you do?{Style.RESET_ALL}")
                print(f"1. {Fore.GREEN}Attack{Style.RESET_ALL}")
                print(f"2. {Fore.CYAN}Use item{Style.RESET_ALL}")
                print(f"3. {Fore.RED}Run away{Style.RESET_ALL}")
                
                choice = input(f"{Fore.WHITE}Enter your choice (1-3): {Style.RESET_ALL}")
                
                if choice == '1':  # Attack
                    player_damage = random.randint(10, 20)
                    self.enemy_health -= player_damage
                    print(f"\n{Fore.GREEN}You attack the {self.enemy_name} for {player_damage} damage!{Style.RESET_ALL}")
                    
                    if self.enemy_health <= 0:
                        slow_print(f"\n{Fore.GREEN}You defeated the {self.enemy_name}!{Style.RESET_ALL}")
                        break
                
                elif choice == '2':  # Use item
                    if not player.inventory:
                        print(f"\n{Fore.RED}You don't have any items!{Style.RESET_ALL}")
                    else:
                        print(f"\n{Fore.YELLOW}Your inventory:{Style.RESET_ALL}")
                        for i, item in enumerate(player.inventory, 1):
                            print(f"{i}. {Fore.CYAN}{item}{Style.RESET_ALL}")
                        
                        item_choice = input(f"\n{Fore.WHITE}Which item do you want to use? (Enter number or 0 to cancel): {Style.RESET_ALL}")
                        
                        try:
                            item_idx = int(item_choice) - 1
                            if 0 <= item_idx < len(player.inventory):
                                item = player.inventory[item_idx]
                                
                                if item == "Health Potion":
                                    player.heal(30)
                                    player.remove_item(item)
                                    print(f"\n{Fore.GREEN}You used a Health Potion and recovered 30 health!{Style.RESET_ALL}")
                                elif item == "Sword":
                                    player_damage = random.randint(15, 25)
                                    self.enemy_health -= player_damage
                                    print(f"\n{Fore.GREEN}You attack with your Sword for {player_damage} damage!{Style.RESET_ALL}")
                                    
                                    if self.enemy_health <= 0:
                                        slow_print(f"\n{Fore.GREEN}You defeated the {self.enemy_name}!{Style.RESET_ALL}")
                                        break
                                else:
                                    print(f"\n{Fore.YELLOW}You can't use that item in combat!{Style.RESET_ALL}")
                        except (ValueError, IndexError):
                            print(f"\n{Fore.RED}Invalid choice.{Style.RESET_ALL}")
                
                elif choice == '3':  # Run away
                    escape_chance = random.random()
                    if escape_chance > 0.5:
                        print(f"\n{Fore.GREEN}You successfully escaped from the {self.enemy_name}!{Style.RESET_ALL}")
                        return False  # Event not fully triggered
                    else:
                        print(f"\n{Fore.RED}You failed to escape!{Style.RESET_ALL}")
                
                else:
                    print(f"\n{Fore.RED}Invalid choice.{Style.RESET_ALL}")
                
                # Enemy's turn
                if self.enemy_health > 0:
                    enemy_damage = random.randint(5, self.damage)
                    player.take_damage(enemy_damage)
                    print(f"\n{Fore.RED}The {self.enemy_name} attacks you for {enemy_damage} damage!{Style.RESET_ALL}")
                    
                    if player.health <= 0:
                        slow_print(f"\n{Fore.RED}You were defeated by the {self.enemy_name}!{Style.RESET_ALL}")
                        break
            
            self.triggered = True
            return True
        
        return False

def create_game_world():
    """Create the game world with locations and events."""
    # Create locations
    forest_entrance = Location("Forest Entrance", 
                         "You stand at the entrance of a dense, mysterious forest. The trees tower above you, their leaves rustling in the gentle breeze. A narrow path leads deeper into the woods.")
    
    forest_clearing = Location("Forest Clearing",
                         "You find yourself in a small clearing within the forest. Sunlight filters through the canopy, illuminating a patch of wildflowers. You notice some movement in the bushes nearby.")
    
    dark_cave = Location("Dark Cave",
                   "The cave is damp and cold. Stalactites hang from the ceiling, and the sound of dripping water echoes around you. Your footsteps disturb small creatures that scurry away into the darkness.")
    
    underground_lake = Location("Underground Lake",
                          "A vast underground lake stretches before you, its surface still as glass. The ceiling above is studded with bioluminescent fungi that cast an eerie blue glow over everything.")
    
    ancient_ruins = Location("Ancient Ruins",
                       "Crumbling stone structures rise from the forest floor. These ruins appear to be centuries old, with strange symbols carved into the weathered stones. You sense powerful magic lingering here.")
    
    mountain_pass = Location("Mountain Pass",
                       "The narrow path winds between towering cliff faces. The air is thin and cold at this altitude. Below, you can see the entire forest stretching to the horizon.")
    
    hidden_temple = Location("Hidden Temple",
                       "This ancient temple is remarkably well-preserved. Golden idols and elaborate mosaics line the walls, depicting scenes of great battles and mystical rituals. A pedestal stands at the center of the room.")
    
    # Connect locations
    forest_entrance.add_connection("north", forest_clearing)
    
    forest_clearing.add_connection("south", forest_entrance)
    forest_clearing.add_connection("east", dark_cave)
    forest_clearing.add_connection("west", ancient_ruins)
    
    dark_cave.add_connection("west", forest_clearing)
    dark_cave.add_connection("north", underground_lake)
    
    underground_lake.add_connection("south", dark_cave)
    
    ancient_ruins.add_connection("east", forest_clearing)
    ancient_ruins.add_connection("north", mountain_pass)
    
    mountain_pass.add_connection("south", ancient_ruins)
    mountain_pass.add_connection("north", hidden_temple)
    
    hidden_temple.add_connection("south", mountain_pass)
    
    # Add items
    forest_entrance.add_item("Map")
    forest_clearing.add_item("Health Potion")
    dark_cave.add_item("Torch")
    ancient_ruins.add_item("Ancient Key")
    mountain_pass.add_item("Sword")
    
    # Add events
    forest_clearing.add_event(Event("A deer watches you cautiously from between the trees before bounding away."))
    dark_cave.add_event(Combat("A giant bat swoops down from the ceiling!", "Giant Bat", 50, 10))
    underground_lake.add_event(Event("You spot a glimmer beneath the surface of the lake. It might be worth investigating."))
    ancient_ruins.add_event(Event("The symbols on the wall begin to glow with an unearthly light as you approach."))
    mountain_pass.add_event(Combat("A mountain troll blocks your path!", "Mountain Troll", 80, 15))
    hidden_temple.add_event(Event("The pedestal seems designed to hold something. Perhaps the ancient artifact you seek?"))
    
    return forest_entrance

def show_help():
    """Display available commands."""
    print(f"\n{Fore.CYAN}Available Commands:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}look{Style.RESET_ALL} - Look around your current location")
    print(f"{Fore.GREEN}go [direction]{Style.RESET_ALL} - Move in a direction (north, south, east, west)")
    print(f"{Fore.GREEN}take [item]{Style.RESET_ALL} - Pick up an item")
    print(f"{Fore.GREEN}inventory{Style.RESET_ALL} - Check your inventory")
    print(f"{Fore.GREEN}health{Style.RESET_ALL} - Check your health")
    print(f"{Fore.GREEN}use [item]{Style.RESET_ALL} - Use an item")
    print(f"{Fore.GREEN}help{Style.RESET_ALL} - Show this help message")
    print(f"{Fore.GREEN}quit{Style.RESET_ALL} - Exit the game")
    print()

def main():
    """Main game function."""
    clear_screen()
    print_header()
    
    # Introduction
    slow_print(f"{Fore.CYAN}Welcome to the Text Adventure!{Style.RESET_ALL}")
    print()
    slow_print(f"{Fore.WHITE}You are about to embark on a perilous journey to find the legendary Crystal of Power.{Style.RESET_ALL}")
    slow_print(f"{Fore.WHITE}Legend says it's hidden deep within an ancient temple, guarded by fearsome creatures.{Style.RESET_ALL}")
    slow_print(f"{Fore.WHITE}Your choices will determine your fate. Choose wisely...{Style.RESET_ALL}")
    print()
    
    # Get player name
    player_name = input(f"{Fore.YELLOW}Enter your name, brave adventurer: {Style.RESET_ALL}")
    player = Player(player_name)
    
    # Create game world
    start_location = create_game_world()
    player.location = start_location
    
    # Show initial location description
    clear_screen()
    print_header()
    print(player.location.describe())
    
    # Main game loop
    game_running = True
    while game_running and player.health > 0:
        # Check for events at the current location
        for event in player.location.events:
            if not event.triggered:
                event.trigger(player)
                time.sleep(1)
        
        # Get player command
        command = input(f"\n{Fore.GREEN}What will you do? {Style.RESET_ALL}").lower().strip()
        
        if command == "quit":
            sure = input(f"{Fore.RED}Are you sure you want to quit? (y/n): {Style.RESET_ALL}").lower()
            if sure.startswith('y'):
                game_running = False
        
        elif command == "help":
            show_help()
        
        elif command == "look":
            print(player.location.describe())
        
        elif command.startswith("go "):
            direction = command[3:].strip()
            if direction in player.location.connections:
                player.location = player.location.connections[direction]
                clear_screen()
                print_header()
                print(player.location.describe())
            else:
                print(f"{Fore.RED}You can't go that way.{Style.RESET_ALL}")
        
        elif command.startswith("take "):
            item = command[5:].strip()
            if item in player.location.items:
                player.add_item(item)
                player.location.remove_item(item)
                print(f"{Fore.GREEN}You took the {item}.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}There's no {item} here.{Style.RESET_ALL}")
        
        elif command == "inventory":
            if player.inventory:
                print(f"{Fore.YELLOW}You are carrying:{Style.RESET_ALL}")
                for item in player.inventory:
                    print(f"- {Fore.CYAN}{item}{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}Your inventory is empty.{Style.RESET_ALL}")
        
        elif command == "health":
            health_color = Fore.GREEN if player.health > 50 else Fore.YELLOW if player.health > 25 else Fore.RED
            print(f"{Fore.WHITE}Your health: {health_color}{player.health}/100{Style.RESET_ALL}")
        
        elif command.startswith("use "):
            item = command[4:].strip()
            if player.has_item(item):
                if item == "Health Potion":
                    player.heal(30)
                    player.remove_item(item)
                    print(f"{Fore.GREEN}You used the Health Potion and recovered 30 health!{Style.RESET_ALL}")
                elif item == "Torch" and player.location.name == "Dark Cave":
                    print(f"{Fore.YELLOW}You light the torch, illuminating the cave. You notice a small passage you missed before.{Style.RESET_ALL}")
                elif item == "Map":
                    print(f"{Fore.YELLOW}You consult the map. It shows the general layout of the area, but some parts are faded or missing.{Style.RESET_ALL}")
                elif item == "Ancient Key" and player.location.name == "Hidden Temple":
                    print(f"{Fore.YELLOW}You insert the key into a hidden keyhole on the pedestal. With a rumble, the pedestal opens to reveal...{Style.RESET_ALL}")
                    time.sleep(2)
                    print(f"{Fore.CYAN}The Crystal of Power! You've found it!{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}Congratulations, {player.name}! You've completed your quest and found the legendary artifact!{Style.RESET_ALL}")
                    
                    time.sleep(2)
                    game_running = False  # End the game
                else:
                    print(f"{Fore.YELLOW}You can't use that item here.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}You don't have that item.{Style.RESET_ALL}")
        
        else:
            print(f"{Fore.RED}I don't understand that command. Type 'help' for a list of commands.{Style.RESET_ALL}")
    
    # Game over
    if player.health <= 0:
        print(f"\n{Fore.RED}Game Over! Your health reached zero.{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.CYAN}Thanks for playing!{Style.RESET_ALL}")

if __name__ == "__main__":
    main() 