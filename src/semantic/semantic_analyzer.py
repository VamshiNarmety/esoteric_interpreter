"""
Semantic analyzer for the Pascal interpreter.
Builds symbol table and performs semantic checks.
"""
from src.parser.ast_nodes import (Program, Block, VarDecl, Type, BinOp, Num, UnaryOp, Compound, Assign, Var, NoOp)
from src.semantic.symbols import SymbolTable, VarSymbol

class NodeVisitor:
    """Base visitor class"""
    def visit(self, node):
        method_name = 'visit_'+type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')
    
class SemanticAnalyzer(NodeVisitor):
    """
    Semantic analyzer that builds symbol table and checks semantics.
    """
    def __init__(self):
        self.symtab = SymbolTable()

    def visit_Program(self, node):
        self.visit(node.block)

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_VarDecl(self, node):
        """Visit variable declaration node."""
        type_name = node.type_node.value
        type_symbol = self.symtab.lookup(type_name)
        #Define variable symbol with its type
        var_name = node.var_node.value
        var_symbol = VarSymbol(var_name, type_symbol)
        self.symtab.define(var_symbol)

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Assign(self, node):
        # Check that variable is declared (or auto-declare it)
        var_name = node.left.value
        var_symbol = self.symtab.lookup(var_name)
        if var_symbol is None:
            # Auto-declare as INTEGER for backward compatibility
            integer_type = self.symtab.lookup('INTEGER')
            var_symbol = VarSymbol(var_name, integer_type)
            self.symtab.define(var_symbol)
        
        self.visit(node.right)

    def visit_Var(self, node):
        """Visit variable reference node"""
        var_name = node.value
        var_symbol = self.symtab.lookup(var_name)
        if var_symbol is None:
            # Auto-declare as INTEGER for backward compatibility
            integer_type = self.symtab.lookup('INTEGER')
            var_symbol = VarSymbol(var_name, integer_type)
            self.symtab.define(var_symbol)
        
    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOp(self, node):
        self.visit(node.expr)

    def visit_Num(self, node):
        pass

    def visit_NoOp(self, node):
        pass