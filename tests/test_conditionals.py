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

def test_simple_if_true():
    """Test simple IF statement with true condition."""
    text = """
    PROGRAM Test;
    VAR
        x, result : INTEGER;
    BEGIN
        x := 10;
        IF x = 10 THEN
            result := 1
        END
    END.
    """
    res = interpret(text)
    assert res.get('result') == 1

def test_simple_if_false():
    """Test simple IF statement with false condition."""
    text = """
    PROGRAM Test;
    VAR
        x, result : INTEGER;
    BEGIN
        x := 5;
        result := 0;
        IF x = 10 THEN
            result := 1
        END
    END.
    """
    res = interpret(text)
    assert res.get('result') == 0

def test_if_else_true_branch():
    """Test IF-ELSE with true condition (then branch)."""
    text = """
    PROGRAM Test;
    VAR
        x, result : INTEGER;
    BEGIN
        x := 10;
        IF x = 10 THEN
            result := 1
        ELSE
            result := 2
        END
    END.
    """
    res = interpret(text)
    assert res.get('result') == 1

def test_if_else_false_branch():
    """Test IF-ELSE with false condition (else branch)."""
    text = """
    PROGRAM Test;
    VAR
        x, result : INTEGER;
    BEGIN
        x := 5;
        IF x = 10 THEN
            result := 1
        ELSE
            result := 2
        END
    END.
    """
    res = interpret(text)
    assert res.get('result') == 2

def test_comparison_less_than():
    """Test less than comparison."""
    text = """
    PROGRAM Test;
    VAR
        result : INTEGER;
    BEGIN
        IF 5 < 10 THEN
            result := 1
        ELSE
            result := 0
        END
    END.
    """
    res = interpret(text)
    assert res.get('result') == 1

def test_comparison_greater_than():
    """Test greater than comparison."""
    text = """
    PROGRAM Test;
    VAR
        result : INTEGER;
    BEGIN
        IF 15 > 10 THEN
            result := 1
        ELSE
            result := 0
        END
    END.
    """
    res = interpret(text)
    assert res.get('result') == 1

def test_comparison_less_equal():
    """Test less than or equal comparison."""
    text = """
    PROGRAM Test;
    VAR
        result1, result2 : INTEGER;
    BEGIN
        IF 5 <= 10 THEN
            result1 := 1
        ELSE
            result1 := 0
        END;
        
        IF 10 <= 10 THEN
            result2 := 1
        ELSE
            result2 := 0
        END
    END.
    """
    res = interpret(text)
    assert res.get('result1') == 1
    assert res.get('result2') == 1

def test_comparison_greater_equal():
    """Test greater than or equal comparison."""
    text = """
    PROGRAM Test;
    VAR
        result1, result2 : INTEGER;
    BEGIN
        IF 15 >= 10 THEN
            result1 := 1
        ELSE
            result1 := 0
        END;
        
        IF 10 >= 10 THEN
            result2 := 1
        ELSE
            result2 := 0
        END
    END.
    """
    res = interpret(text)
    assert res.get('result1') == 1
    assert res.get('result2') == 1

def test_comparison_not_equal():
    """Test not equal comparison."""
    text = """
    PROGRAM Test;
    VAR
        result1, result2 : INTEGER;
    BEGIN
        IF 5 <> 10 THEN
            result1 := 1
        ELSE
            result1 := 0
        END;
        
        IF 10 <> 10 THEN
            result2 := 1
        ELSE
            result2 := 0
        END
    END.
    """
    res = interpret(text)
    assert res.get('result1') == 1
    assert res.get('result2') == 0

def test_boolean_and():
    """Test AND logical operator."""
    text = """
    PROGRAM Test;
    VAR
        result1, result2 : INTEGER;
    BEGIN
        IF 5 < 10 AND 3 < 7 THEN
            result1 := 1
        ELSE
            result1 := 0
        END;

        IF 5 < 10 AND 3 > 7 THEN
            result2 := 1
        ELSE
            result2 := 0
        END
    END.
    """
    res = interpret(text)
    assert res.get('result1') == 1
    assert res.get('result2') == 0

def test_boolean_or():
    """Test OR logical operator."""
    text = """
    PROGRAM Test;
    VAR
        result1, result2 : INTEGER;
    BEGIN
        IF 5 > 10 OR 3 < 7 THEN
            result1 := 1
        ELSE
            result1 := 0
        END;

        IF 5 > 10 OR 3 > 7 THEN
            result2 := 1
        ELSE
            result2 := 0
        END
    END.
    """
    res = interpret(text)
    assert res.get('result1') == 1
    assert res.get('result2') == 0

def test_boolean_not():
    """Test NOT logical operator."""
    text = """
    PROGRAM Test;
    VAR
        result1, result2 : INTEGER;
    BEGIN
        IF NOT 5 > 10 THEN
            result1 := 1
        ELSE
            result1 := 0
        END;

        IF NOT 5 < 10 THEN
            result2 := 1
        ELSE
            result2 := 0
        END
    END.
    """
    res = interpret(text)
    assert res.get('result1') == 1
    assert res.get('result2') == 0

def test_complex_boolean_expression():
    """Test complex boolean expression with multiple operators."""
    text = """
    PROGRAM Test;
    VAR
        x, y, result : INTEGER;
    BEGIN
        x := 5;
        y := 10;
        IF x < y AND x + y = 15 OR x > 20 THEN
            result := 1
        ELSE
            result := 0
        END
    END.
    """
    res = interpret(text)
    assert res.get('result') == 1

def test_nested_if_statements():
    """Test nested IF statements."""
    text = """
    PROGRAM Test;
    VAR
        x, y, result : INTEGER;
    BEGIN
        x := 10;
        y := 5;
        IF x > y THEN
            IF x = 10 THEN
                result := 1
            ELSE
                result := 2
            END
        ELSE
            result := 3
        END
    END.
    """
    res = interpret(text)
    assert res.get('result') == 1

def test_if_with_compound_statement():
    """Test IF with compound statement (multiple assignments)."""
    text = """
    PROGRAM Test;
    VAR
        x, y, z : INTEGER;
    BEGIN
        IF 5 < 10 THEN
            BEGIN
                x := 1;
                y := 2;
                z := 3
            END
        ELSE
            BEGIN
                x := 10;
                y := 20;
                z := 30
            END
        END
    END.
    """
    res = interpret(text)
    assert res.get('x') == 1
    assert res.get('y') == 2
    assert res.get('z') == 3

def test_recursive_factorial_with_if():
    """Test recursive factorial function using IF."""
    text = """
    PROGRAM Test;
    VAR
        result : INTEGER;
    
    FUNCTION Factorial(n : INTEGER) : INTEGER;
    BEGIN
        IF n <= 1 THEN
            Factorial := 1
        ELSE
            Factorial := n * Factorial(n - 1)
        END
    END;
    
    BEGIN
        result := Factorial(5)
    END.
    """
    res = interpret(text)
    assert res.get('result') == 120  # 5! = 5*4*3*2*1 = 120

def test_if_in_function():
    """Test IF statement inside function."""
    text = """
    PROGRAM Test;
    VAR
        result1, result2 : INTEGER;
    
    FUNCTION Max(a, b : INTEGER) : INTEGER;
    BEGIN
        IF a > b THEN
            Max := a
        ELSE
            Max := b
        END
    END;
    
    BEGIN
        result1 := Max(10, 5);
        result2 := Max(3, 8)
    END.
    """
    res = interpret(text)
    assert res.get('result1') == 10
    assert res.get('result2') == 8