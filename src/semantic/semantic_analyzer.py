"""
Semantic analyzer for the Pascal interpreter.
Builds symbol table and performs semantic checks.
"""
import os
from src.parser.ast_nodes import (Program, Block, VarDecl, FunctionDecl, Param, FunctionCall, Type, BinOp, Num, UnaryOp, Compound, Assign, Var, NoOp, ComparisonOp, BooleanOp, UnaryBoolOp, IfStatement, WhileLoop, ForLoop)
from src.semantic.symbols import SymbolTable, VarSymbol, BuiltinTypeSymbol, FunctionSymbol, ScopedSymbolTable
from src.errors import SemanticError

# Control debug output via environment variable
_DEBUG = os.environ.get('PASCAL_DEBUG', '0') == '1'

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
    supports nested scopes for BEGIN...END blocks and functions.
    """
    def __init__(self):
        self.current_scope=None
        self.scope_counter = 0
        self.global_scope = None  # Store reference for tests
        
    def error(self, message):
        raise SemanticError(message)

    def visit_Program(self, node):
        if _DEBUG:
            print('ENTER scope: global')
        global_scope = ScopedSymbolTable(
            scope_name='global',
            scope_level=1,
            enclosing_scope=self.current_scope #None for global
        )
        global_scope._init_builtins()
        self.current_scope = global_scope
        self.global_scope = global_scope  # Store for later access
        self.visit(node.block)
        if _DEBUG:
            print(global_scope)
            print('LEAVE scope: global')
        self.current_scope = self.current_scope.enclosing_scope

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_VarDecl(self, node):
        """Visit variable declaration node."""
        type_name = node.type_node.value
        type_symbol = self.current_scope.lookup(type_name)
        # Check for duplicate declarations in current scope only
        var_name = node.var_node.value
        if self.current_scope.lookup(var_name, current_scope_only=True) is not None:
            self.error(f"Duplicate identifier '{var_name}'")
        # Define variable symbol with its type
        var_symbol = VarSymbol(var_name, type_symbol)
        self.current_scope.define(var_symbol)

    def visit_FunctionDecl(self, node):
        """Visit function declaration node."""
        func_name = node.func_name
        #check for duplicate function declaration
        if self.current_scope.lookup(func_name, current_scope_only=True) is not None:
            self.error(f"Duplicate identifier '{func_name}'")
        # Get return type
        return_type_symbol = self.current_scope.lookup(node.return_type.value)
        # Create function symbol with parameters
        func_symbol = FunctionSymbol(func_name, return_type=return_type_symbol)
        self.current_scope.define(func_symbol)
        # Create new scope for function
        if _DEBUG:
            print(f'ENTER scope: {func_name}')
        function_scope = ScopedSymbolTable(
            scope_name=func_name,
            scope_level=self.current_scope.scope_level + 1,
            enclosing_scope=self.current_scope
        )
        self.current_scope = function_scope
        # Define function name as variable in its own scope (for return value assignment)
        func_return_var = VarSymbol(func_name, return_type_symbol)
        self.current_scope.define(func_return_var)
        # Define parameters in function scope
        for param in node.params:
            param_type = self.current_scope.lookup(param.type_node.value)
            param_name = param.var_node.value
            # Check for duplicate parameters
            if self.current_scope.lookup(param_name, current_scope_only=True) is not None:
                self.error(f"Duplicate parameter '{param_name}'")
            var_symbol = VarSymbol(param_name, param_type)
            self.current_scope.define(var_symbol)
            func_symbol.params.append(var_symbol)
        # Visit function body
        self.visit(node.block_node)
        if _DEBUG:
            print(function_scope)
            print(f'LEAVE scope: {func_name}')
        self.current_scope = self.current_scope.enclosing_scope

    def visit_FunctionCall(self, node):
        """Visit function call node."""
        func_name = node.func_name
        # First check if it's a function in enclosing scope (for recursion)
        # When in a function, the function name is also a variable (return value)
        # so we need to check enclosing scope first
        func_symbol = None
        scope = self.current_scope
        while scope is not None:
            symbol = scope.lookup(func_name, current_scope_only=True)
            if symbol is not None and isinstance(symbol, FunctionSymbol):
                func_symbol = symbol
                break
            scope = scope.enclosing_scope
        
        if func_symbol is None:
            self.error(f"Undefined function '{func_name}'")
        
        # Check parameter count
        expected_params = len(func_symbol.params)
        actual_params = len(node.actual_params) if node.actual_params else 0
        if expected_params != actual_params:
            self.error(f"Function '{func_name}' expects {expected_params} parameter(s), got {actual_params}")
        for param_node in (node.actual_params or []):
            self.visit(param_node)

    def visit_Compound(self, node):
        """
        Visit compound statement (BEGIN...END block).
        Each compound creates a new nested scope.
        """
        # Only create nested scope if we're not at the program level
        # (program-level compound doesn't create new scope)
        if self.current_scope.scope_level>1 or self._is_nested_compound(node):
            self.scope_counter+=1
            scope_name = f'block{self.scope_counter}'
            if _DEBUG:
                print(f'ENTER scope: {scope_name}')
            nested_scope = ScopedSymbolTable(
                scope_name=scope_name, scope_level=self.current_scope.scope_level+1, enclosing_scope=self.current_scope
            )
            self.current_scope=nested_scope
            #visit children
            for child in node.children:
                self.visit(child)
            if _DEBUG:
                print(nested_scope)
                print(f'LEAVE scope: {scope_name}')
            self.current_scope = self.current_scope.enclosing_scope
        else:
            for child in node.children:
                self.visit(child)

    def _is_nested_compound(self, node):
        """Check if this compound statement is nested inside another compound."""
        return self.scope_counter>0 or self.current_scope.scope_level>1

    def visit_Assign(self, node):
        # Check that variable is declared
        var_name = node.left.value
        var_symbol = self.current_scope.lookup(var_name)
        if var_symbol is None:
            self.error(f"Cannot assign to undeclared variable '{var_name}'")
        self.visit(node.right)

    def visit_Var(self, node):
        """Visit variable reference node"""
        var_name = node.value
        var_symbol = self.current_scope.lookup(var_name)
        if var_symbol is None:
            self.error(f"Undeclared variable '{var_name}'")
        
    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOp(self, node):
        self.visit(node.expr)

    def visit_IfStatement(self, node):
        """Analyze if statement."""
        self.visit(node.condition)
        self.visit(node.then_branch)
        if node.else_branch:
            self.visit(node.else_branch)

    def visit_ComparisonOp(self, node):
        """Analyze comparison operation."""
        self.visit(node.left)
        self.visit(node.right)

    def visit_BooleanOp(self, node):
        """Analyze boolean operation."""
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryBoolOp(self, node):
        """Analyze unary boolean operation."""
        self.visit(node.expr)
        
    def visit_WhileLoop(self, node):
        self.visit(node.condition)
        self.visit(node.body)
        
    def visit_ForLoop(self, node):
        var_name = node.var_node.value
        var_symbol = self.current_scope.lookup(var_name)
        if var_symbol is None:
            self.error(f"undefined variable '{var_name}' in FOR loop")
        self.visit(node.start_expr)
        self.visit(node.end_expr)
        self.visit(node.body)

    def visit_Num(self, node):
        pass

    def visit_NoOp(self, node):
        pass

    def visit_Type(self, node):
        pass

    def visit_Param(self, node):
        pass


