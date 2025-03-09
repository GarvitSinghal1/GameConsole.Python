#!/bin/bash

echo "Starting Python Game Console..."
echo "You will be asked to choose between Terminal or GUI mode."
echo ""
python3 main.py "$@"

if [ $? -ne 0 ]; then
    echo "Failed to start the game console."
    echo "Please make sure Python 3 is installed and in your PATH."
    read -p "Press Enter to continue..."
fi 