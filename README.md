# Esoteric Pascal Interpreter

A complete interpreter for a Pascal-like esoteric programming language implemented in Python. The interpreter supports variables, functions, recursion, conditionals, loops, and comprehensive error handling.

## Features

- Variables with INTEGER and REAL types
- Arithmetic expressions with standard operators
- User-defined functions with parameters
- Recursive function calls
- Conditional statements (IF-THEN-ELSE)
- Loop constructs (WHILE, FOR...TO, FOR...DOWNTO)
- Boolean expressions with logical operators (AND, OR, NOT)
- Comparison operators (=, <>, <, >, <=, >=)
- Multi-line comments using curly braces
- Line and column tracking for error reporting

## Installation

```bash
# Clone the repository
git clone https://github.com/VamshiNarmety/esoteric_interpreter.git
cd esoteric_interpreter

# Install dependencies (required for testing only)
pip install -r requirements.txt
```

## Usage

### Running Programs from Files

Execute a program stored in a text file:

```bash
python3 run_interpreter.py program.txt
```

### Interactive REPL Mode

Launch the interactive interpreter:

```bash
python3 run_interpreter.py
```

Available commands in REPL mode:
- `show` - Display all global variables and their values
- `clear` - Reset all variables to empty state
- `help` - Show help information
- `exit` - Exit the interpreter

## Language Syntax

### Program Structure

```pascal
PROGRAM ProgramName;
VAR
    x, y : INTEGER;
    result : REAL;

FUNCTION Add(a : INTEGER; b : INTEGER) : INTEGER;
BEGIN
    Add := a + b
END;

BEGIN
    x := 10;
    y := 20;
    result := Add(x, y)
END.
```

### Variables

Variables must be declared before use with INTEGER or REAL types:

```pascal
VAR
    count : INTEGER;
    price, total : REAL;
```

### Functions

Functions support parameters and return values. The return value is assigned by setting the function name to a value:

```pascal
FUNCTION Factorial(n : INTEGER) : INTEGER;
BEGIN
    IF n <= 1 THEN
        Factorial := 1
    ELSE
        Factorial := n * Factorial(n - 1)
    END
END;
```

### Conditional Statements

```pascal
IF x > 10 THEN
    y := x * 2
ELSE
    y := x / 2
END;
```

### Loops

WHILE loops:
```pascal
WHILE x < 100 DO
BEGIN
    x := x + 1
END;
```

FOR loops with TO:
```pascal
FOR i := 1 TO 10 DO
    sum := sum + i;
```

FOR loops with DOWNTO:
```pascal
FOR i := 10 DOWNTO 1 DO
    sum := sum + i;
```

### Comments

Comments are enclosed in curly braces and can span multiple lines:

```pascal
{ This is a single-line comment }

{
    This is a multi-line
    comment block
}
```

## Example Program

```pascal
PROGRAM Example;
VAR
    n, factorial, fib : INTEGER;

FUNCTION Fact(x : INTEGER) : INTEGER;
BEGIN
    IF x <= 1 THEN
        Fact := 1
    ELSE
        Fact := x * Fact(x - 1)
    END
END;

FUNCTION Fib(n : INTEGER) : INTEGER;
VAR
    a, b, temp, i : INTEGER;
BEGIN
    a := 0;
    b := 1;
    FOR i := 1 TO n DO
    BEGIN
        temp := a + b;
        a := b;
        b := temp
    END;
    Fib := a
END;

BEGIN
    n := 6;
    factorial := Fact(n);
    fib := Fib(10)
END.
```

Save this as `example.txt` and run with:
```bash
python3 run_interpreter.py example.txt
```

## Error Handling

The interpreter provides detailed error messages with line and column information:

```
LexerError at line 5, column 12: Invalid character '@'
ParserError: Expected token 'END', got 'BEGIN'
SemanticError: Undefined function 'Calculate'
RuntimeError: Division by zero
```

## Testing

Run the complete test suite:

```bash
pytest tests/ -v
```

Run specific test categories:

```bash
pytest tests/test_functions.py -v
pytest tests/test_loops.py -v
pytest tests/test_errors.py -v
```

## Project Structure

```
esoteric_interpreter/
├── src/
│   ├── lexer/
│   │   ├── lexer.py           # Tokenization and lexical analysis
│   │   └── token.py           # Token definitions
│   ├── parser/
│   │   ├── parser.py          # Syntax analysis and AST construction
│   │   └── ast_nodes.py       # AST node definitions
│   ├── semantic/
│   │   ├── semantic_analyzer.py  # Semantic validation
│   │   └── symbols.py         # Symbol table implementation
│   ├── interpreter/
│   │   ├── interpreter.py     # AST execution engine
│   │   └── activation_record.py  # Function call management
│   └── errors.py              # Custom exception classes
├── tests/                     # Comprehensive test suite
├── run_interpreter.py         # Main executable script
├── example.txt                # Example program
├── grammar.txt                # Complete language grammar
└── README.md                  # This file
```

## Architecture

The interpreter follows a multi-stage architecture:

1. **Lexer**: Converts source code into tokens
2. **Parser**: Builds an Abstract Syntax Tree (AST) from tokens
3. **Semantic Analyzer**: Validates types, scopes, and symbol definitions
4. **Interpreter**: Executes the AST using the visitor pattern

## Language Grammar

For the complete formal grammar specification, see [grammar.txt](grammar.txt).