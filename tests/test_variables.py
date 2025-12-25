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

def test_simple_assignment():
    Interpreter.GLOBAL_SCOPE.clear()
    interpret('''
        PROGRAM Test;
        BEGIN
            a := 5
        END.
    ''')
    assert Interpreter.GLOBAL_SCOPE['a'] == 5

def test_multiple_assignments():
    Interpreter.GLOBAL_SCOPE.clear()
    interpret('''
        PROGRAM Test;
        BEGIN
            x := 2;
            y := 3;
            z := x + y
        END.
    ''')
    assert Interpreter.GLOBAL_SCOPE['x'] == 2
    assert Interpreter.GLOBAL_SCOPE['y'] == 3
    assert Interpreter.GLOBAL_SCOPE['z'] == 5

def test_complex_expression_with_variables():
    Interpreter.GLOBAL_SCOPE.clear()
    interpret('''
        PROGRAM Test;
        BEGIN
            a := 2;
            b := 10 * a + 10 * a
        END.
    ''')
    assert Interpreter.GLOBAL_SCOPE['a'] == 2
    assert Interpreter.GLOBAL_SCOPE['b'] == 40

def test_nested_begin_end():
    Interpreter.GLOBAL_SCOPE.clear()
    interpret('''
        PROGRAM Test;
        BEGIN
            BEGIN
                number := 2
            END;
            a := number;
            b := 10 * a + 10 * number
        END.
    ''')
    assert Interpreter.GLOBAL_SCOPE['number'] == 2
    assert Interpreter.GLOBAL_SCOPE['a'] == 2
    assert Interpreter.GLOBAL_SCOPE['b'] == 40

def test_variable_reassignment():
    Interpreter.GLOBAL_SCOPE.clear()
    interpret('''
        PROGRAM Test;
        BEGIN
            x := 5;
            x := x + 3;
            x := x * 2
        END.
    ''')
    assert Interpreter.GLOBAL_SCOPE['x'] == 16

def test_multiple_variables_in_expression():
    Interpreter.GLOBAL_SCOPE.clear()
    interpret('''
        PROGRAM Test;
        BEGIN
            a := 3;
            b := 4;
            c := 5;
            result := a + b * c
        END.
    ''')
    assert Interpreter.GLOBAL_SCOPE['result'] == 23

def test_variables_with_unary_operators():
    Interpreter.GLOBAL_SCOPE.clear()
    interpret('''
        PROGRAM Test;
        BEGIN
            x := 10;
            result := -x + 5
        END.
    ''')
    assert Interpreter.GLOBAL_SCOPE['result'] == -5
