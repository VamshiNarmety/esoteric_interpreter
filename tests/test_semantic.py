import pytest
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.semantic_analyzer import SemanticAnalyzer

def analyze(text):
    """Helper to parse and analyze text"""
    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    semantic_analyzer = SemanticAnalyzer()
    semantic_analyzer.visit(tree)
    return semantic_analyzer.symtab

def test_symbol_table_builtin_types():
    text = '''
        PROGRAM Test;
        BEGIN
        END.
    '''
    symtab = analyze(text)
    assert symtab.lookup('INTEGER') is not None
    assert symtab.lookup('REAL') is not None

def test_symbol_table_var_declarations():
    text = '''
        PROGRAM Test;
        VAR
            x, y : INTEGER;
            z : REAL;
        BEGIN
        END.
    '''
    symtab = analyze(text)
    
    x_symbol = symtab.lookup('x')
    assert x_symbol is not None
    assert x_symbol.type.name == 'INTEGER'
    
    y_symbol = symtab.lookup('y')
    assert y_symbol is not None
    assert y_symbol.type.name == 'INTEGER'
    
    z_symbol = symtab.lookup('z')
    assert z_symbol is not None
    assert z_symbol.type.name == 'REAL'

def test_undeclared_variable_error():
    text = '''
        PROGRAM Test;
        BEGIN
            x := 5
        END.
    '''
    # Should auto-declare x as INTEGER
    symtab = analyze(text)
    assert symtab.lookup('x') is not None
    assert symtab.lookup('x').type.name == 'INTEGER'

def test_variable_reference_after_declaration():
    text = '''
        PROGRAM Test;
        VAR
            x, y : INTEGER;
        BEGIN
            x := 5;
            y := x + 3
        END.
    '''
    # Should not raise any errors
    symtab = analyze(text)
    assert symtab.lookup('x') is not None
    assert symtab.lookup('y') is not None

def test_undeclared_variable_in_expression():
    text = '''
        PROGRAM Test;
        VAR
            x : INTEGER;
        BEGIN
            x := y + 5
        END.
    '''
    # Should auto-declare y as INTEGER
    symtab = analyze(text)
    assert symtab.lookup('y') is not None
    assert symtab.lookup('y').type.name == 'INTEGER'

def test_multiple_var_sections():
    text = '''
        PROGRAM Test;
        VAR
            a, b, c : INTEGER;
            x, y : REAL;
        BEGIN
            a := 1;
            x := 2.5
        END.
    '''
    symtab = analyze(text)
    assert symtab.lookup('a').type.name == 'INTEGER'
    assert symtab.lookup('b').type.name == 'INTEGER'
    assert symtab.lookup('c').type.name == 'INTEGER'
    assert symtab.lookup('x').type.name == 'REAL'
    assert symtab.lookup('y').type.name == 'REAL'