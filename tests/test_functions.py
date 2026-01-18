"""
Tests for functions with return values (simplified - no call stack yet).
"""
import pytest
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.semantic_analyzer import SemanticAnalyzer
from src.interpreter.interpreter import Interpreter

def analyze(text):
    """Helper to run semantic analysis."""
    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    semantic_analyzer = SemanticAnalyzer()
    semantic_analyzer.visit(tree)
    return semantic_analyzer

def interpret(text):
    """Helper to interpret Pascal code."""
    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpret()
    return interpreter.GLOBAL_SCOPE

def test_simple_function_no_params():
    """Test simple function without parameters."""
    text = """
    PROGRAM Test;
    VAR
        result : INTEGER;
    
    FUNCTION GetValue : INTEGER;
    BEGIN
        GetValue := 42
    END;
    
    BEGIN
        result := GetValue()
    END.
    """
    res = interpret(text)
    assert res.get('result') == 42

def test_function_with_one_parameter():
    """Test function with single parameter."""
    text = """
    PROGRAM Test;
    VAR
        result : INTEGER;
    
    FUNCTION Double(x : INTEGER) : INTEGER;
    BEGIN
        Double := x * 2
    END;
    
    BEGIN
        result := Double(21)
    END.
    """
    res = interpret(text)
    assert res.get('result') == 42

def test_function_with_multiple_parameters():
    """Test function with multiple parameters."""
    text = """
    PROGRAM Test;
    VAR
        result : INTEGER;
    
    FUNCTION Add(a : INTEGER; b : INTEGER) : INTEGER;
    BEGIN
        Add := a + b
    END;
    
    BEGIN
        result := Add(15, 27)
    END.
    """
    res = interpret(text)
    assert res.get('result') == 42

def test_function_in_expression():
    """Test using function result in expression."""
    text = """
    PROGRAM Test;
    VAR
        result : INTEGER;
    
    FUNCTION Square(x : INTEGER) : INTEGER;
    BEGIN
        Square := x * x
    END;
    
    BEGIN
        result := Square(5) + Square(3)
    END.
    """
    res = interpret(text)
    assert res.get('result') == 34  # 25 + 9

def test_function_multiple_params_same_type():
    """Test function with multiple parameters of same type."""
    text = """
    PROGRAM Test;
    VAR
        result : INTEGER;
    
    FUNCTION Sum(a, b, c : INTEGER) : INTEGER;
    BEGIN
        Sum := a + b + c
    END;
    
    BEGIN
        result := Sum(10, 20, 12)
    END.
    """
    res = interpret(text)
    assert res.get('result') == 42

def test_function_real_return_type():
    """Test function with REAL return type."""
    text = """
    PROGRAM Test;
    VAR
        result : REAL;
    
    FUNCTION Average(a, b : REAL) : REAL;
    BEGIN
        Average := (a + b) / 2
    END;
    
    BEGIN
        result := Average(10.0, 14.0)
    END.
    """
    res = interpret(text)
    assert res.get('result') == 12.0

def test_function_with_local_vars():
    """Test function with local variable declarations."""
    text = """
    PROGRAM Test;
    VAR
        result : INTEGER;
    
    FUNCTION Calculate : INTEGER;
    VAR
        temp : INTEGER;
    BEGIN
        temp := 21;
        Calculate := temp * 2
    END;
    
    BEGIN
        result := Calculate()
    END.
    """
    res = interpret(text)
    assert res.get('result') == 42

def test_nested_function_calls():
    """Test calling function within another function call."""
    text = """
    PROGRAM Test;
    VAR
        result : INTEGER;
    
    FUNCTION Double(x : INTEGER) : INTEGER;
    BEGIN
        Double := x * 2
    END;
    
    FUNCTION Add(a : INTEGER; b : INTEGER) : INTEGER;
    BEGIN
        Add := a + b
    END;
    
    BEGIN
        result := Add(Double(5), Double(6))
    END.
    """
    res = interpret(text)
    assert res.get('result') == 22  # (5*2) + (6*2) = 10 + 12

def test_multiple_functions():
    """Test program with multiple functions."""
    text = """
    PROGRAM Test;
    VAR
        x, y : INTEGER;
    
    FUNCTION Square(n : INTEGER) : INTEGER;
    BEGIN
        Square := n * n
    END;
    
    FUNCTION Cube(n : INTEGER) : INTEGER;
    BEGIN
        Cube := n * n * n
    END;
    
    BEGIN
        x := Square(4);
        y := Cube(3)
    END.
    """
    res = interpret(text)
    assert res.get('x') == 16
    assert res.get('y') == 27

def test_function_modifying_global_vars():
    """Test function modifying global variables."""
    text = """
    PROGRAM Test;
    VAR
        counter : INTEGER;
        result : INTEGER;
    
    FUNCTION IncrementAndReturn(amount : INTEGER) : INTEGER;
    BEGIN
        counter := counter + amount;
        IncrementAndReturn := counter
    END;
    
    BEGIN
        counter := 0;
        result := IncrementAndReturn(5);
        result := IncrementAndReturn(10)
    END.
    """
    res = interpret(text)
    assert res.get('counter') == 15
    assert res.get('result') == 15

def test_undeclared_function_call():
    """Test calling undeclared function raises error."""
    text = """
    PROGRAM Test;
    VAR
        result : INTEGER;
    BEGIN
        result := UndeclaredFunc()
    END.
    """
    with pytest.raises(Exception, match="Function 'UndeclaredFunc' not declared"):
        analyze(text)

def test_function_wrong_parameter_count():
    """Test calling function with wrong number of arguments."""
    text = """
    PROGRAM Test;
    VAR
        result : INTEGER;
    
    FUNCTION Add(a : INTEGER; b : INTEGER) : INTEGER;
    BEGIN
        Add := a + b
    END;
    
    BEGIN
        result := Add(1)
    END.
    """
    with pytest.raises(Exception, match="expects 2 arguments, got 1"):
        analyze(text)

def test_duplicate_function_declaration():
    """Test duplicate function declaration raises error."""
    text = """
    PROGRAM Test;
    
    FUNCTION F : INTEGER;
    BEGIN
        F := 1
    END;
    
    FUNCTION F : INTEGER;
    BEGIN
        F := 2
    END;
    
    BEGIN
    END.
    """
    with pytest.raises(Exception, match="Duplicate identifier 'F'"):
        analyze(text)

def test_duplicate_parameter_name():
    """Test duplicate parameter names raise error."""
    text = """
    PROGRAM Test;
    
    FUNCTION F(x : INTEGER; x : INTEGER) : INTEGER;
    BEGIN
        F := x
    END;
    
    BEGIN
    END.
    """
    with pytest.raises(Exception, match="Duplicate parameter 'x'"):
        analyze(text)