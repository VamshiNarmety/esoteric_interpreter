"""
Parser for building Abstract syntax trees.
The parser consumes tokens from the lexer and builds an AST.
"""
from src.lexer.token import (INTEGER_CONST, REAL_CONST, PLUS, MINUS, MUL, INTEGER_DIV, FLOAT_DIV, LPAREN, RPAREN, ID, ASSIGN, BEGIN, END, SEMI, DOT, PROGRAM, VAR, COLON, COMMA, INTEGER, REAL, FUNCTION, EQUAL, NOT_EQUAL, LESS_THAN, GREATER_THAN, LESS_EQUAL, GREATER_EQUAL, AND, OR, NOT, IF, THEN, ELSE, EOF, WHILE, FOR, DO, TO, DOWNTO, PRINT, WRITELN)
from src.parser.ast_nodes import (Program, Block, VarDecl, FunctionDecl, Param, FunctionCall, Type, BinOp, Num, UnaryOp, Compound, Assign, Var, NoOp, ComparisonOp, BooleanOp, UnaryBoolOp, IfStatement, WhileLoop, ForLoop, Print)
from src.errors import ParserError

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, message=None):
        msg = message or f"Invalid syntax: unexpected token '{self.current_token.type}'"
        raise ParserError(msg)
    
    def eat(self, token_type):
        """
        Verify current token type and get next token.
        """
        if self.current_token.type==token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"Expected token '{token_type}', got {self.current_token.type}")

    def program(self):
        self.eat(PROGRAM)
        var_node = self.variable()
        prog_name = var_node.value
        self.eat(SEMI)
        block_node = self.block()
        program_node = Program(prog_name, block_node)
        self.eat(DOT)
        return program_node
    
    def block(self):
        declaration_nodes = self.declarations()
        compound_statement_node = self.compound_statement()
        node = Block(declaration_nodes, compound_statement_node)
        return node
    
    def declarations(self):
        declarations = []
        #Variable declaraions
        if self.current_token.type==VAR:
            self.eat(VAR)
            while self.current_token.type==ID:
                var_decl = self.variable_declaration()
                declarations.extend(var_decl)
                self.eat(SEMI)
        #Function declarations
        while self.current_token.type==FUNCTION:
            self.eat(FUNCTION)
            func_name = self.current_token.value
            self.eat(ID)
            params = []
            if self.current_token.type==LPAREN:
                self.eat(LPAREN)
                params = self.formal_parameter_list()
                self.eat(RPAREN)
            self.eat(COLON)
            return_type = self.type_spec()
            self.eat(SEMI)
            block_node = self.block()
            func_decl = FunctionDecl(func_name, params, return_type, block_node)
            declarations.append(func_decl)
            self.eat(SEMI)
        return declarations
    
    def formal_parameter_list(self):
        if self.current_token.type!=ID:
            return []
        params = self.formal_parameters()
        while self.current_token.type==SEMI:
            self.eat(SEMI)
            params.extend(self.formal_parameters())
        return params
    
    def formal_parameters(self):
        param_nodes = []
        param_tokens = [self.current_token]
        self.eat(ID)
        while self.current_token.type==COMMA:
            self.eat(COMMA)
            param_tokens.append(self.current_token)
            self.eat(ID)
        self.eat(COLON)
        type_node = self.type_spec()
        for param_token in param_tokens:
            param_nodes.append(Param(Var(param_token), type_node))
        return param_nodes
    
    def variable_declaration(self):
        var_nodes = [Var(self.current_token)]
        self.eat(ID)
        while self.current_token.type==COMMA:
            self.eat(COMMA)
            var_nodes.append(Var(self.current_token))
            self.eat(ID)
        self.eat(COLON)
        type_node = self.type_spec()
        var_declarations = [VarDecl(var_node, type_node) for var_node in var_nodes]
        return var_declarations
    
    def type_spec(self):
        token = self.current_token
        if self.current_token.type==INTEGER:
            self.eat(INTEGER)
        else:
            self.eat(REAL)
        node = Type(token)
        return node
    
    def compound_statement(self):
        self.eat(BEGIN)
        nodes = self.statement_list()
        self.eat(END)
        root = Compound()
        for node in nodes:
            root.children.append(node)
        return root
    
    def statement_list(self):
        node = self.statement()
        results = [node]
        while self.current_token.type==SEMI:
            self.eat(SEMI)
            results.append(self.statement())
        if self.current_token.type==ID:
            self.error()
        return results
    
    def statement(self):
        if self.current_token.type == BEGIN:
            node = self.compound_statement()
        elif self.current_token.type == IF:
            node = self.if_statement()
        elif self.current_token.type==WHILE:
            node = self.while_statement()
        elif self.current_token.type==FOR:
            node = self.for_statement()
        elif self.current_token.type in (PRINT, WRITELN):
            node = self.print_statement()
        elif self.current_token.type == ID:
            node = self.assignment_statement()
        else:
            node = self.empty()
        return node
    
    def if_statement(self):
        self.eat(IF)
        condition = self.boolean_expression()
        self.eat(THEN)
        then_branch = self.statement()
        else_branch = None
        if self.current_token.type == ELSE:
            self.eat(ELSE)
            else_branch = self.statement()
        self.eat(END)
        return IfStatement(condition, then_branch, else_branch)
    
    def while_statement(self):
        self.eat(WHILE)
        condition = self.boolean_expression()
        self.eat(DO)
        body = self.statement()
        return WhileLoop(condition, body)
    
    def for_statement(self):
        self.eat(FOR)
        var_node = self.variable()
        self.eat(ASSIGN)
        start_expr = self.expr()
        #check if TO or DOWNTO
        is_downto = False
        if self.current_token.type==TO:
            self.eat(TO)
        elif self.current_token.type==DOWNTO:
            self.eat(DOWNTO)
            is_downto=True
        else:
            self.error()
        end_expr = self.expr()
        self.eat(DO)
        body = self.statement()
        return ForLoop(var_node, start_expr, end_expr, body, is_downto)
    
    def print_statement(self):
        newline = True
        if self.current_token.type==PRINT:
            self.eat(PRINT)
            newline=False
        elif self.current_token.type==WRITELN:
            self.eat(WRITELN)
            newline=True
        self.eat(LPAREN)
        expressions = []
        expressions.append(self.expr())
        while self.current_token.type==COMMA:
            self.eat(COMMA)
            expressions.append(self.expr())
        self.eat(RPAREN)
        return Print(expressions, newline)
    
    def boolean_expression(self):
        node = self.boolean_term()
        while self.current_token.type == OR:
            token = self.current_token
            self.eat(OR)
            node = BooleanOp(left=node, op=token, right=self.boolean_term())
        return node
    
    def boolean_term(self):
        node = self.boolean_factor()
        while self.current_token.type == AND:
            token = self.current_token
            self.eat(AND)
            node = BooleanOp(left=node, op=token, right=self.boolean_factor())
        return node
    
    def boolean_factor(self):
        if self.current_token.type == NOT:
            token = self.current_token
            self.eat(NOT)
            return UnaryBoolOp(op=token, expr=self.boolean_factor())
        elif self.current_token.type == LPAREN:
            self.eat(LPAREN)
            node = self.boolean_expression()
            self.eat(RPAREN)
            return node
        else:
            return self.comparison()
        
    def comparison(self):
        node = self.expr()
        if self.current_token.type in (EQUAL, NOT_EQUAL, LESS_THAN, GREATER_THAN, 
                                       LESS_EQUAL, GREATER_EQUAL):
            token = self.current_token
            if token.type == EQUAL:
                self.eat(EQUAL)
            elif token.type == NOT_EQUAL:
                self.eat(NOT_EQUAL)
            elif token.type == LESS_THAN:
                self.eat(LESS_THAN)
            elif token.type == GREATER_THAN:
                self.eat(GREATER_THAN)
            elif token.type == LESS_EQUAL:
                self.eat(LESS_EQUAL)
            elif token.type == GREATER_EQUAL:
                self.eat(GREATER_EQUAL)
            node = ComparisonOp(left=node, op=token, right=self.expr())
        return node
    
    def assignment_statement(self):
        left = self.variable()
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node
    
    def variable(self):
        node = Var(self.current_token)
        self.eat(ID)
        return node
    
    def empty(self):
        return NoOp()

    def factor(self):
        token = self.current_token
        if token.type==PLUS:
            self.eat(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type==MINUS:
            self.eat(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type==INTEGER_CONST:
            self.eat(INTEGER_CONST)
            return Num(token)
        elif token.type==REAL_CONST:
            self.eat(REAL_CONST)
            return Num(token)
        elif token.type==LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        elif token.type==ID:
            if self.lexer.current_char=='(':
                return self.function_call()
            else:
                return self.variable()
        else:
            self.error()

    def function_call(self):
        token = self.current_token
        func_name = self.current_token.value
        self.eat(ID)
        self.eat(LPAREN)
        actual_params = []
        if self.current_token.type!=RPAREN:
            actual_params.append(self.expr())
            while self.current_token.type==COMMA:
                self.eat(COMMA)
                actual_params.append(self.expr())
        self.eat(RPAREN)
        return FunctionCall(func_name, actual_params, token)
        
    def term(self):
        node = self.factor()
        while self.current_token.type in (MUL, INTEGER_DIV, FLOAT_DIV):
            token = self.current_token
            if token.type==MUL:
                self.eat(MUL)
            elif token.type==INTEGER_DIV:
                self.eat(INTEGER_DIV)
            elif token.type==FLOAT_DIV:
                self.eat(FLOAT_DIV)
            node = BinOp(node, token, self.factor())
        return node
    
    def expr(self):
        node = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type==PLUS:
                self.eat(PLUS)
            elif token.type==MINUS:
                self.eat(MINUS)
            node = BinOp(node, token, self.term())
        return node
    
    def parse(self):
        node = self.program()
        if self.current_token.type!=EOF:
            self.error()
        return node
    
    