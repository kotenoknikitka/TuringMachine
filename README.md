# Turing Machine with Graphical Interface

A complete implementation of a deterministic Turing Machine with an intuitive graphical interface built in Python. Features a visual transition table editor, step-by-step execution, and change rollback capability. Includes implementations of complex algorithms like bubble sort and Sieve of Eratosthenes.

## ✨ Features

- **Full-Featured GUI**: Visual transition table editor with real-time editing
- **Interactive Tape Display**: Real-time tape visualization with automatic scrolling
- **Flexible Control**:
  - Step-by-step execution (forward/backward)
  - Auto-run mode with adjustable speed
  - Save/load programs and tape states
- **Algorithm Examples**:
  - Bubble Sort
  - Sieve of Eratosthenes
- **Extensible Architecture**: Easy to add new algorithms and functionality

## 🚀 Quick Start

### Requirements
- Python 3.7+
- Libraries: `tkinter` (usually included in standard Python distribution)

### Installation & Run
```bash
git clone https://github.com/kotenoknikitka/TuringMachine.git
cd turing-machine
python main.py
```

# 🎮 How to Use

## Interface Overview

*   **Transition Table** - Edit states, symbols, and transitions.
*   **Tape Visualization** - Current tape state with highlighted head position.
*   **Control Panel:**
    *   Step forward/backward
    *   Run/pause automatic execution
    *   Reset machine state
    *   Save/load programs
*   **Info Panel** - Current state and step counter.

## Creating Your First Program

1.  Click **"Add State"** to create new states.
2.  Click **"Add Symbol"** to expand the alphabet.
3.  Fill transition table cells in the format: `symbol state direction`.
4.  Click **"Apply Table"** to save transitions.
5.  Create initial tape via **"Create Tape"**.
6.  Start execution!

## 💡 Transition Format

Each cell in the transition table follows the format:

`<write_symbol> <next_state> <direction>`

### Parameters:
- **`write_symbol`** - symbol to write to the current tape cell
- **`next_state`** - state to transition to  
- **`direction`** - move direction: `<` (left), `>` (right), `.` (stay) or `!` (stop machine)

## 🛠 Technical Details

*   **Deterministic Turing Machine** implementation
*   **Infinite tape support** in both directions
*   **History limitation** to prevent memory leaks
*   **Transition validation** with clear error messages
*   **State persistence** for programs and tapes

## 🤝 Contributing

Contributions are welcome! Particularly appreciated:

*   New algorithm examples
*   UI/UX improvements  
*   Bug fixes and optimizations
