#!/bin/bash
# Launcher script for the Hunting Exam Preparation application
# Sets up the library path and environment variables for tkinter

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIB_PATH="$SCRIPT_DIR/.local/lib"

# Set environment variables for tkinter
export LD_LIBRARY_PATH="$LIB_PATH:${LD_LIBRARY_PATH}"
export TCL_LIBRARY="$LIB_PATH/tcl8.6"
export TK_LIBRARY="$LIB_PATH/tk8.6"

# Run the application using the virtual environment Python
"$SCRIPT_DIR/.venv/bin/python" "$SCRIPT_DIR/main.py" "$@"
