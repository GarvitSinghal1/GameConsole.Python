#!/usr/bin/env python3
"""
2048 game package.
This package contains both terminal and GUI versions of the 2048 game.
"""

# Import the main modules to make them available directly from the package
from games.game_2048.game_2048 import main as terminal_main
from games.game_2048.game_2048_gui import main as gui_main 