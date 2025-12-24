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


def test_addition():
    result = interpret('BEGIN result := 3+5 END.')
    assert result == 8

def test_subtraction():
    result = interpret('BEGIN result := 7-2 END.')
    assert result == 5

def test_addition_with_spaces():
    result = interpret('BEGIN result := 3 + 5 END.')
    assert result == 8

def test_subtraction_with_spaces():
    result = interpret('BEGIN result := 9 - 4 END.')
    assert result == 5

def test_double_digits_only():
    result = interpret('BEGIN result := 33 + 55 END.')
    assert result == 88

def test_invalid_syntax_missing_operator():
    with pytest.raises(Exception):
        interpret('BEGIN result := 3 5 END.')

def test_invalid_syntax_missing_operand():
    with pytest.raises(Exception):
        interpret('BEGIN result := 3+ END.')

def test_invalid_character():
    with pytest.raises(Exception):
        interpret('BEGIN result := 3$5 END.')

def test_multi_digit_addition():
    result = interpret('BEGIN result := 12+34 END.')
    assert result == 46

def test_multi_digit_subtraction():
    result = interpret('BEGIN result := 100-50 END.')
    assert result == 50

def test_large_numbers():
    result = interpret('BEGIN result := 999+1 END.')
    assert result == 1000

def test_multi_digit_with_spaces():
    result = interpret('BEGIN result := 123 + 456 END.')
    assert result == 579

def test_multiplication():
    result = interpret('BEGIN result := 3 * 5 END.')
    assert result == 15

def test_division():
    result = interpret('BEGIN result := 10 / 2 END.')
    assert result == 5

def test_multiple_operations():
    result = interpret('BEGIN result := 7+3 -2 END.')
    assert result == 8

def test_all_four_operations_without_precedence():
    result = interpret('BEGIN result := 10 - 3 + 5 * 2 / 2 END.')
    assert result == 12

def test_precedence_mul_before_add():
    result = interpret('BEGIN result := 2+3*4 END.')
    assert result == 14

def test_precedence_div_before_sub():
    result = interpret('BEGIN result := 10-8/4 END.')
    assert result == 8

def test_precedence_complex():
    result = interpret('BEGIN result := 7+3*2-4/2 END.')
    assert result == 11

def test_precedence_left_to_right_same_level():
    result = interpret('BEGIN result := 10/2*3 END.')
    assert result == 15

def test_parentheses_simple():
    result = interpret('BEGIN result := (2+3)*4 END.')
    assert result == 20

def test_parentheses_override_precedence():
    result = interpret('BEGIN result := 2*(3+4) END.')
    assert result == 14

def test_nested_parentheses():
    result = interpret('BEGIN result := ((2+3)*4) END.')
    assert result == 20

def test_complex_with_parentheses():
    result = interpret('BEGIN result := 7 + 3 * (10 / (12 / (3 + 1) - 1)) END.')
    assert result == 22

def test_multiple_parentheses():
    result = interpret('BEGIN result := (2+3)*(4+5) END.')
    assert result == 45

def test_unary_plus():
    result = interpret('BEGIN result := +5 END.')
    assert result == 5

def test_unary_minus():
    result = interpret('BEGIN result := -3 END.')
    assert result == -3

def test_unary_with_addition():
    result = interpret('BEGIN result := 5 + -3 END.')
    assert result == 2

def test_unary_with_subtraction():
    result = interpret('BEGIN result := 5 - -3 END.')
    assert result == 8

def test_unary_with_multiplication():
    result = interpret('BEGIN result := 5 * -3 END.')
    assert result == -15

def test_double_unary():
    result = interpret('BEGIN result := --3 END.')
    assert result == 3

def test_complex_unary():
    result = interpret('BEGIN result := -5 + -3 END.')
    assert result == -8

def test_simple_assignment():
    Interpreter.GLOBAL_SCOPE.clear()
    interpret('''
        BEGIN
            a := 5
        END.
    ''')
    assert Interpreter.GLOBAL_SCOPE['a'] == 5

def test_multiple_assignments():
    Interpreter.GLOBAL_SCOPE.clear()
    interpret('''
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