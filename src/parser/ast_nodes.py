"""Abstract Syntax Tree (AST) node definitions.
Each node represents a construct in the language.
"""

class AST:
    """
    Base class for all AST nodes.
    """
    pass

class Program(AST):
    """Represents a program with a name and a block"""
    def __init__(self, name, block):
        self.name = name
        self.block = block

class Block(AST):
    """Represents a block with declarations and compound statement"""
    def __init__(self, declarations, compound_statement):
        self.declarations = declarations
        self.compound_statement = compound_statement

class VarDecl(AST):
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node

class FunctionDecl(AST):
    """Function declaration node"""
    def __init__(self, func_name, params, return_type, block_node):
        self.func_name = func_name
        self.params = params #List of param nodes
        self.return_type = return_type
        self.block_node = block_node

class Param(AST):
    """Function parameter node"""
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node

class FunctionCall(AST):
    """Function call node(can be used in expressions)"""
    def __init__(self, func_name, actual_params, token):
        self.func_name = func_name
        self.actual_params = actual_params
        self.token = token

class Type(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

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

