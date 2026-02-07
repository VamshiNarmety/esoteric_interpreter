"""Tests for error handling."""
import pytest
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.interpreter.interpreter import Interpreter
from src.semantic.semantic_analyzer import SemanticAnalyzer
from src.errors import LexerError, ParserError, SemanticError, RuntimeError

def test_lexer_error_invalid_character():
    """Test lexer error for invalid character."""
    text = "PROGRAM Test; BEGIN x := 5 @ 3 END."
    lexer = Lexer(text)
    parser = Parser(lexer)
    with pytest.raises(LexerError) as exc_info:
        parser.parse()
    assert "Invalid character" in str(exc_info.value)

def test_lexer_error_unterminated_comment():
    """Test lexer error for unterminated comment."""
    text = "PROGRAM Test; BEGIN { this comment never ends"
    lexer = Lexer(text)
    parser = Parser(lexer)
    with pytest.raises(LexerError) as exc_info:
        parser.parse()
    assert "Unterminated comment" in str(exc_info.value)

def test_parser_error_missing_semicolon():
    """Test parser error for missing semicolon."""
    text = "PROGRAM Test VAR x : INTEGER; BEGIN x := 5 END."
    lexer = Lexer(text)
    parser = Parser(lexer)
    with pytest.raises(ParserError) as exc_info:
        parser.parse()
    assert "Expected token" in str(exc_info.value)

def test_semantic_error_undeclared_variable():
    """Test semantic error for undeclared variable."""
    text = """
    PROGRAM Test;
    BEGIN
        x := 5
    END.
    """
    lexer = Lexer(text)
    parser = Parser(lexer)
    with pytest.raises(SemanticError) as exc_info:
        interpreter = Interpreter(parser)
        interpreter.interpret()
    assert "undeclared variable" in str(exc_info.value).lower()

def test_semantic_error_undefined_function():
    """Test semantic error for undefined function."""
    text = """
    PROGRAM Test;
    VAR
        x : INTEGER;
    BEGIN
        x := Foo(5)
    END.
    """
    lexer = Lexer(text)
    parser = Parser(lexer)
    with pytest.raises(SemanticError) as exc_info:
        interpreter = Interpreter(parser)
        interpreter.interpret()
    assert "Undefined function" in str(exc_info.value)

def test_semantic_error_wrong_parameter_count():
    """Test semantic error for wrong number of parameters."""
    text = """
    PROGRAM Test;
    VAR
        x : INTEGER;
    
    FUNCTION Add(a : INTEGER; b : INTEGER) : INTEGER;
    BEGIN
        Add := a + b
    END;
    
    BEGIN
        x := Add(5)
    END.
    """
    lexer = Lexer(text)
    parser = Parser(lexer)
    with pytest.raises(SemanticError) as exc_info:
        interpreter = Interpreter(parser)
        interpreter.interpret()
    assert "expects 2 parameter" in str(exc_info.value)

def test_runtime_error_division_by_zero():
    """Test runtime error for division by zero."""
    text = """
    PROGRAM Test;
    VAR
        x, y : INTEGER;
    BEGIN
        x := 10;
        y := 0;
        x := x / y
    END.
    """
    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    with pytest.raises(RuntimeError) as exc_info:
        interpreter.interpret()
    assert "Division by zero" in str(exc_info.value)

def test_error_with_line_numbers():
    """Test that errors include line number information."""
    text = """
    PROGRAM Test;
    VAR
        x : INTEGER;
    BEGIN
        y := 5
    END.
    """
    lexer = Lexer(text)
    parser = Parser(lexer)
    with pytest.raises(SemanticError) as exc_info:
        interpreter = Interpreter(parser)
        interpreter.interpret()
    error_msg = str(exc_info.value)
    assert "line" in error_msg.lower() or "undeclared" in error_msg.lower()