# Pseudo Code Parser

This repository contains a collection of scripts that allow the user to translate pseudo code snippets to Python scripts and execute them in order to determine their output, which is printed on-screen.

## Installation

_This repository does not require any third-party dependencies, just basic Python modules._

### macOS / UNIX

```bash
# Remember to move to a valid working directory!
git clone https://github.com/erlete/pseudo-code-parser
cd pseudo-code-parser

# Virtual environment setup (recommended):
python3 -m venv .venv
source .venv/bin/activate

# Dependency installation:
python3 -m pip install -r requirements.txt

# Application execution:
python3 main.py
```

### Windows

Installation on Windows is the same as in macOS / UNIX but you have to ensure that Git and Python are installed on your device.

## Usage

Usage instructions are as simple as possible:

1. Execute `main.py` and run the application.
2. Copy the pseudo code snippet you want to translate.
3. Paste it in the text box on the left side of the application.
4. Visualize parsed output on the right side of the application.
5. Execute your code using the "Execute code" button.
6. Visualize executed output at the bottom of the application.
7. Clear the input using the "Clear text" button.
8. Repeat as many times as you want!

## Support

### Operators

| Symbol | Parsed symbol |        Identifier        | Supported |
| :----: | :-----------: | :----------------------: | :-------: |
|  `<-`  |      `=`      |        Assignment        |     ✅     |
|  `+`   |      `+`      |         Addition         |     ✅     |
|  `-`   |      `-`      |       Subtraction        |     ✅     |
|  `*`   |      `*`      |      Multiplication      |     ✅     |
|  `/`   |      `/`      |         Division         |     ✅     |
| `MOD`  |      `%`      |         Modulus          |     ✅     |
|  `=`   |     `==`      |         Equalto          |     ✅     |
|  `<>`  |     `!=`      |      Different from      |     ✅     |
|  `<`   |      `<`      |        Lower than        |     ✅     |
|  `>`   |      `>`      |       Greater than       |     ✅     |
|  `<=`  |     `<=`      |  Lower than or equal to  |     ✅     |
|  `>=`  |     `>=`      | Greater than or equal to |     ✅     |

### Control statements

|       Statement        | Parsed statement |    Identifier    | Supported |
| :--------------------: | :--------------: | :--------------: | :-------: |
|          `SI`          |       `if`       |   If statement   |     ❌     |
|        `SI_NO`         |      `else`      |  Else statement  |     ❌     |
|         `CASO`         |     `switch`     | Switch statement |     ❌     |
| `DESDE...HASTA...PASO` |      `for`       |     For loop     |     ✅     |
|   `MIENTRAS...HACER`   |     `while`      |    While loop    |     ❌     |
|   `HACER...MIENTRAS`   |       `do`       |  Do-while loop   |     ❌     |

### Other statements

| Statement  | Parsed statement |   Identifier    | Supported |
| :--------: | :--------------: | :-------------: | :-------: |
| `ESCRIBIR` |     `print`      | Print statement |     ✅     |
|   `LEER`   |     `input`      | Input statement |     ❌     |

## Disclaimer

Programs contained in this repository are tested against specific pseudo code syntax and rules, any slight variation of said parameters might result on innacurate results or unexpected program crashes. The author should not be, in any way, related to the output of the programs and/or made responsible for their usage, as they are just a tool.
