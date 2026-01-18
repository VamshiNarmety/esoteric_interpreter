"""
Interpreter that walks the Abstract syntax tree.
Uses the visitor to pattern to traverse and interpret AST nodes.
"""
from src.parser.parser import Parser
from src.parser.ast_nodes import Program, Block, VarDecl, FunctionDecl, Param, FunctionCall, Type, BinOp, Num, UnaryOp, Compound, Assign, Var, NoOp
from src.lexer.token import PLUS, MINUS, MUL, INTEGER_DIV, FLOAT_DIV
from src.semantic.semantic_analyzer import SemanticAnalyzer

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
        self.functions = {} #store function AST nodes

    def visit_Program(self, node):
        self.visit(node.block)

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_VarDecl(self, node):
        pass

    def visit_FunctionDecl(self, node):
        """Store function for later execution."""
        self.functions[node.func_name] = node

    def visit_FunctionCall(self, node):
        """
        Execute a function call and return its value.
        NOTE: Simplified implementation - stores params in GLOBAL_SCOPE temporarily.
        """
        func_name = node.func_name
        func_node = self.functions.get(func_name)
        
        if func_node is None:
            raise Exception(f"Function '{func_name}' not found")
        
        # Evaluate actual parameter expressions
        param_values = [self.visit(arg_expr) for arg_expr in node.actual_params]
        
        # Bind parameters to GLOBAL_SCOPE temporarily
        saved_params = {}
        for param_node, arg_value in zip(func_node.params, param_values):
            param_name = param_node.var_node.value
            # Save old value if exists
            if param_name in self.GLOBAL_SCOPE:
                saved_params[param_name] = self.GLOBAL_SCOPE[param_name]
            # Set parameter value
            self.GLOBAL_SCOPE[param_name] = arg_value
        
        # Execute function body
        self.visit(func_node.block_node)
        
        # Get return value (should be assigned to function name)
        return_value = self.GLOBAL_SCOPE.get(func_name)
        
        # Clean up: remove parameters from GLOBAL_SCOPE
        for param_node in func_node.params:
            param_name = param_node.var_node.value
            if param_name in saved_params:
                # Restore old value
                self.GLOBAL_SCOPE[param_name] = saved_params[param_name]
            else:
                # Remove parameter
                if param_name in self.GLOBAL_SCOPE:
                    del self.GLOBAL_SCOPE[param_name]
        
        return return_value

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
        #Semantic analysis
        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.visit(tree)
        return self.visit(tree)