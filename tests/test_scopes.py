"""
Tests for scoped symbol tables and nested scopes.
"""
import pytest
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.semantic_analyzer import SemanticAnalyzer

def analyze(text):
    """Helper function to run semantic analysis."""
    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    semantic_analyzer = SemanticAnalyzer()
    semantic_analyzer.visit(tree)
    return semantic_analyzer

def test_global_scope_creation():
    """Test that global scope is created with level 1."""
    text = """
    PROGRAM Test;
    VAR
        x : INTEGER;
    BEGIN
        x := 5
    END.
    """
    analyzer = analyze(text)
    # After visiting, current_scope should be None (we left global scope)
    assert analyzer.current_scope is None

def test_variable_declaration_in_global_scope():
    """Test basic variable declaration in global scope."""
    text = """
    PROGRAM Test;
    VAR
        x : INTEGER;
        y : REAL;
    BEGIN
        x := 5;
        y := 3.14
    END.
    """
    analyze(text)  # Should not raise

def test_variable_lookup_in_global_scope():
    """Test variable lookup and usage in global scope."""
    text = """
    PROGRAM Test;
    VAR
        x : INTEGER;
        y : INTEGER;
        result : INTEGER;
    BEGIN
        x := 5;
        y := 10;
        result := x + y
    END.
    """
    analyze(text)  # Should not raise

def test_undeclared_variable_error():
    """Test that using undeclared variable raises error."""
    text = """
    PROGRAM Test;
    VAR
        x : INTEGER;
    BEGIN
        y := 5
    END.
    """
    with pytest.raises(Exception, match=r"[Cc]annot assign to undeclared variable 'y'"):
        analyze(text)

def test_duplicate_variable_in_same_scope():
    """Test that duplicate variable declaration raises error."""
    text = """
    PROGRAM Test;
    VAR
        x : INTEGER;
        x : REAL;
    BEGIN
        x := 5
    END.
    """
    with pytest.raises(Exception, match="Duplicate identifier 'x'"):
        analyze(text)

def test_builtin_types_available():
    """Test that INTEGER and REAL built-in types are available."""
    text = """
    PROGRAM Test;
    VAR
        a : INTEGER;
        b : REAL;
    BEGIN
        a := 10;
        b := 2.5
    END.
    """
    analyze(text)  # Should not raise

def test_multiple_variables_in_global_scope():
    """Test multiple variable declarations and assignments."""
    text = """
    PROGRAM Test;
    VAR
        a : INTEGER;
        b : INTEGER;
        c : INTEGER;
        result : INTEGER;
    BEGIN
        a := 1;
        b := 2;
        c := 3;
        result := a + b + c
    END.
    """
    analyze(text)  # Should not raise

def test_nested_begin_end_scope():
    """Test that nested BEGIN...END creates a new scope."""
    text = """
    PROGRAM Test;
    VAR
        x : INTEGER;
    BEGIN
        x := 5;
        BEGIN
            x := 10
        END
    END.
    """
    analyze(text)  # Should not raise

def test_variable_access_from_outer_scope():
    """Test that inner scope can access outer scope variables."""
    text = """
    PROGRAM Test;
    VAR
        x : INTEGER;
        y : INTEGER;
    BEGIN
        x := 5;
        BEGIN
            y := x + 10
        END
    END.
    """
    analyze(text)  # Should not raise

def test_multiple_nested_scopes():
    """Test multiple levels of nested scopes."""
    text = """
    PROGRAM Test;
    VAR
        x : INTEGER;
    BEGIN
        x := 1;
        BEGIN
            x := 2;
            BEGIN
                x := 3
            END
        END
    END.
    """
    analyze(text)  # Should not raise

def test_sibling_nested_scopes():
    """Test multiple sibling nested scopes."""
    text = """
    PROGRAM Test;
    VAR
        x : INTEGER;
        y : INTEGER;
    BEGIN
        BEGIN
            x := 5
        END;
        BEGIN
            y := 10
        END
    END.
    """
    analyze(text)  # Should not raise

def test_nested_scope_variable_visibility():
    """Test that nested scopes can access all parent scope variables."""
    text = """
    PROGRAM Test;
    VAR
        a : INTEGER;
        b : INTEGER;
        c : INTEGER;
    BEGIN
        a := 1;
        BEGIN
            b := a + 2;
            BEGIN
                c := a + b + 3
            END
        END
    END.
    """
    analyze(text)  # Should not raise

def test_undeclared_variable_in_nested_scope():
    """Test that undeclared variable in nested scope raises error."""
    text = """
    PROGRAM Test;
    VAR
        x : INTEGER;
    BEGIN
        BEGIN
            y := 5
        END
    END.
    """
    with pytest.raises(Exception, match=r"[Cc]annot assign to undeclared variable 'y'"):
        analyze(text)

def test_complex_nested_structure():
    """Test complex nested structure with multiple levels and siblings."""
    text = """
    PROGRAM Test;
    VAR
        x : INTEGER;
        y : INTEGER;
        z : INTEGER;
    BEGIN
        x := 1;
        BEGIN
            y := x + 1;
            BEGIN
                z := x + y
            END;
            BEGIN
                z := y + 2
            END
        END;
        BEGIN
            y := x + 10
        END
    END.
    """
    analyze(text)  # Should not raise

def test_empty_nested_scope():
    """Test empty nested BEGIN...END blocks."""
    text = """
    PROGRAM Test;
    VAR
        x : INTEGER;
    BEGIN
        x := 5;
        BEGIN
        END
    END.
    """
    analyze(text)  # Should not raise

def test_deeply_nested_scopes():
    """Test deeply nested scopes (5 levels)."""
    text = """
    PROGRAM Test;
    VAR
        x : INTEGER;
    BEGIN
        x := 1;
        BEGIN
            x := 2;
            BEGIN
                x := 3;
                BEGIN
                    x := 4;
                    BEGIN
                        x := 5
                    END
                END
            END
        END
    END.
    """
    analyze(text)  # Should not raise

def test_scope_isolation_for_assignments():
    """Test that assignments in nested scopes work correctly."""
    text = """
    PROGRAM Test;
    VAR
        a : INTEGER;
        b : INTEGER;
        c : INTEGER;
    BEGIN
        a := 1;
        b := 2;
        c := 3;
        BEGIN
            a := a + 1;
            BEGIN
                b := b + a;
                c := c + b
            END
        END
    END.
    """
    analyze(text)  # Should not raise