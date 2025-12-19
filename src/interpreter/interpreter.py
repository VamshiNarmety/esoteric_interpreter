"""
Interpreter that walks the Abstract syntax tree.
Uses the visitor to pattern to traverse and interpret AST nodes.
"""
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.parser.ast_nodes import BinOp, Num
from src.lexer.token import PLUS, MINUS, MUL, DIV

class NodeVisitor:
    """
    Base visitor class.
    Subclasses implement visit_NodeType methods.
    """
    def visit(self, node):
        method_name = 'visit_'+type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        """Called if no visit_NodeType method exists."""
        raise Exception(f'No visit_{type(node).__name__} method')
    

class Interpreter(NodeVisitor):
    """
    Interpreter that evaluates the AST. Walks the tree and computes the result.
    """
    def __init__(self, parser):
        """ Initialize interpreter with a parser."""
        self.parser = parser

    def visit_BinOp(self, node):
        """ Visit binary operator node."""
        if node.op.type==PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type==MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type==MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type==DIV:
            return self.visit(node.left) // self.visit(node.right)
        
    def visit_Num(self, node):
        """Visit number node."""
        return node.value
    
    def interpret(self):
        """Interpret the AST."""
        tree = self.parser.parse()
        return self.visit(tree)