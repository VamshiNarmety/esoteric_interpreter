"""
Interpreter that walks the Abstract syntax tree.
Uses the visitor to pattern to traverse and interpret AST nodes.
"""
from src.parser.parser import Parser
from src.parser.ast_nodes import Program, Block, VarDecl, Type, BinOp, Num, UnaryOp, Compound, Assign, Var, NoOp
from src.lexer.token import PLUS, MINUS, MUL, INTEGER_DIV, FLOAT_DIV

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
    GLOBAL_SCOPE = {}
    
    def __init__(self, parser):
        """ Initialize interpreter with a parser."""
        self.parser = parser

    def visit_Program(self, node):
        self.visit(node.block)

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_VarDecl(self, node):
        pass

    def visit_Type(self, node):
        pass

    def visit_BinOp(self, node):
        """ Visit binary operator node."""
        if node.op.type==PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type==MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type==MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type==INTEGER_DIV:
            return self.visit(node.left) // self.visit(node.right)
        elif node.op.type==FLOAT_DIV:
            return self.visit(node.left)/self.visit(node.right)
        
    def visit_Num(self, node):
        """Visit number node."""
        return node.value
    
    def visit_UnaryOp(self, node):
        """ Visit Unary operator node."""
        op = node.op.type
        if op==PLUS:
            return +self.visit(node.expr)
        elif op==MINUS:
            return -self.visit(node.expr)
        
    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Assign(self, node):
        var_name = node.left.value
        self.GLOBAL_SCOPE[var_name]=self.visit(node.right)

    def visit_Var(self, node):
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is None:
            raise NameError(f"variable '{var_name}' not found")
        return val
    
    def visit_NoOp(self, node):
        pass
    
    def interpret(self):
        """Interpret the AST."""
        tree = self.parser.parse()
        if tree is None:
            return ''
        return self.visit(tree)