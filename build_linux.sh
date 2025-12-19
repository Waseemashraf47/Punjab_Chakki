#!/bin/bash

# Define virtual env path
VENV_PATH="./virt"
PYTHON_BIN="$VENV_PATH/bin/python"
PIP_BIN="$VENV_PATH/bin/pip"
PYINSTALLER_BIN="$VENV_PATH/bin/pyinstaller"

# Check if virtual env exists
if [ ! -d "$VENV_PATH" ]; then
    echo "Virtual environment not found at $VENV_PATH. Please create it or adjust the script."
    exit 1
fi

# Install PyInstaller if not present (although we did it manually, good to have in script)
if [ ! -f "$PYINSTALLER_BIN" ]; then
    echo "PyInstaller not found. Installing..."
    "$PIP_BIN" install pyinstaller
fi

# Clean previous build
rm -rf build dist *.spec

# Build for Linux
# --onefile: Create a single executable
# --windowed: No console window (GUI app)
# --name: Name of the executable
# --add-data: Include the ui folder (if needed, but imports usually handled)
# We might need to handle the database location. PyInstaller runs in a temp dir.
# The app looks for 'punjab_chakki.db' in the current working directory usually.
# If we want it bundled we use --add-data, but for a DB that needs writing, 
# it should stay outside the exe or in a user data dir. 
# The request implies just running the app. I'll keep the DB external for persistence 
# as is standard for simple SQLite apps unless specified otherwise.
# Using --collect-all for tkinter just in case, though usually auto-detected.

echo "Building Linux executable..."
"$PYINSTALLER_BIN" --noconfirm --onefile --windowed --name "Punjab_Chakki" \
    --hidden-import "PIL" \
    --hidden-import "PIL._tkinter_finder" \
    --collect-all "tkinter" \
    --collect-all "ui" \
    main.py

echo "Build complete. Executable is in dist/Punjab_Chakki"
