"""
Interpreter that walks the Abstract syntax tree.
Uses the visitor to pattern to traverse and interpret AST nodes.
Implements call stack and activation records for proper function execution.
"""
from src.parser.parser import Parser
from src.parser.ast_nodes import Program, Block, VarDecl, FunctionDecl, Param, FunctionCall, Type, BinOp, Num, UnaryOp, Compound, Assign, Var, NoOp
from src.lexer.token import PLUS, MINUS, MUL, INTEGER_DIV, FLOAT_DIV
from src.semantic.semantic_analyzer import SemanticAnalyzer
from src.interpreter.activation_record import ActivationRecord

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
    Uses call stack with activation records for proper function execution.
    """
    GLOBAL_SCOPE = {}
    
    def __init__(self, parser):
        """ Initialize interpreter with a parser."""
        self.parser = parser
        self.functions = {} #store function AST nodes
        self.call_stack = [] #stack of activation records
        self.global_ar = ActivationRecord('GLOBAL', 0)

    def push_ar(self, ar):
        self.call_stack.append(ar)

    def pop_ar(self):
        return self.call_stack.pop()
    
    def current_ar(self):
        if self.call_stack:
            return self.call_stack[-1]
        return self.global_ar

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
        Execute a function call with proper call stack and activation records.
        Each function call creates its own activation record on the call stack.
        """
        func_name = node.func_name
        func_node = self.functions.get(func_name)
        
        if func_node is None:
            raise Exception(f"Function '{func_name}' not found")
        
        # Evaluate actual parameter expressions
        param_values = [self.visit(arg_expr) for arg_expr in node.actual_params]

        #create activation record for this function call
        ar = ActivationRecord(func_name, self.current_ar().level+1, self.current_ar())
        
        # Bind parameters to activation record
        for param_node, arg_value in zip(func_node.params, param_values):
            param_name = param_node.var_node.value
            ar[param_name] = arg_value
        #push acccctivation record onto call stack
        self.push_ar(ar)
        #Execute function body
        self.visit(func_node.block_node)
        #Get return value from AR
        return_value = ar[func_name]
        #pop AR from call stack
        self.pop_ar()
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
        value = self.visit(node.right)
        #Assign to current ar or global scope
        ar = self.current_ar()
        
        #If we're in the global AR, also store in GLOBAL_SCOPE
        if ar is self.global_ar:
            self.GLOBAL_SCOPE[var_name] = value
            ar[var_name] = value
        #check if variable exists in current AR
        elif var_name in ar.members or var_name == ar.name:
            #Assign to current AR (local or return value)
            ar[var_name] = value
        elif var_name in self.GLOBAL_SCOPE:
            #assign to global scope
            self.GLOBAL_SCOPE[var_name] = value
        else:
            #New variable - assign to current AR
            ar[var_name] = value

    def visit_Var(self, node):
        var_name = node.value
        #look up in current AR first
        ar = self.current_ar()
        if var_name in ar.members:
            return ar[var_name]
        #Then look in global scope
        if var_name in self.GLOBAL_SCOPE:
            return self.GLOBAL_SCOPE[var_name]
        raise NameError(f"Variable '{var_name}' is not defined")
    
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