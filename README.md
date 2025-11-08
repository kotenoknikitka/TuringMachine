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

### Directions:
- **`>`** - move right
- **`<`** - move left  
- **`.`** - stay in place
- **`!`** - stop execution

**Important:** The blank symbol (representing empty cells on the infinite tape) is represented as underscore `_` in the transition table.

### Examples:

- `1 q2 >` - write symbol `1`, transition to state `q2`, move right
- `_ q0 <` - write blank symbol, transition to state `q0`, move left  
- `0 q1 .` - write symbol `0`, transition to state `q1`, stay in place

## 🛠 Technical Details

*   **Deterministic Turing Machine** implementation
*   **Infinite tape support** in both directions
*   Blank symbol: `_` (underscore) represents empty cells
*   **History limitation** to prevent memory leaks
*   **Transition validation** with clear error messages
*   **State persistence** for programs and tapes

## 🤝 Contributing

Contributions are welcome! Particularly appreciated:

*   New algorithm examples
*   UI/UX improvements  
*   Bug fixes and optimizations
