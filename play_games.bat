@echo off
echo Starting Python Game Console...
echo You will be asked to choose between Terminal or GUI mode.
echo.
python main.py %*
if errorlevel 1 (
    echo Failed to start the game console.
    echo Please make sure Python is installed and in your PATH.
    pause
) 