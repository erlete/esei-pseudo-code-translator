# Pseudo Code Translator

This repository contains a collection of scripts that allow the user to translate pseudo code to Python scripts and execute them in order to determine their output.

## Installation

### Executable version (binary file)

The executable version of this package does not require any dependencies, sice the `.exe` file contains all libraries and the Python interpreter itself.

The binary file can be found in the latest release of this repository. It is recommended to download the latest version of the package, since it will contain the latest bug fixes and improvements.

_**Note:** the executable version is only available for Windows. It will not be available for macOS/UNIX._

## Usage

### Executable version

The `.exe` file can be executed by double clicking it. It will open a GUI window that will allow the user to translate and execute pseudo code. All information on how to use the software can be found in the "Usage instructions" section of the window.

_**Note:** the executable version might be flagged as a virus by some antivirus software (and even Windows Defender). This is due to the fact that the executable file contains the Python interpreter and all required libraries. Furthermore, it is not signed, so it might be considered a threat. This is a false positive, since the executable file is safe to use (the source code is available for inspection)._

## Translation support

### Data types

| Data type | Translation | Supported |
| :-------: | :---------: | :-------: |
| `Entero` | `int` | ✅ |
| `Real` | `float` | ✅ |
| `Caracter` | `str` | ✅ |
| `Cadena` | `str` | ✅ |
| `Logico` | `bool` | ✅ |
| `Registro` | `class` | ✅ |

### Operators

| Operation | Symbol | Translation | Supported |
| :-------: | :----: | :---------: | :-------: |
| Assignment | `<-` | `=` | ✅ |
| Addition | `+`[^1] | `+` | ✅ |
| Subtraction | `-`[^1] | `-` | ✅ |
| Multiplication | `*`[^1] | `*` | ✅ |
| Division | `/`[^1] | `/` | ✅ |
| Modulus | `MOD` | `%` | ✅ |
| Equalto | `=` | `==` | ✅ |
| Different from | `<>` | `!=` | ✅ |
| Lower than | `<`[^1] | `<` | ✅ |
| Greater than | `>`[^1] | `>` | ✅ |
| Lower than or equal to | `<=` | `<=` | ✅ |
| Greater than or equal to | `>=` | `>=` | ✅ |

### Methods

| Method | Translation | Supported |
| :----: | :---------: | :-------: |
| `ESCRIBIR` | `print` | ✅ |
| `LEER` | `input` | ✅ |

### Control statements

| Statement | Structure | Translation | Supported |
| :-------: | :-------: | :---------: | :-------: |
| Conditional | `SI...ENTONCES` | `if` | ✅ |
| While | `MIENTRAS...HACER` | `while` | ✅ |
| Do While | `HACER...MIENTRAS` | `do while`[^2] | ✅ |
| For | `DESDE...HASTA` | `from` | ✅ |
| Match | `CASO...SEA` | `match` | ✅ |
| Function | `FUNCION...` | `def`[^3] | ✅ |
| Procedure | `PROCEDIMIENTO...` | `def`[^3] | ✅ |
| Main function[^4] | `INICIO...FIN` | `def main()` | ✅ |

## Disclaimer

**This software serves as educative tool for the author, as well as a tool for users to learn how to translate pseudo code to Python. The software is provided "as is", without warranty of any kind, and shall not be related to any external entities and/or their products.**

**The author does not guarantee the correct operation of the software in any scenario excluded from the internal testing process. The author will not be liable for any repercusions the usage of this software might have on the user.**

**The source code is available for inspection and vulnerability reports. The source code is available for commercial use, patent use, private use, modification and distribution on the conditions stated in the _GNU Affero General Public License v3.0_, available [here](LICENSE).**

[^1]: The `+`, `-`, `*` and `/` operators are not explicitely translated, since they are equivalent to the corresponding Python operators, but they are formatted adding spacing between the operands and the operator.

[^2]: The `do while` block is translated to a combination of the code inside the `do while` structure followd by a `while` block with the same code and condition, since the `do while` structure is not supported by Python.

[^3]: Functions and procedures with pointers as parameters are simulated using the `globals` keyword, since Python does not support pointers.

[^4]: All programs must contain a `INICIO...FIN` block, which will be translated to a `main` function. If the code does not contain such method, non-block elements will be skipped.
