import pytest
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.interpreter.interpreter import Interpreter


def interpret(text):
    """Helper to interpret text."""
    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    return interpreter.interpret()


def test_addition():
    result = interpret('3+5')
    assert result == 8

def test_subtraction():
    result = interpret('7-2')
    assert result == 5

def test_addition_with_spaces():
    result = interpret('3 + 5')
    assert result == 8

def test_subtraction_with_spaces():
    result = interpret('9 - 4')
    assert result == 5

def test_double_digits_only():
    result = interpret('33 + 55')
    assert result == 88

def test_invalid_syntax_missing_operator():
    with pytest.raises(Exception):
        interpret('3 5')

def test_invalid_syntax_missing_operand():
    with pytest.raises(Exception):
        interpret('3+')

def test_invalid_character():
    with pytest.raises(Exception):
        interpret('3$5')

def test_multi_digit_addition():
    result = interpret('12+34')
    assert result == 46

def test_multi_digit_subtraction():
    result = interpret('100-50')
    assert result == 50

def test_large_numbers():
    result = interpret('999+1')
    assert result == 1000

def test_multi_digit_with_spaces():
    result = interpret('123 + 456')
    assert result == 579

def test_multiplication():
    result = interpret('3 * 5')
    assert result == 15

def test_division():
    result = interpret('10 / 2')
    assert result == 5

def test_multiple_operations():
    result = interpret('7+3 -2')
    assert result == 8

def test_all_four_operations_without_precedence():
    result = interpret('10 - 3 + 5 * 2 / 2')
    assert result == 12

def test_precedence_mul_before_add():
    result = interpret('2+3*4')
    assert result == 14

def test_precedence_div_before_sub():
    result = interpret('10-8/4')
    assert result == 8

def test_precedence_complex():
    result = interpret('7+3*2-4/2')
    assert result == 11

def test_precedence_left_to_right_same_level():
    result = interpret('10/2*3')
    assert result == 15

def test_parentheses_simple():
    result = interpret('(2+3)*4')
    assert result == 20

def test_parentheses_override_precedence():
    result = interpret('2*(3+4)')
    assert result == 14

def test_nested_parentheses():
    result = interpret('((2+3)*4)')
    assert result == 20

def test_complex_with_parentheses():
    result = interpret('7 + 3 * (10 / (12 / (3 + 1) - 1))')
    assert result == 22

def test_multiple_parentheses():
    result = interpret('(2+3)*(4+5)')
    assert result == 45
