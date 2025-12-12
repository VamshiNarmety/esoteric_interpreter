import pytest
from src.interpreter.interpreter import Interpreter

def test_addition():
    interpreter = Interpreter('3+5')
    result = interpreter.expr()
    assert result == 8

def test_subtraction():
    interpreter = Interpreter('7-2')
    result = interpreter.expr()
    assert result == 5

def test_addition_with_spaces():
    interpreter = Interpreter('3 + 5')
    result = interpreter.expr()
    assert result == 8

def test_subtraction_with_spaces():
    interpreter = Interpreter('9 - 4')
    result = interpreter.expr()
    assert result == 5

def test_double_digits_only():
    interpreter = Interpreter('33+55')
    result = interpreter.expr()
    assert result == 88

def test_invalid_syntax_missing_operator():
    interpreter = Interpreter('3 5')
    with pytest.raises(Exception):
        interpreter.expr()

def test_invalid_syntax_missing_operand():
    interpreter = Interpreter('3+')
    with pytest.raises(Exception):
        interpreter.expr()

def test_invalid_character():
    interpreter = Interpreter('3*5')
    with pytest.raises(Exception):
        interpreter.expr()