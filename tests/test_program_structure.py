import pytest
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.interpreter.interpreter import Interpreter

def interpret(text):
    """Helper to interpret text and return result variable."""
    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpret()
    return Interpreter.GLOBAL_SCOPE.get('result')

def test_program_with_var_declarations():
    Interpreter.GLOBAL_SCOPE.clear()
    interpret('''
        PROGRAM Part10;
        VAR
            a, b, result : INTEGER;
            c : REAL;
        BEGIN
            a := 5;
            b := 10;
            c := 2.5;
            result := a + b
        END.
    ''')
    assert Interpreter.GLOBAL_SCOPE['a'] == 5
    assert Interpreter.GLOBAL_SCOPE['b'] == 10
    assert Interpreter.GLOBAL_SCOPE['c'] == 2.5
    assert Interpreter.GLOBAL_SCOPE['result'] == 15

def test_integer_division():
    result = interpret('''
        PROGRAM Test;
        VAR result : INTEGER;
        BEGIN
            result := 7 DIV 2
        END.
    ''')
    assert result == 3

def test_float_division_with_slash():
    result = interpret('''
        PROGRAM Test;
        VAR result : REAL;
        BEGIN
            result := 7 / 2
        END.
    ''')
    assert result == 3.5

def test_real_number_addition():
    result = interpret('''
        PROGRAM Test;
        VAR result : REAL;
        BEGIN
            result := 3.14 + 2.86
        END.
    ''')
    assert result == 6.0

def test_real_number_multiplication():
    result = interpret('''
        PROGRAM Test;
        VAR result : REAL;
        BEGIN
            result := 2.5 * 4.0
        END.
    ''')
    assert result == 10.0

def test_mixed_integer_real_operations():
    result = interpret('''
        PROGRAM Test;
        VAR result : REAL;
        BEGIN
            result := 5 + 2.5
        END.
    ''')
    assert result == 7.5

def test_multiple_var_declarations():
    Interpreter.GLOBAL_SCOPE.clear()
    interpret('''
        PROGRAM Test;
        VAR
            x, y, z : INTEGER;
            a, b, result : REAL;
        BEGIN
            x := 1;
            y := 2;
            z := 3;
            a := 1.5;
            b := 2.5;
            result := x + y + z
        END.
    ''')
    assert Interpreter.GLOBAL_SCOPE['x'] == 1
    assert Interpreter.GLOBAL_SCOPE['y'] == 2
    assert Interpreter.GLOBAL_SCOPE['z'] == 3
    assert Interpreter.GLOBAL_SCOPE['a'] == 1.5
    assert Interpreter.GLOBAL_SCOPE['b'] == 2.5
    assert Interpreter.GLOBAL_SCOPE['result'] == 6

def test_integer_div_vs_float_div():
    Interpreter.GLOBAL_SCOPE.clear()
    interpret('''
        PROGRAM Test;
        VAR
            a, b : INTEGER;
        BEGIN
            a := 10 DIV 3;
            b := 10 / 3
        END.
    ''')
    assert Interpreter.GLOBAL_SCOPE['a'] == 3
    assert abs(Interpreter.GLOBAL_SCOPE['b'] - 3.333333) < 0.0001

def test_complex_program():
    Interpreter.GLOBAL_SCOPE.clear()
    interpret('''
        PROGRAM Complex;
        VAR
            number : INTEGER;
            a, b, c : INTEGER;
            x, y : REAL;
        BEGIN
            BEGIN
                number := 2;
                a := number;
                b := 10 * a + 10 * number;
            END;
            x := 11 / 2;
            y := 11 DIV 2;
            c := a + b
        END.
    ''')
    assert Interpreter.GLOBAL_SCOPE['number'] == 2
    assert Interpreter.GLOBAL_SCOPE['a'] == 2
    assert Interpreter.GLOBAL_SCOPE['b'] == 40
    assert Interpreter.GLOBAL_SCOPE['x'] == 5.5
    assert Interpreter.GLOBAL_SCOPE['y'] == 5
    assert Interpreter.GLOBAL_SCOPE['c'] == 42

def test_case_insensitive_program_keyword():
    result = interpret('''
        program Test;
        var result : integer;
        begin
            result := 42
        end.
    ''')
    assert result == 42

def test_case_insensitive_var_declarations():
    Interpreter.GLOBAL_SCOPE.clear()
    interpret('''
        PROGRAM Test;
        var
            x : integer;
            y : real;
        begin
            x := 5;
            y := 3.14
        end.
    ''')
    assert Interpreter.GLOBAL_SCOPE['x'] == 5
    assert Interpreter.GLOBAL_SCOPE['y'] == 3.14

def test_program_without_var_section():
    result = interpret('''
        PROGRAM SimpleTest;
        VAR result : INTEGER;
        BEGIN
            result := 100
        END.
    ''')
    assert result == 100

def test_var_declarations_with_expressions():
    Interpreter.GLOBAL_SCOPE.clear()
    interpret('''
        PROGRAM Test;
        VAR
            x, y, z : INTEGER;
        BEGIN
            x := 10;
            y := 20;
            z := (x + y) * 2
        END.
    ''')
    assert Interpreter.GLOBAL_SCOPE['z'] == 60

def test_real_with_integer_div():
    result = interpret('''
        PROGRAM Test;
        VAR
            x, result : REAL;
        BEGIN
            x := 10.0 DIV 3.0;
            result := x
        END.
    ''')
    assert result == 3

def test_multiple_real_operations():
    result = interpret('''
        PROGRAM Test;
        VAR
            a, b, c, result : REAL;
        BEGIN
            a := 1.5;
            b := 2.5;
            c := a * b + 3.0;
            result := c
        END.
    ''')
    assert result == 6.75
