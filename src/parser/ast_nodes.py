"""Abstract Syntax Tree (AST) node definitions.
Each node represents a construct in the language.
"""

class AST:
    """
    Base class for all AST nodes.
    """
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr
        
class Compound(AST):
    """ Represents a 'BEGIN ... END' block"""
    def __init__(self):
        self.children = []

class Assign(AST):
    """Assignment statement node"""
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Var(AST):
    """Variable node"""
    def __init__(self, token):
        self.token = token
        self.value = token.value

class NoOp(AST):
    """Empty statement node"""
    pass

