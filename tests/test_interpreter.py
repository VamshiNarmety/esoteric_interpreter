import pytest
from src.interpreter.interpreter import Interpreter

def test_addition():
    interpreter = Interpreter('3+5')
    result = interpreter.parse()
    assert result == 8

def test_subtraction():
    interpreter = Interpreter('7-2')
    result = interpreter.parse()
    assert result == 5

def test_addition_with_spaces():
    interpreter = Interpreter('3 + 5')
    result = interpreter.parse()
    assert result == 8

def test_subtraction_with_spaces():
    interpreter = Interpreter('9 - 4')
    result = interpreter.parse()
    assert result == 5

def test_double_digits_only():
    interpreter = Interpreter('33+55')
    result = interpreter.parse()
    assert result == 88

def test_invalid_syntax_missing_operator():
    interpreter = Interpreter('3 5')
    with pytest.raises(Exception):
        interpreter.parse()

def test_invalid_syntax_missing_operand():
    interpreter = Interpreter('3+')
    with pytest.raises(Exception):
        interpreter.parse()

def test_invalid_character():
    interpreter = Interpreter('3$5')
    with pytest.raises(Exception):
        interpreter.parse()

def test_multi_digit_addition():
    interpreter = Interpreter('12+34')
    result = interpreter.parse()
    assert result == 46

def test_multi_digit_subtraction():
    interpreter = Interpreter('100-50')
    result = interpreter.parse()
    assert result == 50

def test_large_numbers():
    interpreter = Interpreter('999+1')
    result = interpreter.parse()
    assert result == 1000

def test_multi_digit_with_spaces():
    interpreter = Interpreter('123 + 456')
    result = interpreter.parse()
    assert result == 579

def test_multiplication():
    interpreter = Interpreter(' 3 * 5 ')
    result = interpreter.parse()
    assert result == 15

def test_division():
    interpreter = Interpreter(' 10 / 2 ')
    result = interpreter.parse()
    assert result == 5

def test_multiple_operations():
    interpreter = Interpreter(' 7+3 -2 ')
    result = interpreter.parse()
    assert result == 8

def test_all_four_operations_without_precedence():
    """Test all four operations."""
    interpreter = Interpreter('10 - 3 + 5 * 2 / 2')
    result = interpreter.parse()
    assert result == 12

def test_precedence_mul_before_add():
    interpreter = Interpreter('2+3*4')
    result = interpreter.parse()
    assert result == 14

def test_precedence_div_before_sub():
    interpreter = Interpreter('10-8/4')
    result = interpreter.parse()
    assert result == 8

def test_precedence_complex():
    interpreter = Interpreter('7+3*2-4/2')
    result = interpreter.parse()
    assert result == 11

def test_precedence_left_to_right_same_level():
    interpreter = Interpreter('10/2*3')
    result = interpreter.parse()
    assert result == 15

def test_parentheses_simple():
    interpreter = Interpreter('(2+3)*4')
    result = interpreter.parse()
    assert result == 20

def test_parentheses_override_precedence():
    interpreter = Interpreter('2*(3+4)')
    result = interpreter.parse()
    assert result == 14

def test_nested_parentheses():
    interpreter = Interpreter('((2+3)*4)')
    result = interpreter.parse()
    assert result == 20

def test_complex_with_parentheses():
    interpreter = Interpreter('7 + 3 * (10 / (12 / (3 + 1) - 1))')
    result = interpreter.parse()
    assert result == 22

def test_multiple_parentheses():
    interpreter = Interpreter('(2+3)*(4+5)')
    result = interpreter.parse()
    assert result == 45