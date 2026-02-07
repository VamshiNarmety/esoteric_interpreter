"""Tests for loop statements (WHILE and FOR)."""
import pytest
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.interpreter.interpreter import Interpreter

def interpret(text):
    """Helper to interpret Pascal code."""
    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpret()
    return interpreter.GLOBAL_SCOPE

def test_simple_while_loop():
    """Test simple WHILE loop."""
    text = """
    PROGRAM Test;
    VAR
        counter, sum : INTEGER;
    BEGIN
        counter := 1;
        sum := 0;
        WHILE counter <= 5 DO
        BEGIN
            sum := sum + counter;
            counter := counter + 1
        END
    END.
    """
    res = interpret(text)
    assert res.get('sum') == 15  # 1+2+3+4+5
    assert res.get('counter') == 6

def test_while_with_complex_condition():
    """Test WHILE loop with complex boolean condition."""
    text = """
    PROGRAM Test;
    VAR
        x, result : INTEGER;
    BEGIN
        x := 0;
        result := 0;
        WHILE (x < 10) AND (result < 20) DO
        BEGIN
            x := x + 1;
            result := result + x
        END
    END.
    """
    res = interpret(text)
    assert res.get('result') == 21  # 1+2+3+4+5+6

def test_for_loop_to():
    """Test FOR loop with TO."""
    text = """
    PROGRAM Test;
    VAR
        i, sum : INTEGER;
    BEGIN
        sum := 0;
        FOR i := 1 TO 5 DO
            sum := sum + i
    END.
    """
    res = interpret(text)
    assert res.get('sum') == 15  # 1+2+3+4+5
    assert res.get('i') == 6  # Loop variable after loop

def test_for_loop_downto():
    """Test FOR loop with DOWNTO."""
    text = """
    PROGRAM Test;
    VAR
        i, sum : INTEGER;
    BEGIN
        sum := 0;
        FOR i := 5 DOWNTO 1 DO
            sum := sum + i
    END.
    """
    res = interpret(text)
    assert res.get('sum') == 15  # 5+4+3+2+1
    assert res.get('i') == 0

def test_nested_loops():
    """Test nested FOR loops."""
    text = """
    PROGRAM Test;
    VAR
        i, j, result : INTEGER;
    BEGIN
        result := 0;
        FOR i := 1 TO 3 DO
            FOR j := 1 TO 2 DO
                result := result + 1
    END.
    """
    res = interpret(text)
    assert res.get('result') == 6  # 3*2

def test_while_in_function():
    """Test WHILE loop inside function."""
    text = """
    PROGRAM Test;
    VAR
        result : INTEGER;
    
    FUNCTION Factorial(n : INTEGER) : INTEGER;
    VAR
        i, fact : INTEGER;
    BEGIN
        fact := 1;
        i := 1;
        WHILE i <= n DO
        BEGIN
            fact := fact * i;
            i := i + 1
        END;
        Factorial := fact
    END;
    
    BEGIN
        result := Factorial(5)
    END.
    """
    res = interpret(text)
    assert res.get('result') == 120

def test_for_loop_with_expressions():
    """Test FOR loop with expressions as bounds."""
    text = """
    PROGRAM Test;
    VAR
        i, result : INTEGER;
    BEGIN
        result := 0;
        FOR i := 2 * 1 TO 3 + 2 DO
            result := result + i
    END.
    """
    res = interpret(text)
    assert res.get('result') == 14  # 2+3+4+5

def test_while_false_never_executes():
    """Test WHILE with false condition never executes."""
    text = """
    PROGRAM Test;
    VAR
        result : INTEGER;
    BEGIN
        result := 0;
        WHILE 1 > 2 DO
            result := 99
    END.
    """
    res = interpret(text)
    assert res.get('result') == 0

def test_for_empty_range():
    """Test FOR loop with empty range (start > end for TO)."""
    text = """
    PROGRAM Test;
    VAR
        i, result : INTEGER;
    BEGIN
        result := 0;
        FOR i := 5 TO 1 DO
            result := 99
    END.
    """
    res = interpret(text)
    assert res.get('result') == 0  # Loop doesn't execute